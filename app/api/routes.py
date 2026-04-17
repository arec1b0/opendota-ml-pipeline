import logging
from fastapi import APIRouter, Depends
from app.api.endpoints import predict
from app.models.schemas import MatchData
from app.services.opendota_client import OpenDotaClient
from app.services.mlflow_tracker import MLflowTracker
from app.api.dependencies import get_opendota_client, get_mlflow_tracker

logger = logging.getLogger(__name__)
router = APIRouter()

router.include_router(predict.router, tags=["predict"])

@router.get("/match/{match_id}", response_model=MatchData)
async def ingest_match(
    match_id: int,
    opendota_client: OpenDotaClient = Depends(get_opendota_client),
    mlflow_tracker: MLflowTracker = Depends(get_mlflow_tracker)
):
    logger.info(f"Ingesting match_id: {match_id}")
    
    match_data = await opendota_client.fetch_match(match_id)
    mlflow_tracker.log_match_metrics(match_data)
    
    return match_data