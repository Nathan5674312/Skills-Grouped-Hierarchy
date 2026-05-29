#!/usr/bin/env python3
"""Scan a skills directory, group skills, write single CATALOG.md index.

Usage:
    python organize.py <skills_dir> [--out CATALOG.md] [--overrides overrides.json]

Token-efficient by design: produces ONE flat index file. No file moves.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

# Domain-appropriate rules for a developer skill library. First match wins.
RULES = [
    ("Security",    ["security", "auth", "oauth", "vulnerab", "pentest", "encryption", "owasp", "secrets", "compliance audit", "threat", "cve"]),
    ("DevOps",      ["kubernetes", "k8s", "docker", "terraform", "ci/cd", "cicd", "pipeline", "deployment", "infrastructure", "ansible", "helm", "cloud", "aws", "gcp", "azure", "devops", "monitoring", "observability", "sre"]),
    ("Data/AI",     ["machine learning", "ml ", "llm", "data analysis", "dataframe", "pandas", "sql", "database", "postgres", "etl", "data pipeline", "embedding", "rag", "vector", "model training", "analytics", "data engineer"]),
    ("Frontend",    ["react", "vue", "frontend", "css", "tailwind", "ui component", "ux", "design system", "responsive", "animation", "component library", "shadcn", "next.js", "svelte"]),
    ("Backend",     ["api", "backend", "microservice", "rest", "graphql", "server", "endpoint", "fastapi", "express", "django", "rails", "grpc"]),
    ("Languages",   ["python", "typescript", "javascript", "rust", "golang", "go ", "java ", "c++", "kotlin", "swift", "ruby", "php"]),
    ("Testing",     ["testing", "test ", "unit test", "e2e", "playwright", "jest", "pytest", "qa ", "debugging", "debug "]),
    ("Mobile",      ["mobile", "ios", "android", "react native", "flutter", "swiftui"]),
    ("Design",      ["design", "logo", "brand", "visual", "typography", "color palette", "figma", "poster", "art"]),
    ("Docs/Writing",["documentation", "adr", "architecture decision", "technical writing", "changelog", "readme", "content", "writing", "comm"]),
    ("Workspace",   ["gmail", "gws", "google workspace", "calendar", "google drive", "google docs", "sheets", "slides", "google chat", "classroom", "meet ", "workspace", "recipe-", "email triage", "inbox"]),
    ("Productivity",["obsidian", "notion", "workflow", "automation", "planning", "task", "project management", "agile", "scrum"]),
    ("Meta",        ["skill creator", "create a skill", "skill from scratch", "skill organizer", "agent", "orchestrat", "prompt engineering"]),
    ("Engineering", ["code review", "refactor", "tech debt", "technical debt", "build ", "bazel", "monorepo", "binary analysis", "disassembl", "pull request", "pr ", "git ", "embedded", "kernel", "performance", "review", "system"]),
]




def parse_frontmatter(text):
    name = desc = None
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    block = m.group(1) if m else text
    n = re.search(r"^name:\s*(.+)$", block, re.MULTILINE)
    d = re.search(r"^description:\s*(.+(?:\n\s+.+)*)$", block, re.MULTILINE)
    if n:
        name = n.group(1).strip()
    if d:
        desc = " ".join(line.strip() for line in d.group(1).splitlines()).strip()
    return name, desc


def categorize(name, desc, overrides):
    if name in overrides:
        return overrides[name]
    hay = f"{name} {desc}".lower()
    for cat, kws in RULES:
        if any(k in hay for k in kws):
            return cat
    return "Uncategorized"


def find_skills(root):
    out = []
    for p in Path(root).rglob("SKILL.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        name, desc = parse_frontmatter(text)
        name = name or p.parent.name
        desc = desc or "(no description)"
        out.append({"name": name, "desc": desc, "path": str(p)})
    return out


def short(desc, n=160):
    desc = re.sub(r"\s+", " ", desc).strip()
    return desc if len(desc) <= n else desc[: n - 1].rstrip() + "\u2026"


def build_catalog(skills, overrides):
    groups = {}
    for s in skills:
        cat = categorize(s["name"], s["desc"], overrides)
        groups.setdefault(cat, []).append(s)

    order = ["Languages","Frontend","Backend","Data/AI","DevOps","Security","Testing","Mobile","Design","Docs/Writing","Workspace","Productivity","Engineering","Meta","Uncategorized"]
    cats = [c for c in order if c in groups] + [c for c in groups if c not in order]

    lines = ["# Skill Catalog", ""]
    lines.append(f"{len(skills)} skills across {len(groups)} groups.")
    lines.append("")
    lines.append("| Group | Count |")
    lines.append("|---|---|")
    for c in cats:
        lines.append(f"| {c} | {len(groups[c])} |")
    lines.append("")
    for c in cats:
        lines.append(f"## {c}")
        lines.append("")
        for s in sorted(groups[c], key=lambda x: x["name"]):
            lines.append(f"- **{s['name']}** — {short(s['desc'])}")
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skills_dir")
    ap.add_argument("--out", default="CATALOG.md")
    ap.add_argument("--overrides", help="JSON file: {skill_name: category}")
    args = ap.parse_args()

    overrides = {}
    if args.overrides and os.path.exists(args.overrides):
        overrides = json.load(open(args.overrides))

    skills = find_skills(args.skills_dir)
    if not skills:
        print(f"No SKILL.md found under {args.skills_dir}", file=sys.stderr)
        sys.exit(1)

    catalog = build_catalog(skills, overrides)
    Path(args.out).write_text(catalog, encoding="utf-8")
    print(f"Wrote {args.out} — {len(skills)} skills")


if __name__ == "__main__":
    main()
