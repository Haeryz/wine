# Regression Analysis for Wine Quality Predictions

## Overview

This extension provides detailed analysis and visualization tools for batch wine quality predictions. Since this is a regression problem (predicting a continuous quality score) rather than a classification problem, traditional metrics like precision, recall, and F1-score don't apply. Instead, we've implemented custom analysis approaches that give similar insights for regression predictions.

## Features

### Basic Analysis (`batch_analysis.py`)

This script performs a threshold-based analysis of the regression predictions:

1. **Correctness Determination**:
   - Since we're dealing with regression, we define "correct" vs "incorrect" predictions using a threshold approach
   - Predictions within 0.5 standard deviations of the mean are considered "correct"
   - This simulates a tolerance band for acceptable predictions

2. **Comprehensive Report**:
   - Total number of samples processed
   - Count of "correct" and "incorrect" predictions
   - Accuracy-like metric (percentage of predictions within threshold)
   - Statistical summary of predictions
   - Detailed listing of samples classified as "incorrect"

3. **Visualizations**:
   - Scatter plot of predictions by wine type with correct/incorrect highlighting
   - Scatter plot of predictions by alcohol content
   - Distribution plot showing the density of correct vs incorrect predictions
   - Bar chart with a deliberate gap between correct/incorrect counts

### Advanced Analysis (`advanced_analysis.py`)

This script provides a more sophisticated analysis with simulated actual values:

1. **Simulation of Actual Values**:
   - Since real-world testing would involve known quality values, this script simulates "actual" values
   - Predictions plus controlled random noise create a realistic testing scenario

2. **Regression Metrics**:
   - Mean Absolute Error (MAE)
   - Mean Squared Error (MSE)
   - Root Mean Squared Error (RMSE)
   - R² Score (coefficient of determination)
   - Accuracy-like metric (percentage within defined error threshold)

3. **Advanced Visualizations**:
   - Actual vs Predicted scatter plot with perfect prediction line
   - Error distribution histogram with threshold indicator
   - Error analysis by wine type (box plot)
   - Error correlation with alcohol content
   - Prediction status counts with gap between bars and percentage labels
   - Feature correlation with prediction error (simulated feature importance)
   - Error heatmap by key features

## How to Use

### Running the Analyses

1. Start the Wine Quality Prediction API server:
   ```
   python main.py
   ```

2. Run the analysis scripts:
   ```
   python batch_analysis.py
   python advanced_analysis.py
   ```
   
   Or use the provided PowerShell script:
   ```
   .\run_analysis.ps1
   ```

3. Review the outputs:
   - Console output with detailed reports
   - Generated visualization files:
     - `regression_analysis.png` (basic analysis)
     - `advanced_regression_analysis.png` (advanced analysis)
   - CSV files with analyzed data:
     - `prediction_results.csv`
     - `prediction_results_advanced.csv`
     - `analyzed_predictions.csv`

### Understanding the Results

- **Threshold-Based Accuracy**: Unlike classification where predictions are either right or wrong, our regression analysis defines "correctness" based on a threshold.
- **Error Analysis**: Pay attention to which samples have higher errors and which features correlate with errors.
- **Feature Relationships**: The visualizations help identify patterns in how features relate to prediction quality.

## Customization

You can customize these analyses by:

1. Adjusting the threshold value in the function calls:
   ```python
   df, accuracy, error_message = analyze_regression_predictions(df, threshold=0.5)  # Adjust threshold
   ```

2. Adding domain-specific analyses based on wine industry knowledge.

3. Extending with additional visualizations for specific features of interest.
