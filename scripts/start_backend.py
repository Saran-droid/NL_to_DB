"""Start the FastAPI backend server."""
import uvicorn

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
        "nl_to_sql.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
