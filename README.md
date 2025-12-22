# LangSmith Custom Output Renderer

A single-file custom output renderer for LangSmith that displays conversation traces with a clean chat interface, built for [Chat LangChain](https://chat.langchain.com).

![Custom Output Renderer](assets/custom_output.png)

> **Note:** This was entirely built using Claude Code. I have zero background in HTML/CSS/JS.

## What This Does

Transforms raw LangSmith trace JSON into a readable chat interface with:
- Message bubbles (blue for users, green for AI, yellow for tools)
- Markdown rendering with syntax highlighting
- Collapsible tool outputs
- Toggle to view raw JSON

## Quick Start

### 1. Host the File

Upload `chat.html` to any static host:

**GitHub Pages (Easiest):**
1. Push file to your repo
2. Go to repo Settings → Pages
3. Deploy from main branch
4. Your URL: `https://YOUR-USERNAME.github.io/REPO-NAME/chat.html`

**Other Options:** Vercel, Netlify, AWS S3, any web server

### 2. Configure in LangSmith

1. Go to your LangSmith project/dataset/annotation queue settings
2. Find **Custom Output Rendering**
3. Paste your hosted URL
4. Save

Done! Your traces now render with the custom interface.

## File Structure

This repo contains:
- **`chat.html`** - Single HTML file with inline CSS and JavaScript (~1,000 lines)
- **`assets/`** - Screenshot and other assets

## How It Works

```
LangSmith → postMessage API → Your Renderer → Rendered UI
```

LangSmith loads your HTML in an iframe and sends message data via the browser's `postMessage` API. Your renderer listens for these messages and displays them however you want.

**Important:** LangSmith sends one postMessage per message in the trace. A 10-message conversation = 10 rapid events. Initially,this caused a lot of flashing in the render. Claude implemented debouncing to handle this more smoothly, but it's not perfect yet.

## LangSmith Docs
- [LangSmith Custom Output Rendering Docs](https://docs.langchain.com/langsmith/custom-output-rendering)

## License
MIT
