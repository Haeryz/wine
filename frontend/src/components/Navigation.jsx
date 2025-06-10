'use client';
import { useState } from 'react';

export default function Navigation({ activeTab, setActiveTab }) {  const tabs = [
    { id: 'single', name: 'Single Prediction', icon: '🍷' },
    { id: 'batch', name: 'Batch', icon: '📊' },
    // { id: 'about', name: 'About', icon: 'ℹ️' }
  ];

  return (
    <nav className="bg-white shadow-lg border-b">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-3">
            <h1 className="text-2xl font-bold text-gray-800">🍷 Wine Quality Predictor</h1>
          </div>
          
          <div className="flex space-x-1">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
