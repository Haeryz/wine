export default function About() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold mb-6 text-gray-800">About Wine Quality Predictor</h2>
        
        <div className="prose prose-lg text-gray-600">
          <p className="mb-6">
            This application uses machine learning to predict wine quality based on various chemical properties. 
            Our model analyzes key wine characteristics to provide accurate quality predictions on a scale of 1-10.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-blue-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-4 text-blue-800">Features Analyzed</h3>
              <ul className="space-y-2 text-sm">
                <li>• <strong>Volatile Acidity:</strong> Affects wine taste</li>
                <li>• <strong>Chlorides:</strong> Salt content in wine</li>
                <li>• <strong>Free Sulfur Dioxide:</strong> Antimicrobial agent</li>
                <li>• <strong>Total Sulfur Dioxide:</strong> Preservative levels</li>
                <li>• <strong>Density:</strong> Related to alcohol and sugar content</li>
                <li>• <strong>pH:</strong> Acidity/alkalinity measure</li>
                <li>• <strong>Sulphates:</strong> Wine additive</li>
                <li>• <strong>Alcohol:</strong> Alcohol percentage</li>
                <li>• <strong>Wine Type:</strong> Red or White wine</li>
              </ul>
            </div>
            
            <div className="bg-green-50 p-6 rounded-lg">
              <h3 className="text-xl font-semibold mb-4 text-green-800">API Capabilities</h3>
              <ul className="space-y-2 text-sm">
                <li>• <strong>REST API:</strong> Standard HTTP endpoints</li>
                <li>• <strong>GraphQL API:</strong> Flexible query interface</li>
                <li>• <strong>Single Predictions:</strong> Individual wine analysis</li>
                <li>• <strong>Batch Processing:</strong> CSV file uploads</li>
                <li>• <strong>Real-time Results:</strong> Instant predictions</li>
                <li>• <strong>Download Results:</strong> Export predictions</li>
              </ul>
            </div>
          </div>
          
          <div className="bg-gray-50 p-6 rounded-lg mb-6">
            <h3 className="text-xl font-semibold mb-4 text-gray-800">How to Use</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Single Prediction</h4>
                <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1">
                  <li>Enter wine chemical properties</li>
                  <li>Select wine type (Red/White)</li>
                  <li>Click "Predict Wine Quality"</li>
                  <li>View your quality score</li>
                </ol>
              </div>
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Batch Prediction</h4>
                <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1">
                  <li>Prepare CSV with required columns</li>
                  <li>Upload your CSV file</li>
                  <li>Submit for analysis</li>
                  <li>Download results or view summary</li>
                </ol>
              </div>
            </div>
          </div>
          
          <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
            <h3 className="text-lg font-semibold mb-2 text-yellow-800">⚠️ Note</h3>
            <p className="text-sm text-yellow-700">
              This tool is for educational and research purposes. Wine quality is subjective and can vary 
              based on personal preferences, storage conditions, and other factors not captured in the model.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
