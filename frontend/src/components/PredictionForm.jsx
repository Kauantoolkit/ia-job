import React, { useState } from 'react';

const PredictionForm = ({ onSubmit, isLoading, isModelTrained }) => {
  const [formData, setFormData] = useState({
    route_variant_id: 'ROTA_001',
    planned_departure_hour: 8,
    traffic_level_forecast: 'medio',
    rain_forecast_mm: 0,
    cargo_weight_kg: 2000,
    vehicle_type: 'Caminhão Baú',
    historical_avg_route_time_min: 100,
    historical_delay_rate_route: 0.2,
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-row">
        <div className="form-group">
          <label className="form-label">ID da Rota</label>
          <input
            type="text"
            name="route_variant_id"
            className="form-input"
            value={formData.route_variant_id}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Hora de Partida (0-23)</label>
          <input
            type="number"
            name="planned_departure_hour"
            className="form-input"
            min="0"
            max="23"
            value={formData.planned_departure_hour}
            onChange={handleChange}
            required
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label className="form-label">Nível de Tráfego</label>
          <select
            name="traffic_level_forecast"
            className="form-select"
            value={formData.traffic_level_forecast}
            onChange={handleChange}
            required
          >
            <option value="baixo">Baixo</option>
            <option value="medio">Médio</option>
            <option value="alto">Alto</option>
          </select>
        </div>

        <div className="form-group">
          <label className="form-label">Previsão de Chuva (mm)</label>
          <input
            type="number"
            name="rain_forecast_mm"
            className="form-input"
            min="0"
            step="0.1"
            value={formData.rain_forecast_mm}
            onChange={handleChange}
            required
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label className="form-label">Peso da Carga (kg)</label>
          <input
            type="number"
            name="cargo_weight_kg"
            className="form-input"
            min="0"
            value={formData.cargo_weight_kg}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Tipo de Veículo</label>
          <select
            name="vehicle_type"
            className="form-select"
            value={formData.vehicle_type}
            onChange={handleChange}
            required
          >
            <option value="Caminhão Baú">Caminhão Baú</option>
            <option value="Caminhão Truck">Caminhão Truck</option>
            <option value="Caminhão Bitrem">Caminhão Bitrem</option>
            <option value="Vanqua">Vanqua</option>
          </select>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label className="form-label">Tempo Médio Histórico da Rota (min)</label>
          <input
            type="number"
            name="historical_avg_route_time_min"
            className="form-input"
            min="0"
            value={formData.historical_avg_route_time_min}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Taxa Histórica de Atraso da Rota</label>
          <input
            type="number"
            name="historical_delay_rate_route"
            className="form-input"
            min="0"
            max="1"
            step="0.01"
            value={formData.historical_delay_rate_route}
            onChange={handleChange}
            required
          />
        </div>
      </div>

      <button
        type="submit"
        className="btn btn-primary"
        disabled={isLoading || !isModelTrained}
        style={{ width: '100%', marginTop: '16px' }}
      >
        {isLoading ? (
          <>
            <span className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }}></span>
            Calculando...
          </>
        ) : (
          'Calcular Probabilidade de Atraso'
        )}
      </button>

      {!isModelTrained && (
        <p style={{ color: 'var(--warning)', marginTop: '12px', textAlign: 'center' }}>
          Treine o modelo primeiro para fazer predições
        </p>
      )}
    </form>
  );
};

export default PredictionForm;
