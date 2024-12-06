"""Issue detection and analysis for network shares."""

import logging
from datetime import datetime, timezone
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class IssueDetector:
    """Detects and analyzes network share issues."""
    
    def __init__(self):
        """Initialize the issue detector."""
        self.issues = []
        self.thresholds = {
            'rtt_warning_ms': 50,
            'rtt_critical_ms': 100,
            'packet_loss_warning': 0.1,
            'packet_loss_critical': 1.0,
            'retransmission_warning': 1.0,
            'retransmission_critical': 5.0,
            'window_size_min': 65535
        }
        
    def analyze_metrics(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze network metrics for issues."""
        self.issues = []
        
        # Check RTT
        if metrics['rtt']['avg'] > self.thresholds['rtt_critical_ms']:
            self._add_issue('critical', 'High latency detected', {
                'avg_rtt': metrics['rtt']['avg'],
                'threshold': self.thresholds['rtt_critical_ms']
            })
        elif metrics['rtt']['avg'] > self.thresholds['rtt_warning_ms']:
            self._add_issue('warning', 'Elevated latency detected', {
                'avg_rtt': metrics['rtt']['avg'],
                'threshold': self.thresholds['rtt_warning_ms']
            })
            
        # Check packet loss
        if metrics['packet_loss_rate'] > self.thresholds['packet_loss_critical']:
            self._add_issue('critical', 'Severe packet loss detected', {
                'loss_rate': metrics['packet_loss_rate'],
                'threshold': self.thresholds['packet_loss_critical']
            })
        elif metrics['packet_loss_rate'] > self.thresholds['packet_loss_warning']:
            self._add_issue('warning', 'Packet loss detected', {
                'loss_rate': metrics['packet_loss_rate'],
                'threshold': self.thresholds['packet_loss_warning']
            })
            
        # Check retransmission rate
        if metrics['retransmission_rate'] > self.thresholds['retransmission_critical']:
            self._add_issue('critical', 'High retransmission rate detected', {
                'retrans_rate': metrics['retransmission_rate'],
                'threshold': self.thresholds['retransmission_critical']
            })
        elif metrics['retransmission_rate'] > self.thresholds['retransmission_warning']:
            self._add_issue('warning', 'Elevated retransmission rate', {
                'retrans_rate': metrics['retransmission_rate'],
                'threshold': self.thresholds['retransmission_warning']
            })
            
        # Check window size
        if metrics['window_size']['avg'] < self.thresholds['window_size_min']:
            self._add_issue('warning', 'Suboptimal window size', {
                'avg_window': metrics['window_size']['avg'],
                'recommended': self.thresholds['window_size_min']
            })
            
        return self.issues
        
    def analyze_protocol(self, protocol_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze protocol information for issues."""
        # Check security settings
        if protocol_info['security'].get('encryption', {}).get('value') != 'enabled':
            self._add_issue('warning', 'Encryption not enabled', {
                'protocol': protocol_info['protocol']['type'],
                'recommendation': 'Enable encryption for better security'
            })
            
        # Check protocol version
        if protocol_info['protocol']['type'] == 'SMB':
            version = protocol_info['protocol']['version']
            if version and version.startswith('1'):
                self._add_issue('warning', 'Legacy SMB version detected', {
                    'version': version,
                    'recommendation': 'Upgrade to SMB3 for better performance and security'
                })
                
        return self.issues
        
    def _add_issue(self, severity: str, message: str, details: Dict[str, Any]):
        """Add an issue to the list."""
        self.issues.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'severity': severity,
            'message': message,
            'details': details
        })
        
    def get_issues(self) -> List[Dict[str, Any]]:
        """Get all detected issues."""
        return self.issues
        
    def reset(self):
        """Reset the issue detector."""
        self.issues = []