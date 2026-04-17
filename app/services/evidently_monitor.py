import logging
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from prometheus_client import Gauge

logger = logging.getLogger(__name__)

# Expose a Prometheus gauge for the drift score
DRIFT_SCORE_GAUGE = Gauge('evidently_data_drift_score', 'Data drift score computed by Evidently AI')

class EvidentlyMonitor:
    def __init__(self):
        logger.info("Initializing EvidentlyMonitor and mocking baseline distribution...")
        
        # Mocking a baseline training distribution for our 5 features
        np.random.seed(42)
        n_samples = 1000
        self.reference_data = pd.DataFrame({
            'kills': np.random.poisson(5, n_samples),
            'deaths': np.random.poisson(5, n_samples),
            'assists': np.random.poisson(10, n_samples),
            'gold_per_min': np.random.normal(450, 100, n_samples),
            'xp_per_min': np.random.normal(500, 100, n_samples)
        })
        
        # We process things in batches to avoid calculating drift on single rows too often
        # But for this demo, we might calculate it on every request or a small batch
        self.current_batch: List[Dict[str, Any]] = []
        
        # Pre-initialize Evidently Report
        self.drift_report = Report(metrics=[DataDriftPreset()])
        
    def log_features(self, features: Dict[str, Any]):
        """Logs features and computes drift if batch is large enough."""
        
        clean_features = {
            'kills': features.get('kills', 0),
            'deaths': features.get('deaths', 0),
            'assists': features.get('assists', 0),
            'gold_per_min': features.get('gold_per_min', 0),
            'xp_per_min': features.get('xp_per_min', 0)
        }
        self.current_batch.append(clean_features)
        
        # For demo purposes, we compute drift on every 5 requests
        if len(self.current_batch) >= 5:
            self.compute_drift()
            self.current_batch = [] # Reset batch
            
    def compute_drift(self):
        try:
            current_data = pd.DataFrame(self.current_batch)
            self.drift_report.run(reference_data=self.reference_data, current_data=current_data)
            
            result = self.drift_report.as_dict()
            # Extract dataset drift score (share of drifted features)
            drift_share = result['metrics'][0]['result']['shared_parameters']['dataset_drift_score']
            
            logger.info(f"Computed Data Drift Score: {drift_share}")
            DRIFT_SCORE_GAUGE.set(drift_share)
            
        except Exception as e:
            logger.error(f"Error computing Evidently drift: {e}")
