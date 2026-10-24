# MasteryLoop 1-Click PowerShell Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "           MasteryLoop - Starting Full Stack            " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$root = $PSScriptRoot

Write-Host "`n[1/2] Launching FastAPI Backend on http://127.0.0.1:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\backend'; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Launching React Vite Frontend on http://127.0.0.1:5173..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\frontend'; npm run dev"

Start-Sleep -Seconds 3
Write-Host "`nOpening http://127.0.0.1:5173/ in your browser..." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:5173/"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "Both servers are launching!" -ForegroundColor Cyan
Write-Host "Frontend: http://127.0.0.1:5173/" -ForegroundColor White
Write-Host "Backend:  http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
