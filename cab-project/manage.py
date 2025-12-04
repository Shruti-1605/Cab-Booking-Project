import threading
import subprocess
import sys
import os
import time

def run_backend():
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--reload', '--port', '8000'], cwd=backend_path)

def run_frontend():
    time.sleep(3)
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend-new')
    subprocess.run(['npm', 'run', 'dev'], shell=True, cwd=frontend_path)

def runserver():
    print("Starting Cab Booking App...")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:5173")
    
    # Backend thread mein chalao
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Frontend main thread mein chalao
    run_frontend()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        runserver()
    else:
        print("Usage: python manage.py runserver")


        