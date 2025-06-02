#!/bin/bash
# Setup script for Wine Quality Prediction API
# This script creates a virtual environment and installs all required dependencies

# Create virtual environment if it doesn't exist
if [ ! -d "./virtual" ]; then
    echo "Creating virtual environment 'virtual'..."
    python3 -m venv virtual
fi

# Activate virtual environment
echo "Activating virtual environment..."
source virtual/bin/activate

# Install dependencies
echo "Installing required packages..."
pip install -r requirements.txt

# Check if model exists
if [ ! -f "./wine.pkl" ]; then
    echo "WARNING: wine.pkl model file was not found!"
    echo "Please ensure the model file exists before running the application."
    echo "Model should contain: model, feature_names, model_type, and feature_set_name."
fi

echo ""
echo "Setup complete! You can now run the API with:"
echo "python main.py"
echo ""
echo "The API will be available at:"
echo "- FastAPI: http://127.0.0.1:8000"
echo "- Flask: http://127.0.0.1:8000/flask"
echo "- GraphQL: http://127.0.0.1:8000/graphql"
echo ""
echo "To test all APIs, run:"
echo "python test_api.py"
