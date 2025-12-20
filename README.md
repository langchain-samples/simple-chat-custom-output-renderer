# LangSmith Custom Output Renderer for Chat LangChain

A local server and dark-themed frontend specifically designed for visualizing Chat LangChain conversation traces from LangSmith.

## Overview

This project provides a complete setup for creating custom visualizations of LangSmith run outputs and dataset reference outputs. It includes specialized renderers optimized for Chat LangChain conversation traces, displaying:

- Multi-turn conversations with user, assistant, and tool messages
- Tool calls with function names and arguments
- Tool responses from search operations (SearchDocsByLangChain, search_support_articles, etc.)
- Formatted search results with titles, links, and content
- Complete conversation flow visualization

## Features

- **Dark Theme Interface**: Easy-to-read dark theme optimized for code and JSON viewing
- **Real-time Message Display**: Instantly visualize postMessage events from LangSmith
- **Syntax Highlighting**: Automatic JSON syntax highlighting with color-coded keys, values, and data types
- **Local Testing**: Test your renderer locally before deploying to LangSmith
- **CORS-enabled Server**: Simple Python server with proper headers for embedding in LangSmith

## Quick Start

### 1. Start the Local Server

```bash
cd chat_langchain_custom_output_renderer
python3 server.py
```

The server will start on `http://localhost:8000`

### 2. Test with Real Traces

Open `http://localhost:8000/demo.html` in your browser to see actual traces from your Chat-LangChain project visualized in the custom renderer.

The demo includes 5 actual conversation traces fetched from your LangSmith project. You can:
- Select different traces from the dropdown
- See the conversation flow with user questions, assistant responses, and tool calls
- View formatted search results from documentation and support articles

### 3. Test with Simulated Data

Open `http://localhost:8000/test.html` to test with simulated postMessage events (for generic testing).

### 4. Configure in LangSmith

**For Chat LangChain Project:**
1. Copy the URL: `http://localhost:8000/index_chat.html`
2. Go to your Chat-LangChain project settings in LangSmith
3. Navigate to **Custom Output Rendering** section
4. Paste the URL and save

**For Generic Projects:**
1. Use `http://localhost:8000/index.html` for general-purpose trace rendering

## Files

- **`index.html`** - Generic custom output renderer with dark theme
- **`index_chat.html`** - Chat LangChain-specific renderer optimized for conversation traces
- **`demo.html`** - Demo page that loads actual traces from your LangSmith project
- **`test.html`** - Local testing page to simulate postMessage events
- **`server.py`** - Simple Python HTTP server with CORS support
- **`traces/`** - Directory containing fetched traces from your Chat-LangChain project
- **`fetch_traces.py`** - (Optional) Python script to fetch traces if needed
- **`README.md`** - This file

## Chat LangChain Features

The `index_chat.html` renderer is specifically designed for Chat LangChain traces and includes:

### Conversation Display
- **User Messages**: Blue-themed cards showing user questions
- **Assistant Messages**: Green-themed cards showing assistant responses
- **Tool Messages**: Purple-themed cards showing tool execution results

### Tool Call Visualization
- Function names displayed with syntax highlighting
- Arguments shown in formatted JSON
- Tool call IDs for tracking

### Search Result Parsing
- Automatic parsing of search results from `SearchDocsByLangChain`
- Formatted display of:
  - Document titles
  - Links to source documents
  - Content excerpts
- Scrollable content areas for long results

### Demo with Real Traces

The `demo.html` page allows you to:
1. Select from actual traces fetched from your LangSmith project
2. Load and visualize them in the custom renderer
3. See exactly how your traces will appear in LangSmith

## How It Works

### Message Structure

LangSmith sends messages to your custom renderer using the postMessage API with this structure:

```javascript
{
  type: "output" | "reference",
  data: {
    // The actual output or reference data
  },
  metadata: {
    inputs: {
      // Input data that generated this output
    }
  }
}
```

### Message Delivery

LangSmith uses exponential backoff retry (up to 6 attempts) to ensure message delivery:
- Attempt 1: 100ms delay
- Attempt 2: 200ms delay
- Attempt 3: 400ms delay
- Attempt 4: 800ms delay
- Attempt 5: 1600ms delay
- Attempt 6: 3200ms delay

## Customization

### Modifying the Renderer

Edit `index.html` to customize how your data is displayed:

1. **Styling**: Modify the `<style>` section to change colors, fonts, and layout
2. **Data Parsing**: Update the `renderValue()` function to handle specific data types
3. **Message Handling**: Enhance the `window.addEventListener('message')` handler for custom logic

### Example: Adding Custom Data Type Handling

```javascript
function renderValue(value) {
    // Custom handling for image URLs
    if (typeof value === 'string' && value.match(/\.(jpg|jpeg|png|gif)$/i)) {
        return `<img src="${value}" style="max-width: 100%; border-radius: 8px;">`;
    }

    // Custom handling for markdown
    if (typeof value === 'object' && value.format === 'markdown') {
        return `<div class="markdown">${marked(value.content)}</div>`;
    }

    // Default handling
    if (typeof value === 'object') {
        return `<div class="code-block">${syntaxHighlight(value)}</div>`;
    }

    return `<div class="data-display">${String(value)}</div>`;
}
```

## Configuration Locations in LangSmith

Custom output rendering can be configured at three levels (with precedence: annotation queue > dataset > tracing project):

1. **Tracing Projects**: Project settings → Custom Output Rendering section
2. **Datasets**: Dataset menu (⋮) → Custom Output Rendering option
3. **Annotation Queues**: Queue settings → Custom Output Rendering section

## Where Custom Rendering Appears

- Experiment comparison views
- Run detail panes for dataset-associated runs
- Annotation queues

## Common Use Cases

### 1. Domain-Specific Formatting

Display specialized data types in their native format:
- Medical records with structured fields
- Legal documents with citations
- Financial data with tables and charts

### 2. Custom Visualizations

Create rich visualizations from structured data:
- Charts and graphs from metrics
- Timeline views for conversation history
- Network diagrams for agent interactions

### 3. Multi-Modal Outputs

Handle different types of content:
- Images and videos
- Code snippets with syntax highlighting
- Interactive components

## Testing Examples

The `test.html` page includes several preset messages:

- **Simple Text**: Basic string output with metadata
- **Structured Data**: Complex nested JSON objects
- **Conversation**: Multi-turn chat messages
- **Error Output**: Error handling display

## Troubleshooting

### Renderer not loading in LangSmith

- Ensure the server is running on `http://localhost:8000`
- Check that the URL in LangSmith settings is correct
- Verify CORS headers are enabled (they are by default in `server.py`)

### Messages not appearing

- Open the browser console to check for JavaScript errors
- Verify the message structure matches the expected format
- Check that the postMessage is being sent to the correct window

### Styling issues

- Check browser compatibility (modern browsers recommended)
- Clear browser cache and reload
- Inspect CSS with browser DevTools

## Development Tips

1. **Test locally first**: Always test with `test.html` before deploying
2. **Console logging**: The renderer logs received messages to the console
3. **Incremental changes**: Make small changes and test frequently
4. **Browser DevTools**: Use the Elements and Console tabs for debugging

## Port Configuration

By default, the server runs on port 8000. To change this:

```python
# Edit server.py
PORT = 3000  # Change to your desired port
```

Then update the URL in LangSmith accordingly.

## Security Notes

- This server is intended for local development only
- Do not expose this server to the public internet
- CORS is enabled (`Access-Control-Allow-Origin: *`) for development convenience
- For production use, consider restricting CORS to specific origins

## Learn More

- [LangSmith Documentation](https://docs.langchain.com/langsmith/)
- [Custom Output Rendering Guide](https://docs.langchain.com/langsmith/custom-output-rendering)
- [postMessage API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)

## License

This is a demonstration project for LangSmith custom output rendering.
