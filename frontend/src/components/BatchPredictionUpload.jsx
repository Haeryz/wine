'use client';
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
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Batch Wine Quality Prediction</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Upload CSV File:
            <input
              type="file"
              accept=".csv"
              onChange={handleFileChange}
              className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              required
            />
          </label>
          <div className="mt-2 p-3 bg-gray-50 rounded-md">
            <p className="text-xs text-gray-600 mb-2">
              <strong>Required CSV columns:</strong>
            </p>
            <p className="text-xs text-gray-500">
              volatile_acidity, chlorides, free_sulfur_dioxide, total_sulfur_dioxide, 
              density, pH, sulphates, alcohol, type_white
            </p>
          </div>
        </div>
        
        <div className="flex space-x-3">
          <button
            type="submit"
            disabled={loading || !file}
            className="flex-1 py-3 px-4 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Processing...' : 'Submit for Analysis'}
          </button>
          
          <button
            type="button"
            onClick={handleDownload}
            disabled={loading || !file}
            className="flex-1 py-3 px-4 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Download Results
          </button>
        </div>
      </form>
      
      {error && (
        <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-md">
          {error}
        </div>
      )}
      
      {results && (
        <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200">
          <h3 className="text-xl font-semibold mb-4 text-gray-800">Batch Results</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-white p-4 rounded border text-center">
              <p className="text-2xl font-bold text-blue-600">{results.row_count}</p>
              <p className="text-sm text-gray-600">Rows Processed</p>
            </div>
            <div className="bg-white p-4 rounded border text-center">
              <p className="text-2xl font-bold text-green-600">
                {(results.success_rate * 100).toFixed(1)}%
              </p>
              <p className="text-sm text-gray-600">Success Rate</p>
            </div>
            <div className="bg-white p-4 rounded border text-center">
              <p className="text-2xl font-bold text-purple-600">{results.predictions.length}</p>
              <p className="text-sm text-gray-600">Predictions</p>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded border">
            <h4 className="text-lg font-medium mb-3 text-gray-800">Sample Predictions:</h4>
            <div className="max-h-40 overflow-y-auto">
              <ul className="space-y-1">
                {results.predictions.slice(0, 10).map((pred, i) => (
                  <li key={i} className="flex justify-between items-center text-sm">
                    <span className="text-gray-600">Wine {i + 1}:</span>
                    <span className="font-medium text-blue-600">{pred.toFixed(2)} / 10</span>
                  </li>
                ))}
                {results.predictions.length > 10 && (
                  <li className="text-xs text-gray-500 text-center pt-2">
                    ...and {results.predictions.length - 10} more predictions
                  </li>
                )}
              </ul>
            </div>
          </div>
        </div>
      )}
      
      {/* Sample CSV Format */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg border">
        <h4 className="text-lg font-medium mb-2 text-gray-800">Sample CSV Format:</h4>
        <pre className="text-xs bg-white p-3 rounded border overflow-x-auto">
{`volatile_acidity,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,type_white
0.7,0.08,15,110,0.9978,3.2,0.6,10.5,1
0.5,0.05,20,80,0.9950,3.3,0.7,11.0,0
0.4,0.06,25,90,0.9940,3.1,0.8,12.0,1`}
        </pre>
      </div>
    </div>
  );
}
