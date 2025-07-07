import subprocess
import threading
import webbrowser
import time
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

def run_api():
    """Run the FastAPI backend"""
    print("Starting the API backend...")
    subprocess.run([sys.executable, "app/api.py"], check=True)

def run_frontend():
    """Serve the frontend using a simple HTTP server"""
    print("Starting the frontend server...")
    os.chdir("frontend")
    
    class NoCacheHTTPRequestHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            super().end_headers()
    
    httpd = HTTPServer(('localhost', 8080), NoCacheHTTPRequestHandler)
    httpd.serve_forever()

def open_browser():
    """Open the browser to the frontend application"""
    print("Opening browser to http://localhost:8080")
    time.sleep(2)  # Give servers time to start
    webbrowser.open('http://localhost:8080')

if __name__ == "__main__":
    # Start the API thread
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Start the browser thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run the frontend server in the main thread
    run_frontend() 