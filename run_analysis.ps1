cd d:\semester_6\wine
.\virtual\Scripts\Activate.ps1
$ErrorActionPreference = "Continue"

# Start the server in background
Write-Host "Starting the API server..."
$serverProcess = Start-Process -FilePath "python" -ArgumentList "-m uvicorn main:fastapi_app --host 127.0.0.1 --port 8000" -PassThru -WindowStyle Hidden

# Wait for the server to start
Write-Host "Waiting 5 seconds for server to start..."
Start-Sleep -Seconds 5

try {
    # Run analysis scripts
    Write-Host "Running basic analysis..."
    python batch_analysis.py
    Write-Host "Basic analysis completed"
    
    Write-Host "Running advanced analysis..."
    python advanced_analysis.py 
    Write-Host "Advanced analysis completed"
} catch {
    Write-Host "Error: $_"
} finally {
    # Stop the server
    Write-Host "Stopping the API server..."
    Stop-Process -Id $serverProcess.Id -Force
    Write-Host "Server stopped."
}
