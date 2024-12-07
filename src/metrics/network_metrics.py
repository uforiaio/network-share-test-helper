"""Network metrics collection and analysis."""

import statistics
import os
import threading
from datetime import datetime, timezone
import warnings
import subprocess

# Configure scapy to be quiet about warnings
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import sniff, wrpcap, conf
from scapy.layers.inet import IP, TCP
from contextlib import contextmanager
from ..utils.logging import setup_logger

# Disable scapy warnings
conf.verb = 0

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
        self._pcap_dir = None
        
    def set_output_dirs(self, pcap_dir):
        """Set output directories for captures.
        
        Args:
            pcap_dir (str): Directory to store pcap files
            
        Returns:
            bool: True if directory was set successfully, False otherwise
        """
        try:
            if not pcap_dir:
                logger.error("Invalid pcap directory: directory path is empty")
                return False
                
            logger.debug(f"Setting pcap directory to: {pcap_dir}")
            self._pcap_dir = pcap_dir
            os.makedirs(self._pcap_dir, exist_ok=True)
            
            # Verify directory exists and is writable
            if not os.path.exists(self._pcap_dir):
                logger.error(f"Failed to create pcap directory: {pcap_dir}")
                return False
            if not os.access(self._pcap_dir, os.W_OK):
                logger.error(f"Pcap directory is not writable: {pcap_dir}")
                return False
                
            # Set capture file path
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self._capture_file = os.path.join(self._pcap_dir, f'capture_{timestamp}.pcap')
            logger.debug(f"Set capture file path to: {self._capture_file}")
                
            return True
        except Exception as e:
            logger.error(f"Error setting pcap directory: {e}")
            return False
            
    def cleanup(self):
        """Clean up resources and stop packet capture."""
        try:
            self.stop_capture()
            self.reset()
            return True
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            return False
            
    def _capture_packets(self, interface, filter_str, timeout):
        """Background packet capture function."""
        try:
            # Get tshark path
            tshark_path = os.getenv('TSHARK_PATH', 'C:\\Program Files\\Wireshark\\tshark.exe')
            
            if not os.path.exists(tshark_path):
                raise RuntimeError(f"tshark not found at {tshark_path}")
            
            # Create output directory
            os.makedirs(os.path.dirname(self._capture_file), exist_ok=True)
            
            # Basic tshark command - simplified for reliability
            args = [
                tshark_path,
                '-i', '1',                    # Interface
                '-w', self._capture_file,     # Output file
                '-f', 'port 445 or port 139'  # SMB traffic
            ]
            
            logger.info(f"Starting tshark with command: {' '.join(args)}")
            
            # Run tshark directly
            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            
            self._capture = process
            
            # Check if process started successfully
            import time
            time.sleep(1)  # Give it a moment to start
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                error_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
                raise RuntimeError(f"tshark failed to start: {error_msg}")
            
            logger.info(f"tshark started with PID {process.pid}")
            
            # Wait for timeout
            time.sleep(timeout)
            
            # Stop capture
            logger.info("Stopping tshark capture...")
            if process.poll() is None:  # If still running
                process.terminate()
                process.wait(timeout=5)  # Wait up to 5 seconds
                
            if process.returncode and process.returncode != 0:
                stdout, stderr = process.communicate()
                error_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
                raise RuntimeError(f"tshark exited with code {process.returncode}: {error_msg}")
                
            logger.info("Packet capture completed successfully")
            
        except Exception as e:
            logger.error(f"Error during packet capture: {e}")
            raise
            
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
                    # wrpcap(self._capture_file, self._capture)
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
        """Reset all metrics but preserve output directory settings."""
        # Store output settings
        pcap_dir = self._pcap_dir
        capture_file = self._capture_file
        
        # Reset everything
        self.rtt_samples = []
        self.packet_sizes = []
        self.retransmissions = 0
        self.window_sizes = []
        self.packet_loss_count = 0
        self.total_packets = 0
        self._capture = None
        self._capture_thread = None
        self._stop_capture = threading.Event()
        
        # Restore output settings
        self._pcap_dir = pcap_dir
        self._capture_file = capture_file

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
            # Verify output directory is set
            if not self._pcap_dir:
                raise ValueError("Output directory not set. Cannot start capture.")
                
            # Set up capture file in session-specific directory
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self._capture_file = os.path.join(self._pcap_dir, f'capture_{timestamp}.pcap')
            logger.debug(f"Setting up packet capture to file: {self._capture_file}")
            
            # Start capture in background thread
            self._stop_capture.clear()
            self._capture_thread = threading.Thread(
                target=self._capture_packets,
                args=(interface, filter_str, timeout)
            )
            self._capture_thread.daemon = True  # Make thread daemon so it exits with main program
            self._capture_thread.start()
            logger.info(f"Started packet capture on {interface or 'default interface'}")
            
            yield True
            
        except Exception as e:
            logger.error(f"Failed to start packet capture: {e}")
            yield False
            
        finally:
            # Cleanup
            self.stop_capture()

    def collect_metrics(self, share_path, duration=60, capture_filter=None):
        """Collect network metrics for the specified share.
        
        Args:
            share_path (str): Path to the network share
            duration (int): Duration in seconds to capture traffic
            capture_filter (str, optional): Custom Wireshark capture filter
            
        Returns:
            dict: Collected network metrics
        """
        try:
            # Reset metrics before starting new collection
            self.reset()
            
            # Verify output directory is set
            if not self._pcap_dir:
                logger.error("Output directory not set. Cannot start capture.")
                return None
                
            # Set up capture filter for the share
            if not capture_filter:
                # Get IP address from share path
                share_parts = share_path.strip('\\').split('\\')
                if share_parts:
                    host = share_parts[0]
                    try:
                        import socket
                        ip = socket.gethostbyname(host)
                        capture_filter = f"host {ip}"
                    except Exception as e:
                        logger.warning(f"Could not resolve host {host}: {e}")
                        capture_filter = None
            
            # Start packet capture
            with self.capture_packets(filter_str=capture_filter, timeout=duration) as success:
                if not success:
                    logger.error("Failed to start packet capture")
                    return None
                    
                # Wait for capture to complete
                import time
                time.sleep(duration)
            
            # Return collected statistics
            return self.get_statistics()
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            return None
