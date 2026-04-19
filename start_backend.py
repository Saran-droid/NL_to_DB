"""Start the FastAPI backend server."""
import uvicorn
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("="*80)
    print("Starting Natural Language to SQL Backend Server")
    print("="*80)
    print("\n📡 API will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled for development")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*80)
    
    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
