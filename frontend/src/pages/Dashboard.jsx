import React, { useEffect, useState } from 'react';
import MetricCard from '../components/MetricCard';
import { getModelInfo, getMetrics } from '../services/api';

const Dashboard = () => {
  const [modelInfo, setModelInfo] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const info = await getModelInfo();
      setModelInfo(info);
      
      if (info.is_trained) {
        const metricsData = await getMetrics();
        setMetrics(metricsData);
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
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

  return (
    <div className="fade-in">
      <h1 className="page-title">Dashboard</h1>
      <p className="page-subtitle">Visão geral do sistema de previsão de atrasos</p>

      {/* Status do Modelo */}
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-header">
          <h2 className="card-title">Status do Modelo</h2>
          <div className={`status-badge ${modelInfo?.is_trained ? 'trained' : 'not-trained'}`}>
            <span className="status-dot"></span>
            {modelInfo?.is_trained ? `Treinado (v${modelInfo.version})` : 'Não Treinado'}
          </div>
        </div>

        {modelInfo?.is_trained ? (
          <div style={{ color: 'var(--text-secondary)' }}>
            <p>Modelo treinado em: {modelInfo.training_date}</p>
            <p>Features utilizadas: {modelInfo.categorical_features?.length + modelInfo.numerical_features?.length}</p>
          </div>
        ) : (
          <div className="alert alert-error">
            <p>Nenhum modelo treinado. Vá para a página "Treinar Modelo" para treinar o modelo.</p>
          </div>
        )}
      </div>

      {/* Métricas */}
      {metrics && (
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
            value={metrics.auc?.toFixed(3) || 'N/A'}
            label="AUC-ROC"
          />
          
          <MetricCard
            icon={
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                <line x1="3" y1="9" x2="21" y2="9" />
                <line x1="9" y1="21" x2="9" y2="9" />
              </svg>
            }
            iconColor="yellow"
            value={metrics.test_size || 0}
            label="Tamanho do Teste"
          />
          
          <MetricCard
            icon={
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            }
            iconColor="blue"
            value={metrics.train_size || 0}
            label="Tamanho do Treino"
          />
        </div>
      )}

      {/* Informações Adicionais */}
      <div className="grid-2">
        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '16px' }}>Sobre o Sistema</h3>
          <div style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
            <p>Este sistema utiliza Machine Learning (RandomForest) para prever a probabilidade de atraso em entregas de fretes.</p>
            <br />
            <p><strong>Features utilizadas:</strong></p>
            <ul style={{ marginLeft: '20px', marginTop: '8px' }}>
              <li>ID da Rota</li>
              <li>Hora de Partida</li>
              <li>Nível de Tráfego</li>
              <li>Previsão de Chuva</li>
              <li>Peso da Carga</li>
              <li>Tipo de Veículo</li>
              <li>Tempo Médio Histórico</li>
              <li>Taxa Histórica de Atraso</li>
            </ul>
          </div>
        </div>

        <div className="card">
          <h3 className="card-title" style={{ marginBottom: '16px' }}>Como Usar</h3>
          <div style={{ color: 'var(--text-secondary)', lineHeight: 1.8 }}>
            <p><strong>1. Treinar Modelo:</strong> Faça upload de um arquivo CSV com dados históricos de fretes.</p>
            <br />
            <p><strong>2. Verificar Métricas:</strong> Após o treino, visualize a accuracy e AUC do modelo.</p>
            <br />
            <p><strong>3. Prever Atraso:</strong> Insira os dados de um novo frete para obter a probabilidade de atraso.</p>
            <br />
            <p><strong>4. Re-treinar:</strong> Adicione novos dados periodicamente para melhorar o modelo.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
