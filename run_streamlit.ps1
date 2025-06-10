# Run Streamlit Dashboard

# Activate the virtual environment if available
if (Test-Path "virtual") {
    Write-Host "Activating virtual environment..."
    & .\virtual\Scripts\Activate.ps1
}

# Install required packages if not already installed
Write-Host "Installing required packages..."
pip install -r streamlit_requirements.txt

# Run Streamlit app
Write-Host "Starting Streamlit Dashboard..."
streamlit run streamlit_dashboard.py
