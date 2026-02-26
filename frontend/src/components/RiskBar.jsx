import React from 'react';

const RiskBar = ({ probability }) => {
  const percentage = Math.round(probability * 100);
  
  const getRiskLevel = () => {
    if (percentage < 30) return { level: 'baixo', color: '#10B981', label: 'BAIXO RISCO' };
    if (percentage < 70) return { level: 'medio', color: '#F59E0B', label: 'MÉDIO RISCO' };
    return { level: 'alto', color: '#EF4444', label: 'ALTO RISCO' };
  };
  
  const risk = getRiskLevel();
  
  return (
    <div className="risk-bar-container">
      <div className="risk-bar-label">
        <span>0%</span>
        <span>Probabilidade de Atraso</span>
        <span>100%</span>
      </div>
      
      <div className="risk-bar">
        <div 
          className="risk-indicator"
          style={{ left: `${percentage}%` }}
        >
          {percentage}%
        </div>
      </div>
      
      <div className={`risk-level ${risk.level}`}>
        {risk.label}
      </div>
    </div>
  );
};

export default RiskBar;
