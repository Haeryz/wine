# Wine Quality Prediction API: Frontend Integration Guide

This guide is specifically designed for frontend developers using NextJS who need to integrate with the Wine Quality Prediction API.

## Overview

The Wine Quality API provides several ways to predict wine quality based on chemical properties:

- **REST API** (FastAPI and Flask endpoints)
- **GraphQL API**
- **Batch prediction** via CSV file uploads
- **Regression analysis** visualization capabilities

## Quick Start for NextJS Developers

### Installation

You'll need to install the appropriate packages for API interaction:

```bash
# For REST API
npm install axios 

# For GraphQL
npm install graphql graphql-request
```

### Base Configuration

Create a service configuration file (e.g., `services/wineApi.js`):

```javascript
// services/wineApi.js
import axios from 'axios';
import { GraphQLClient, gql } from 'graphql-request';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// REST API client
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// GraphQL client
export const graphqlClient = new GraphQLClient(`${API_BASE_URL}/graphql`);

// Wine API services
export const wineApiService = {
  // Get model information using REST
  getModelInfo: async () => {
    const response = await apiClient.get('/info');
    return response.data;
  },
  
  // Make a single prediction using REST
  predictWineQuality: async (wineData) => {
    const response = await apiClient.post('/predict', wineData);
    return response.data;
  },
  
  // Upload a CSV file for batch prediction using REST
  batchPredict: async (csvFile, downloadCsv = false) => {
    const formData = new FormData();
    formData.append('file', csvFile);
    
    const url = downloadCsv 
      ? '/batch-predict?download=true' 
      : '/batch-predict';
      
    const response = await apiClient.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      responseType: downloadCsv ? 'blob' : 'json',
    });
    
    if (downloadCsv) {
      // Return the blob for download
      return response.data;
    }
    
    return response.data;
  },
  
  // Make a single prediction using GraphQL
  predictWithGraphQL: async (wineData) => {
    const mutation = gql`
      mutation PredictWineQuality($input: WineQualityInput!) {
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
    `;
    
    return graphqlClient.request(mutation, { input: wineData });
  },
  
  // Get model info using GraphQL
  getModelInfoGraphQL: async () => {
    const query = gql`
      query {
        modelInfo {
          modelType
          featureSet
        }
      }
    `;
    
    return graphqlClient.request(query);
  }
};

export default wineApiService;
```

## Implementation Examples

### Single Wine Prediction Form

```jsx
// components/WinePredictionForm.jsx
import { useState } from 'react';
import { wineApiService } from '../services/wineApi';

export default function WinePredictionForm() {
  const [formData, setFormData] = useState({
    volatile_acidity: 0.7,
    chlorides: 0.08,
    free_sulfur_dioxide: 15,
    total_sulfur_dioxide: 110,
    density: 0.9978,
    pH: 3.2,
    sulphates: 0.6,
    alcohol: 10.5,
    type_white: 1
  });
  
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    // Convert numeric fields to numbers
    const parsedValue = ['type_white'].includes(name) 
      ? parseInt(value, 10) 
      : parseFloat(value);
      
    setFormData({
      ...formData,
      [name]: parsedValue
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      // Using REST API
      const result = await wineApiService.predictWineQuality(formData);
      setPrediction(result);
      
      // Or using GraphQL
      // const result = await wineApiService.predictWithGraphQL(formData);
      // setPrediction(result.predictQuality);
    } catch (err) {
      setError('Failed to predict wine quality. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-4">Wine Quality Prediction</h2>
      
      <form onSubmit={handleSubmit}>
        {/* Form fields - just a few examples */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">
            Volatile Acidity:
            <input
              type="number"
              name="volatile_acidity"
              step="0.01"
              value={formData.volatile_acidity}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">
            Alcohol:
            <input
              type="number"
              name="alcohol"
              step="0.1"
              value={formData.alcohol}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">
            Wine Type:
            <select
              name="type_white"
              value={formData.type_white}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded"
            >
              <option value={1}>White</option>
              <option value={0}>Red</option>
            </select>
          </label>
        </div>
        
        {/* Add other fields similarly */}
        
        <button
          type="submit"
          disabled={loading}
          className="w-full py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {loading ? 'Predicting...' : 'Predict Quality'}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {prediction && (
        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h3 className="text-lg font-semibold mb-2">Prediction Result</h3>
          <p className="text-2xl font-bold text-blue-600">
            {prediction.prediction.toFixed(2)} / 10
          </p>
          <p className="text-sm text-gray-600 mt-2">
            Model: {prediction.model_info.model_type}
          </p>
        </div>
      )}
    </div>
  );
}
```

### Batch Prediction Component

```jsx
// components/BatchPredictionUpload.jsx
import { useState } from 'react';
import { wineApiService } from '../services/wineApi';

export default function BatchPredictionUpload() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith('.csv')) {
      setFile(selectedFile);
      setError(null);
    } else {
      setFile(null);
      setError('Please select a valid CSV file');
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await wineApiService.batchPredict(file);
      setResults(result);
    } catch (err) {
      setError('Failed to process batch prediction. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleDownload = async () => {
    if (!file) return;
    
    setLoading(true);
    
    try {
      const blob = await wineApiService.batchPredict(file, true);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'wine_predictions.csv';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err) {
      setError('Failed to download prediction results');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-xl font-bold mb-4">Batch Wine Quality Prediction</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1">
            Upload CSV File:
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="mt-1 block w-full"
              required
            />
          </label>
          <p className="text-xs text-gray-500 mt-1">
            CSV must contain columns: volatile_acidity, chlorides, free_sulfur_dioxide, 
            total_sulfur_dioxide, density, pH, sulphates, alcohol, type_white
          </p>
        </div>
        
        <div className="flex space-x-2">
          <button
            type="submit"
            disabled={loading || !file}
            className="flex-1 py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Submit for Analysis'}
          </button>
          
          <button
            type="button"
            onClick={handleDownload}
            disabled={loading || !file}
            className="flex-1 py-2 px-4 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
          >
            Download Results
          </button>
        </div>
      </form>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {results && (
        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h3 className="text-lg font-semibold mb-2">Batch Results</h3>
          <p>Processed {results.row_count} rows</p>
          <p>Success rate: {(results.success_rate * 100).toFixed(2)}%</p>
          <p>Predictions: {results.predictions.length}</p>
          
          <div className="mt-3 max-h-40 overflow-y-auto">
            <h4 className="text-sm font-medium mb-1">Sample predictions:</h4>
            <ul className="list-disc list-inside text-sm">
              {results.predictions.slice(0, 5).map((pred, i) => (
                <li key={i}>Wine {i+1}: {pred.toFixed(2)} / 10</li>
              ))}
              {results.predictions.length > 5 && (
                <li>...and {results.predictions.length - 5} more</li>
              )}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
```

## CSV Template

Your CSV file for batch predictions should have the following format:

```csv
volatile_acidity,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,type_white
0.7,0.08,15,110,0.9978,3.2,0.6,10.5,1
0.5,0.05,20,80,0.9950,3.3,0.7,11.0,0
0.4,0.06,25,90,0.9940,3.1,0.8,12.0,1
```

## Using GraphQL in NextJS

For a more elegant GraphQL integration, you can use Apollo Client:

```bash
npm install @apollo/client
```

```jsx
// lib/apollo.js
import { ApolloClient, InMemoryCache, createHttpLink } from '@apollo/client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const client = new ApolloClient({
  link: createHttpLink({
    uri: `${API_BASE_URL}/graphql`,
  }),
  cache: new InMemoryCache(),
});
```

```jsx
// pages/_app.js
import { ApolloProvider } from '@apollo/client';
import { client } from '../lib/apollo';

function MyApp({ Component, pageProps }) {
  return (
    <ApolloProvider client={client}>
      <Component {...pageProps} />
    </ApolloProvider>
  );
}

export default MyApp;
```

```jsx
// components/GraphQLExample.jsx
import { gql, useMutation, useQuery } from '@apollo/client';
import { useState } from 'react';

const GET_MODEL_INFO = gql`
  query {
    modelInfo {
      modelType
      featureSet
    }
  }
`;

const PREDICT_WINE = gql`
  mutation PredictWineQuality($input: WineQualityInput!) {
    predictQuality(wineInput: $input) {
      prediction
      modelInfo {
        modelType
        featureSet
      }
    }
  }
`;

export default function GraphQLExample() {
  const { data: modelData, loading: modelLoading } = useQuery(GET_MODEL_INFO);
  const [predictWine, { data, loading, error }] = useMutation(PREDICT_WINE);
  const [wineValues, setWineValues] = useState({
    volatileAcidity: 0.7,
    chlorides: 0.08,
    freeSulfurDioxide: 15,
    totalSulfurDioxide: 110,
    density: 0.9978,
    pH: 3.2,
    sulphates: 0.6,
    alcohol: 10.5,
    typeWhite: 1
  });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    predictWine({
      variables: {
        input: wineValues
      }
    });
  };
  
  // Form handling code omitted for brevity...
  
  return (
    <div>
      {/* Display model info */}
      {modelData && (
        <div>
          <p>Model: {modelData.modelInfo.modelType}</p>
          <p>Feature Set: {modelData.modelInfo.featureSet}</p>
        </div>
      )}
      
      {/* Form elements here */}
      
      {/* Display prediction results */}
      {data && (
        <div>
          <p>Prediction: {data.predictQuality.prediction}</p>
        </div>
      )}
    </div>
  );
}
```

## API Reference

### REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/info` | GET | Get model information |
| `/predict` | POST | Make a single prediction |
| `/batch-predict` | POST | Make batch predictions from CSV |
| `/batch-predict?download=true` | POST | Download batch predictions as CSV |
| `/flask/info` | GET | Get model info (Flask alternative) |
| `/flask/predict` | POST | Make prediction (Flask alternative) |
| `/flask/batch-predict` | POST | Batch predict (Flask alternative) |

### GraphQL Schema

```graphql
type Query {
  modelInfo: ModelInfo!
}

type Mutation {
  predictQuality(wineInput: WineQualityInput!): WineQualityPrediction!
}

type WineQualityPrediction {
  prediction: Float!
  featuresUsed: WineFeatures!
  modelInfo: ModelInfo!
}

input WineQualityInput {
  volatileAcidity: Float!
  chlorides: Float!
  freeSulfurDioxide: Float!
  totalSulfurDioxide: Float!
  density: Float!
  pH: Float!
  sulphates: Float!
  alcohol: Float!
  typeWhite: Int!
}

type WineFeatures {
  volatileAcidity: Float!
  chlorides: Float!
  freeSulfurDioxide: Float!
  totalSulfurDioxide: Float!
  density: Float!
  pH: Float!
  sulphates: Float!
  alcohol: Float!
  typeWhite: Int!
  totalSulfurDioxideToFreeSulfurDioxide: Float!
}

type ModelInfo {
  modelType: String!
  featureSet: String!
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid input or missing fields
- `422 Unprocessable Entity`: Input validation failed
- `500 Internal Server Error`: Server-side error

With error responses generally in this format:
```json
{
  "error": "Error message description"
}
```

## Performance Considerations

- For single predictions, both REST and GraphQL APIs are suitable
- For batch processing of large datasets, use the batch prediction endpoint
- If you need to visualize prediction results, consider using the analyzed CSV returned by the API

## Security Notes

- The API doesn't currently implement authentication
- For production use, consider adding authentication and HTTPS

## Additional Resources

For more detailed information about the regression analysis capabilities and the machine learning model behind the API, see [REGRESSION_ANALYSIS.md](REGRESSION_ANALYSIS.md) in the project repository.
