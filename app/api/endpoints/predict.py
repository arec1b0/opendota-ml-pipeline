import logging
from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.api.dependencies import get_model_server, get_evidently_monitor
from app.services.model_serving import ModelServer
from app.services.evidently_monitor import EvidentlyMonitor
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

class PredictionRequest(BaseModel):
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    gold_per_min: int = 0
    xp_per_min: int = 0

@router.post("/predict")
async def predict_match_outcome(
    request: PredictionRequest,
    model_server: ModelServer = Depends(get_model_server),
    evidently_monitor: EvidentlyMonitor = Depends(get_evidently_monitor)
):
    logger.info("Received prediction request")
    
    features = request.model_dump()
    
    # Track features for drift detection
    evidently_monitor.log_features(features)
    
    # Make prediction
    prediction = model_server.predict(features)
    
    return prediction
