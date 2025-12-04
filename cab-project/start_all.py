import subprocess
import webbrowser
import time
import os
from pathlib import Path

def start_project():
    print("Starting Cab Booking Project...")
    
    # Start backend server in background
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    
    # Start server
    server_process = subprocess.Popen([
        "python", "run_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    time.sleep(3)
    
    # Open frontend in browser
    frontend_path = Path(__file__).parent / "frontend" / "leaflet-map.html"
    webbrowser.open(f"file:///{frontend_path}")
    
    # Open API docs
    webbrowser.open("http://localhost:8000/docs")
    
    print("✅ Backend: http://localhost:8000")
    print("✅ Frontend: Opened in browser")
    print("✅ API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop server")
    
    try:
        server_process.wait()
    except KeyboardInterrupt:
        server_process.terminate()
        print("\nServer stopped!")

if __name__ == "__main__":
    start_project()