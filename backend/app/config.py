"""
Configurações da aplicação
"""
import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

# Criar diretórios se não existirem
MODELS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Configurações do modelo
MODEL_FILENAME = "delay_predictor.pkl"
MODEL_VERSION_FILE = "model_version.txt"

# Configurações do servidor
HOST = "0.0.0.0"
PORT = 8000

# Colunas obrigatórias do CSV
REQUIRED_COLUMNS = [
    "freight_description",
    "delay_label",
    "route_variant_id",
    "planned_departure_hour",
    "traffic_level_forecast",
    "rain_forecast_mm",
    "cargo_weight_kg",
    "vehicle_type",
    "historical_avg_route_time_min",
    "distance_km"
]

# Valores válidos
VALID_TRAFFIC_LEVELS = ["baixo", "medio", "alto"]
VALID_DELAY_LABELS = ["atrasado", "em_tempo"]

# Configurações do RandomForest
RANDOM_FOREST_PARAMS = {
    "n_estimators": 100,
    "max_depth": 10,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "random_state": 42,
    "n_jobs": -1
}
