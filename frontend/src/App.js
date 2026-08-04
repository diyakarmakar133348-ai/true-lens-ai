import React, { useState } from 'react';
import UploadArea from './components/UploadArea';
import ResultsDashboard from './components/ResultsDashboard';
import api from './api';
import './styles/globals.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    setReport(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/api/scan', formData);
      setReport(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-navy py-10 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-extrabold text-white tracking-tight">
            <span className="text-cyan">True</span> Lens <span className="text-cyan">AI</span>
          </h1>
          <p className="text-gray-400 mt-2 text-lg">
            Forensic Media Authenticator – Scan images, videos, and audio for manipulation.
          </p>
        </div>

        {/* Upload Section */}
        <UploadArea onUpload={handleUpload} isLoading={loading} />

        {/* Loading State */}
        {loading && (
          <div className="text-center mt-8">
            <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-cyan border-r-transparent"></div>
            <p className="text-gray-400 mt-2 text-sm">Scanning file with AI forensic models...</p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="max-w-2xl mx-auto mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-300 text-center">
            {error}
          </div>
        )}

        {/* Results */}
        {report && <ResultsDashboard report={report} />}

        {/* Footer */}
        <div className="text-center text-gray-600 text-xs mt-16 border-t border-gray-800 pt-6">
          <p>🔐 Files are encrypted in transit and auto-deleted within 24 hours.</p>
          <p className="mt-1">True Lens AI v1.0 – Built for truth.</p>
        </div>
      </div>
    </div>
  );
}

export default App;