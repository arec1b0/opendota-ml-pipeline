from app.services.opendota_client import OpenDotaClient
from app.services.mlflow_tracker import MLflowTracker

def get_opendota_client() -> OpenDotaClient:
    return OpenDotaClient()

def get_mlflow_tracker() -> MLflowTracker:
    return MLflowTracker()