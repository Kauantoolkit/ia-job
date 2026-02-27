"""
Validador de dados CSV
"""
import pandas as pd
from typing import Tuple, List, Dict, Any
from app.config import REQUIRED_COLUMNS, VALID_TRAFFIC_LEVELS, VALID_DELAY_LABELS


class CSVValidator:
    """Classe para validar dados do CSV"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_csv(self, df: pd.DataFrame) -> Tuple[bool, List[str], List[str]]:
        """
        Valida o DataFrame contendo os dados do CSV
        
        Args:
            df: DataFrame pandas com os dados
            
        Returns:
            Tuple de (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Verificar colunas obrigatórias
        self._validate_columns(df)
        
        # Verificar tipos de dados
        self._validate_data_types(df)
        
        # Verificar valores válidos
        self._validate_values(df)
        
        # Verificar dados faltantes
        self._validate_missing_data(df)
        
        is_valid = len(self.errors) == 0
        
        return is_valid, self.errors, self.warnings
    
    def _validate_columns(self, df: pd.DataFrame):
        """Verifica se todas as colunas obrigatórias estão presentes"""
        missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)
        
        if missing_columns:
            self.errors.append(
                f"Colunas obrigatórias faltando: {', '.join(missing_columns)}"
            )
        
        # Verificar colunas extras (aviso)
        extra_columns = set(df.columns) - set(REQUIRED_COLUMNS)
        if extra_columns:
            self.warnings.append(
                f"Colunas extras detectadas (serão ignoradas): {', '.join(extra_columns)}"
            )
    
    def _validate_data_types(self, df: pd.DataFrame):
        """Valida os tipos de dados das colunas"""
        # planned_departure_hour deve ser numérico
        if "planned_departure_hour" in df.columns:
            if not pd.api.types.is_numeric_dtype(df["planned_departure_hour"]):
                self.errors.append(
                    "planned_departure_hour deve ser numérico (int)"
                )
            else:
                # Verificar range 0-23
                invalid_hours = df[
                    (df["planned_departure_hour"] < 0) | 
                    (df["planned_departure_hour"] > 23)
                ]
                if len(invalid_hours) > 0:
                    self.errors.append(
                        f"planned_departure_hour deve estar entre 0 e 23. "
                        f"Encontrados {len(invalid_hours)} valores inválidos."
                    )
        
        # rain_forecast_mm deve ser numérico
        if "rain_forecast_mm" in df.columns:
            if not pd.api.types.is_numeric_dtype(df["rain_forecast_mm"]):
                self.errors.append("rain_forecast_mm deve ser numérico (float)")
        
        # cargo_weight_kg deve ser numérico
        if "cargo_weight_kg" in df.columns:
            if not pd.api.types.is_numeric_dtype(df["cargo_weight_kg"]):
                self.errors.append("cargo_weight_kg deve ser numérico (float)")
        
        # historical_avg_route_time_min deve ser numérico
        if "historical_avg_route_time_min" in df.columns:
            if not pd.api.types.is_numeric_dtype(df["historical_avg_route_time_min"]):
                self.errors.append(
                    "historical_avg_route_time_min deve ser numérico (float)"
                )
        
        # distance_km deve ser numérico
        if "distance_km" in df.columns:
            if not pd.api.types.is_numeric_dtype(df["distance_km"]):
                self.errors.append("distance_km deve ser numérico (float)")
    
    def _validate_values(self, df: pd.DataFrame):
        """Valida valores específicos"""
        # traffic_level_forecast
        if "traffic_level_forecast" in df.columns:
            invalid_traffic = ~df["traffic_level_forecast"].isin(VALID_TRAFFIC_LEVELS)
            if invalid_traffic.any():
                invalid_values = df.loc[invalid_traffic, "traffic_level_forecast"].unique()
                self.errors.append(
                    f"traffic_level_forecast deve ser um de: {VALID_TRAFFIC_LEVELS}. "
                    f"Encontrados: {list(invalid_values)}"
                )
        
        # delay_label
        if "delay_label" in df.columns:
            invalid_labels = ~df["delay_label"].isin(VALID_DELAY_LABELS)
            if invalid_labels.any():
                invalid_values = df.loc[invalid_labels, "delay_label"].unique()
                self.errors.append(
                    f"delay_label deve ser um de: {VALID_DELAY_LABELS}. "
                    f"Encontrados: {list(invalid_values)}"
                )
    
    def _validate_missing_data(self, df: pd.DataFrame):
        """Verifica dados faltantes"""
        # Colunas que não podem ter valores faltantes
        required_cols_no_null = [
            "delay_label",
            "planned_departure_hour",
            "traffic_level_forecast",
            "rain_forecast_mm",
            "cargo_weight_kg",
            "vehicle_type",
            "historical_avg_route_time_min",
            "distance_km"
        ]
        
        for col in required_cols_no_null:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                if null_count > 0:
                    self.errors.append(
                        f"Coluna '{col}' tem {null_count} valores faltantes"
                    )
    
    def get_feature_columns(self, df: pd.DataFrame) -> Tuple[List[str], List[str]]:
        """
        Identifica colunas categóricas e numéricas para features
        
        Returns:
            Tuple de (categorical_columns, numerical_columns)
        """
        # Colunas que são features (excluindo freight_description e delay_label)
        feature_cols = [col for col in df.columns if col not in ["freight_description", "delay_label"]]
        
        categorical = []
        numerical = []
        
        for col in feature_cols:
            if df[col].dtype == "object":
                categorical.append(col)
            else:
                numerical.append(col)
        
        return categorical, numerical


def validate_prediction_input(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valida os dados de entrada para predição
    
    Args:
        data: Dicionário com os dados do frete
        
    Returns:
        Tuple de (is_valid, errors)
    """
    errors = []
    
    # Verificar campos numéricos
    numeric_fields = [
        "planned_departure_hour",
        "rain_forecast_mm",
        "cargo_weight_kg",
        "historical_avg_route_time_min",
        "distance_km"
    ]
    
    for field in numeric_fields:
        if field not in data:
            errors.append(f"Campo '{field}' é obrigatório")
        elif not isinstance(data[field], (int, float)):
            errors.append(f"Campo '{field}' deve ser numérico")
    
    # Verificar range de planned_departure_hour
    if "planned_departure_hour" in data:
        hour = data["planned_departure_hour"]
        if not (0 <= hour <= 23):
            errors.append("planned_departure_hour deve estar entre 0 e 23")
    
    # Verificar traffic_level_forecast
    if "traffic_level_forecast" not in data:
        errors.append("Campo 'traffic_level_forecast' é obrigatório")
    elif data["traffic_level_forecast"] not in VALID_TRAFFIC_LEVELS:
        errors.append(
            f"traffic_level_forecast deve ser um de: {VALID_TRAFFIC_LEVELS}"
        )
    
    # Verificar vehicle_type
    if "vehicle_type" not in data:
        errors.append("Campo 'vehicle_type' é obrigatório")
    
    # Verificar route_variant_id
    if "route_variant_id" not in data:
        errors.append("Campo 'route_variant_id' é obrigatório")
    
    return len(errors) == 0, errors
