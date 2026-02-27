import React, { useState, useEffect } from 'react';
import UploadZone from '../components/UploadZone';
import LogsPanel from '../components/LogsPanel';
import MetricCard from '../components/MetricCard';
import { trainModel, getModelInfo } from '../services/api';

const Train = ({ onModelTrained }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isTraining, setIsTraining] = useState(false);
  const [logs, setLogs] = useState([]);
  const [result, setResult] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [error, setError] = useState(null);
  const [testSize, setTestSize] = useState(0.2);

  useEffect(() => {
    loadModelInfo();
  }, []);

  const loadModelInfo = async () => {
    try {
      const info = await getModelInfo();
      setModelInfo(info);
    } catch (err) {
      console.error('Erro ao carregar info do modelo:', err);
    }
  };

  const addLog = (level, message) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, { timestamp, level, message }]);
  };

  const handleFileSelect = (file) => {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      setError('Por favor, selecione um arquivo CSV válido.');
      return;
    }
    setSelectedFile(file);
    setError(null);
    addLog('info', `Arquivo selecionado: ${file.name} (${(file.size / 1024).toFixed(2)} KB)`);
  };

  const handleTrain = async () => {
    if (!selectedFile) {
      setError('Por favor, selecione um arquivo CSV primeiro.');
      return;
    }

    setIsTraining(true);
    setResult(null);
    setError(null);
    setLogs([]);

    try {
      addLog('info', `Iniciando treinamento do modelo... (test_size: ${testSize * 100}%)`);
      
      const response = await trainModel(selectedFile, testSize);
      
      addLog('success', 'Treinamento concluído com sucesso!');
      addLog('info', `Versão do modelo: ${response.version}`);
      addLog('info', `Accuracy: ${(response.metrics.accuracy * 100).toFixed(2)}%`);
      addLog('info', `AUC-ROC: ${response.metrics.auc.toFixed(4)}`);
      addLog('info', `Tamanho treino: ${response.metrics.train_size}`);
      addLog('info', `Tamanho teste: ${response.metrics.test_size}`);
      
      if (response.warnings && response.warnings.length > 0) {
        response.warnings.forEach(w => addLog('warning', w));
      }

      setResult(response);
      
      // Refresh model info
      await loadModelInfo();
      
      // Notify parent
      if (onModelTrained) {
        onModelTrained(response);
      }
      
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Erro desconhecido';
      addLog('error', `Erro: ${errorMsg}`);
      setError(errorMsg);
    } finally {
      setIsTraining(false);
    }
  };

  return (
    <div className="fade-in">
      <h1 className="page-title">Treinar Modelo</h1>
      <p className="page-subtitle">Faça upload de um CSV com dados históricos para treinar o modelo</p>

      <div className="grid-2">
        {/* Upload Section */}
        <div className="card">
          <h2 className="card-title" style={{ marginBottom: '20px' }}>Upload de Dados</h2>
          
          <UploadZone 
            onFileSelect={handleFileSelect} 
            disabled={isTraining}
          />

          {/* Test Size Selector */}
          <div style={{ marginTop: '20px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '8px', 
              fontWeight: 500,
              color: 'var(--text-primary)'
            }}>
              Proporção Teste/Treino:
            </label>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <input
                type="range"
                min="0.1"
                max="0.5"
                step="0.05"
                value={testSize}
                onChange={(e) => setTestSize(parseFloat(e.target.value))}
                disabled={isTraining}
                style={{ flex: 1 }}
              />
              <span style={{ 
                minWidth: '50px', 
                textAlign: 'right',
                fontWeight: 600,
                color: 'var(--accent)'
              }}>
                {Math.round(testSize * 100)}%
              </span>
            </div>
            <p style={{ 
              fontSize: '0.75rem', 
              color: 'var(--text-secondary)',
              marginTop: '4px'
            }}>
              Com {Math.round(testSize * 100)}% para teste, ~{Math.round(80 * (1 - testSize))} amostras para treino e ~{Math.round(80 * testSize)} para teste (com 80 dados)
            </p>
          </div>
          
          {selectedFile && (
            <div style={{ marginTop: '16px', padding: '12px', background: 'var(--background)', borderRadius: '8px' }}>
              <p style={{ fontWeight: 500 }}>{selectedFile.name}</p>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
          )}

          {error && (
            <div className="alert alert-error" style={{ marginTop: '16px' }}>
              {error}
            </div>
          )}

          <button
            className="btn btn-success"
            onClick={handleTrain}
            disabled={!selectedFile || isTraining}
            style={{ width: '100%', marginTop: '20px' }}
          >
            {isTraining ? (
              <>
                <span className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }}></span>
                Treinando...
              </>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polygon points="5 3 19 12 5 21 5 3" />
                </svg>
                Iniciar Treinamento
              </>
            )}
          </button>
        </div>

        {/* Logs Section */}
        <div className="card">
          <h2 className="card-title" style={{ marginBottom: '20px' }}>Logs de Treinamento</h2>
          <LogsPanel logs={logs} />
        </div>
      </div>

      {/* Results */}
      {result && (
        <div style={{ marginTop: '24px' }}>
          <h2 className="card-title" style={{ marginBottom: '16px' }}>Resultados do Treinamento</h2>
          
          <div className="metrics-grid">
            <MetricCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                  <polyline points="22 4 12 14.01 9 11.01" />
                </svg>
              }
              iconColor="green"
              value={`${(result.metrics.accuracy * 100).toFixed(1)}%`}
              label="Accuracy"
            />
            
            <MetricCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                </svg>
              }
              iconColor="blue"
              value={result.metrics.auc.toFixed(4)}
              label="AUC-ROC"
            />
            
            <MetricCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                  <circle cx="9" cy="7" r="4" />
                </svg>
              }
              iconColor="yellow"
              value={result.metrics.train_size}
              label="Amostras Treino"
            />
            
            <MetricCard
              icon={
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                  <line x1="3" y1="9" x2="21" y2="9" />
                  <line x1="9" y1="21" x2="9" y2="9" />
                </svg>
              }
              iconColor="red"
              value={result.metrics.test_size}
              label="Amostras Teste"
            />
          </div>
        </div>
      )}

      {/* Model Info */}
      {modelInfo?.is_trained && (
        <div className="card" style={{ marginTop: '24px' }}>
          <h2 className="card-title" style={{ marginBottom: '16px' }}>Modelo Atual</h2>
          <div style={{ color: 'var(--text-secondary)' }}>
            <p><strong>Versão:</strong> {modelInfo.version}</p>
            <p><strong>Data do último treino:</strong> {modelInfo.training_date}</p>
            <p><strong>Features categóricas:</strong> {modelInfo.categorical_features?.join(', ')}</p>
            <p><strong>Features numéricas:</strong> {modelInfo.numerical_features?.join(', ')}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Train;
