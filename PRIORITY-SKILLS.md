# ⭐ PRIORITY SKILLS — USE THESE FIRST

These are the high-value skills pulled from the curated video lists. When a task touches any of these domains, **reach for the skill named here before anything generic.** This file exists so the router and any agent treat these as first-class defaults, not afterthoughts.

The router reads this file's group hints; an agent reading the hub should load this before CATALOG.md.

---

## The core stack (use constantly)

### 1. UI/UX Pro Max  →  `ui-ux-pro-max` (group: Design / Frontend)
AI-reasoning design engine. Analyzes the project, picks a real design system, kills generic "AI slop" layouts. **Use for any frontend/UI task before the default frontend-design skill.** 240+ styles, font pairings, UX rules.

### 2. Stop Slop  →  `stop-slop` (group: Docs/Writing)
Strips AI writing tells: em-dashes, "it's not X it's Y", filler, robotic cadence. **Run on any prose, doc, README, or user-facing copy before shipping.** 7 rules + a scoring rubric.

### 3. Superpowers  →  `superpowers` family (group: Engineering)
Turns the agent into a disciplined senior dev: brainstorm spec → plan → execute with checkpoints, TDD, subagent review. **Use before any non-trivial build.** Sub-skills: `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`, `requesting-code-review`.

### 4. Code Review  →  `code-reviewer` / `code-review-excellence` (group: Engineering/Security)
Pre-merge review against spec + code quality. **Run before merging anything.**

### 5. awesome-design  →  `awesome-design` (group: Design)
Brand-matched DESIGN.md systems (Stripe, Vercel, Linear look). **Use when you want a specific aesthetic, or when default frontend output feels samey.**

---

## Capability adds (use when the task calls for it)

### RAG-Anything  →  `rag-anything` (group: Data/AI)
Multimodal RAG: ingests text + images + scanned PDFs + tables into one knowledge base. Use for any rich-document retrieval. *(Python framework — needs `pip install raganything` + LLM key.)*

### Firecrawl  →  `firecrawl-*` (group: Productivity/Engineering)
Web scraping/crawling at scale, beats native fetch, handles bot protection (hosted). Sub-skills: `firecrawl-scrape`, `firecrawl-crawl`, `firecrawl-search`, `firecrawl-map`. *(Needs Firecrawl API key.)*

### GWS — Google Workspace  →  `gws-*` (group: Workspace)
Gmail, Calendar, Drive, Docs, Sheets, Slides from Claude Code. 92 skills + recipes. Huge productivity unlock. *(Needs Google OAuth.)*

---

## ⚠️ These are MCP servers, NOT skills (separate install)

Do not look for these in `skills/`. They run as services and need API keys. Setup in `mcp-servers/README.md`.

- **Stitch** — Google UI mockup generation (text → screens → HTML). Free API, needs Google Cloud project. "Nano Banana 2" = the Gemini image model *inside* Stitch, not a separate install.
- **21st.dev Magic** — React/3D/reactive component library, generates components in-IDE. Needs 21st.dev API key.
- **Firecrawl (MCP variant)** — same as the skill but as an MCP server, if you prefer that wiring.

---

## Honest note on "use constantly"

Whether these fire automatically depends on the agent runtime, not this file alone. The skills (folders) auto-trigger in Claude Code when their description matches your task — keep this hub on your machine so they're discoverable. The MCP servers (Stitch, 21st, GWS-via-OAuth, Firecrawl) need **your** API keys configured in **your** client; they can't run from a sandbox. This file maximizes the chance the right one is picked, but it can't force a tool to run without its credentials present.
