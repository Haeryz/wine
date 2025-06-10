import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import joblib
from io import StringIO
import json
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Set page config
st.set_page_config(
    page_title="Wine Quality Dashboard",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define API endpoints
API_BASE_URL = "http://localhost:8000"
FASTAPI_PREDICT_URL = f"{API_BASE_URL}/predict"
FASTAPI_BATCH_URL = f"{API_BASE_URL}/batch-predict"
FASTAPI_INFO_URL = f"{API_BASE_URL}/info"
GRAPHQL_URL = f"{API_BASE_URL}/graphql"

# Custom styles
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2563EB;
        margin-bottom: 0.5rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: white;
        box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
        margin-bottom: 1rem;
    }
    .prediction-result {
        background: linear-gradient(to right, #DBEAFE, #EDE9FE);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #BFDBFE;
        margin-top: 1.5rem;
    }
    .prediction-score {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2563EB;
        text-align: center;
    }
    .info-box {
        padding: 0.75rem;
        background-color: white;
        border-radius: 0.25rem;
        border: 1px solid #E5E7EB;
    }
    .batch-result {
        background: linear-gradient(to right, #ECFDF5, #DBEAFE);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #A7F3D0;
        margin-top: 1.5rem;
    }
    .metric-box {
        background-color: white;
        padding: 1rem;
        border-radius: 0.25rem;
        border: 1px solid #E5E7EB;
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.875rem;
        color: #4B5563;
    }
    .sample-csv {
        background-color: #F9FAFB;
        padding: 1rem;
        border-radius: 0.25rem;
        border: 1px solid #E5E7EB;
        margin-top: 1.5rem;
    }
    .code-sample {
        font-family: monospace;
        font-size: 0.75rem;
        background-color: white;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #E5E7EB;
        overflow-x: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Functions to interact with the API
def get_model_info():
    try:
        response = requests.get(FASTAPI_INFO_URL)
        return response.json()
    except Exception as e:
        st.error(f"Failed to get model info: {str(e)}")
        return None

def predict_wine_quality(wine_data):
    try:
        response = requests.post(FASTAPI_PREDICT_URL, json=wine_data)
        return response.json()
    except Exception as e:
        st.error(f"Failed to predict wine quality: {str(e)}")
        return None

def batch_predict(csv_file, download=False):
    try:
        files = {'file': csv_file}
        response = requests.post(
            f"{FASTAPI_BATCH_URL}{'?download=true' if download else ''}",
            files=files
        )
        if download:
            return response.content
        return response.json()
    except Exception as e:
        st.error(f"Failed to process batch prediction: {str(e)}")
        return None

def get_download_link(df, filename="wine_predictions.csv", text="Download CSV"):
    """Generate a link to download the dataframe as a CSV file"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Navigation
def render_sidebar():
    st.sidebar.markdown('<div class="main-header">🍷 Wine Quality</div>', unsafe_allow_html=True)
    
    # Get model info
    model_info = get_model_info()
    if model_info:
        st.sidebar.markdown("### Model Information")
        st.sidebar.markdown(f"**Model Type:** {model_info.get('model_type', 'Unknown')}")
        st.sidebar.markdown(f"**Feature Set:** {model_info.get('feature_set', 'Unknown')}")
        st.sidebar.markdown(f"**API Type:** {model_info.get('api_type', 'FastAPI')}")
    
    # Navigation
    pages = {
        "Single Prediction": single_prediction_page,
        "Batch Prediction": batch_prediction_page,
        "Visualization Dashboard": visualization_dashboard_page,
        "About": about_page,
    }
    
    st.sidebar.markdown("### Navigation")
    page = st.sidebar.radio("", list(pages.keys()))
    
    # Render the selected page
    pages[page]()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Sample Data")
    with st.sidebar.expander("View Sample Input Data"):
        st.code("""
volatile_acidity,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,type_white
0.7,0.08,15,110,0.9978,3.2,0.6,10.5,1
0.5,0.05,20,80,0.9950,3.3,0.7,11.0,0
0.4,0.06,25,90,0.9940,3.1,0.8,12.0,1
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Developed with Streamlit")
    st.sidebar.info("This dashboard complements the existing NextJS frontend.")

# Single Prediction Page
def single_prediction_page():
    st.markdown('<div class="main-header">Wine Quality Prediction</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Create a form for wine data input
        with st.form("wine_prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                volatile_acidity = st.number_input(
                    "Volatile Acidity", 
                    min_value=0.0, 
                    max_value=2.0, 
                    value=0.7, 
                    step=0.01,
                    format="%.2f"
                )
                
                chlorides = st.number_input(
                    "Chlorides", 
                    min_value=0.0, 
                    max_value=1.0, 
                    value=0.08, 
                    step=0.001,
                    format="%.3f"
                )
                
                free_sulfur_dioxide = st.number_input(
                    "Free Sulfur Dioxide", 
                    min_value=0, 
                    max_value=300, 
                    value=15, 
                    step=1
                )
                
                total_sulfur_dioxide = st.number_input(
                    "Total Sulfur Dioxide", 
                    min_value=0, 
                    max_value=500, 
                    value=110, 
                    step=1
                )
            
            with col2:
                density = st.number_input(
                    "Density", 
                    min_value=0.9, 
                    max_value=1.1, 
                    value=0.9978, 
                    step=0.0001,
                    format="%.4f"
                )
                
                ph = st.number_input(
                    "pH", 
                    min_value=2.0, 
                    max_value=5.0, 
                    value=3.2, 
                    step=0.01,
                    format="%.2f"
                )
                
                sulphates = st.number_input(
                    "Sulphates", 
                    min_value=0.0, 
                    max_value=2.0, 
                    value=0.6, 
                    step=0.01,
                    format="%.2f"
                )
                
                alcohol = st.number_input(
                    "Alcohol", 
                    min_value=8.0, 
                    max_value=15.0, 
                    value=10.5, 
                    step=0.1,
                    format="%.1f"
                )
            
            col_type = st.selectbox(
                "Wine Type",
                options=["White Wine", "Red Wine"],
                index=0
            )
            
            type_white = 1 if col_type == "White Wine" else 0
            
            # Form submit button
            submitted = st.form_submit_button("Predict Wine Quality", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process the form submission
        if submitted:
            # Prepare input data
            wine_data = {
                "volatile_acidity": volatile_acidity,
                "chlorides": chlorides,
                "free_sulfur_dioxide": free_sulfur_dioxide,
                "total_sulfur_dioxide": total_sulfur_dioxide,
                "density": density,
                "pH": ph,
                "sulphates": sulphates,
                "alcohol": alcohol,
                "type_white": type_white
            }
            
            # Show loading spinner
            with st.spinner("Predicting wine quality..."):
                # Call API to get prediction
                prediction = predict_wine_quality(wine_data)
            
            # Display prediction result
            if prediction:
                st.markdown('<div class="prediction-result">', unsafe_allow_html=True)
                st.markdown('<h3 class="sub-header" style="text-align:center;">Prediction Result</h3>', unsafe_allow_html=True)
                
                st.markdown(f'<div class="prediction-score">{prediction["prediction"]:.2f} / 10</div>', unsafe_allow_html=True)
                st.markdown('<p style="text-align:center;color:#4B5563;font-size:1.2rem;">Wine Quality Score</p>', unsafe_allow_html=True)
                
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.markdown(f"**Model:** {prediction['model_info']['model_type']}")
                st.markdown(f"**Wine Type:** {'White Wine' if type_white == 1 else 'Red Wine'}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Visualize the importance of features
                st.markdown('<h4 style="margin-top:1rem;">Feature Values:</h4>', unsafe_allow_html=True)
                
                # Create a horizontal bar chart of the features
                features_df = pd.DataFrame({
                    'Feature': list(prediction['features_used'].keys()),
                    'Value': list(prediction['features_used'].values())
                })
                
                fig = px.bar(
                    features_df, 
                    x='Value', 
                    y='Feature',
                    orientation='h',
                    title="Input Features",
                    color='Value',
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# Batch Prediction Page
def batch_prediction_page():
    st.markdown('<div class="main-header">Batch Wine Quality Prediction</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
        
        # Display required CSV format
        st.markdown('<div class="sample-csv">', unsafe_allow_html=True)
        st.markdown('#### Required CSV columns:')
        st.markdown('volatile_acidity, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol, type_white')
        
        st.markdown('#### Sample CSV Format:')
        st.markdown('<div class="code-sample">', unsafe_allow_html=True)
        st.code("""
volatile_acidity,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,type_white
0.7,0.08,15,110,0.9978,3.2,0.6,10.5,1
0.5,0.05,20,80,0.9950,3.3,0.7,11.0,0
0.4,0.06,25,90,0.9940,3.1,0.8,12.0,1
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.button("Submit for Analysis", disabled=uploaded_file is None, use_container_width=True)
        
        with col2:
            download_button = st.button("Download Results", disabled=uploaded_file is None, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process the file submission
        if uploaded_file is not None and (submit_button or download_button):
            # Process the uploaded file
            with st.spinner("Processing batch prediction..." if submit_button else "Generating download..."):
                if download_button:
                    # Get predictions with download=True
                    csv_content = batch_predict(uploaded_file, download=True)
                    
                    if csv_content:
                        # Create a download link for the CSV
                        st.download_button(
                            label="Download Predictions CSV",
                            data=csv_content,
                            file_name="wine_predictions.csv",
                            mime="text/csv",
                        )
                else:
                    # Process for display
                    results = batch_predict(uploaded_file)
                    
                    if results:
                        # Display results
                        st.markdown('<div class="batch-result">', unsafe_allow_html=True)
                        st.markdown('<h3 class="sub-header" style="text-align:center;">Batch Results</h3>', unsafe_allow_html=True)
                        
                        # Create metrics
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            st.markdown(f'<div class="metric-value">{results["row_count"]}</div>', unsafe_allow_html=True)
                            st.markdown('<div class="metric-label">Rows Processed</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            st.markdown(f'<div class="metric-value">{results["success_rate"]*100:.1f}%</div>', unsafe_allow_html=True)
                            st.markdown('<div class="metric-label">Success Rate</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            st.markdown(f'<div class="metric-value">{len(results["predictions"])}</div>', unsafe_allow_html=True)
                            st.markdown('<div class="metric-label">Predictions</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display sample predictions
                        st.markdown('<div style="background-color:white;padding:1rem;border-radius:0.25rem;border:1px solid #E5E7EB;margin-top:1rem;">', unsafe_allow_html=True)
                        st.markdown('#### Sample Predictions:')
                        
                        # Convert predictions to DataFrame for display
                        sample_count = min(10, len(results["predictions"]))
                        if sample_count > 0:
                            sample_df = pd.DataFrame({
                                'Wine': [f"Wine {i+1}" for i in range(sample_count)],
                                'Prediction': [round(pred, 2) for pred in results["predictions"][:sample_count]]
                            })
                            
                            # Display as a table
                            st.dataframe(
                                sample_df,
                                column_config={
                                    "Wine": st.column_config.TextColumn("Wine"),
                                    "Prediction": st.column_config.NumberColumn("Quality Score", format="%.2f / 10")
                                },
                                hide_index=True,
                                use_container_width=True
                            )
                            
                            if len(results["predictions"]) > 10:
                                st.markdown(f"*...and {len(results['predictions']) - 10} more predictions*")
                        else:
                            st.info("No predictions available")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Add visualization of prediction distribution
                        if len(results["predictions"]) > 0:
                            st.markdown('#### Prediction Distribution:')
                            
                            fig = px.histogram(
                                x=results["predictions"],
                                nbins=20,
                                labels={"x": "Wine Quality Score"},
                                title="Distribution of Predicted Wine Quality",
                                color_discrete_sequence=['#6366F1']
                            )
                            
                            fig.update_layout(
                                xaxis_title="Wine Quality Score",
                                yaxis_title="Count",
                                bargap=0.1
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)

# Visualization Dashboard Page
def visualization_dashboard_page():
    st.markdown('<div class="main-header">Wine Quality Visualization Dashboard</div>', unsafe_allow_html=True)
    
    # Check if we have a file already
    if 'visualization_data' not in st.session_state:
        st.session_state.visualization_data = None
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # File upload section
        uploaded_file = st.file_uploader("Upload CSV file for analysis", type=["csv"])
        
        if uploaded_file:
            analyze_button = st.button("Analyze Data", use_container_width=True)
            
            if analyze_button:
                with st.spinner("Analyzing data..."):
                    # Get batch predictions and store for visualization
                    results = batch_predict(uploaded_file)
                    
                    if results:
                        # Read the uploaded file into a DataFrame
                        df = pd.read_csv(uploaded_file)
                        
                        if len(results["predictions"]) == len(df):
                            # Add predictions to the dataframe
                            df['prediction'] = results["predictions"]
                            
                            # Store the data for visualization
                            st.session_state.visualization_data = df
                            
                            st.success("Data analyzed successfully! Scroll down to view visualizations.")
                        else:
                            st.error("Error: Prediction count doesn't match data rows.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display visualizations if data is available
    if st.session_state.visualization_data is not None:
        df = st.session_state.visualization_data
        
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["Quality Distribution", "Feature Relationships", "Feature Importance"])
        
        with tab1:
            st.markdown('<div class="sub-header">Quality Score Distribution</div>', unsafe_allow_html=True)
            
            # Quality distribution histogram
            fig_hist = px.histogram(
                df, 
                x="prediction", 
                color_discrete_sequence=['#6366F1'],
                title="Distribution of Wine Quality Scores",
                nbins=20
            )
            
            fig_hist.update_layout(
                xaxis_title="Quality Score",
                yaxis_title="Count"
            )
            
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Wine type distribution
            col1, col2 = st.columns(2)
            
            with col1:
                # Count by wine type
                wine_counts = df['type_white'].value_counts().reset_index()
                wine_counts.columns = ['Type', 'Count']
                wine_counts['Type'] = wine_counts['Type'].map({1: 'White Wine', 0: 'Red Wine'})
                
                fig_pie = px.pie(
                    wine_counts, 
                    values='Count', 
                    names='Type',
                    title="Wine Type Distribution",
                    color_discrete_sequence=['#EF4444', '#FBBF24']
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Quality by wine type
                fig_box = px.box(
                    df, 
                    x=df['type_white'].map({1: 'White Wine', 0: 'Red Wine'}), 
                    y='prediction',
                    title="Quality Score by Wine Type",
                    color=df['type_white'].map({1: 'White Wine', 0: 'Red Wine'}),
                    color_discrete_sequence=['#FBBF24', '#EF4444']
                )
                
                fig_box.update_layout(
                    xaxis_title="Wine Type",
                    yaxis_title="Quality Score"
                )
                
                st.plotly_chart(fig_box, use_container_width=True)
        
        with tab2:
            st.markdown('<div class="sub-header">Feature Relationships</div>', unsafe_allow_html=True)
            
            # Feature selection for scatter plot
            col1, col2 = st.columns(2)
            
            with col1:
                x_feature = st.selectbox(
                    "X-axis Feature",
                    options=[col for col in df.columns if col not in ['prediction', 'type_white']],
                    index=0
                )
            
            with col2:
                y_feature = st.selectbox(
                    "Y-axis Feature",
                    options=[col for col in df.columns if col not in ['prediction', 'type_white']],
                    index=1
                )
            
            # Create scatter plot
            fig_scatter = px.scatter(
                df, 
                x=x_feature, 
                y=y_feature,
                color='prediction',
                color_continuous_scale='viridis',
                title=f"Relationship between {x_feature} and {y_feature}",
                hover_data=['prediction'],
                size_max=10
            )
            
            fig_scatter.update_layout(
                xaxis_title=x_feature,
                yaxis_title=y_feature,
                coloraxis_colorbar_title="Quality Score"
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Correlation heatmap
            st.markdown('<h3>Feature Correlation</h3>', unsafe_allow_html=True)
            
            # Calculate correlation matrix
            corr_matrix = df.corr()
            
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                title="Feature Correlation Heatmap"
            )
            
            fig_heatmap.update_layout(
                height=600,
                width=800,
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with tab3:
            st.markdown('<div class="sub-header">Feature Importance Analysis</div>', unsafe_allow_html=True)
            
            # Simulate feature importance with correlation to prediction
            feature_importance = pd.DataFrame({
                'Feature': [col for col in df.columns if col != 'prediction'],
                'Importance': [abs(df[col].corr(df['prediction'])) for col in df.columns if col != 'prediction']
            }).sort_values('Importance', ascending=False)
            
            # Create horizontal bar chart
            fig_imp = px.bar(
                feature_importance, 
                y='Feature', 
                x='Importance',
                orientation='h',
                color='Importance',
                color_continuous_scale='viridis',
                title="Feature Correlation with Wine Quality"
            )
            
            fig_imp.update_layout(
                xaxis_title="Absolute Correlation",
                yaxis_title="Feature",
                height=500
            )
            
            st.plotly_chart(fig_imp, use_container_width=True)
            
            # Feature pair plots (selected features)
            st.markdown('<h3>Feature Pair Relationships</h3>', unsafe_allow_html=True)
            
            # Get top 4 features by importance
            top_features = feature_importance['Feature'].head(4).tolist()
            top_features.append('prediction')
            
            # Create a subset dataframe with top features
            df_subset = df[top_features]
            
            # Create pair plot
            fig = px.scatter_matrix(
                df_subset,
                dimensions=top_features[:-1],
                color=df['type_white'].map({1: 'White Wine', 0: 'Red Wine'}),
                title="Pair Plot of Top Features",
                color_discrete_sequence=['#EF4444', '#3B82F6']
            )
            
            fig.update_layout(height=800)
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Upload a CSV file and click 'Analyze Data' to view visualizations")

# About Page
def about_page():
    st.markdown('<div class="main-header">About Wine Quality Prediction</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown("""
        ## Wine Quality Prediction Dashboard

        This Streamlit dashboard allows you to predict wine quality using a machine learning model. 
        You can submit individual wine samples or batch process multiple samples through a CSV file.

        ### Features:
        - **Individual Wine Prediction**: Submit detailed information about a single wine sample
        - **Batch Prediction**: Upload CSV files with multiple wine samples
        - **Visualization Dashboard**: Analyze prediction results with interactive visualizations
        - **API Integration**: Connects with FastAPI, Flask and GraphQL endpoints

        ### Model Information:
        The wine quality prediction model was trained on a dataset of red and white wine samples.
        It uses features such as acidity, alcohol content, and chemical properties to predict
        a quality score on a scale of 0-10.
        
        ### Technical Stack:
        - **Backend**: FastAPI, Flask, GraphQL
        - **Dashboard**: Streamlit
        - **Frontend**: Next.js
        - **Visualization**: Plotly, Matplotlib
        - **Machine Learning**: Scikit-learn
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main function
def main():
    render_sidebar()

if __name__ == "__main__":
    main()
