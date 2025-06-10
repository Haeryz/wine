import os
import joblib
import io
import csv
import pandas as pd
from flask import Flask, request, jsonify, send_file
from fastapi import FastAPI, Depends, UploadFile, File, Response
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import uvicorn
import numpy as np
import strawberry
from strawberry.fastapi import GraphQLRouter
import graphql

# Load the wine model
model_path = os.path.join(os.path.dirname(__file__), "wine.pkl")
model_data = joblib.load(model_path)
model = model_data['model']
feature_names = model_data['feature_names']
model_type = model_data.get('model_type', 'Unknown')
feature_set_name = model_data.get('feature_set_name', 'Unknown')

# Create Flask application
flask_app = Flask(__name__)

# Create FastAPI application
fastapi_app = FastAPI(
    title="Wine Quality Prediction API",
    description="API for predicting wine quality using a machine learning model",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for input validation
class WineInput(BaseModel):
    volatile_acidity: float = Field(..., description="Volatile acidity of the wine")
    chlorides: float = Field(..., description="Chlorides content in the wine")
    free_sulfur_dioxide: float = Field(..., description="Free sulfur dioxide in the wine")
    total_sulfur_dioxide: float = Field(..., description="Total sulfur dioxide in the wine")
    density: float = Field(..., description="Density of the wine")
    pH: float = Field(..., description="pH of the wine")
    sulphates: float = Field(..., description="Sulphates content in the wine")
    alcohol: float = Field(..., description="Alcohol content of the wine")
    type_white: int = Field(..., description="Binary indicator if wine is white (1) or red (0)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }

# Pydantic model for response
class WinePrediction(BaseModel):
    prediction: float
    features_used: Dict[str, float]
    model_info: Dict[str, str]

# Pydantic model for batch prediction response
class BatchPredictionResponse(BaseModel):
    predictions: List[float]
    row_count: int
    model_info: Dict[str, str]
    success_rate: float

# Function to preprocess input and make predictions
def predict_wine_quality(wine_data: WineInput):
    # Convert input to feature array suitable for the model
    input_features = {
        'volatile acidity': wine_data.volatile_acidity,
        'chlorides': wine_data.chlorides,
        'free sulfur dioxide': wine_data.free_sulfur_dioxide,
        'total sulfur dioxide': wine_data.total_sulfur_dioxide,
        'density': wine_data.density,
        'pH': wine_data.pH,
        'sulphates': wine_data.sulphates,
        'alcohol': wine_data.alcohol,
        'type_white': wine_data.type_white
    }
    
    # Calculate the derived feature
    input_features['total_sulfur_dioxide_to_free_sulfur_dioxide'] = (
        input_features['total sulfur dioxide'] / input_features['free sulfur dioxide']
        if input_features['free sulfur dioxide'] > 0 else 0
    )
    
    # Ensure features are in the correct order
    X = [input_features[feature_name] for feature_name in feature_names]
    X = np.array(X).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(X)[0]
    
    return {
        "prediction": float(prediction),
        "features_used": input_features,
        "model_info": {
            "model_type": model_type,
            "feature_set": feature_set_name
        }
    }

# Function to process CSV data for batch predictions
def process_batch_csv(file_content):
    # Read CSV file into pandas DataFrame
    df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
    
    # Expected columns (excluding the derived feature which we'll calculate)
    expected_columns = [
        'volatile_acidity', 'chlorides', 'free_sulfur_dioxide', 
        'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 
        'alcohol', 'type_white'
    ]
    
    # Check if all required columns are present
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}")
    
    # Process each row
    predictions = []
    successful_rows = 0
    
    for _, row in df.iterrows():
        try:
            # Create WineInput object from DataFrame row
            wine_input = WineInput(
                volatile_acidity=float(row.get('volatile_acidity')),
                chlorides=float(row.get('chlorides')),
                free_sulfur_dioxide=float(row.get('free_sulfur_dioxide')),
                total_sulfur_dioxide=float(row.get('total_sulfur_dioxide')),
                density=float(row.get('density')),
                pH=float(row.get('pH')),
                sulphates=float(row.get('sulphates')),
                alcohol=float(row.get('alcohol')),
                type_white=int(row.get('type_white'))
            )
            
            # Make prediction
            result = predict_wine_quality(wine_input)
            predictions.append(result["prediction"])
            successful_rows += 1
        except Exception as e:
            # Append None for failed predictions
            predictions.append(None)
    
    # Create result DataFrame with predictions
    df['prediction'] = predictions
    
    # Calculate success rate
    success_rate = successful_rows / len(df) if len(df) > 0 else 0
    
    return {
        "predictions": [p for p in predictions if p is not None],
        "row_count": len(df),
        "success_rate": success_rate,
        "model_info": {
            "model_type": model_type,
            "feature_set": feature_set_name
        }
    }, df

# Flask routes
@flask_app.route('/predict', methods=['POST'])
def flask_predict():
    data = request.json
    wine_input = WineInput(**data)
    result = predict_wine_quality(wine_input)
    return jsonify(result)

@flask_app.route('/batch-predict', methods=['POST'])
def flask_batch_predict():
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if file is CSV
    if not file.filename.endswith('.csv'):
        return jsonify({"error": "File must be CSV format"}), 400
    
    try:
        # Process the CSV file
        file_content = file.read()
        result, df_with_predictions = process_batch_csv(file_content)
        
        # Check if download parameter is set
        download_csv = request.args.get('download', '').lower() in ['true', '1', 't', 'y', 'yes']
        
        if download_csv:
            # Return CSV file with predictions
            output = io.StringIO()
            df_with_predictions.to_csv(output, index=False)
            mem = io.BytesIO()
            mem.write(output.getvalue().encode('utf-8'))
            mem.seek(0)
            return send_file(
                mem,
                mimetype='text/csv',
                as_attachment=True,
                download_name='wine_predictions.csv'
            )
        else:
            # Return JSON response
            return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@flask_app.route('/info', methods=['GET'])
def flask_info():
    return jsonify({
        "model_type": model_type,
        "feature_set": feature_set_name,
        "features": feature_names,
        "api_type": "Flask"
    })

# FastAPI routes
@fastapi_app.post("/predict", response_model=WinePrediction)
async def fastapi_predict(wine_data: WineInput):
    return predict_wine_quality(wine_data)

@fastapi_app.post("/batch-predict", response_model=BatchPredictionResponse)
async def fastapi_batch_predict(
    file: UploadFile = File(...),
    download: bool = False
):
    # Check if file is CSV
    if not file.filename.endswith('.csv'):
        raise ValueError("File must be CSV format")
    
    # Read file content
    file_content = await file.read()
    
    # Process the CSV file
    result, df_with_predictions = process_batch_csv(file_content)
    
    if download:
        # Return CSV file with predictions
        output = io.StringIO()
        df_with_predictions.to_csv(output, index=False)
        
        return StreamingResponse(
            io.StringIO(output.getvalue()),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=wine_predictions.csv"}
        )
    else:
        # Return JSON response
        return result

@fastapi_app.get("/info")
async def fastapi_info():
    return {
        "model_type": model_type,
        "feature_set": feature_set_name,
        "features": feature_names,
        "api_type": "FastAPI"
    }

# GraphQL schema using Strawberry
@strawberry.type
class WineFeatures:
    volatile_acidity: float = strawberry.field(description="Volatile acidity of the wine")
    chlorides: float = strawberry.field(description="Chlorides content in the wine")
    free_sulfur_dioxide: float = strawberry.field(description="Free sulfur dioxide in the wine")
    total_sulfur_dioxide: float = strawberry.field(description="Total sulfur dioxide in the wine")
    density: float = strawberry.field(description="Density of the wine")
    pH: float = strawberry.field(description="pH of the wine")
    sulphates: float = strawberry.field(description="Sulphates content in the wine")
    alcohol: float = strawberry.field(description="Alcohol content of the wine")
    type_white: int = strawberry.field(description="Binary indicator if wine is white (1) or red (0)")
    total_sulfur_dioxide_to_free_sulfur_dioxide: float = strawberry.field(description="Ratio of total to free sulfur dioxide")

@strawberry.type
class ModelInfo:
    model_type: str = strawberry.field(description="Type of model used for prediction")
    feature_set: str = strawberry.field(description="Name of the feature set used in the model")

@strawberry.type
class WineQualityPrediction:
    prediction: float = strawberry.field(description="Predicted quality of the wine")
    features_used: WineFeatures = strawberry.field(description="Features used for prediction")
    model_info: ModelInfo = strawberry.field(description="Information about the model")

@strawberry.input
class WineQualityInput:
    volatile_acidity: float = strawberry.field(description="Volatile acidity of the wine")
    chlorides: float = strawberry.field(description="Chlorides content in the wine")
    free_sulfur_dioxide: float = strawberry.field(description="Free sulfur dioxide in the wine")
    total_sulfur_dioxide: float = strawberry.field(description="Total sulfur dioxide in the wine")
    density: float = strawberry.field(description="Density of the wine")
    pH: float = strawberry.field(description="pH of the wine")
    sulphates: float = strawberry.field(description="Sulphates content in the wine")
    alcohol: float = strawberry.field(description="Alcohol content of the wine")
    type_white: int = strawberry.field(description="Binary indicator if wine is white (1) or red (0)")

@strawberry.type
class Query:
    @strawberry.field(description="Get information about the wine quality model")
    def model_info(self) -> ModelInfo:
        return ModelInfo(
            model_type=model_type,
            feature_set=feature_set_name
        )

@strawberry.type
class Mutation:
    @strawberry.field(description="Predict wine quality based on input features")
    def predict_quality(self, wine_input: WineQualityInput) -> WineQualityPrediction:
        # Create WineInput object from GraphQL arguments
        wine_data = WineInput(
            volatile_acidity=wine_input.volatile_acidity,
            chlorides=wine_input.chlorides,
            free_sulfur_dioxide=wine_input.free_sulfur_dioxide,
            total_sulfur_dioxide=wine_input.total_sulfur_dioxide,
            density=wine_input.density,
            pH=wine_input.pH,
            sulphates=wine_input.sulphates,
            alcohol=wine_input.alcohol,
            type_white=wine_input.type_white
        )
        
        # Make prediction
        result = predict_wine_quality(wine_data)
        
        # Transform prediction result to GraphQL structure
        features = WineFeatures(
            volatile_acidity=result["features_used"]["volatile acidity"],
            chlorides=result["features_used"]["chlorides"],
            free_sulfur_dioxide=result["features_used"]["free sulfur dioxide"],
            total_sulfur_dioxide=result["features_used"]["total sulfur dioxide"],
            density=result["features_used"]["density"],
            pH=result["features_used"]["pH"],
            sulphates=result["features_used"]["sulphates"],
            alcohol=result["features_used"]["alcohol"],
            type_white=result["features_used"]["type_white"],
            total_sulfur_dioxide_to_free_sulfur_dioxide=result["features_used"]["total_sulfur_dioxide_to_free_sulfur_dioxide"]
        )
        
        model_info = ModelInfo(
            model_type=result["model_info"]["model_type"],
            feature_set=result["model_info"]["feature_set"]
        )
        
        return WineQualityPrediction(
            prediction=result["prediction"],
            features_used=features,
            model_info=model_info
        )

# Create GraphQL schema
graphql_schema = strawberry.Schema(query=Query, mutation=Mutation)

# Add GraphQL endpoint to FastAPI
graphql_router = GraphQLRouter(graphql_schema)
fastapi_app.include_router(graphql_router, prefix="/graphql")

# Mount Flask app under FastAPI
fastapi_app.mount("/flask", WSGIMiddleware(flask_app))

# Create a requirements.txt file with dependencies
def create_requirements_file():
    requirements = [
        "flask>=3.1.0",
        "fastapi>=0.115.0",
        "uvicorn>=0.34.0",
        "strawberry-graphql>=0.270.5",
        "joblib>=1.5.0",
        "scikit-learn>=1.6.0",
        "numpy>=2.2.0",
        "pandas>=2.2.0",
        "pydantic>=2.11.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))

if __name__ == "__main__":
    # Create requirements file if it doesn't exist or is empty
    if not os.path.exists("requirements.txt") or os.path.getsize("requirements.txt") == 0:
        create_requirements_file()
    
    # Run FastAPI application
    print("Starting Wine Quality Prediction API...")
    print("FastAPI running on http://127.0.0.1:8000")
    print("Flask apps mounted at http://127.0.0.1:8000/flask")
    print("GraphQL endpoint available at http://127.0.0.1:8000/graphql")
    print("Model type:", model_type)
    print("Feature set:", feature_set_name)
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8000)