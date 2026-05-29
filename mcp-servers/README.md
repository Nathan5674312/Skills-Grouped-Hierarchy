# MCP Servers (NOT skills)

These two are **MCP servers**, not skills. They do not go in the skills folder. They run as background services your AI client connects to. Each needs setup + an API key.

Drop the relevant block into your client's MCP config file:
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Claude Code: run `claude mcp add ...` (see below)
- Cursor: Settings > MCP > Add New Server

---

## 1. Google Stitch (UI mockup generation)

Generates UI screens from text, exports HTML/code. Free API, needs a Google Cloud project.

Setup:
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

Config:
```json
{
  "mcpServers": {
    "stitch": {
      "command": "npx",
      "args": ["-y", "stitch-mcp"],
      "env": { "GOOGLE_CLOUD_PROJECT": "YOUR_PROJECT_ID" }
    }
  }
}
```
Repo: https://github.com/Kargatharaakash/stitch-mcp

---

## 2. 21st.dev Magic (React component library)

Generates modern UI components, pulls from 21st.dev's library. Needs API key from https://21st.dev/magic

Claude Code one-liner:
```bash
npx @21st-dev/cli@latest install --api-key YOUR_KEY
```

Manual config:
```json
{
  "mcpServers": {
    "@21st-dev/magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/magic@latest", "API_KEY=\"YOUR_KEY\""]
    }
  }
}
```
Repo: https://github.com/21st-dev/magic-mcp

---

Note on "Nano Banana 2": that's Google's Gemini image model used *inside* Stitch for asset generation, not a separate install. Once Stitch is connected you get image generation through it.

---

## 3. Firecrawl (web scraping, optional MCP variant)

Firecrawl is also bundled as a *skill* (`skills/firecrawl-*`). If you'd rather run it as an MCP server, use this. Needs API key from https://firecrawl.dev/app/api-keys

```json
{
  "mcpServers": {
    "firecrawl-mcp": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": { "FIRECRAWL_API_KEY": "fc-YOUR_API_KEY" }
    }
  }
}
```
Open-source self-host exists too; hosted handles bot protection better.
Repo: https://github.com/firecrawl/firecrawl-mcp-server
