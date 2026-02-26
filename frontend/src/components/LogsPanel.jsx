import React from 'react';

const LogsPanel = ({ logs }) => {
  return (
    <div className="logs-panel">
      {logs.length === 0 ? (
        <div style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '20px' }}>
          Nenhum log ainda...
        </div>
      ) : (
        logs.map((log, index) => (
          <div key={index} className="log-entry">
            <span className="log-timestamp">{log.timestamp}</span>
            <span className={`log-level ${log.level}`}>{log.level.toUpperCase()}</span>
            <span>{log.message}</span>
          </div>
        ))
      )}
    </div>
  );
};

export default LogsPanel;
