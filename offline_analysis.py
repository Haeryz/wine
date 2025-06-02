
    
    # Generate predictions based on features to simulate a real model
    # This is a simplistic model for demonstration
    df['prediction'] = (
        5.0 +  # Base quality
        -0.5 * df['volatile_acidity'] +  # Higher acidity reduces quality
        -0.2 * df['chlorides'] +  # Higher chlorides reduces quality
        0.01 * df['free_sulfur_dioxide'] +  # Slight positive effect
        -0.005 * df['total_sulfur_dioxide'] +  # Slight negative effect
        -2.0 * (df['density'] - 0.995) +  # Density matters
        -0.1 * (df['pH'] - 3.2) +  # pH effect around optimal
        0.3 * df['sulphates'] +  # Sulphates improve quality
        0.2 * df['alcohol'] +  # Higher alcohol improves quality
        0.2 * df['type_white']  # White wines slightly higher rated
    )
    
    # Add some random noise to make it more realistic
    df['prediction'] = df['prediction'] + np.random.normal(0, 0.1, size=len(df))
    df['prediction'] = df['prediction'].clip(3, 8)  # Keep within typical range
    df['prediction'] = df['prediction'].round(4)
    
    # Add simulated "actual" values for advanced analysis
    df['actual_quality'] = df['prediction'] + np.random.normal(0, 0.5, len(df))
    df['actual_quality'] = df['actual_quality'].clip(3, 8)
    df['actual_quality'] = df['actual_quality'].round(2)
    
    return df

def analyze_regression_predictions(df, threshold=0.5):
    """Analyze regression predictions with simulated ground truth"""
    # Calculate error metrics
    df['absolute_error'] = abs(df['actual_quality'] - df['prediction'])
    df['squared_error'] = (df['actual_quality'] - df['prediction'])**2
    
    # Determine if prediction is "correct" based on threshold
    df['prediction_status'] = df['absolute_error'] <= threshold
    df['status'] = df['prediction_status'].map({True: 'Correct', False: 'Incorrect'})
    
    # Calculate metrics
    mean_abs_error = df['absolute_error'].mean()
    mean_squared_error = df['squared_error'].mean()
    root_mean_squared_error = np.sqrt(mean_squared_error)
    accuracy = df['prediction_status'].mean() * 100
    
    return df, {
        'accuracy': accuracy,
        'mae': mean_abs_error,
        'mse': mean_squared_error,
        'rmse': root_mean_squared_error,
        'threshold': threshold
    }

def generate_report(df, metrics):
    """Generate a comprehensive report"""
    print("\n=== Wine Quality Prediction Analysis ===")
    print(f"Total samples: {len(df)}")
    print(f"Error threshold for 'correctness': {metrics['threshold']}")
    print(f"Correct predictions: {df['prediction_status'].sum()} ({metrics['accuracy']:.2f}%)")
    print(f"Incorrect predictions: {len(df) - df['prediction_status'].sum()} ({100 - metrics['accuracy']:.2f}%)")
    
    print("\nRegression Metrics:")
    print(f"Mean Absolute Error (MAE): {metrics['mae']:.4f}")
    print(f"Mean Squared Error (MSE): {metrics['mse']:.4f}")
    print(f"Root Mean Squared Error (RMSE): {metrics['rmse']:.4f}")
    
    print("\nSample statistics:")
    print(f"Mean actual quality: {df['actual_quality'].mean():.4f}")
    print(f"Mean predicted quality: {df['prediction'].mean():.4f}")
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

def create_visualizations(df):
    """Create comprehensive visualizations"""
    # Set style
    sns.set(style="whitegrid")
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(18, 12))
    
    # Define grid layout
    gs = fig.add_gridspec(2, 3)
    
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
    threshold = df.loc[~df['prediction_status'], 'absolute_error'].min() if len(df.loc[~df['prediction_status']]) > 0 else 0.5
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
    
    # 2. Error by wine type
    ax2 = fig.add_subplot(gs[0, 2])
    wine_types = {0: "Red", 1: "White"}
    df['wine_type'] = df['type_white'].map(wine_types)
    
    box_plot = sns.boxplot(
        x="wine_type",
        y="absolute_error",
        data=df,
        palette=["#8B0000", "#F8F8FF"],
        ax=ax2
    )
    ax2.set_title("Error by Wine Type", fontsize=16)
    ax2.set_xlabel("Wine Type", fontsize=14)
    ax2.set_ylabel("Absolute Error", fontsize=14)
    
    # 3. Prediction status counts with gap
    ax3 = fig.add_subplot(gs[1, 0])
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    # Create positions with gap
    positions = [0, 1.5]
    colors_list = [colors[status] for status in status_counts['Status']]
    
    bars = ax3.bar(
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
        ax3.text(
            bar.get_x() + bar.get_width()/2.,
            height + 0.1,
            f"{height} ({percentage:.1f}%)",
            ha='center',
            va='bottom',
            fontsize=12
        )
    
    ax3.set_title("Prediction Status Distribution", fontsize=16)
    ax3.set_ylabel("Count", fontsize=14)
    ax3.set_xticks(positions)
    ax3.set_xticklabels(status_counts['Status'], fontsize=12)
    
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
    
    # 5. Feature correlation with error
    ax5 = fig.add_subplot(gs[1, 2])
    
    # Calculate correlations with absolute error
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
    
    feature_bars = ax5.barh(
        features,
        importances,
        color='teal',
        alpha=0.7
    )
    
    # Add value labels
    for bar in feature_bars:
        width = bar.get_width()
        ax5.text(
            width + 0.01,
            bar.get_y() + bar.get_height()/2.,
            f"{width:.3f}",
            ha='left',
            va='center',
            fontsize=10
        )
    
    ax5.set_title("Feature Correlation with Prediction Error", fontsize=16)
    ax5.set_xlabel("Absolute Correlation", fontsize=14)
    
    # Adjust layout
    plt.tight_layout()
    plt.savefig("offline_wine_analysis.png", dpi=300)
    print("\nChart saved as 'offline_wine_analysis.png'")
    
    # Show the plot if in an interactive environment
    plt.show()

def main():
    # Check if the CSV file exists
    csv_file_path = 'test_batch.csv'
    if not os.path.exists(csv_file_path):
        print(f"Error: {csv_file_path} not found. Please create a CSV file with wine data.")
        return
    
    # Generate mock predictions (simulate model)
    df = generate_mock_predictions(csv_file_path)
    
    # Analyze the predictions
    df, metrics = analyze_regression_predictions(df, threshold=0.5)
    
    # Generate report
    generate_report(df, metrics)
    
    # Create visualizations
    create_visualizations(df)
    
    # Save the analyzed data
    df.to_csv('offline_analyzed_predictions.csv', index=False)
    print("Analysis results saved to 'offline_analyzed_predictions.csv'")

if __name__ == "__main__":
    main()
