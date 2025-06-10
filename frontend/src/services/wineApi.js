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
