"""Performance optimization recommendations for network shares."""

from datetime import datetime, timezone
from typing import Dict, List, Any
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class PerformanceOptimizer:
    """Generates performance optimization recommendations."""
    
    def __init__(self):
        """Initialize the performance optimizer."""
        self.recommendations = []
        self.optimal_settings = {
            'tcp_window_size': 65535,
            'max_rtt_ms': 50,
            'min_bandwidth_mbps': 100
        }
    
    def analyze_performance(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze performance metrics and generate recommendations."""
        self.recommendations = []
        
        # Window size optimization
        if metrics['window_size']['avg'] < self.optimal_settings['tcp_window_size']:
            self._add_recommendation('medium', 'Increase TCP window size', {
                'current': metrics['window_size']['avg'],
                'recommended': self.optimal_settings['tcp_window_size']
            })
        
        # Latency optimization
        if metrics['rtt']['avg'] > self.optimal_settings['max_rtt_ms']:
            self._add_recommendation('high', 'Reduce network latency', {
                'current_rtt': metrics['rtt']['avg'],
                'target_rtt': self.optimal_settings['max_rtt_ms']
            })
        
        return self.recommendations
    
    def _add_recommendation(self, priority: str, message: str, details: Dict[str, Any]):
        """Add a recommendation to the list."""
        self.recommendations.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'priority': priority,
            'message': message,
            'details': details
        })
    
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """Get all performance recommendations."""
        return self.recommendations
    
    def reset(self):
        """Reset the optimizer state."""
        self.recommendations = []
