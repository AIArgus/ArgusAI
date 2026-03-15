# Skrypt do uruchamiania backendu ArgusAI
# Automatycznie zabija stary proces na porcie 8000 jeśli istnieje

Write-Host "=== ArgusAI Backend Starter ===" -ForegroundColor Cyan
Write-Host ""

# Sprawdź czy port 8000 jest zajęty
$port = 8000
$processInfo = netstat -ano | Select-String ":$port\s" | Select-String "LISTENING"

if ($processInfo) {
    # Wyciągnij PID z ostatniej kolumny
    $pid = ($processInfo -split '\s+')[-1]
    Write-Host "Port $port jest zajety przez proces PID: $pid" -ForegroundColor Yellow
    Write-Host "Zabijam stary proces..." -ForegroundColor Yellow
    
    try {
        taskkill /PID $pid /F | Out-Null
        Write-Host "Proces zabity!" -ForegroundColor Green
        Start-Sleep -Seconds 1
    } catch {
        Write-Host "Nie udalo sie zabic procesu. Moze juz nie istnieje?" -ForegroundColor Red
    }
} else {
    Write-Host "Port $port jest wolny" -ForegroundColor Green
}

Write-Host ""
Write-Host "Uruchamiam backend..." -ForegroundColor Cyan
Write-Host "Backend bedzie dostepny pod: http://localhost:8000" -ForegroundColor Green
Write-Host "Nacisnij Ctrl+C aby zatrzymac serwer" -ForegroundColor Yellow
Write-Host ""

# Uruchom backend
python main.py

