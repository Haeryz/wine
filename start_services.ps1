# Start FastAPI in one process
$fastAPIProcess = Start-Process -PassThru -FilePath "$PSScriptRoot\virtual\Scripts\uvicorn.exe" -ArgumentList "main:app", "--reload" -WindowStyle Normal

Write-Host "FastAPI server started with PID: $($fastAPIProcess.Id)"
Write-Host "Waiting 5 seconds for the FastAPI server to initialize..."
Start-Sleep -Seconds 5

# Start Streamlit in another process
$streamlitProcess = Start-Process -PassThru -FilePath "$PSScriptRoot\virtual\Scripts\streamlit.exe" -ArgumentList "run", "streamlit_dashboard.py" -WindowStyle Normal

Write-Host "Streamlit dashboard started with PID: $($streamlitProcess.Id)"
Write-Host "Both services are now running!"
Write-Host "FastAPI: http://localhost:8000"
Write-Host "Streamlit: http://localhost:8501"

Write-Host "Press Ctrl+C to stop both services..."
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    # Clean up processes when script is interrupted
    Write-Host "Stopping services..."
    if ($fastAPIProcess -and !$fastAPIProcess.HasExited) {
        Stop-Process -Id $fastAPIProcess.Id -Force
        Write-Host "FastAPI server stopped."
    }
    if ($streamlitProcess -and !$streamlitProcess.HasExited) {
        Stop-Process -Id $streamlitProcess.Id -Force
        Write-Host "Streamlit dashboard stopped."
    }
}
