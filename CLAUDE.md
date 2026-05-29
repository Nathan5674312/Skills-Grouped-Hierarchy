# Skills Hub — Claude Code Instructions

This repo is your personal skills hub. Read this file on every session start.

## Always do this first

1. Read `PRIORITY-SKILLS.md` — these are the mandatory high-value skills. Use them constantly.
2. Before any task, run the router to find the right skill:
   ```bash
   python skill-router/scripts/route.py index.json "describe the task here"
   ```
3. Read the matched skill's `SKILL.md`, then follow it.

## Non-negotiable defaults

- Any UI/frontend task → use `ui-ux-pro-max` first, not generic output.
- Any writing/prose/docs → run through `stop-slop` before finishing.
- Any non-trivial build → start with `superpowers/brainstorming`.
- Any PR or code → run `code-review-excellence` before calling it done.
- Any branded UI → use `awesome-design` with the matching DESIGN.md.
- Web scraping → `firecrawl-*` skills.
- Gmail/Calendar/Drive/Docs → `gws-*` skills.
- Multimodal RAG → `rag-anything`.

## Structure

```
skills-hub/
├── CLAUDE.md            ← you are here
├── PRIORITY-SKILLS.md   ← must-use skill list with emphasis
├── CATALOG.md           ← all 447 skills grouped by domain
├── index.json           ← router index
├── skill-router/        ← router scripts
├── skills/              ← 447 skill folders
└── mcp-servers/         ← MCP server setup (Stitch, 21st.dev, Firecrawl)
```

## Adding new skills

```bash
# 1. Drop skill folder into skills/
# 2. Rebuild catalog and index
python skill-router/scripts/organize.py skills --out CATALOG.md
python skill-router/scripts/build_index.py skills CATALOG.md --out index.json
# 3. Commit and push
git add . && git commit -m "add [skill name]" && git push
```
