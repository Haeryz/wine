import requests
import json
import io
import csv
import os
import pandas as pd

# Base URL
base_url = "http://127.0.0.1:8000"

# Test data
test_data = {
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

def test_fastapi():
    print("\n=== Testing FastAPI ===")
    
    # Test info endpoint
    print("Testing /info endpoint...")
    response = requests.get(f"{base_url}/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test predict endpoint
    print("\nTesting /predict endpoint...")
    response = requests.post(f"{base_url}/predict", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_flask():
    print("\n=== Testing Flask ===")
    
    # Test info endpoint
    print("Testing /flask/info endpoint...")
    response = requests.get(f"{base_url}/flask/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test predict endpoint
    print("\nTesting /flask/predict endpoint...")
    response = requests.post(f"{base_url}/flask/predict", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_graphql():
    print("\n=== Testing GraphQL ===")
    
    # Test model_info query
    print("Testing model_info query...")
    query = """
    query {
      modelInfo {
        modelType
        featureSet
      }
    }
    """
    response = requests.post(f"{base_url}/graphql", json={"query": query})
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test predict_quality mutation
    print("\nTesting predict_quality mutation...")
    mutation = """
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
    """
    variables = {
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
    response = requests.post(
        f"{base_url}/graphql",
        json={"query": mutation, "variables": variables}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# Function to create a test CSV file
def create_test_csv():
    # Create a sample DataFrame with multiple wine entries
    data = [
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
        },
        {
            "volatile_acidity": 0.5,
            "chlorides": 0.05,
            "free_sulfur_dioxide": 20,
            "total_sulfur_dioxide": 80,
            "density": 0.9950,
            "pH": 3.3,
            "sulphates": 0.7,
            "alcohol": 11.0,
            "type_white": 0
        },
        {
            "volatile_acidity": 0.4,
            "chlorides": 0.06,
            "free_sulfur_dioxide": 25,
            "total_sulfur_dioxide": 90,
            "density": 0.9940,
            "pH": 3.1,
            "sulphates": 0.8,
            "alcohol": 12.0,
            "type_white": 1
        }
    ]
    
    df = pd.DataFrame(data)
    
    # Save to a CSV file
    filename = "test_wines.csv"
    df.to_csv(filename, index=False)
    
    print(f"Created test CSV file: {filename}")
    return filename

def test_batch_fastapi():
    print("\n=== Testing FastAPI Batch Prediction ===")
    
    # Create test CSV file
    csv_file = create_test_csv()
    
    try:
        # Test batch prediction endpoint
        with open(csv_file, 'rb') as f:
            files = {'file': (csv_file, f, 'text/csv')}
            print("Testing /batch-predict endpoint...")
            response = requests.post(f"{base_url}/batch-predict", files=files)
            
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test batch prediction with download
        with open(csv_file, 'rb') as f:
            files = {'file': (csv_file, f, 'text/csv')}
            print("\nTesting /batch-predict with download=true...")
            response = requests.post(f"{base_url}/batch-predict", files=files, params={'download': 'true'})
            
        print(f"Status: {response.status_code}")
        content_type = response.headers.get('Content-Type', '')
        print(f"Content-Type: {content_type}")
        
        if 'csv' in content_type:
            print("Successfully received CSV file response")
            
            # Save the CSV file
            with open("result_wines_fastapi.csv", "wb") as f:
                f.write(response.content)
                
            print("Saved result to: result_wines_fastapi.csv")
            
    finally:
        # Cleanup
        if os.path.exists(csv_file):
            os.remove(csv_file)

def test_batch_flask():
    print("\n=== Testing Flask Batch Prediction ===")
    
    # Create test CSV file
    csv_file = create_test_csv()
    
    try:
        # Test batch prediction endpoint
        with open(csv_file, 'rb') as f:
            files = {'file': (csv_file, f, 'text/csv')}
            print("Testing /flask/batch-predict endpoint...")
            response = requests.post(f"{base_url}/flask/batch-predict", files=files)
            
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Test batch prediction with download
        with open(csv_file, 'rb') as f:
            files = {'file': (csv_file, f, 'text/csv')}
            print("\nTesting /flask/batch-predict with download=true...")
            response = requests.post(f"{base_url}/flask/batch-predict", files=files, params={'download': 'true'})
            
        print(f"Status: {response.status_code}")
        content_type = response.headers.get('Content-Type', '')
        print(f"Content-Type: {content_type}")
        
        if 'csv' in content_type:
            print("Successfully received CSV file response")
            
            # Save the CSV file
            with open("result_wines_flask.csv", "wb") as f:
                f.write(response.content)
                
            print("Saved result to: result_wines_flask.csv")
            
    finally:
        # Cleanup
        if os.path.exists(csv_file):
            os.remove(csv_file)

if __name__ == "__main__":
    test_fastapi()
    test_flask()
    test_graphql()
    test_batch_fastapi()
    test_batch_flask()
