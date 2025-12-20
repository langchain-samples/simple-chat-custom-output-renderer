#!/usr/bin/env python3
"""
Simple HTTP server for LangSmith Custom Output Renderer
Serves the index.html file with proper CORS headers to allow embedding in LangSmith
"""

import http.server
import socketserver
from pathlib import Path

PORT = 8000


class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler with CORS support"""

    def end_headers(self):
        # Add CORS headers to allow embedding in LangSmith
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


def run_server(port=PORT):
    """Start the HTTP server"""
    handler = CORSHTTPRequestHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"╔═══════════════════════════════════════════════════════════════╗")
        print(f"║  LangSmith Custom Output Renderer Server                     ║")
        print(f"╠═══════════════════════════════════════════════════════════════╣")
        print(f"║  Server running at: http://localhost:{port}                   ║")
        print(f"║                                                               ║")
        print(f"║  To use in LangSmith:                                         ║")
        print(f"║  1. Copy the URL: http://localhost:{port}/index.html          ║")
        print(f"║  2. Go to your LangSmith project settings                     ║")
        print(f"║  3. Navigate to 'Custom Output Rendering'                     ║")
        print(f"║  4. Paste the URL and save                                    ║")
        print(f"║                                                               ║")
        print(f"║  Press Ctrl+C to stop the server                              ║")
        print(f"╚═══════════════════════════════════════════════════════════════╝")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()


if __name__ == "__main__":
    # Change to the script's directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)

    run_server()
