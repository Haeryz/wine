'use client';
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
    } catch (err) {
      setError('Failed to predict wine quality. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Wine Quality Prediction</h2>
      
      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Volatile Acidity:
            <input
              type="number"
              name="volatile_acidity"
              step="0.01"
              value={formData.volatile_acidity}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Chlorides:
            <input
              type="number"
              name="chlorides"
              step="0.001"
              value={formData.chlorides}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Free Sulfur Dioxide:
            <input
              type="number"
              name="free_sulfur_dioxide"
              step="1"
              value={formData.free_sulfur_dioxide}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Total Sulfur Dioxide:
            <input
              type="number"
              name="total_sulfur_dioxide"
              step="1"
              value={formData.total_sulfur_dioxide}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Density:
            <input
              type="number"
              name="density"
              step="0.0001"
              value={formData.density}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            pH:
            <input
              type="number"
              name="pH"
              step="0.01"
              value={formData.pH}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Sulphates:
            <input
              type="number"
              name="sulphates"
              step="0.01"
              value={formData.sulphates}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Alcohol:
            <input
              type="number"
              name="alcohol"
              step="0.1"
              value={formData.alcohol}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </label>
        </div>
        
        <div className="mb-4 md:col-span-2">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Wine Type:
            <select
              name="type_white"
              value={formData.type_white}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={1}>White Wine</option>
              <option value={0}>Red Wine</option>
            </select>
          </label>
        </div>
        
        <div className="md:col-span-2">
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Predicting...' : 'Predict Wine Quality'}
          </button>
        </div>
      </form>
      
      {error && (
        <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
          {error}
        </div>
      )}
      
      {prediction && (
        <div className="mt-6 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">Prediction Result</h3>
          <div className="text-center">
            <p className="text-4xl font-bold text-blue-600 mb-2">
              {prediction.prediction.toFixed(2)} / 10
            </p>
            <p className="text-lg text-gray-600">Wine Quality Score</p>
          </div>
          <div className="mt-4 p-3 bg-white rounded border">
            <p className="text-sm text-gray-600">
              <strong>Model:</strong> {prediction.model_info?.model_type || 'Unknown'}
            </p>
            <p className="text-sm text-gray-600">
              <strong>Wine Type:</strong> {formData.type_white ? 'White Wine' : 'Red Wine'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
