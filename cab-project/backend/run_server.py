import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("Starting Cab Booking Server...")
    print("Server will run at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Map Interface: Open leaflet-map.html in browser")
    print("Stripe Payment: Configured and Ready")
    print("\n" + "="*50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )