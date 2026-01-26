@echo off
echo ================================
echo Starting MindSpace Application
echo ================================
echo.

:: Start Python Mood Analysis API
echo [1/3] Starting Python Mood Analysis API (Port 5001)...
start "Mood Analysis API" cmd /k "cd mood-analysis-system && python api_server.py"
timeout /t 5 /nobreak >nul

:: Start Node.js Backend Server
echo [2/3] Starting Node.js Backend Server (Port 5000)...
start "Backend Server" cmd /k "cd backend && npm start"
timeout /t 3 /nobreak >nul

:: Start Next.js Frontend
echo [3/3] Starting Next.js Frontend (Port 3000)...
start "Frontend" cmd /k "npm run dev"
timeout /t 2 /nobreak >nul

echo.
echo ================================
echo All servers started successfully!
echo ================================
echo.
echo Frontend:          http://localhost:3000
echo Backend API:       http://localhost:5000
echo Mood Analysis API: http://localhost:5001
echo.
echo Press any key to close this window (servers will continue running)...
pause >nul
