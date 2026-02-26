"""
FastAPI Application - Entry Point
Sistema de Previsão de Atraso de Entregas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.controllers.api import router as ml_router
from app.config import HOST, PORT

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Criar aplicação FastAPI
app = FastAPI(
    title="Delivery Delay Predictor API",
    description="API para previsão de atraso de entregas usando Machine Learning",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(ml_router)

# Rota raiz
@app.get("/")
async def root():
    return {
        "name": "Delivery Delay Predictor API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "health": "/api/health",
            "train": "/api/train",
            "predict": "/api/predict",
            "retrain": "/api/retrain",
            "metrics": "/api/metrics",
            "feature_importance": "/api/features/importance",
            "model_info": "/api/model/info"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar o servidor"""
    logger.info("=" * 50)
    logger.info("Iniciando Delivery Delay Predictor API")
    logger.info("=" * 50)
    
    # Tentar carregar modelo existente
    from app.models.predictor import predictor
    from app.config import MODELS_DIR, MODEL_FILENAME
    
    model_path = MODELS_DIR / MODEL_FILENAME
    if model_path.exists():
        try:
            predictor.load(model_path)
            logger.info(f"Modelo carregado: versão {predictor.version}")
        except Exception as e:
            logger.warning(f"Não foi possível carregar modelo existente: {e}")
    else:
        logger.info("Nenhum modelo encontrado. Execute o treino primeiro.")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado ao encerrar o servidor"""
    logger.info("Encerrando Delivery Delay Predictor API")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
