import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import os

def get_batch_predictions(csv_file_path):
    """Get batch predictions from the API"""
    print(f"Getting batch predictions for {csv_file_path}...")
    
    with open(csv_file_path, 'rb') as f:
        files = {'file': (os.path.basename(csv_file_path), f, 'text/csv')}
        response = requests.post('http://localhost:8000/batch-predict', files=files)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
        
    result_json = response.json()
    
    # Also get the CSV with predictions to have actual data
    with open(csv_file_path, 'rb') as f:
        files = {'file': (os.path.basename(csv_file_path), f, 'text/csv')}
        response = requests.post('http://localhost:8000/batch-predict?download=true', files=files)
    
    # Save and read the CSV with predictions
    result_csv_path = 'prediction_results.csv'
    with open(result_csv_path, 'wb') as f:
        f.write(response.content)
    
    df = pd.read_csv(result_csv_path)
    return df, result_json

def analyze_regression_predictions(df, threshold=0.5, actual_column=None):
    """
    Analyze regression predictions using a threshold to classify "correct" vs "incorrect"
    Since we don't have actual values, we'll consider predictions within the threshold 
    of the mean as "correct" and outside as "incorrect".
    
    If actual_column is provided, we'll use that for comparison instead.
    """
    # If we have actual values, use them
    if actual_column and actual_column in df.columns:
        # Calculate absolute error
        df['absolute_error'] = abs(df[actual_column] - df['prediction'])
        mean_error = df['absolute_error'].mean()
        
        # Define correct/incorrect based on error threshold
        df['prediction_status'] = df['absolute_error'] <= threshold
        error_message = f"Prediction considered incorrect if absolute error > {threshold}"
    else:
        # Calculate stats
        mean_prediction = df['prediction'].mean()
        std_prediction = df['prediction'].std()
        
        # Define a threshold based on standard deviation
        lower_bound = mean_prediction - threshold * std_prediction
        upper_bound = mean_prediction + threshold * std_prediction
        
        # Mark predictions as correct if they're within the threshold of the mean
        df['prediction_status'] = (df['prediction'] >= lower_bound) & (df['prediction'] <= upper_bound)
        error_message = f"Prediction considered incorrect if it's outside {threshold} standard deviations from the mean"
    
    # Map boolean to string for better display
    df['status'] = df['prediction_status'].map({True: 'Correct', False: 'Incorrect'})
    
    # Calculate accuracy-like metric
    accuracy = df['prediction_status'].mean() * 100
    
    return df, accuracy, error_message

def generate_regression_report(df, accuracy, error_message):
    """Generate a report similar to classification report but for regression"""
    print("\n=== Regression Analysis Report ===")
    print(f"Total samples: {len(df)}")
    print(f"Correct predictions: {df['prediction_status'].sum()}")
    print(f"Incorrect predictions: {len(df) - df['prediction_status'].sum()}")
    print(f"Accuracy-like metric: {accuracy:.2f}%")
    print(f"Note: {error_message}")
    
    print("\nSample statistics:")
    print(f"Mean prediction: {df['prediction'].mean():.4f}")
    print(f"Std prediction: {df['prediction'].std():.4f}")
    print(f"Min prediction: {df['prediction'].min():.4f}")
    print(f"Max prediction: {df['prediction'].max():.4f}")
    
    print("\nIncorrect predictions:")
    incorrect_df = df[~df['prediction_status']]
    if len(incorrect_df) > 0:
        for _, row in incorrect_df.iterrows():
            features_str = ", ".join([f"{col}: {row[col]}" for col in df.columns if col not in ['prediction', 'prediction_status', 'status']])
            print(f"  Sample [{features_str}] -> Predicted: {row['prediction']:.4f}")
    else:
        print("  None")

def create_visualization(df):
    """Create visualizations of the regression results"""
    # Set style
    sns.set(style="whitegrid")
    
    # Create a figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Scatter plot of predictions by wine type with correct/incorrect highlighted
    ax1 = axes[0, 0]
    colors = {"Correct": "green", "Incorrect": "red"}
    sns.scatterplot(
        x="type_white", 
        y="prediction", 
        hue="status",
        palette=colors,
        s=100,
        alpha=0.7,
        data=df,
        ax=ax1
    )
    ax1.set_title("Wine Quality Predictions by Type", fontsize=14)
    ax1.set_xlabel("Wine Type (0=Red, 1=White)", fontsize=12)
    ax1.set_ylabel("Predicted Quality", fontsize=12)
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(["Red", "White"])
    
    # 2. Scatter plot by alcohol content
    ax2 = axes[0, 1]
    sns.scatterplot(
        x="alcohol", 
        y="prediction", 
        hue="status",
        palette=colors,
        s=100,
        alpha=0.7,
        data=df,
        ax=ax2
    )
    ax2.set_title("Wine Quality Predictions by Alcohol Content", fontsize=14)
    ax2.set_xlabel("Alcohol Content", fontsize=12)
    ax2.set_ylabel("Predicted Quality", fontsize=12)
    
    # 3. Distribution of predictions with highlighting
    ax3 = axes[1, 0]
    for status, color in colors.items():
        subset = df[df['status'] == status]
        sns.kdeplot(
            subset['prediction'], 
            fill=True, 
            color=color, 
            label=status,
            alpha=0.5,
            ax=ax3
        )
    ax3.set_title("Distribution of Predictions", fontsize=14)
    ax3.set_xlabel("Predicted Quality", fontsize=12)
    ax3.set_ylabel("Density", fontsize=12)
    
    # 4. Bar chart of prediction counts by status with a gap between bars
    ax4 = axes[1, 1]
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    # Create custom positions with a gap
    positions = [0, 1.5]  # Add a gap of 0.5 between positions
    colors_list = [colors[status] for status in status_counts['Status']]
    
    bars = ax4.bar(
        positions,
        status_counts['Count'],
        color=colors_list,
        width=0.7
    )
    
    # Add value labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax4.text(
            bar.get_x() + bar.get_width()/2.,
            height + 0.1,
            f"{height}",
            ha='center',
            va='bottom',
            fontsize=12
        )
    
    ax4.set_title("Prediction Counts by Status", fontsize=14)
    ax4.set_ylabel("Count", fontsize=12)
    ax4.set_xticks(positions)
    ax4.set_xticklabels(status_counts['Status'])
    
    # Adjust layout
    plt.tight_layout()
    plt.savefig("regression_analysis.png")
    print("\nChart saved as 'regression_analysis.png'")
    
    # Show the plot if in an interactive environment
    plt.show()

def main():
    # Get predictions for the test batch
    df, result_json = get_batch_predictions('test_batch.csv')
    if df is None:
        print("Failed to get predictions. Is the API server running?")
        return
    
    # Analyze predictions (using 0.5 standard deviations as the threshold)
    df, accuracy, error_message = analyze_regression_predictions(df, threshold=0.5)
    
    # Generate report
    generate_regression_report(df, accuracy, error_message)
    
    # Create visualizations
    create_visualization(df)

if __name__ == "__main__":
    main()
