import React from 'react';

const MetricCard = ({ icon, iconColor, value, label }) => {
  return (
    <div className="metric-card">
      <div className={`metric-icon ${iconColor}`}>
        {icon}
      </div>
      <div className="metric-value">{value}</div>
      <div className="metric-label">{label}</div>
    </div>
  );
};

export default MetricCard;
