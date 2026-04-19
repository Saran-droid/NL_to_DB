#!/usr/bin/env python3
"""Main entry point for Natural Language to SQL application."""
import sys
import subprocess
from pathlib import Path

def main():
    """Run the application based on command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python run.py [cli|backend|frontend|all]")
        print("\nCommands:")
        print("  cli       - Run command-line interface")
        print("  backend   - Start FastAPI backend server")
        print("  frontend  - Start Streamlit frontend")
        print("  all       - Start both backend and frontend")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "cli":
        from nl_to_sql.cli import main as cli_main
        cli_main()
    
    elif command == "backend":
        subprocess.run([sys.executable, "scripts/start_backend.py"])
    
    elif command == "frontend":
        subprocess.run([sys.executable, "scripts/start_frontend.py"])
    
    elif command == "all":
        import platform
        if platform.system() == "Windows":
            subprocess.run(["start_all.bat"], shell=True)
        else:
            subprocess.run(["./start_all.sh"], shell=True)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
