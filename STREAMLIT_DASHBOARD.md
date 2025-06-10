# Streamlit Dashboard for Wine Quality Prediction

This document provides information about the Streamlit dashboard included in this project, which complements the Next.js frontend application.

## Overview

The Streamlit dashboard provides an interactive web interface for:

1. Making individual wine quality predictions
2. Batch processing CSV files with multiple wine samples
3. Visualizing and analyzing prediction results
4. Exploring feature relationships and importance

## Features

### Single Prediction

- Input form for entering wine properties
- Real-time prediction using the trained model
- Visualization of input features and prediction results

### Batch Prediction

- Upload CSV files with multiple wine samples
- Process all samples in one go
- View summary statistics of predictions
- Download results as a CSV file

### Visualization Dashboard

- Distribution of wine quality predictions
- Analysis by wine type (red vs. white)
- Feature correlation analysis
- Interactive scatter plots for exploring relationships
- Feature importance visualization

### About 

- Information about the project, model, and technical stack

## Technical Details

The dashboard connects to the same API endpoints used by the Next.js frontend:

- FastAPI endpoints for predictions and batch processing
- Same model and processing logic as the main API

## Running the Dashboard

### Prerequisites

- Python 3.9+
- Virtual environment (same as for the API)
- Additional dependencies in `streamlit_requirements.txt`

### Starting the Dashboard

**Using PowerShell Script (Windows):**

```powershell
.\run_streamlit.ps1
```

**Using Bash Script (Unix/Linux/Mac):**

```bash
bash run_streamlit.sh
```

**Manual Start:**

```bash
pip install -r streamlit_requirements.txt
streamlit run streamlit_dashboard.py
```

The dashboard will be available at http://localhost:8501 by default.

## Important Notes

1. The API server (from `main.py`) must be running for the dashboard to function correctly.
2. The dashboard and Next.js frontend can run simultaneously, providing different UIs for the same functionality.
3. The Streamlit dashboard prioritizes data visualization and analysis, complementing the more application-focused Next.js frontend.

## Screenshots

[Screenshots would be included here after deployment]

## Future Enhancements

- Real-time model training visualization
- Advanced filtering options for batch results
- User authentication and saved predictions
- Custom model parameter tuning interface
