import mlflow
import logging
from app.core.config import settings
from app.models.schemas import MatchData

logger = logging.getLogger(__name__)

class MLflowTracker:
    def __init__(self):
        self.tracking_uri = settings.MLFLOW_TRACKING_URI
        self.experiment_name = settings.PROJECT_NAME
        self._initialized = False

    def _initialize(self) -> None:
        if self._initialized:
            return
        
        try:
            mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(self.experiment_name)
            self._initialized = True
        except Exception as e:
            logger.error(f"MLflow connection failed. Metrics will be skipped. Error: {str(e)}")

    def log_match_metrics(self, match_data: MatchData) -> None:
        self._initialize()
        
        if not self._initialized:
            logger.warning(f"Skipping metrics for match {match_data.match_id} due to MLflow unavailability.")
            return

        try:
            with mlflow.start_run(run_name=f"match_{match_data.match_id}"):
                mlflow.log_param("patch", str(match_data.patch))
                mlflow.log_metric("duration", match_data.duration)
                
                gpms = [p.gold_per_min for p in match_data.players if p.gold_per_min is not None]
                if gpms:
                    avg_gpm = sum(gpms) / len(gpms)
                    mlflow.log_metric("avg_gpm", avg_gpm)
                    
        except Exception as e:
            logger.error(f"Failed to log metrics to MLflow: {str(e)}")