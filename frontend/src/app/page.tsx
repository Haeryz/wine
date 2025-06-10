'use client';
import { useState } from 'react';
import Navigation from '../components/Navigation';
import WinePredictionForm from '../components/WinePredictionForm';
import BatchPredictionUpload from '../components/BatchPredictionUpload';
import About from '../components/About';

export default function Home() {
  const [activeTab, setActiveTab] = useState('single');

  const renderContent = () => {
    switch (activeTab) {
      case 'single':
        return <WinePredictionForm />;
      case 'batch':
        return <BatchPredictionUpload />;
      case 'about':
        return <About />;
      default:
        return <WinePredictionForm />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="container mx-auto px-4 py-8">
        {renderContent()}
      </main>
    </div>
  );
}
