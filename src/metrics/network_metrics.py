"""Network metrics collection and analysis."""

import statistics
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class NetworkMetrics:
    """Collects and analyzes network performance metrics."""
    
    def __init__(self):
        """Initialize network metrics collection."""
        self.rtt_samples = []
        self.packet_sizes = []
        self.retransmissions = 0
        self.window_sizes = []
        self.packet_loss_count = 0
        self.total_packets = 0
        
    def add_rtt_sample(self, rtt_ms):
        """Add a round-trip time sample."""
        if rtt_ms > 0:
            self.rtt_samples.append(rtt_ms)
            
    def add_packet_size(self, size_bytes):
        """Add a packet size sample."""
        if size_bytes > 0:
            self.packet_sizes.append(size_bytes)
            
    def increment_retransmissions(self):
        """Increment retransmission counter."""
        self.retransmissions += 1
        
    def add_window_size(self, size_bytes):
        """Add a window size sample."""
        if size_bytes > 0:
            self.window_sizes.append(size_bytes)
            
    def increment_packet_loss(self):
        """Increment packet loss counter."""
        self.packet_loss_count += 1
        
    def increment_total_packets(self):
        """Increment total packet counter."""
        self.total_packets += 1
        
    def get_statistics(self):
        """Calculate current network statistics."""
        stats = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rtt": {
                "min": min(self.rtt_samples) if self.rtt_samples else 0,
                "max": max(self.rtt_samples) if self.rtt_samples else 0,
                "avg": statistics.mean(self.rtt_samples) if self.rtt_samples else 0,
                "median": statistics.median(self.rtt_samples) if self.rtt_samples else 0
            },
            "packet_size": {
                "min": min(self.packet_sizes) if self.packet_sizes else 0,
                "max": max(self.packet_sizes) if self.packet_sizes else 0,
                "avg": statistics.mean(self.packet_sizes) if self.packet_sizes else 0
            },
            "window_size": {
                "min": min(self.window_sizes) if self.window_sizes else 0,
                "max": max(self.window_sizes) if self.window_sizes else 0,
                "avg": statistics.mean(self.window_sizes) if self.window_sizes else 0
            },
            "retransmission_rate": (
                self.retransmissions / self.total_packets * 100 
                if self.total_packets > 0 else 0
            ),
            "packet_loss_rate": (
                self.packet_loss_count / self.total_packets * 100
                if self.total_packets > 0 else 0
            ),
            "total_packets": self.total_packets
        }
        return stats
        
    def reset(self):
        """Reset all metrics."""
        self.__init__()
