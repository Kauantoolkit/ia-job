import React, { useEffect, useState } from 'react';
import MetricCard from '../components/MetricCard';
import { getMetrics, getFeatureImportance, getModelInfo } from '../services/api';

const Metrics = () => {
  const [metrics, setMetrics] = useState(null);
  const [featureImportance, setFeatureImportance] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      const info = await getModelInfo();
      setModelInfo(info);
      
      if (info.is_trained) {
        const metricsData = await getMetrics();
        setMetrics(metricsData);
        
        const importanceData = await getFeatureImportance();
        setFeatureImportance(importanceData.features || []);
      }
    } catch (err) {
      setError(err.message || 'Erro ao carregar métricas');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!modelInfo?.is_trained) {
    return (
      <div className="fade-in">
        <h1 className="page-title">Métricas do Modelo</h1>
        <p className="page-subtitle">Visualize as métricas de desempenho do modelo</p>
        
        <div className="alert alert-error">
          <p>Nenhum modelo treinado ainda. Vá para a página "Treinar Modelo" para treinar o modelo.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fade-in">
      <h1 className="page-title">Métricas do Modelo</h1>
      <p className="page-subtitle">Visualize as métricas de desempenho do modelo</p>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {/* Métricas Principais */}
      <div className="metrics-grid">
        <MetricCard
          icon={
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          }
          iconColor="green"
          value={`${(metrics.accuracy * 100).toFixed(1)}%`}
          label="Accuracy"
        />
        
        <MetricCard
          icon={
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
            </svg>
          }
          iconColor="blue"
          value={metrics.auc?.toFixed(4) || 'N/A'}
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
          value={metrics.train_size || 0}
          label="Tamanho Treino"
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
          value={metrics.test_size || 0}
          label="Tamanho Teste"
        />
      </div>

      {/* Matriz de Confusão */}
      {metrics.confusion_matrix && (
        <div className="card" style={{ marginBottom: '24px' }}>
          <h2 className="card-title" style={{ marginBottom: '20px' }}>Matriz de Confusão</h2>
          
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '4px', maxWidth: '300px' }}>
              {metrics.confusion_matrix.map((row, i) => 
                row.map((value, j) => (
                  <div 
                    key={`${i}-${j}`}
                    style={{
                      padding: '20px',
                      background: i === j ? 'var(--accent)' : 'var(--surface-light)',
                      borderRadius: '8px',
                      textAlign: 'center',
                      fontWeight: 700,
                      fontSize: '1.5rem'
                    }}
                  >
                    <div style={{ fontSize: '0.75rem', opacity: 0.7, marginBottom: '4px' }}>
                      {i === 0 && j === 0 ? 'TN' : i === 0 && j === 1 ? 'FP' : i === 1 && j === 0 ? 'FN' : 'TP'}
                    </div>
                    {value}
                  </div>
                ))
              )}
            </div>
          </div>
          
          <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', marginTop: '16px', color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            <span>TN: True Negative</span>
            <span>FP: False Positive</span>
            <span>FN: False Negative</span>
            <span>TP: True Positive</span>
          </div>
        </div>
      )}

      {/* Feature Importance */}
      <div className="card">
        <h2 className="card-title" style={{ marginBottom: '20px' }}>Importância das Features</h2>
        
        {featureImportance.length > 0 ? (
          <div className="feature-list">
            {featureImportance.map((item, index) => (
              <div key={index} className="feature-item">
                <span className="feature-name">{item.feature}</span>
                <div className="feature-bar">
                  <div 
                    className="feature-bar-fill" 
                    style={{ width: `${item.importance * 100}%` }}
                  />
                </div>
                <span className="feature-value">{(item.importance * 100).toFixed(2)}%</span>
              </div>
            ))}
          </div>
        ) : (
          <p style={{ color: 'var(--text-secondary)' }}>Nenhum dado de importância disponível.</p>
        )}
      </div>

      {/* Informações do Modelo */}
      <div className="card" style={{ marginTop: '24px' }}>
        <h2 className="card-title" style={{ marginBottom: '16px' }}>Informações do Modelo</h2>
        <div style={{ color: 'var(--text-secondary)', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
          <div>
            <p><strong>Versão</strong></p>
            <p>{modelInfo.version}</p>
          </div>
          <div>
            <p><strong>Data do Treino</strong></p>
            <p>{modelInfo.training_date}</p>
          </div>
          <div>
            <p><strong>Features Categóricas</strong></p>
            <p>{modelInfo.categorical_features?.join(', ')}</p>
          </div>
          <div>
            <p><strong>Features Numéricas</strong></p>
            <p>{modelInfo.numerical_features?.join(', ')}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Metrics;
