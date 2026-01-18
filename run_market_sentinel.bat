@echo off
REM Market Sentinel Runner - Single Command to Launch
echo 🚀 Starting Market Sentinel...

REM Start Docker service in WSL2
echo 🐳 Starting Docker service...
wsl bash -c "sudo service docker start"

REM Run docker compose
echo 🚀 Launching Market Sentinel...
echo 📊 Dashboard will be available at: http://localhost:8501
echo Press Ctrl+C to stop...
echo.

wsl bash -c "cd /mnt/c/RaveMinds/Projects/market-sentinel && docker compose up"