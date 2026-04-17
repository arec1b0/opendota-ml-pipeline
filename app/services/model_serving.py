import logging
import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

class ModelServer:
    def __init__(self):
        # We are mocking the model loading process
        logger.info("Initializing ModelServer and loading (mock) ML model...")
        self.model = LogisticRegression()
        
        # Mock training to populate weights for prediction
        # Assume features are: kills, deaths, assists, gold_per_min, xp_per_min
        # and some dummy labels
        X_dummy = np.random.rand(100, 5) * 100
        y_dummy = np.random.randint(0, 2, 100)
        self.model.fit(X_dummy, y_dummy)
        self.version = "v1.0-mock"

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expects a dictionary of features:
        kills, deaths, assists, gold_per_min, xp_per_min
        """
        try:
            # We assume features are provided as a single row
            df = pd.DataFrame([features])
            X = df[['kills', 'deaths', 'assists', 'gold_per_min', 'xp_per_min']].fillna(0).values
            
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0][1] # Probability of class 1

            return {
                "label": int(prediction),
                "proba": float(probability),
                "model_version": self.version
            }
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
