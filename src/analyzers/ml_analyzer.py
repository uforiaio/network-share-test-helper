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
            protocol_data (dict): Protocol analysis data
            issues (list): Detected issues
            
        Returns:
            dict: ML analysis results
        """
        try:
            # Skip analysis if no data
            if not network_data or not protocol_data:
                logger.warning("No data available for ML analysis")
                return {
                    'anomalies': [],
                    'predictions': [],
                    'recommendations': []
                }
                
            results = {}
            
            # Get current performance stats
            current_stats = self._get_current_stats(network_data, protocol_data)
            
            # Run basic anomaly detection
            results['anomalies'] = self._detect_anomalies(current_stats)
            
            # Make performance predictions
            results['predictions'] = self._predict_performance(current_stats)
            
            return results
            
        except Exception as e:
            logger.error(f"ML analysis failed: {e}")
            return {
                'anomalies': [],
                'predictions': [],
                'recommendations': []
            }
            
    def _get_current_stats(self, network_data, protocol_data):
        """Extract relevant statistics for ML analysis.
        
        Args:
            network_data (dict): Network metrics data
            protocol_data (dict): Protocol analysis data
            
        Returns:
            dict: Current performance statistics
        """
        stats = {}
        
        # Extract network metrics
        stats['packet_loss'] = protocol_data.get('error_rates', {}).get('packet_loss_rate', 0)
        stats['retransmission_rate'] = protocol_data.get('error_rates', {}).get('retransmission_rate', 0)
        stats['avg_window_size'] = protocol_data.get('tcp_stats', {}).get('avg_window_size', 0)
        
        # Add packet statistics
        if network_data:
            stats['total_packets'] = network_data.get('total_packets', 0)
            stats['avg_packet_size'] = sum(network_data.get('packet_sizes', [])) / len(network_data.get('packet_sizes', [1])) if network_data.get('packet_sizes') else 0
            
        return stats
        
    def _detect_anomalies(self, stats):
        """Detect anomalies in current performance stats.
        
        Args:
            stats (dict): Current performance statistics
            
        Returns:
            list: Detected anomalies
        """
        anomalies = []
        
        # Check for unusual packet loss
        if stats.get('packet_loss', 0) > 0.1:  # More than 10% loss
            anomalies.append({
                'type': 'high_packet_loss',
                'severity': 'high',
                'value': stats['packet_loss']
            })
            
        # Check for unusual window size
        if stats.get('avg_window_size', 0) < 4096:  # Less than 4KB
            anomalies.append({
                'type': 'small_window_size',
                'severity': 'medium',
                'value': stats['avg_window_size']
            })
            
        return anomalies
        
    def _predict_performance(self, stats):
        """Make performance predictions based on current stats.
        
        Args:
            stats (dict): Current performance statistics
            
        Returns:
            list: Performance predictions
        """
        predictions = []
        
        # Predict potential throughput issues
        if stats.get('packet_loss', 0) > 0.05 and stats.get('avg_window_size', 0) < 8192:
            predictions.append({
                'type': 'throughput_degradation',
                'probability': 'high',
                'impact': 'significant',
                'reason': 'High packet loss combined with small window size'
            })
            
        return predictions
            
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
            
    def _format_anomalies(self, df, anomaly_indices):
        """Format detected anomalies into structured output.
        
        Args:
            df (pd.DataFrame): DataFrame containing the metrics
            anomaly_indices (np.ndarray): Indices of detected anomalies
            
        Returns:
            list: List of formatted anomaly dictionaries
        """
        anomalies = []
        metrics = df.columns.tolist()
        
        for idx in anomaly_indices:
            anomaly = {
                'timestamp': datetime.now().isoformat(),
                'metrics': {},
                'severity': 'high'  # Can be enhanced with actual severity calculation
            }
            
            # Add anomalous values for each metric
            for metric in metrics:
                value = df.iloc[idx][metric]
                mean = df[metric].mean()
                std = df[metric].std()
                z_score = (value - mean) / std if std != 0 else 0
                
                anomaly['metrics'][metric] = {
                    'value': float(value),
                    'mean': float(mean),
                    'std': float(std),
                    'z_score': float(z_score),
                    'deviation_percentage': float(abs((value - mean) / mean * 100)) if mean != 0 else 0
                }
            
            # Add description based on the most deviant metric
            most_deviant = max(
                anomaly['metrics'].items(),
                key=lambda x: abs(x[1]['z_score'])
            )
            
            anomaly['description'] = (
                f"Anomalous {most_deviant[0]} detected: "
                f"{most_deviant[1]['value']:.2f} "
                f"({most_deviant[1]['deviation_percentage']:.1f}% deviation from mean)"
            )
            
            anomalies.append(anomaly)
        
        return anomalies
            
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
            current_stats = self._get_current_stats(metrics, {})
            
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
            
    def _filter_recent_data(self, timeframe_minutes):
        # TO DO: implement filtering of recent data
        pass
        
    def _calculate_trends(self):
        # TO DO: implement trend calculation
        return []
        
    def _generate_ai_prediction(self):
        # TO DO: implement AI prediction generation
        return None
