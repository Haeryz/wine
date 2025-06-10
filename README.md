# Wine Quality Prediction API

This project provides a multi-interface API for predicting wine quality using a machine learning model. The API is available through three different interfaces: REST API with FastAPI, REST API with Flask, and GraphQL. It also includes frontend interfaces in Next.js and Streamlit.

## Features

- **Multiple API Interfaces**: Choose between FastAPI, Flask, or GraphQL
- **Wine Quality Prediction**: Get predictions for wine quality based on chemical properties
- **Batch Prediction**: Upload CSV files with multiple wine samples for batch processing
- **Model Information**: Get information about the model used for predictions
- **Regression Analysis**: Comprehensive analysis of prediction results with visual reports
- **Frontend Integration**: 
  - Next.js frontend (see [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md))
  - Streamlit dashboard for data visualization and prediction

## Requirements

- Python 3.9+
- Virtual environment (named 'virtual')
- Dependencies listed in requirements.txt

## Installation

1. Ensure you have Python 3.9+ installed
2. Clone this repository
3. Create and activate a virtual environment:

```powershell
# Create virtual environment
python -m venv virtual

# Activate virtual environment
.\virtual\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Running the API

```powershell
# Activate virtual environment (if not already activated)
.\virtual\Scripts\Activate.ps1

# Start the API server
python main.py
```

The server will start and listen on http://127.0.0.1:8000 by default.

## Running the Streamlit Dashboard

```powershell
# Activate virtual environment (if not already activated)
.\virtual\Scripts\Activate.ps1

# Install Streamlit requirements
pip install -r streamlit_requirements.txt

# Run the Streamlit dashboard
streamlit run streamlit_dashboard.py
```

Or simply run the provided PowerShell script:

```powershell
.\run_streamlit.ps1
```

The Streamlit dashboard will be available at http://localhost:8501 by default.

## API Documentation

### REST API (FastAPI)

#### Get Model Information

```
GET /info
```

Response:
```json
{
  "model_type": "RandomForest",
  "feature_set": "SFS_Forward_10",
  "features": [
    "volatile acidity",
    "chlorides",
    "free sulfur dioxide",
    "total sulfur dioxide",
    "density",
    "pH",
    "sulphates",
    "alcohol",
    "total_sulfur_dioxide_to_free_sulfur_dioxide",
    "type_white"
  ],
  "api_type": "FastAPI"
}
```

#### Predict Wine Quality

```
POST /predict
```

Request body:
```json
{
  "volatile_acidity": 0.7,
  "chlorides": 0.08,
  "free_sulfur_dioxide": 15,
  "total_sulfur_dioxide": 110,
  "density": 0.9978,
  "pH": 3.2,
  "sulphates": 0.6,
  "alcohol": 10.5,
  "type_white": 1
}
```

Response:
```json
{
  "prediction": 5.4125,
  "features_used": {
    "volatile acidity": 0.7,
    "chlorides": 0.08,
    "free sulfur dioxide": 15.0,
    "total sulfur dioxide": 110.0,
    "density": 0.9978,
    "pH": 3.2,
    "sulphates": 0.6,
    "alcohol": 10.5,
    "type_white": 1.0,
    "total_sulfur_dioxide_to_free_sulfur_dioxide": 7.333333333333333
  },
  "model_info": {
    "model_type": "RandomForest",
    "feature_set": "SFS_Forward_10"
  }
}
```

#### Batch Predict Wine Quality

Use this endpoint to upload a CSV file with multiple wine samples for batch prediction.

```
POST /batch-predict
```

Request:
- Form data with a CSV file containing columns: `volatile_acidity`, `chlorides`, `free_sulfur_dioxide`, `total_sulfur_dioxide`, `density`, `pH`, `sulphates`, `alcohol`, `type_white`
- Query parameter `download=true` (optional) to receive results as CSV file

Example CSV file format:
```
volatile_acidity,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,type_white
0.7,0.08,15,110,0.9978,3.2,0.6,10.5,1
0.5,0.05,20,80,0.9950,3.3,0.7,11.0,0
0.4,0.06,25,90,0.9940,3.1,0.8,12.0,1
```

JSON Response:
```json
{
  "predictions": [5.4125, 5.7628, 6.1234],
  "row_count": 3,
  "success_rate": 1.0,
  "model_info": {
    "model_type": "RandomForest",
    "feature_set": "SFS_Forward_10"
  }
}
```

With `download=true`, you'll receive a CSV file with an additional `prediction` column:
```
volatile_acidity,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,type_white,prediction
0.7,0.08,15,110,0.9978,3.2,0.6,10.5,1,5.4125
0.5,0.05,20,80,0.9950,3.3,0.7,11.0,0,5.7628
0.4,0.06,25,90,0.9940,3.1,0.8,12.0,1,6.1234
```
```

### REST API (Flask)

The Flask API mirrors the FastAPI routes but is accessible through the `/flask` prefix.

#### Get Model Information

```
GET /flask/info
```

#### Predict Wine Quality

```
POST /flask/predict
```

#### Batch Predict Wine Quality

```
POST /flask/batch-predict
```

The request format and response are the same as the FastAPI batch prediction endpoint.

### GraphQL API

GraphQL endpoint: `/graphql`

#### Get Model Information

```graphql
query {
  modelInfo {
    modelType
    featureSet
  }
}
```

#### Predict Wine Quality

```graphql
mutation PredictQuality($input: WineQualityInput!) {
  predictQuality(wineInput: $input) {
    prediction
    featuresUsed {
      volatileAcidity
      chlorides
      freeSulfurDioxide
      totalSulfurDioxide
      density
      pH
      sulphates
      alcohol
      typeWhite
      totalSulfurDioxideToFreeSulfurDioxide
    }
    modelInfo {
      modelType
      featureSet
    }
  }
}
```

Variables:
```json
{
  "input": {
    "volatileAcidity": 0.7,
    "chlorides": 0.08,
    "freeSulfurDioxide": 15,
    "totalSulfurDioxide": 110,
    "density": 0.9978,
    "pH": 3.2,
    "sulphates": 0.6,
    "alcohol": 10.5,
    "typeWhite": 1
  }
}
```

## Feature Descriptions

- **volatile_acidity**: Volatile acidity of the wine
- **chlorides**: Chlorides content in the wine
- **free_sulfur_dioxide**: Free sulfur dioxide in the wine
- **total_sulfur_dioxide**: Total sulfur dioxide in the wine
- **density**: Density of the wine
- **pH**: pH of the wine
- **sulphates**: Sulphates content in the wine
- **alcohol**: Alcohol content of the wine
- **type_white**: Binary indicator if wine is white (1) or red (0)
- **total_sulfur_dioxide_to_free_sulfur_dioxide**: Derived feature (calculated automatically)

## Testing the API

You can use the included `test_api.py` script to test all three interfaces:

```powershell
# Activate virtual environment (if not already activated)
.\virtual\Scripts\Activate.ps1

# Run the tests
python test_api.py
```

## Regression Analysis

The project includes specialized tools for analyzing the regression predictions:

```powershell
# Run basic regression analysis with visualizations
python batch_analysis.py

# Run advanced analysis with simulated actual values
python advanced_analysis.py

# Or run both with the convenience script
.\run_analysis.ps1
```

This will generate detailed reports and visualizations:
- Accuracy-like metrics for regression predictions
- Identification of "incorrect" predictions based on thresholds
- Visual charts showing the distribution of prediction errors
- Feature correlation with prediction accuracy

For more information, see [REGRESSION_ANALYSIS.md](REGRESSION_ANALYSIS.md)

## Development

### Project Structure

- `main.py`: Main API application with FastAPI, Flask, and GraphQL implementations
- `wine.pkl`: Serialized machine learning model for wine quality prediction
- `requirements.txt`: Project dependencies
- `test_api.py`: Script to test all API interfaces
- `FRONTEND_INTEGRATION.md`: Comprehensive guide for NextJS frontend developers
- `batch_analysis.py` & `advanced_analysis.py`: Regression analysis tools with visualizations

### Model Information

- Model Type: RandomForest
- Feature Set: SFS_Forward_10
- Features: 10 (9 inputs + 1 derived)

### Dependencies

All required dependencies are listed in the requirements.txt file, including:

- flask
- fastapi
- uvicorn
- strawberry-graphql
- joblib
- scikit-learn
- numpy
- pandas
- pydantic
- requests (for testing)

## Frontend Integration

For frontend developers using NextJS, please refer to our detailed integration guide: [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)

This guide includes:

- API service setup in NextJS
- Example components for single predictions and batch processing
- GraphQL setup with Apollo Client
- Complete code examples with error handling
- Performance recommendations
