#!/bin/bash
# Run Streamlit Dashboard

# Activate the virtual environment if available
if [ -d "virtual" ]; then
    echo "Activating virtual environment..."
    source virtual/bin/activate
fi

# Install required packages if not already installed
echo "Installing required packages..."
pip install -r streamlit_requirements.txt

# Run Streamlit app
echo "Starting Streamlit Dashboard..."
streamlit run streamlit_dashboard.py
