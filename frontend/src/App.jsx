import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Train from './pages/Train';
import Metrics from './pages/Metrics';
import Predict from './pages/Predict';
import { getModelInfo } from './services/api';

function App() {
  const [modelStatus, setModelStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadModelStatus();
  }, []);

  const loadModelStatus = async () => {
    try {
      const info = await getModelInfo();
      setModelStatus({
        is_trained: info.is_trained || false,
        version: info.version || '0.0.0',
        training_date: info.training_date
      });
    } catch (error) {
      console.error('Erro ao carregar status do modelo:', error);
      setModelStatus({ is_trained: false, version: '0.0.0' });
    } finally {
      setLoading(false);
    }
  };

  const handleModelTrained = (result) => {
    setModelStatus({
      is_trained: true,
      version: result.version,
      training_date: result.training_date
    });
  };

  if (loading) {
    return (
      <div className="app" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="app">
        <Navbar modelStatus={modelStatus} />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/train" element={<Train onModelTrained={handleModelTrained} />} />
            <Route path="/metrics" element={<Metrics />} />
            <Route path="/predict" element={<Predict modelStatus={modelStatus} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
