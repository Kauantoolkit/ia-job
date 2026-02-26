"""
Controlador da API - Endpoints para ML
"""
import os
import io
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, List
import logging

from app.models.predictor import predictor
from app.config import DATA_DIR
from app.utils.validator import validate_prediction_input

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar router
router = APIRouter(prefix="/api", tags=["ML"])


@router.get("/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {
        "status": "healthy",
        "model_loaded": predictor.is_trained,
        "model_version": predictor.version if predictor.is_trained else None
    }


@router.get("/model/info")
async def get_model_info():
    """Retorna informações sobre o modelo atual"""
    info = predictor.get_info()
    
    if not info["is_trained"]:
        return JSONResponse(
            status_code=404,
            content={
                "message": "Modelo ainda não foi treinado",
                "is_trained": False
            }
        )
    
    return info


@router.post("/train")
async def train_model(
    file: UploadFile = File(..., description="Arquivo CSV com dados de treino")
):
    """
    Treina o modelo com os dados fornecidos
    
    Args:
        file: Arquivo CSV com os dados
        
    Returns:
        Métricas do modelo treinado
    """
    logger.info(f"Iniciando treino com arquivo: {file.filename}")
    
    try:
        # Ler arquivo CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        logger.info(f"Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
        logger.info(f"Colunas: {list(df.columns)}")
        
        # Treinar modelo
        result = predictor.train(df)
        
        # Salvar modelo
        model_path = predictor.save()
        logger.info(f"Modelo salvo em: {model_path}")
        
        return {
            "status": "success",
            "message": "Modelo treinado com sucesso",
            "metrics": result["metrics"],
            "warnings": result.get("warnings", []),
            "version": result["version"],
            "training_date": result["training_date"],
            "model_path": model_path
        }
        
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro durante treino: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro durante treino: {str(e)}")


@router.post("/retrain")
async def retrain_model(
    file: UploadFile = File(..., description="Arquivo CSV com novos dados")
):
    """
    Re-treina o modelo com novos dados
    
    Args:
        file: Arquivo CSV com dados adicionais
        
    Returns:
        Métricas do modelo re-treinado
    """
    logger.info(f"Iniciando re-treino com arquivo: {file.filename}")
    
    if not predictor.is_trained:
        raise HTTPException(
            status_code=400, 
            detail="Modelo precisa ser treinado primeiro"
        )
    
    try:
        # Ler arquivo CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        logger.info(f"Dados carregados: {len(df)} linhas")
        
        # Re-treinar modelo (usando todos os dados para treino final após validação)
        result = predictor.train(df)
        
        # Salvar modelo
        model_path = predictor.save()
        
        return {
            "status": "success",
            "message": "Modelo re-treinado com sucesso",
            "metrics": result["metrics"],
            "version": result["version"],
            "training_date": result["training_date"],
            "model_path": model_path
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro durante re-treino: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro durante re-treino: {str(e)}")


@router.post("/predict")
async def predict_delay(data: Dict[str, Any]):
    """
    Faz predição de atraso para novos dados
    
    Args:
        data: Dados do frete
        
    Returns:
        Probabilidade de atraso
    """
    logger.info(f"Recebida requisição de predição")
    
    if not predictor.is_trained:
        raise HTTPException(
            status_code=400,
            detail="Modelo precisa ser treinado primeiro"
        )
    
    # Validar entrada
    is_valid, errors = validate_prediction_input(data)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Erros de validação: {errors}")
    
    try:
        # Fazer predição
        result = predictor.predict(data)
        
        logger.info(
            f"Predição: {result['prediction']} "
            f"(probabilidade: {result['probability_percent']}%)"
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Erro durante predição: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro durante predição: {str(e)}")


@router.get("/metrics")
async def get_metrics():
    """Retorna métricas do último treino"""
    if not predictor.is_trained:
        raise HTTPException(
            status_code=400,
            detail="Modelo precisa ser treinado primeiro"
        )
    
    return predictor.last_metrics


@router.get("/features/importance")
async def get_feature_importance():
    """Retorna importância das features"""
    if not predictor.is_trained:
        raise HTTPException(
            status_code=400,
            detail="Modelo precisa ser treinado primeiro"
        )
    
    importance = predictor.get_feature_importance()
    
    return {
        "features": importance,
        "total_features": len(importance)
    }


@router.post("/load-model")
async def load_existing_model():
    """Carrega o modelo salvo anteriormente"""
    from app.config import MODELS_DIR, MODEL_FILENAME
    
    model_path = MODELS_DIR / MODEL_FILENAME
    
    if not model_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Nenhum modelo encontrado"
        )
    
    success = predictor.load(model_path)
    
    if success:
        return {
            "status": "success",
            "message": "Modelo carregado com sucesso",
            "version": predictor.version,
            "training_date": predictor.training_date
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Erro ao carregar modelo"
        )
