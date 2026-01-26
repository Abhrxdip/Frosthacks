#!/bin/bash

echo "================================"
echo "Starting MindSpace Application"
echo "================================"
echo

# Start Python Mood Analysis API
echo "[1/3] Starting Python Mood Analysis API (Port 5001)..."
cd mood-analysis-system
python api_server.py &
PYTHON_PID=$!
cd ..
sleep 5

# Start Node.js Backend Server
echo "[2/3] Starting Node.js Backend Server (Port 5000)..."
cd backend
npm start &
BACKEND_PID=$!
cd ..
sleep 3

# Start Next.js Frontend
echo "[3/3] Starting Next.js Frontend (Port 3000)..."
npm run dev &
FRONTEND_PID=$!
sleep 2

echo
echo "================================"
echo "All servers started successfully!"
echo "================================"
echo
echo "Frontend:          http://localhost:3000"
echo "Backend API:       http://localhost:5000"
echo "Mood Analysis API: http://localhost:5001"
echo
echo "Process IDs:"
echo "  Python API: $PYTHON_PID"
echo "  Backend:    $BACKEND_PID"
echo "  Frontend:   $FRONTEND_PID"
echo
echo "Press Ctrl+C to stop all servers"

# Wait for Ctrl+C
trap "kill $PYTHON_PID $BACKEND_PID $FRONTEND_PID; exit" INT
wait
