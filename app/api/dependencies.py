from functools import lru_cache
from app.services.opendota_client import OpenDotaClient
from app.services.mlflow_tracker import MLflowTracker
from app.services.model_serving import ModelServer
from app.services.evidently_monitor import EvidentlyMonitor

def get_opendota_client() -> OpenDotaClient:
    return OpenDotaClient()

def get_mlflow_tracker() -> MLflowTracker:
    return MLflowTracker()

@lru_cache()
def get_model_server() -> ModelServer:
    return ModelServer()

@lru_cache()
def get_evidently_monitor() -> EvidentlyMonitor:
    return EvidentlyMonitor()