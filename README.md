# LangSmith Custom Output Renderer

A single-file custom output renderer for LangSmith that displays conversation traces with a clean, modern interface.

## Overview

This is a production-ready custom output renderer built as a single HTML file containing all CSS and JavaScript. It provides:

- **Multi-turn conversations** - User, assistant, and tool messages with distinct styling
- **Markdown rendering** - Full GitHub-flavored markdown support with syntax highlighting
- **JSON syntax highlighting** - Color-coded display of structured data
- **Tool call visualization** - Function names, arguments, and results
- **Raw JSON toggle** - View the original message structure
- **Optimized loading** - Handles LangSmith's rapid initial message burst without flashing

## Quick Start

### 1. Host the Renderer

Upload `index_chat.html` to any static file host:

**Option A: GitHub Pages**
```bash
# Your file is already hosted at:
# https://stephen-chu.github.io/custom-output-renderer-chat-langchain/index_chat.html
```

**Option B: Other Static Hosts**
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any web server

### 2. Configure in LangSmith

1. Go to your LangSmith project settings
2. Navigate to **Custom Output Rendering**
3. Paste your hosted URL (e.g., `https://your-username.github.io/repo-name/index_chat.html`)
4. Save

That's it! Your traces will now render with the custom interface.

## Features

### Message Display
- **User Messages** - Blue gradient bubbles, left-aligned
- **Assistant Messages** - Green gradient bubbles, right-aligned, markdown rendered
- **Tool Messages** - Yellow gradient bubbles, right-aligned, collapsible

### Interactive Elements
- **Raw Toggle** - View the original JSON structure of any message
- **Expand/Collapse** - Tool messages start collapsed for cleaner display
- **Syntax Highlighting** - Automatic highlighting for code blocks and JSON

### Performance Optimizations
- **Debounced rendering** - 500ms during initial load, 150ms after
- **Animation suppression** - No animations during the first 3 seconds
- **Smart updates** - Only re-renders when necessary

## Configuration Locations

Custom output rendering can be configured at three levels:

1. **Tracing Projects** - Project settings → Custom Output Rendering
2. **Datasets** - Dataset menu (⋮) → Custom Output Rendering
3. **Annotation Queues** - Queue settings → Custom Output Rendering

Precedence: Annotation Queue > Dataset > Project

## How It Works

### Data Flow

```
LangSmith → postMessage API → index_chat.html → Rendered UI
```

LangSmith sends messages via the browser's `postMessage` API:

```javascript
{
  data: {
    // Array of messages or single message object
  }
}
```

On initial load, LangSmith sends **one postMessage per message** in the trace history, which is why the renderer uses debouncing and animation suppression.

### Message Structure

Each message typically contains:
```javascript
{
  role: "human" | "ai" | "tool",
  content: "string or array of content blocks",
  name: "optional tool/function name",
  tool_calls: [...], // For assistant messages
  // ... other fields
}
```

## Customization

The renderer is a single HTML file, making it easy to customize:

### Styling

Edit the CSS variables in the `<style>` section (lines ~9-72):

```css
:root {
    --user-bg-start: #e0f2fe;  /* User message background */
    --assistant-bg-start: #f0fdf4;  /* Assistant message background */
    --tool-bg-start: #fef3c7;  /* Tool message background */
    /* ... more colors */
}
```

### Rendering Logic

Edit the JavaScript functions (lines ~568-1037):

- `formatContent()` - How message content is rendered
- `renderMessage()` - Overall message structure
- `parseMarkdown()` - Markdown parsing (uses marked.js)
- `syntaxHighlightJSON()` - JSON syntax highlighting

### Performance Tuning

Adjust timing constants (lines ~928-930):

```javascript
const INITIAL_LOAD_DURATION = 3000;  // How long to suppress animations
const INITIAL_DEBOUNCE = 500;  // Debounce during initial load
const NORMAL_DEBOUNCE = 150;  // Debounce after initial load
```

## Technical Details

### Dependencies

- **marked.js** (v11.1.1) - Loaded from CDN for markdown parsing
- No other dependencies - everything else is vanilla JavaScript

### Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Uses CSS variables and ES6+ features
- No polyfills included

### File Size

- ~1,000 lines total
- ~40KB uncompressed
- ~10KB gzipped

## Common Issues

### Messages not rendering
- Check browser console for JavaScript errors
- Verify the URL is accessible from LangSmith (no firewall/VPN blocking)
- Ensure CORS headers allow iframe embedding

### Flashing on load
- This should be fixed with the current debouncing implementation
- If still present, increase `INITIAL_DEBOUNCE` value

### Toggle buttons not working
- Make sure you're using the latest version
- Functions must be on `window` object for inline event handlers

## Architecture

**Single-file approach:**
- ✅ Simple deployment (just upload one file)
- ✅ Easy to customize (all code in one place)
- ✅ No build process required
- ✅ Good for prototypes and small projects

**Compared to React/Next.js:**
- More lines in one file, but less total code
- Direct DOM manipulation vs declarative components
- Faster initial setup, slower to add complex features

## Learn More

- [LangSmith Documentation](https://docs.langchain.com/langsmith/)
- [Custom Output Rendering Guide](https://docs.langchain.com/langsmith/custom-output-rendering)
- [postMessage API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)

## Related Projects

- [langchain-samples/custom-output-rendering](https://github.com/langchain-samples/custom-output-rendering) - React/Next.js approach with multiple renderers

## License

MIT
