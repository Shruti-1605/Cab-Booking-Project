import subprocess
import sys
import os
import time
import threading

def run_backend():
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    subprocess.run([sys.executable, '-m', 'uvicorn', 'main_advanced:app', '--reload', '--port', '8000'], cwd=backend_path)

def run_frontend():
    time.sleep(3)
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend-new')
    subprocess.run(['npm', 'run', 'dev'], shell=True, cwd=frontend_path)

if __name__ == "__main__":
    print("Starting Cab Booking App...")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:5173")
    
    # Backend thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Frontend main thread
    run_frontend()