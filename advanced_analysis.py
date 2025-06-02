import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

def get_batch_predictions(csv_file_path):
    """Get batch predictions from the API"""
    print(f"Getting batch predictions for {csv_file_path}...")
    
    # Get CSV with predictions
    with open(csv_file_path, 'rb') as f:
        files = {'file': (os.path.basename(csv_file_path), f, 'text/csv')}
        response = requests.post('http://localhost:8000/batch-predict?download=true', files=files)
    
    # Save and read the CSV with predictions
    result_csv_path = 'prediction_results_advanced.csv'
    with open(result_csv_path, 'wb') as f:
        f.write(response.content)
    
    df = pd.read_csv(result_csv_path)
    
    # Simulate "actual" quality values for demonstration purposes
    # In a real scenario, you would have actual values to compare against
    np.random.seed(42)  # For reproducibility
    
    # Generate simulated actual values around predictions with some noise
    df['actual_quality'] = df['prediction'] + np.random.normal(0, 0.5, len(df))
    
    # Ensure values are in the typical wine quality range (0-10)
    df['actual_quality'] = df['actual_quality'].clip(0, 10)
    df['actual_quality'] = df['actual_quality'].round(2)
    
    return df

def advanced_regression_analysis(df, error_threshold=0.5):
    """Perform advanced regression analysis with actual vs predicted values"""
    
    # Calculate errors
    df['absolute_error'] = abs(df['actual_quality'] - df['prediction'])
    df['squared_error'] = (df['actual_quality'] - df['prediction'])**2
    
    # Determine if prediction is "correct" based on threshold
    df['prediction_status'] = df['absolute_error'] <= error_threshold
    df['status'] = df['prediction_status'].map({True: 'Correct', False: 'Incorrect'})
    
    # Calculate regression metrics
    mse = mean_squared_error(df['actual_quality'], df['prediction'])
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(df['actual_quality'], df['prediction'])
    r2 = r2_score(df['actual_quality'], df['prediction'])
    
    accuracy = df['prediction_status'].mean() * 100
    
    return df, {
        'accuracy': accuracy,
        'mse': mse,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'threshold': error_threshold
    }

def generate_advanced_report(df, metrics):
    """Generate a comprehensive regression analysis report"""
    print("\n=== Advanced Regression Analysis Report ===")
    print(f"Total samples: {len(df)}")
    print(f"Threshold for 'correctness': {metrics['threshold']}")
    print(f"Correct predictions: {df['prediction_status'].sum()} ({metrics['accuracy']:.2f}%)")
    print(f"Incorrect predictions: {len(df) - df['prediction_status'].sum()} ({100 - metrics['accuracy']:.2f}%)")
    
    print("\nRegression Metrics:")
    print(f"Mean Absolute Error (MAE): {metrics['mae']:.4f}")
    print(f"Mean Squared Error (MSE): {metrics['mse']:.4f}")
    print(f"Root Mean Squared Error (RMSE): {metrics['rmse']:.4f}")
    print(f"R² Score: {metrics['r2']:.4f}")
    
    print("\nSample statistics:")
    print(f"Mean prediction: {df['prediction'].mean():.4f}")
    print(f"Mean actual: {df['actual_quality'].mean():.4f}")
    print(f"Mean absolute error: {df['absolute_error'].mean():.4f}")
    
    print("\nIncorrect predictions:")
    incorrect_df = df[~df['prediction_status']]
    if len(incorrect_df) > 0:
        for i, (_, row) in enumerate(incorrect_df.iterrows(), 1):
            print(f"  Sample {i}:")
            print(f"    Wine type: {'White' if row['type_white'] == 1 else 'Red'}")
            print(f"    Key features: acidity={row['volatile_acidity']}, alcohol={row['alcohol']}, pH={row['pH']}")
            print(f"    Actual: {row['actual_quality']:.2f}, Predicted: {row['prediction']:.2f}")
            print(f"    Absolute error: {row['absolute_error']:.2f}")
    else:
        print("  None")

def create_advanced_visualizations(df):
    """Create comprehensive visualizations for regression analysis"""
    # Set style
    sns.set(style="whitegrid")
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(18, 15))
    
    # Define grid layout
    gs = fig.add_gridspec(3, 3)
    
    # 1. Actual vs Predicted scatter plot with correctness
    ax1 = fig.add_subplot(gs[0, 0:2])
    colors = {"Correct": "green", "Incorrect": "red"}
    scatter = sns.scatterplot(
        x="actual_quality",
        y="prediction",
        hue="status",
        palette=colors,
        s=100,
        alpha=0.7,
        data=df,
        ax=ax1
    )
    
    # Add perfect prediction line
    min_val = min(df['actual_quality'].min(), df['prediction'].min()) - 0.5
    max_val = max(df['actual_quality'].max(), df['prediction'].max()) + 0.5
    ax1.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5)
    
    # Add error threshold lines
    threshold = abs(df.loc[~df['prediction_status'], 'absolute_error'].min())
    ax1.fill_between(
        [min_val, max_val], 
        [min_val - threshold, max_val - threshold], 
        [min_val + threshold, max_val + threshold], 
        color='gray', 
        alpha=0.1
    )
    
    ax1.set_title("Actual vs Predicted Wine Quality", fontsize=16)
    ax1.set_xlabel("Actual Quality", fontsize=14)
    ax1.set_ylabel("Predicted Quality", fontsize=14)
    ax1.set_xlim(min_val, max_val)
    ax1.set_ylim(min_val, max_val)
    
    # 2. Error distribution
    ax2 = fig.add_subplot(gs[0, 2])
    error_plot = sns.histplot(
        df['absolute_error'], 
        kde=True,
        color="skyblue",
        ax=ax2
    )
    # Add vertical line for threshold
    ax2.axvline(x=threshold, color='red', linestyle='--', alpha=0.7, label=f'Threshold ({threshold})')
    ax2.set_title("Distribution of Absolute Errors", fontsize=16)
    ax2.set_xlabel("Absolute Error", fontsize=14)
    ax2.legend()
    
    # 3. Error by wine type
    ax3 = fig.add_subplot(gs[1, 0])
    wine_types = {0: "Red", 1: "White"}
    df['wine_type'] = df['type_white'].map(wine_types)
    
    box_plot = sns.boxplot(
        x="wine_type",
        y="absolute_error",
        data=df,
        palette=["#8B0000", "#F8F8FF"],
        ax=ax3
    )
    ax3.set_title("Error by Wine Type", fontsize=16)
    ax3.set_xlabel("Wine Type", fontsize=14)
    ax3.set_ylabel("Absolute Error", fontsize=14)
    
    # 4. Error by alcohol content
    ax4 = fig.add_subplot(gs[1, 1])
    sns.scatterplot(
        x="alcohol",
        y="absolute_error",
        hue="wine_type",
        palette=["#8B0000", "#F8F8FF"],
        size="absolute_error",
        sizes=(20, 200),
        data=df,
        ax=ax4
    )
    ax4.set_title("Error by Alcohol Content", fontsize=16)
    ax4.set_xlabel("Alcohol Content (%)", fontsize=14)
    ax4.set_ylabel("Absolute Error", fontsize=14)
    
    # 5. Prediction status counts with gap
    ax5 = fig.add_subplot(gs[1, 2])
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    # Create positions with gap
    positions = [0, 1.5]
    colors_list = [colors[status] for status in status_counts['Status']]
    
    bars = ax5.bar(
        positions,
        status_counts['Count'],
        color=colors_list,
        width=0.7
    )
    
    # Add percentage labels
    total = status_counts['Count'].sum()
    for bar in bars:
        height = bar.get_height()
        percentage = height / total * 100
        ax5.text(
            bar.get_x() + bar.get_width()/2.,
            height + 0.1,
            f"{height} ({percentage:.1f}%)",
            ha='center',
            va='bottom',
            fontsize=12
        )
    
    ax5.set_title("Prediction Status Distribution", fontsize=16)
    ax5.set_ylabel("Count", fontsize=14)
    ax5.set_xticks(positions)
    ax5.set_xticklabels(status_counts['Status'], fontsize=12)
    
    # 6. Feature importance simulation (using correlation with absolute error)
    ax6 = fig.add_subplot(gs[2, 0:2])
    
    # Get correlations with absolute error
    feature_cols = ['volatile_acidity', 'chlorides', 'free_sulfur_dioxide', 
                    'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 
                    'alcohol', 'type_white']
    correlations = []
    
    for feature in feature_cols:
        corr = abs(df[feature].corr(df['absolute_error']))
        correlations.append((feature, corr))
    
    # Sort by correlation
    correlations.sort(key=lambda x: x[1], reverse=True)
    
    # Create feature importance bar chart
    features = [c[0] for c in correlations]
    importances = [c[1] for c in correlations]
    
    feature_bars = ax6.barh(
        features,
        importances,
        color='teal',
        alpha=0.7
    )
    
    # Add value labels
    for bar in feature_bars:
        width = bar.get_width()
        ax6.text(
            width + 0.01,
            bar.get_y() + bar.get_height()/2.,
            f"{width:.3f}",
            ha='left',
            va='center',
            fontsize=10
        )
    
    ax6.set_title("Feature Correlation with Prediction Error", fontsize=16)
    ax6.set_xlabel("Absolute Correlation", fontsize=14)
    
    # 7. Error heatmap by key features
    ax7 = fig.add_subplot(gs[2, 2])
    
    # Get the two most correlated features
    top_features = features[:2]
    
    # Create a pivot table
    if len(top_features) >= 2:
        # Bin the data
        df[f'{top_features[0]}_bin'] = pd.qcut(df[top_features[0]], 
                                               q=3, 
                                               duplicates='drop')
        df[f'{top_features[1]}_bin'] = pd.qcut(df[top_features[1]], 
                                              q=3, 
                                              duplicates='drop')
        
        # Create pivot table
        pivot = df.pivot_table(
            values='absolute_error',
            index=f'{top_features[0]}_bin',
            columns=f'{top_features[1]}_bin',
            aggfunc='mean'
        )
        
        # Create heatmap
        sns.heatmap(
            pivot,
            cmap='YlOrRd',
            annot=True,
            fmt=".2f",
            ax=ax7
        )
        
        ax7.set_title(f"Error Heatmap: {top_features[0]} vs {top_features[1]}", fontsize=16)
    else:
        ax7.text(0.5, 0.5, "Insufficient data for heatmap", 
                 ha='center', va='center', fontsize=14)
    
    # Adjust layout
    plt.tight_layout()
    plt.savefig("advanced_regression_analysis.png", dpi=300)
    print("\nAdvanced chart saved as 'advanced_regression_analysis.png'")
    
    # Show the plot if in an interactive environment
    plt.show()

def main():
    # Get predictions and simulate actual values
    df = get_batch_predictions('test_batch.csv')
    
    # Perform advanced regression analysis
    df, metrics = advanced_regression_analysis(df, error_threshold=0.5)
    
    # Generate report
    generate_advanced_report(df, metrics)
    
    # Create visualizations
    create_advanced_visualizations(df)
    
    # Save the analyzed data
    df.to_csv('analyzed_predictions.csv', index=False)
    print("Analysis results saved to 'analyzed_predictions.csv'")

if __name__ == "__main__":
    main()
