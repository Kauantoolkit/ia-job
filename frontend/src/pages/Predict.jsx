import React, { useState, useEffect } from 'react';
import PredictionForm from '../components/PredictionForm';
import RiskBar from '../components/RiskBar';
import { predict, getModelInfo } from '../services/api';

const Predict = ({ modelStatus }) => {
  const [isModelTrained, setIsModelTrained] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    checkModelStatus();
  }, [modelStatus]);

  const checkModelStatus = async () => {
    try {
      const info = await getModelInfo();
      setIsModelTrained(info.is_trained);
    } catch (err) {
      setIsModelTrained(false);
    }
  };

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await predict(formData);
      setPrediction(result);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Erro desconhecido';
      setError(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const getRiskColor = () => {
    if (!prediction) return 'var(--text-secondary)';
    switch (prediction.risk_color) {
      case 'green': return 'var(--accent)';
      case 'yellow': return 'var(--warning)';
      case 'red': return 'var(--danger)';
      default: return 'var(--text-secondary)';
    }
  };

  return (
    <div className="fade-in">
      <h1 className="page-title">Prever Atraso</h1>
      <p className="page-subtitle">Insira os dados do frete para calcular a probabilidade de atraso</p>

      <div className="grid-2">
        {/* Form Section */}
        <div className="card">
          <h2 className="card-title" style={{ marginBottom: '20px' }}>Dados do Frete</h2>
          
          <PredictionForm 
            onSubmit={handleSubmit}
            isLoading={isLoading}
            isModelTrained={isModelTrained}
          />
          
          {error && (
            <div className="alert alert-error" style={{ marginTop: '16px' }}>
              {error}
            </div>
          )}
        </div>

        {/* Result Section */}
        <div className="card">
          <h2 className="card-title" style={{ marginBottom: '20px' }}>Resultado da Predição</h2>
          
          {prediction ? (
            <div className="prediction-result">
              <div 
                className="prediction-probability"
                style={{ color: getRiskColor() }}
              >
                {prediction.probability_percent}%
              </div>
              <div className="prediction-label">
                probabilidade de atraso
              </div>
              
              <RiskBar probability={prediction.probability} />
              
              <div style={{ marginTop: '24px', padding: '16px', background: 'var(--background)', borderRadius: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Previsao:</span>
                  <span style={{ 
                    fontWeight: 600, 
                    color: prediction.prediction === 'atrasado' ? 'var(--danger)' : 'var(--accent)'
                  }}>
                    {prediction.prediction === 'atrasado' ? 'ATRASADO' : 'EM TEMPO'}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span style={{ color: 'var(--text-secondary)' }}>Nivel de Risco:</span>
                  <span style={{ 
                    fontWeight: 600, 
                    color: prediction.risk_color === 'green' ? 'var(--accent)' : 
                           prediction.risk_color === 'yellow' ? 'var(--warning)' : 'var(--danger)'
                  }}>
                    {prediction.risk_level.toUpperCase()}
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <div style={{ 
              textAlign: 'center', 
              padding: '48px', 
              color: 'var(--text-secondary)' 
            }}>
              <svg 
                width="64" 
                height="64" 
                viewBox="0 0 24 24" 
                fill="none" 
                stroke="currentColor" 
                strokeWidth="1.5"
                style={{ margin: '0 auto 16px', opacity: 0.5 }}
              >
                <circle cx="12" cy="12" r="10" />
                <polyline points="12 6 12 12 16 14" />
              </svg>
              <p>Preencha os dados do frete e clique em "Calcular" para ver o resultado</p>
            </div>
          )}
        </div>
      </div>

      {/* Legenda */}
      <div className="card" style={{ marginTop: '24px' }}>
        <h2 className="card-title" style={{ marginBottom: '16px' }}>Legenda de Risco</h2>
        <div style={{ display: 'flex', gap: '24px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: 16, height: 16, borderRadius: '4px', background: 'var(--accent)' }}></div>
            <span style={{ color: 'var(--text-secondary)' }}>0-30%: Baixo Risco</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: 16, height: 16, borderRadius: '4px', background: 'var(--warning)' }}></div>
            <span style={{ color: 'var(--text-secondary)' }}>31-70%: Medio Risco</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ width: 16, height: 16, borderRadius: '4px', background: 'var(--danger)' }}></div>
            <span style={{ color: 'var(--text-secondary)' }}>71-100%: Alto Risco</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Predict;
