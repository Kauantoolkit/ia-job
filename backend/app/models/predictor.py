"""
Modelo preditor de atraso de entregas
"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Any, Optional, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    roc_auc_score, 
    confusion_matrix,
    classification_report
)

from app.config import (
    MODELS_DIR, 
    MODEL_FILENAME, 
    RANDOM_FOREST_PARAMS,
    VALID_DELAY_LABELS
)
from app.utils.validator import CSVValidator


class DelayPredictor:
    """
    Modelo de predição de atraso de entregas usando RandomForest
    """
    
    def __init__(self):
        self.model: Optional[Pipeline] = None
        self.categorical_features: List[str] = []
        self.numerical_features: List[str] = []
        self.validator = CSVValidator()
        self.is_trained = False
        self.version = "0.0.0"
        self.training_date: Optional[str] = None
        self.feature_importances_: Optional[Dict[str, float]] = None
        self.last_metrics: Optional[Dict[str, float]] = None
    
    def _get_feature_columns(self, df: pd.DataFrame) -> Tuple[List[str], List[str]]:
        """Extrai colunas categóricas e numéricas do DataFrame"""
        # Remover colunas que não são features
        exclude_cols = ["freight_description", "delay_label"]
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        categorical = []
        numerical = []
        
        for col in feature_cols:
            if df[col].dtype == "object":
                categorical.append(col)
            else:
                numerical.append(col)
        
        return categorical, numerical
    
    def _prepare_target(self, df: pd.DataFrame) -> pd.Series:
        """Converte delay_label para binário"""
        # "atrasado" = 1, "em_tempo" = 0
        return (df["delay_label"] == "atrasado").astype(int)
    
    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepara as features para o modelo"""
        # Remover colunas que não são features
        exclude_cols = ["freight_description", "delay_label"]
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        return df[feature_cols].copy()
    
    def train(
        self, 
        df: pd.DataFrame, 
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Dict[str, Any]:
        """
        Treina o modelo com os dados fornecidos
        
        Args:
            df: DataFrame com os dados de treino
            test_size: Proporção dos dados para teste
            random_state: Semente aleatória
            
        Returns:
            Dicionário com métricas e informações do treino
        """
        # Validar dados
        is_valid, errors, warnings = self.validator.validate_csv(df)
        if not is_valid:
            raise ValueError(f"Erros de validação: {errors}")
        
        # Identificar colunas
        self.categorical_features, self.numerical_features = self._get_feature_columns(df)
        
        # Preparar X e y
        X = self._prepare_features(df)
        y = self._prepare_target(df)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Criar pré-processador
        preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.numerical_features),
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), 
                 self.categorical_features)
            ]
        )
        
        # Criar pipeline
        self.model = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(**RANDOM_FOREST_PARAMS))
        ])
        
        # Treinar modelo
        self.model.fit(X_train, y_train)
        
        # Fazer predições
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calcular métricas
        accuracy = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)
        cm = confusion_matrix(y_test, y_pred)
        
        # Feature importances (apenas das features numéricas + categorias do OneHot)
        # Precisamos mapear de volta para nomes originais
        try:
            feature_names = (
                self.numerical_features + 
                list(self.model.named_steps["preprocessor"]
                     .named_transformers_["cat"]
                     .get_feature_names_out(self.categorical_features))
            )
            importances = self.model.named_steps["classifier"].feature_importances_
            self.feature_importances_ = dict(zip(feature_names, importances))
        except:
            self.feature_importances_ = {}
        
        # Salvar métricas
        self.last_metrics = {
            "accuracy": float(accuracy),
            "auc": float(auc),
            "confusion_matrix": cm.tolist(),
            "train_size": len(X_train),
            "test_size": len(X_test)
        }
        
        # Marcar como treinado
        self.is_trained = True
        from datetime import datetime
        self.training_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Incrementar versão
        self._increment_version()
        
        return {
            "status": "success",
            "metrics": self.last_metrics,
            "warnings": warnings,
            "version": self.version,
            "training_date": self.training_date,
            "n_features": len(self.categorical_features) + len(self.numerical_features)
        }
    
    def _increment_version(self):
        """Incrementa a versão do modelo"""
        if self.version == "0.0.0":
            self.version = "1.0.0"
        else:
            parts = self.version.split(".")
            parts[-1] = str(int(parts[-1]) + 1)
            self.version = ".".join(parts)
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Faz predição para novos dados
        
        Args:
            data: Dicionário com os dados do frete
            
        Returns:
            Dicionário com probabilidade de atraso
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Modelo não foi treinado ainda")
        
        # Converter para DataFrame
        df = pd.DataFrame([data])
        
        # Fazer predição
        probability = self.model.predict_proba(df)[0, 1]
        
        # Determinar risco
        if probability < 0.3:
            risk_level = "baixo"
            risk_color = "green"
        elif probability < 0.7:
            risk_level = "medio"
            risk_color = "yellow"
        else:
            risk_level = "alto"
            risk_color = "red"
        
        return {
            "probability": float(probability),
            "probability_percent": round(probability * 100, 2),
            "risk_level": risk_level,
            "risk_color": risk_color,
            "prediction": "atrasado" if probability >= 0.5 else "em_tempo"
        }
    
    def save(self, filepath: Optional[Path] = None) -> str:
        """
        Salva o modelo em arquivo
        
        Args:
            filepath: Caminho do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not self.is_trained:
            raise ValueError("Modelo não foi treinado ainda")
        
        if filepath is None:
            filepath = MODELS_DIR / MODEL_FILENAME
        
        # Criar diretório se não existir
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Salvar modelo com metadados
        model_data = {
            "model": self.model,
            "version": self.version,
            "training_date": self.training_date,
            "categorical_features": self.categorical_features,
            "numerical_features": self.numerical_features,
            "feature_importances": self.feature_importances_,
            "last_metrics": self.last_metrics
        }
        
        joblib.dump(model_data, filepath)
        return str(filepath)
    
    def load(self, filepath: Optional[Path] = None) -> bool:
        """
        Carrega o modelo de arquivo
        
        Args:
            filepath: Caminho do arquivo (opcional)
            
        Returns:
            True se carregou com sucesso
        """
        if filepath is None:
            filepath = MODELS_DIR / MODEL_FILENAME
        
        if not filepath.exists():
            return False
        
        try:
            model_data = joblib.load(filepath)
            
            self.model = model_data["model"]
            self.version = model_data.get("version", "1.0.0")
            self.training_date = model_data.get("training_date")
            self.categorical_features = model_data.get("categorical_features", [])
            self.numerical_features = model_data.get("numerical_features", [])
            self.feature_importances_ = model_data.get("feature_importances", {})
            self.last_metrics = model_data.get("last_metrics")
            self.is_trained = True
            
            return True
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            return False
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo"""
        return {
            "is_trained": self.is_trained,
            "version": self.version,
            "training_date": self.training_date,
            "categorical_features": self.categorical_features,
            "numerical_features": self.numerical_features,
            "last_metrics": self.last_metrics
        }
    
    def get_feature_importance(self) -> List[Dict[str, Any]]:
        """Retorna importância das features"""
        if not self.feature_importances_:
            return []
        
        # Ordenar por importância
        sorted_features = sorted(
            self.feature_importances_.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return [
            {"feature": name, "importance": float(importance)}
            for name, importance in sorted_features
        ]


# Instância global do modelo
predictor = DelayPredictor()
