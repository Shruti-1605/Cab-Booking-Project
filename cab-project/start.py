import os
import subprocess
import time

def start_servers():
    print("Starting Cab Booking App...")
    
    # Backend command
    backend_cmd = 'start "Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"'
    
    # Frontend command  
    frontend_cmd = 'start "Frontend" cmd /k "cd frontend-new && npm run dev"'
    
    # Start backend
    os.system(backend_cmd)
    time.sleep(2)
    
    # Start frontend
    os.system(frontend_cmd)
    
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:5173")
    print("Both servers started in separate windows!")

if __name__ == "__main__":
    start_servers()