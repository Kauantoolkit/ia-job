import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = ({ modelStatus }) => {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
        </svg>
        <span>Delivery Delay Predictor</span>
      </div>
      
      <div className="navbar-nav">
        <Link 
          to="/" 
          className={`nav-link ${isActive('/') ? 'active' : ''}`}
        >
          Dashboard
        </Link>
        <Link 
          to="/train" 
          className={`nav-link ${isActive('/train') ? 'active' : ''}`}
        >
          Treinar Modelo
        </Link>
        <Link 
          to="/metrics" 
          className={`nav-link ${isActive('/metrics') ? 'active' : ''}`}
        >
          Métricas
        </Link>
        <Link 
          to="/predict" 
          className={`nav-link ${isActive('/predict') ? 'active' : ''}`}
        >
          Prever Atraso
        </Link>
      </div>
      
      <div className="status-badge">
        {modelStatus?.is_trained ? (
          <>
            <span className="status-dot"></span>
            Modelo v{modelStatus.version || '1.0.0'}
          </>
        ) : (
          <>
            <span className="status-dot"></span>
            Não treinado
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
