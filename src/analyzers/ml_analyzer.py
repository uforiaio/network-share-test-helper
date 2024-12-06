"""ML analysis functionality for DFS/NFS debugging."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import openai
from datetime import datetime, timedelta
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

class MLAnalyzer:
    """Machine Learning analyzer for network metrics."""
    
    def __init__(self, api_key):
        """Initialize the ML analyzer.
        
        Args:
            api_key (str): OpenAI API key for advanced analysis
        """
        self.api_key = api_key
        openai.api_key = api_key
        self.scaler = StandardScaler()
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.historical_data = []
        
    def analyze(self, network_data, protocol_data, issues):
        """Analyze network data using ML techniques.
        
        Args:
            network_data (dict): Network metrics data
            protocol_data (dict): Protocol information
            issues (list): Detected issues
            
        Returns:
            dict: Analysis results including anomalies and predictions
        """
        try:
            # Basic anomaly detection
            anomalies = self._basic_anomaly_detection(network_data)
            
            # Performance prediction
            predictions = self.predict_performance(network_data)
            
            return {
                'anomalies': anomalies,
                'predictions': predictions,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"ML analysis failed: {str(e)}")
            return None
            
    def _basic_anomaly_detection(self, metrics):
        """Perform basic anomaly detection without OpenAI API.
        
        Args:
            metrics (dict): Network metrics to analyze
            
        Returns:
            list: Detected anomalies
        """
        try:
            # Convert metrics to DataFrame
            df = pd.DataFrame({
                'rtt': metrics.get('rtt_samples', []),
                'packet_size': metrics.get('packet_sizes', []),
                'window_size': metrics.get('window_sizes', [])
            })
            
            if df.empty:
                return []
                
            # Fit and predict
            X = self.scaler.fit_transform(df)
            anomaly_labels = self.isolation_forest.fit_predict(X)
            
            # Find anomaly indices
            anomaly_indices = np.where(anomaly_labels == -1)[0]
            
            return self._format_anomalies(df, anomaly_indices)
            
        except Exception as e:
            logger.error(f"Basic anomaly detection failed: {str(e)}")
            return []
            
    def predict_performance(self, metrics, timeframe_minutes=30):
        """Predict performance trends.
        
        Args:
            metrics (dict): Current network metrics
            timeframe_minutes (int): Prediction timeframe in minutes
            
        Returns:
            dict: Performance predictions
        """
        try:
            # Get current stats
            current_stats = self._get_current_stats(metrics)
            
            # Filter recent data
            self._filter_recent_data(timeframe_minutes)
            
            # Calculate trends
            trends = self._calculate_trends()
            
            # Generate AI prediction if possible
            ai_prediction = self._generate_ai_prediction()
            
            return {
                'current_stats': current_stats,
                'trends': trends,
                'ai_prediction': ai_prediction
            }
            
        except Exception as e:
            logger.error(f"Performance prediction failed: {str(e)}")
            return None
            
    def cleanup(self):
        """Clean up resources."""
        try:
            self.historical_data.clear()
            self.scaler = None
            self.isolation_forest = None
        except Exception as e:
            logger.error(f"ML analyzer cleanup failed: {str(e)}")
