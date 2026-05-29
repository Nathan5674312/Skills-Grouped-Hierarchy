<div align="center">

# 🧠 Skills-Grouped-Hierarchy

**A two-tier intelligent skill router for Claude Code**
*Pick the group. Pick the skill. Never waste tokens scanning 447 files.*

[![Skills](https://img.shields.io/badge/Skills-447-blue?style=flat-square)](./CATALOG.md)
[![Groups](https://img.shields.io/badge/Groups-15-purple?style=flat-square)](./CATALOG.md)
[![Router](https://img.shields.io/badge/Router-Two--Tier-green?style=flat-square)](./skill-router/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)

</div>

---

## What This Is

Most Claude Code setups dump all skills into a flat folder. Claude scans every description on every task — wasteful, slow, imprecise.

This repo solves that with a **two-tier hierarchy**:

```
Task → Score 15 Groups → Pick Winner → Score skills inside that group → Pick best skill(s)
```

Claude never reads all 447 skills. It reads 15 group bags, descends into one, and returns the right skill. Fast, precise, token-efficient.

---

## How the Router Works

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR TASK                            │
│         "build a react dashboard with dark mode"        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              TIER 1 — GROUP SCORING                     │
│   Score 15 keyword bags against the task (fast)         │
│                                                         │
│   Frontend    ████████████  18.5  ← WINNER              │
│   Backend     ████          5.2                         │
│   DevOps      ███           4.1                         │
│   Security    ██            3.0                         │
│   ...         (11 more groups skipped)                  │
└────────────────────┬────────────────────────────────────┘
                     │  descend into Frontend only
                     ▼
┌─────────────────────────────────────────────────────────┐
│              TIER 2 — SKILL SCORING                     │
│   Score 21 Frontend skills against the task (precise)   │
│                                                         │
│   ui-ux-pro-max         ████████████  9.0  ← PICK      │
│   nextjs-app-router     ████          5.7               │
│   tailwind-design       ████          5.2               │
│   react-state-mgmt      ███           4.7               │
│   ...                                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
              Read ui-ux-pro-max/SKILL.md
              Execute with Fortune 500 design intelligence
```

---

## ⭐ Priority Skills

These are weighted to win their domain. Always loaded first.

| Skill | Group | What It Does |
|---|---|---|
| `ui-ux-pro-max` | Frontend / Design | AI reasoning engine for professional UI. No more AI slop design. |
| `stop-slop` | Docs/Writing | Strips em-dashes, filler, robotic cadence from any prose. |
| `superpowers` | Engineering | Senior dev methodology: brainstorm → plan → execute → review. |
| `code-review-excellence` | Engineering | Pre-merge review against spec + quality. |
| `awesome-design` | Design | Brand-matched UI (Stripe, Vercel, Linear aesthetics). |
| `firecrawl-*` | Productivity | Web scraping at scale. Handles bot protection. |
| `gws-*` | Workspace | Full Google Workspace: Gmail, Calendar, Drive, Docs, Sheets. |
| `rag-anything` | Data/AI | Multimodal RAG over text + images + scanned PDFs. |

---

## Skill Groups

| Group | Skills | Covers |
|---|---|---|
| Workspace | 75 | Gmail, Calendar, Drive, Docs, Sheets, Slides, Chat |
| DevOps | 73 | Kubernetes, Docker, Terraform, CI/CD, Cloud |
| Docs/Writing | 44 | Documentation, ADRs, stop-slop, content |
| Security | 44 | Auth, vulnerability scanning, DevSecOps |
| Data/AI | 33 | RAG, ML, SQL, pipelines, embeddings |
| Design | 32 | UI/UX, brand systems, DESIGN.md |
| Backend | 30 | APIs, microservices, GraphQL, databases |
| Engineering | 20 | Code review, refactoring, tech debt, TDD |
| Frontend | 21 | React, Next.js, Tailwind, components |
| Testing | 18 | Playwright, pytest, Jest, E2E |
| Languages | 17 | Python, TypeScript, Rust, Go, C++ |
| Productivity | 17 | Obsidian, automation, planning |
| Mobile | 1 | React Native, Flutter |
| Meta | 4 | Skill creation, router, organizer |

---

## Quick Start

### New device setup

```bash
# 1. Clone the hub
git clone https://github.com/Nathan5674312/Skills-Grouped-Hierarchy ~/.claude/skills-hub

# 2. Register as Claude Code plugin marketplace
# In Claude Code:
/plugin marketplace add Nathan5674312/Skills-Grouped-Hierarchy

# Done. Claude Code reads CLAUDE.md every session and routes all tasks.
```

### Route a task manually

```bash
cd ~/.claude/skills-hub
python skill-router/scripts/route.py index.json "your task here"

# Cross-domain task:
python skill-router/scripts/route.py index.json "your task" --groups 2

# JSON output for chaining:
python skill-router/scripts/route.py index.json "your task" --json
```

### Add a new skill

```bash
# 1. Drop the skill folder into skills/
cp -r /path/to/new-skill skills/

# 2. Rebuild catalog and index
python skill-router/scripts/organize.py skills --out CATALOG.md
python skill-router/scripts/build_index.py skills CATALOG.md --out index.json

# 3. Push
git add . && git commit -m "add: new-skill" && git push
```

---

## Repo Structure

```
Skills-Grouped-Hierarchy/
├── CLAUDE.md              ← Auto-read by Claude Code. Sets non-negotiable defaults.
├── PRIORITY-SKILLS.md     ← Must-use skills, emphasized with context.
├── CATALOG.md             ← All 447 skills grouped. The full index.
├── index.json             ← Pre-built router index (group bags + skill keywords).
├── .gitignore             ← Keeps API keys and credentials out of git.
│
├── skill-router/          ← The router
│   ├── SKILL.md           ← Router skill definition
│   └── scripts/
│       ├── route.py       ← Two-tier router (task → group → skill)
│       ├── build_index.py ← Rebuilds index.json from skills folder
│       └── organize.py    ← Groups skills and writes CATALOG.md
│
├── skills/                ← 447 skill folders (each has a SKILL.md)
│   ├── ui-ux-pro-max/
│   ├── stop-slop/
│   ├── superpowers/
│   ├── brainstorming/
│   ├── gws-gmail/
│   ├── firecrawl-scrape/
│   └── ... (441 more)
│
└── mcp-servers/           ← MCP server configs (NOT skills — need API keys)
    └── README.md          ← Setup for Stitch, 21st.dev Magic, Firecrawl
```

---

## MCP Servers

These run as services alongside the skill hub. Setup in [`mcp-servers/README.md`](./mcp-servers/README.md).

| Server | What | Free? |
|---|---|---|
| Google Stitch | UI mockup generation from text prompts | Yes (needs GCP project) |
| 21st.dev Magic | React + 3D component library in-IDE | Free tier |
| Firecrawl | Web scraping with bot protection bypass | Free tier + paid |

> **Nano Banana 2** is Google's Gemini image model built into Stitch — not a separate install.

---

## Skill Sources

| Repo | Skills | What |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 18 | Official Anthropic marketplace |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 7 | Fortune 500-level UI design |
| [rmyndharis/antigravity-skills](https://github.com/rmyndharis/antigravity-skills) | 305 | Curated dev library |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | 1 | Kill AI writing patterns |
| [obra/superpowers](https://github.com/obra/superpowers) | 14 | Senior dev methodology |
| [firecrawl/firecrawl-claude-plugin](https://github.com/firecrawl/firecrawl-claude-plugin) | 8 | Web scraping at scale |
| [WadeWarren/gws-claude-plugin](https://github.com/WadeWarren/gws-claude-plugin) | 92 | Full Google Workspace |
| [HKUDS/RAG-Anything](https://github.com/HKUDS/RAG-Anything) | 1 | Multimodal RAG |
| [VoltAgent/awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) | 1 | Brand-matched UI |

---

## License

MIT — use, fork, extend freely. Attribution appreciated.

---

<div align="center">
Built for Claude Code · Router is TF-IDF weighted · Priority skills boosted · Stemming-aware matching
</div>
