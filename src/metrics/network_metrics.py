"""Network metrics collection and analysis."""

import statistics
import os
import threading
from datetime import datetime, timezone
from scapy.all import sniff, wrpcap
from scapy.layers.inet import IP, TCP
from contextlib import contextmanager
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

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
        self._capture = None
        self._capture_thread = None
        self._stop_capture = threading.Event()
        self._capture_file = None
        
    @contextmanager
    def capture_packets(self, interface=None, filter_str=None, timeout=None):
        """Start packet capture with proper resource cleanup.
        
        Args:
            interface (str): Network interface to capture on. None for default.
            filter_str (str): BPF filter string for capture. None for all packets.
            timeout (int): Capture timeout in seconds. None for no timeout.
            
        Yields:
            bool: True if capture started successfully, False otherwise.
        """
        try:
            # Set up capture file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self._capture_file = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'captures',
                f'capture_{timestamp}.pcap'
            )
            os.makedirs(os.path.dirname(self._capture_file), exist_ok=True)
            
            # Start capture in background thread
            self._stop_capture.clear()
            self._capture_thread = threading.Thread(
                target=self._capture_packets,
                args=(interface, filter_str, timeout)
            )
            self._capture_thread.start()
            logger.info(f"Started packet capture on {interface or 'default interface'}")
            
            yield True
            
        except Exception as e:
            logger.error(f"Failed to start packet capture: {e}")
            yield False
            
        finally:
            # Cleanup
            self.stop_capture()
            
    def _capture_packets(self, interface, filter_str, timeout):
        """Background packet capture function."""
        try:
            self._capture = sniff(
                iface=interface,
                filter=filter_str,
                timeout=timeout,
                stop_filter=lambda _: self._stop_capture.is_set(),
                prn=self._process_packet,
                store=False
            )
        except Exception as e:
            logger.error(f"Error during packet capture: {e}")
            
    def _process_packet(self, packet):
        """Process a captured packet."""
        try:
            self.increment_total_packets()
            
            if IP in packet and TCP in packet:
                # Get packet size
                self.add_packet_size(len(packet))
                
                # Get window size
                if packet[TCP].window:
                    self.add_window_size(packet[TCP].window)
                    
                # Check for retransmission
                if packet[TCP].flags.R:
                    self.increment_retransmissions()
                    
                # Estimate RTT from TCP timestamps if available
                if hasattr(packet[TCP], 'options'):
                    for opt_name, opt_value in packet[TCP].options:
                        if opt_name == 'Timestamp':
                            self.add_rtt_sample(opt_value[1] - opt_value[0])
                            
        except Exception as e:
            logger.error(f"Error processing packet: {e}")
            
    def stop_capture(self):
        """Stop packet capture and cleanup resources."""
        if self._capture_thread and self._capture_thread.is_alive():
            self._stop_capture.set()
            self._capture_thread.join(timeout=5)
            
            if self._capture_file and self._capture:
                try:
                    wrpcap(self._capture_file, self._capture)
                    logger.info(f"Saved capture to {self._capture_file}")
                except Exception as e:
                    logger.error(f"Failed to save capture file: {e}")
            
            self._capture = None
            self._capture_thread = None
            self._capture_file = None
            
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
