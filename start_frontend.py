"""Start the Streamlit frontend."""
import subprocess
import sys
import os

if __name__ == "__main__":
    print("="*80)
    print("Starting Natural Language to SQL Frontend")
    print("="*80)
    print("\n🌐 Frontend will open in your browser automatically")
    print("📍 URL: http://localhost:8501")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*80)
    
    # Get the path to the frontend app
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "app.py")
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        frontend_path,
        "--server.port=8501",
        "--server.address=localhost"
    ])
