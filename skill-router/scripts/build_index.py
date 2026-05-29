#!/usr/bin/env python3
"""Build a two-tier router index from a skills folder.

Stage 1 (groups): each group gets a keyword bag aggregated from its skills.
Stage 2 (skills): each skill keeps its own name + description + keyword bag.

Output: index.json — small enough to load whole, structured so the router
reads group-level data first and only descends into one group's skills.

Usage:
    python build_index.py <skills_dir> <catalog.md> --out index.json
"""
import argparse
import json
import re
from pathlib import Path

STOP = set("the a an and or of to for with in on at by from is are be use used when this that your you it its as into within via per use using них".split())


def parse_frontmatter(text):
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    block = m.group(1) if m else text
    n = re.search(r"^name:\s*(.+)$", block, re.MULTILINE)
    d = re.search(r"^description:\s*(.+(?:\n\s+.+)*)$", block, re.MULTILINE)
    name = n.group(1).strip() if n else None
    desc = " ".join(l.strip() for l in d.group(1).splitlines()).strip() if d else ""
    return name, desc


def keywords(text, top=12):
    words = re.findall(r"[a-z][a-z0-9+#.-]{2,}", text.lower())
    freq = {}
    for w in words:
        if w in STOP:
            continue
        freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:top]]


def parse_catalog_groups(catalog_path):
    """Map skill name -> group, from CATALOG.md."""
    text = Path(catalog_path).read_text(encoding="utf-8")
    group = None
    mapping = {}
    for line in text.splitlines():
        g = re.match(r"^## (.+)$", line)
        if g:
            group = g.group(1).strip()
            continue
        s = re.match(r"^- \*\*(.+?)\*\*", line)
        if s and group:
            mapping[s.group(1).strip()] = group
    return mapping


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skills_dir")
    ap.add_argument("catalog")
    ap.add_argument("--out", default="index.json")
    args = ap.parse_args()

    name_to_group = parse_catalog_groups(args.catalog)
    groups = {}

    for skill_md in Path(args.skills_dir).rglob("SKILL.md"):
        folder = skill_md.parent.name
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        name, desc = parse_frontmatter(text)
        name = name or folder
        group = name_to_group.get(name) or name_to_group.get(folder) or "Uncategorized"
        kw = keywords(f"{name} {desc}")
        entry = {"folder": folder, "name": name, "desc": desc[:200], "kw": kw}
        groups.setdefault(group, {"skills": [], "kw": {}})
        groups[group]["skills"].append(entry)
        for w in kw:
            groups[group]["kw"][w] = groups[group]["kw"].get(w, 0) + 1

    # condense group keyword bags to top 40
    for g in groups.values():
        g["kw"] = [w for w, _ in sorted(g["kw"].items(), key=lambda x: -x[1])[:40]]

    index = {
        "groups": {
            g: {"count": len(d["skills"]), "kw": d["kw"], "skills": d["skills"]}
            for g, d in sorted(groups.items())
        }
    }
    Path(args.out).write_text(json.dumps(index, indent=1), encoding="utf-8")
    total = sum(len(d["skills"]) for d in groups.values())
    print(f"Wrote {args.out} — {len(groups)} groups, {total} skills")


if __name__ == "__main__":
    main()
