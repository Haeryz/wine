# Setup script for Wine Quality Prediction API
# This script creates a virtual environment and installs all required dependencies

# Check PowerShell version to ensure compatibility
$PSVersionTable.PSVersion

# Create virtual environment if it doesn't exist
if (-not (Test-Path -Path ".\virtual")) {
    Write-Host "Creating virtual environment 'virtual'..."
    python -m venv virtual
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\virtual\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing required packages..."
pip install -r requirements.txt

# Check if model exists
if (-not (Test-Path -Path ".\wine.pkl")) {
    Write-Host "WARNING: wine.pkl model file was not found!"
    Write-Host "Please ensure the model file exists before running the application."
    Write-Host "Model should contain: model, feature_names, model_type, and feature_set_name."
}

Write-Host ""
Write-Host "Setup complete! You can now run the API with:"
Write-Host "python main.py"
Write-Host ""
Write-Host "The API will be available at:"
Write-Host "- FastAPI: http://127.0.0.1:8000"
Write-Host "- Flask: http://127.0.0.1:8000/flask"
Write-Host "- GraphQL: http://127.0.0.1:8000/graphql"
Write-Host ""
Write-Host "To test all APIs, run:"
Write-Host "python test_api.py"
