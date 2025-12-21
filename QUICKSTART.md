# Quick Start Guide

## Get Your Renderer Working in 2 Minutes

### Step 1: Host the File

Your renderer is a single HTML file that needs to be accessible via HTTPS.

**GitHub Pages (Easiest):**
```bash
# If you haven't already, enable GitHub Pages:
# 1. Go to your repo settings
# 2. Pages → Source → Deploy from main branch
# 3. Your file will be at:
# https://YOUR-USERNAME.github.io/REPO-NAME/index_chat.html
```

**Example URL:**
```
https://stephen-chu.github.io/custom-output-renderer-chat-langchain/index_chat.html
```

### Step 2: Configure in LangSmith

1. Go to your LangSmith project
2. Click **Settings** → **Custom Output Rendering**
3. Paste your hosted URL
4. Click **Save**

That's it! 🎉

## Verify It's Working

1. Go to any trace in your project
2. The run detail pane should now show your custom renderer
3. You should see messages with colored bubbles instead of raw JSON

## Features You Get

✅ **Message bubbles** - Blue (user), green (assistant), yellow (tool)
✅ **Markdown rendering** - Rich text, code blocks, links
✅ **JSON viewer** - Syntax-highlighted, collapsible
✅ **Raw toggle** - Switch between rendered and raw JSON
✅ **No flashing** - Optimized for LangSmith's rapid message loading

## Customize

The file is `index_chat.html` - edit it to change:

**Colors** (lines ~9-72):
```css
--user-bg-start: #e0f2fe;  /* Change user message color */
--assistant-bg-start: #f0fdf4;  /* Change AI message color */
--tool-bg-start: #fef3c7;  /* Change tool message color */
```

**Performance** (lines ~928-930):
```javascript
const INITIAL_DEBOUNCE = 500;  // Increase if still flashing
const NORMAL_DEBOUNCE = 150;   // Lower for faster updates
```

After editing, commit and push to GitHub - your changes will be live in ~1 minute.

## Troubleshooting

**Renderer not loading?**
- Check the URL is accessible in your browser
- Ensure it's HTTPS (HTTP won't work in LangSmith)
- Look for errors in browser console (F12)

**Messages not appearing?**
- Check that your traces have the expected structure
- Open browser console and look for `[Message Event]` logs
- Verify postMessage events are being received

**Still flashing on load?**
- Increase `INITIAL_DEBOUNCE` to 1000ms
- Increase `INITIAL_LOAD_DURATION` to 5000ms

## Need Help?

- Full docs: [README.md](README.md)
- LangSmith docs: https://docs.langchain.com/langsmith/custom-output-rendering
- Example repo: https://github.com/langchain-samples/custom-output-rendering
