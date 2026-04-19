#!/bin/bash

echo "========================================"
echo "Starting Natural Language to SQL System"
echo "========================================"
echo ""

# Start backend in background
echo "Starting Backend Server..."
uv run start_backend.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend in background
echo "Starting Frontend..."
uv run start_frontend.py &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Both servers are running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8501"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
