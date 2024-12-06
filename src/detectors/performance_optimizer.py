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
        self.analysis_results = {}
    
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
    
    def get_recommendations(self, network_data, protocol_data, issues):
        """Generate performance optimization recommendations based on analysis data.
        
        Args:
            network_data (dict): Network metrics data
            protocol_data (dict): Protocol analysis data
            issues (list): List of detected issues
            
        Returns:
            list: List of recommendations, each containing:
                - priority: 'high', 'medium', or 'low'
                - category: Type of recommendation
                - description: Human-readable description
                - rationale: Explanation of why this is recommended
        """
        recommendations = []
        
        try:
            # Handle case where input data is missing
            if not network_data or not protocol_data:
                logger.warning("No data available for generating recommendations")
                return recommendations
                
            # Check TCP window size recommendations
            avg_window = protocol_data.get('tcp_stats', {}).get('avg_window_size', 0)
            if avg_window < 65536:  # Less than 64KB
                recommendations.append({
                    'priority': 'medium',
                    'category': 'tcp_tuning',
                    'description': 'Increase TCP window size',
                    'rationale': 'Larger window sizes can improve throughput for high-latency connections'
                })
                
            # Check packet loss related recommendations
            packet_loss_rate = protocol_data.get('error_rates', {}).get('packet_loss_rate', 0)
            if packet_loss_rate > 0.01:  # More than 1% loss
                recommendations.append({
                    'priority': 'high',
                    'category': 'network_quality',
                    'description': 'Investigate network quality issues',
                    'rationale': 'High packet loss is impacting performance'
                })
                
            # Add SMB-specific recommendations
            if protocol_data.get('smb_stats'):
                recommendations.append({
                    'priority': 'low',
                    'category': 'smb_config',
                    'description': 'Consider enabling SMB multichannel',
                    'rationale': 'Multiple connections can improve performance for large file transfers'
                })
                
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return recommendations
    
    def reset(self):
        """Reset optimizer state."""
        self.recommendations = []
        self.analysis_results = {}
        logger.debug("Performance optimizer reset")
