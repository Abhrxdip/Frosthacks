@echo off
echo ========================================
echo MindSpace Setup Script
echo ========================================
echo.

echo Step 1: Installing Node.js dependencies...
echo.

echo [1/2] Installing backend dependencies...
cd backend
call npm install
cd ..

echo [2/2] Installing frontend dependencies...
call npm install

echo.
echo Step 2: Installing Python dependencies...
echo.

cd mood-analysis-system
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python packages...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create mood-analysis-system\.env file with your API key
echo    Copy .env.example to .env and add your GEMINI_API_KEY
echo.
echo 2. Run start-servers.bat to start all servers
echo.
echo Press any key to exit...
pause >nul
