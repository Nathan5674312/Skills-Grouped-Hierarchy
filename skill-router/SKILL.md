---
name: skill-router
description: Route any task to the right skill from a large skill library using a two-tier lookup (pick group, then pick skill within group). Use this skill whenever the user has many skills and wants the right one selected automatically for a task, asks "which skill should I use for X", wants to route/dispatch/match a task to a skill, or is working inside a skills hub with a CATALOG.md and index.json. Token-efficient: reads group-level scores first and only descends into one group's skills, instead of scanning all skills every time.
---

# Skill Router

Picks the right skill for a task from a big library without scanning everything. Two tiers: task → group → skill.

## Why two tiers

Scanning 330 skill descriptions per task is wasteful. Instead: each group has a keyword bag; score the 14 groups first, descend into the top one, score only that group's skills. One group's worth of reading instead of the whole library.

## Files it uses

- `index.json` — prebuilt router index (group bags + per-skill keywords). Built from the skills folder + `CATALOG.md`.
- `scripts/build_index.py` — regenerates `index.json` after skills are added/removed.
- `scripts/route.py` — the router.

## Routing a task

```bash
python scripts/route.py index.json "set up a kubernetes deployment with monitoring"
```

Output: group ranking, the winning group, and the top skills inside it with scores. To then *use* a skill, read its `SKILL.md` at `skills/<folder>/SKILL.md`.

Options:
- `--groups N` — return top N groups (cross-domain tasks, e.g. "API docs" hits Backend + Docs).
- `--skills N` — skills per group (default 5).
- `--json` — machine-readable, for chaining.

## Full workflow for an agent

1. Get the task from the user.
2. Run `route.py` with the task. (Use `--groups 2` if the task spans domains.)
3. Read the top-ranked skill's `SKILL.md`.
4. Follow that skill to do the work.
5. If the top skill is a poor fit, fall to the next, or re-route with `--groups 2`.

## Rebuilding after adding skills

```bash
python scripts/build_index.py skills/ CATALOG.md --out index.json
```
Run the organizer first if `CATALOG.md` is stale (new skills need a group), then rebuild the index.

## How scoring works

TF-IDF-weighted keyword overlap. Generic filler ("expert", "master", "comprehensive") is down-weighted so distinctive terms decide. Group score blends the group's keyword-bag match with its single best skill score, so a group can't win unless it actually holds a relevant skill.

## Limits

- Keyword-based, not semantic. A task using none of a skill's vocabulary may mis-route. Fix by adding synonyms to the skill description, or route with `--groups 2`.
- 13 skills sit in Uncategorized; they're only reachable when that group wins. Override their group in the organizer if they matter.
