"""Protocol information collection and analysis."""

import json
from datetime import datetime, timezone
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class ProtocolInfo:
    """Collects and analyzes protocol-specific information."""
    
    def __init__(self):
        """Initialize protocol information collection."""
        self.protocol_type = None  # SMB or NFS
        self.protocol_version = None
        self.features = {}
        self.capabilities = {}
        self.security_info = {}
        self.dialect_info = {}
        self.connection_info = {}
        
    def set_protocol_type(self, protocol_type, version=None):
        """Set the protocol type and version."""
        self.protocol_type = protocol_type
        if version:
            self.protocol_version = version
            
    def add_feature(self, feature_name, enabled=True):
        """Add protocol feature information."""
        self.features[feature_name] = {
            "enabled": enabled,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_capability(self, capability_name, value):
        """Add protocol capability information."""
        self.capabilities[capability_name] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_security_info(self, key, value):
        """Add security-related information."""
        self.security_info[key] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_dialect_info(self, dialect, negotiated=False):
        """Add SMB dialect information."""
        self.dialect_info[dialect] = {
            "negotiated": negotiated,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_connection_info(self, key, value):
        """Add connection-specific information."""
        self.connection_info[key] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def get_info(self):
        """Get all protocol information."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "protocol": {
                "type": self.protocol_type,
                "version": self.protocol_version
            },
            "features": self.features,
            "capabilities": self.capabilities,
            "security": self.security_info,
            "dialects": self.dialect_info,
            "connection": self.connection_info
        }
        
    def reset(self):
        """Reset all protocol information."""
        self.protocol_type = None
        self.protocol_version = None
        self.features = {}
        self.capabilities = {}
        self.security_info = {}
        self.dialect_info = {}
        self.connection_info = {}
        logger.debug("Protocol info reset")

    def analyze_protocols(self, network_data):
        """Analyze protocol information from network data.
        
        Args:
            network_data (dict): Network metrics data from NetworkMetrics
            
        Returns:
            dict: Protocol analysis results containing:
                - protocol_distribution: Distribution of protocols used
                - smb_stats: SMB-specific statistics if available
                - tcp_stats: TCP connection statistics
                - error_rates: Protocol-specific error rates
        """
        try:
            # Handle None input
            if network_data is None:
                logger.warning("No network data available for protocol analysis")
                return {
                    'protocol_distribution': {},
                    'smb_stats': {},
                    'tcp_stats': {},
                    'error_rates': {}
                }
                
            # Initialize results
            results = {
                'protocol_distribution': {},
                'smb_stats': {},
                'tcp_stats': {},
                'error_rates': {}
            }
            
            # Analyze TCP stats from network data
            window_sizes = network_data.get('window_sizes', [])
            if window_sizes:
                results['tcp_stats']['avg_window_size'] = sum(window_sizes) / len(window_sizes)
            else:
                results['tcp_stats']['avg_window_size'] = 0
                
            results['tcp_stats']['retransmission_count'] = network_data.get('retransmissions', 0)
            
            # Calculate error rates
            total_packets = network_data.get('total_packets', 0)
            if total_packets > 0:
                packet_loss = network_data.get('packet_loss_count', 0)
                results['error_rates']['packet_loss_rate'] = packet_loss / total_packets
                results['error_rates']['retransmission_rate'] = network_data.get('retransmissions', 0) / total_packets
            else:
                results['error_rates']['packet_loss_rate'] = 0
                results['error_rates']['retransmission_rate'] = 0
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing protocols: {e}")
            return {
                'protocol_distribution': {},
                'smb_stats': {},
                'tcp_stats': {},
                'error_rates': {}
            }
