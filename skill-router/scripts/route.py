#!/usr/bin/env python3
"""Two-tier skill router: task -> group -> specific skill(s).

Stage 1: score every group's keyword bag against the task. Pick top group(s).
Stage 2: within the chosen group only, score each skill. Return best matches.

This is the token-efficient path: at runtime an agent reads group scores first
(14 small bags), descends into ONE group, then reads only that group's skills.

Uses TF-IDF-ish weighting so filler words (expert, master) don't dominate.

Usage:
    python route.py index.json "set up a kubernetes deployment with monitoring"
    python route.py index.json "task..." --groups 2 --skills 5 --json
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

STOP = set("the a an and or of to for with in on at by from is are be use used when this that your you it its as into within via per and/or".split())
# generic skill-description filler to down-weight hard
FILLER = set("expert specializing master comprehensive modern implement implementing building creating create build advanced best skill use using working setting".split())

# Priority skills from PRIORITY-SKILLS.md get a score boost so they win ties
# against generic alternatives. Matched by substring against skill folder/name.
PRIORITY = {
    "ui-ux-pro-max": 4.0, "stop-slop": 4.0, "superpowers": 3.0,
    "brainstorming": 3.0, "writing-plans": 2.5, "executing-plans": 2.5,
    "test-driven-development": 2.5, "systematic-debugging": 2.5,
    "code-reviewer": 3.0, "code-review-excellence": 3.0,
    "awesome-design": 3.0, "rag-anything": 2.5,
    "firecrawl": 2.0, "gws-": 1.5,
}


def priority_boost(skill):
    key = (skill.get("folder", "") + " " + skill.get("name", "")).lower()
    return max((v for k, v in PRIORITY.items() if k in key), default=0.0)


def tokens(text):
    raw = [w for w in re.findall(r"[a-z][a-z0-9+#.-]{2,}", text.lower())
           if w not in STOP]
    return [stem(w) for w in raw]


NO_STEM = {"kubernetes", "aws", "kpis", "css", "js", "ts", "nextjs", "redis",
           "devops", "mlops", "https", "dns", "ios", "macos", "series",
           "analysis", "kubernetes", "status", "access", "business"}


def stem(w):
    # light suffix stripping so edit/editing/edited, draft/drafting,
    # test/testing/tested all collapse to one form for matching
    w = w.rstrip(".")
    if w in NO_STEM:
        return w
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def build_idf(index):
    """Document frequency across skills, for weighting."""
    df = {}
    n = 0
    for g in index["groups"].values():
        for s in g["skills"]:
            n += 1
            for w in {stem(k) for k in s["kw"]}:
                df[w] = df.get(w, 0) + 1
    idf = {w: math.log((n + 1) / (c + 1)) + 1 for w, c in df.items()}
    return idf, n


def weight(w, idf):
    base = idf.get(w, 2.0)
    if w in FILLER:
        base *= 0.15
    return base


def score_group(task_toks, group, idf):
    gkw = {stem(k) for k in group["kw"]}
    s = 0.0
    for t in task_toks:
        if t in gkw:
            s += weight(t, idf)
    return s


def score_skill(task_toks, skill, idf):
    hay = {stem(k) for k in skill["kw"]} | set(tokens(skill["name"])) | set(tokens(skill["desc"]))
    s = 0.0
    for t in task_toks:
        if t in hay:
            s += weight(t, idf)
    # small bonus for name match
    name_toks = set(tokens(skill["name"]))
    for t in task_toks:
        if t in name_toks:
            s += 1.5
    # priority boost, but only if the skill already has some relevance
    # (don't surface a priority skill for a totally unrelated task)
    if s > 0:
        s += priority_boost(skill)
    return s


def route(index, task, n_groups=1, n_skills=5):
    idf, _ = build_idf(index)
    task_toks = tokens(task)

    # Score each group two ways and blend: keyword-bag match (cheap signal)
    # plus the group's best individual skill score (prevents tier mismatch
    # where a group wins the bag but holds no actually-relevant skill).
    gscores = []
    per_group_skillscores = {}
    for gname, g in index["groups"].items():
        bag = score_group(task_toks, g, idf)
        sscores = [(s, score_skill(task_toks, s, idf)) for s in g["skills"]]
        sscores.sort(key=lambda x: -x[1])
        per_group_skillscores[gname] = sscores
        best = sscores[0][1] if sscores else 0.0
        # if the group contains a priority skill that matched, lift the group
        # so a high-value skill isn't stranded behind a fluke keyword match
        prio_in_group = max((priority_boost(s) for s, sc in sscores if sc > 0),
                            default=0.0)
        blended = bag + best + prio_in_group  # best-skill dominates; bag + priority break ties
        gscores.append((gname, blended))
    gscores.sort(key=lambda x: -x[1])
    top_groups = [g for g, sc in gscores[:n_groups] if sc > 0] or [gscores[0][0]]

    results = []
    for gname in top_groups:
        sscores = per_group_skillscores[gname]
        picks = [(s, sc) for s, sc in sscores[:n_skills] if sc > 0]
        results.append({
            "group": gname,
            "group_score": round(dict(gscores)[gname], 2),
            "skills": [
                {"name": s["name"], "folder": s["folder"],
                 "score": round(sc, 2), "desc": s["desc"]}
                for s, sc in picks
            ],
        })
    return {"task": task, "routed": results, "group_ranking": gscores[:5]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("index")
    ap.add_argument("task")
    ap.add_argument("--groups", type=int, default=1)
    ap.add_argument("--skills", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    index = json.loads(Path(args.index).read_text())
    out = route(index, args.task, args.groups, args.skills)

    if args.json:
        print(json.dumps(out, indent=1))
        return

    print(f"TASK: {out['task']}\n")
    print("Group ranking:")
    for g, sc in out["group_ranking"]:
        print(f"  {sc:6.2f}  {g}")
    print()
    for r in out["routed"]:
        print(f"=> {r['group']}  (score {r['group_score']})")
        if not r["skills"]:
            print("   (no skill matched within group)")
        for s in r["skills"]:
            print(f"   [{s['score']:5.2f}] {s['name']}")
            print(f"           {s['desc'][:90]}")
        print()


if __name__ == "__main__":
    main()
