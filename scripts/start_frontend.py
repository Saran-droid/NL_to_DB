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
    
    # Get the path to the frontend module
    frontend_module = "nl_to_sql.frontend"
    
    # Run streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "-m", frontend_module,
        "--server.port=8501",
        "--server.address=localhost"
    ])
