# Market Sentinel Runner - PowerShell Script
Write-Host "🚀 Starting Market Sentinel..." -ForegroundColor Green

# Start WSL2 and navigate to project
Write-Host "📁 Opening WSL2 and navigating to project..." -ForegroundColor Yellow
wsl bash -c "cd /mnt/c/RaveMinds/Projects/market-sentinel && pwd"

# Start Docker service
Write-Host "🐳 Starting Docker service..." -ForegroundColor Yellow
wsl bash -c "sudo service docker start"

# Wait a moment for Docker to start
Start-Sleep -Seconds 3

# Run docker compose
Write-Host "🚀 Launching Market Sentinel..." -ForegroundColor Green
Write-Host "📊 Dashboard will be available at: http://localhost:8501" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Run docker compose (this will keep running)
wsl bash -c "cd /mnt/c/RaveMinds/Projects/market-sentinel && docker compose up"

Write-Host ""
Write-Host "🎉 Market Sentinel stopped!" -ForegroundColor Green