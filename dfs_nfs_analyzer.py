import os
import sys
import subprocess
import logging
import json
from datetime import datetime
try:
    import pyshark
    WIRESHARK_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    print("⚠️ Warning: pyshark/Wireshark not available. Some features will be limited.")
    print("Please install Wireshark from: https://www.wireshark.org/download.html")
    WIRESHARK_AVAILABLE = False
import socket
import winreg
import psutil
from scapy.all import *
import re
import emoji
import requests
from colorama import init, Fore, Style
from collections import defaultdict
import statistics
import openai
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from datetime import datetime, timezone, timedelta
import getpass
import platform
import time
import importlib.metadata
from dotenv import load_dotenv

init()  # Initialize colorama

class NetworkMetrics:
    def __init__(self):
        self.rtt_samples = []
        self.packet_sizes = []
        self.retransmissions = 0
        self.window_sizes = []
        self.packet_loss_count = 0
        self.total_packets = 0

    def add_rtt_sample(self, rtt):
        self.rtt_samples.append(rtt)
        
    def add_packet_size(self, size):
        self.packet_sizes.append(size)
        
    def increment_retransmissions(self):
        self.retransmissions += 1
        
    def add_window_size(self, size):
        self.window_sizes.append(size)
        
    def measure_latency(self, target_path):
        """Measure network latency to the target"""
        try:
            start_time = time.time()
            # Use net use to test connection
            if platform.system() == "Windows":
                subprocess.run(['net', 'use', target_path], capture_output=True, check=True)
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            self.rtt_samples.append(latency)
            return latency
        except Exception as e:
            logging.error(f"Error measuring latency: {str(e)}")
            return -1

    def measure_throughput(self, target_path):
        """Measure network throughput to the target"""
        try:
            # Create a test file
            test_size = 1024 * 1024  # 1MB
            test_file = os.path.join(os.path.dirname(target_path), "throughput_test.tmp")
            
            # Write test data
            start_time = time.time()
            with open(test_file, 'wb') as f:
                f.write(b'0' * test_size)
            end_time = time.time()
            
            # Clean up
            try:
                os.remove(test_file)
            except:
                pass
            
            # Calculate throughput in bits per second
            duration = end_time - start_time
            throughput = (test_size * 8) / duration if duration > 0 else 0
            return throughput
        except Exception as e:
            logging.error(f"Error measuring throughput: {str(e)}")
            return -1

    def calculate_packet_loss(self):
        """Calculate packet loss percentage"""
        if self.total_packets == 0:
            return 0
        return (self.packet_loss_count / self.total_packets) * 100 if self.total_packets > 0 else 0

    def update_metrics(self, packet):
        """Update metrics based on packet information"""
        self.total_packets += 1
        
        # Extract packet size
        if hasattr(packet, 'length'):
            self.packet_sizes.append(int(packet.length))
        
        # Check for retransmissions (TCP packets)
        if hasattr(packet, 'tcp'):
            if hasattr(packet.tcp, 'flags_reset') and packet.tcp.flags_reset == '1':
                self.retransmissions += 1
            if hasattr(packet.tcp, 'window_size'):
                self.window_sizes.append(int(packet.tcp.window_size))
        
        # Check for packet loss indicators
        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'analysis_retransmission'):
            self.packet_loss_count += 1

    def get_statistics(self):
        """Get current network statistics"""
        return {
            "avg_latency": sum(self.rtt_samples) / len(self.rtt_samples) if self.rtt_samples else 0,
            "packet_loss_percent": self.calculate_packet_loss(),
            "retransmissions": self.retransmissions,
            "avg_window_size": sum(self.window_sizes) / len(self.window_sizes) if self.window_sizes else 0,
            "avg_packet_size": sum(self.packet_sizes) / len(self.packet_sizes) if self.packet_sizes else 0
        }

class IssueDetector:
    def __init__(self):
        self.issues = []
        self.thresholds = {
            'high_latency': 200,  # ms
            'packet_loss': 5,     # percentage
            'bandwidth_util': 80,  # percentage
            'retransmission': 10, # percentage
            'window_size_min': 8192, # bytes
            'mtu_min': 1400,      # bytes
        }
        
    def check_network_health(self, metrics, network_info):
        """Analyze network health and detect issues"""
        self._check_latency(metrics.rtt_samples)
        self._check_packet_loss(metrics.retransmissions, len(metrics.packet_sizes))
        self._check_window_sizes(metrics.window_sizes)
        self._check_mtu_configuration(network_info)
        self._check_dns_resolution(network_info)
        self._check_routing(network_info)
        return self.issues
        
    def _check_latency(self, rtt_samples):
        if not rtt_samples:
            return
            
        avg_rtt = sum(rtt_samples) / len(rtt_samples)
        if avg_rtt > self.thresholds['high_latency']:
            self.issues.append({
                'type': 'performance',
                'severity': 'high',
                'issue': 'High network latency detected',
                'details': f'Average RTT: {avg_rtt:.2f}ms exceeds threshold of {self.thresholds["high_latency"]}ms',
                'suggestions': [
                    'Check for network congestion',
                    'Verify QoS settings',
                    'Consider using a closer file server',
                    'Review network routing configuration'
                ]
            })
            
    def _check_packet_loss(self, retransmissions, total_packets):
        if total_packets == 0:
            return
            
        loss_rate = (retransmissions / total_packets) * 100
        if loss_rate > self.thresholds['packet_loss']:
            self.issues.append({
                'type': 'reliability',
                'severity': 'high',
                'issue': 'High packet loss detected',
                'details': f'Packet loss rate: {loss_rate:.2f}% exceeds threshold of {self.thresholds["packet_loss"]}%',
                'suggestions': [
                    'Check for network interference',
                    'Verify network cable quality',
                    'Review network driver settings',
                    'Consider network equipment upgrade'
                ]
            })
            
    def _check_window_sizes(self, window_sizes):
        if not window_sizes:
            return
            
        avg_window = sum(window_sizes) / len(window_sizes)
        if avg_window < self.thresholds['window_size_min']:
            self.issues.append({
                'type': 'performance',
                'severity': 'medium',
                'issue': 'Suboptimal TCP window size',
                'details': f'Average window size: {avg_window:.0f} bytes is below recommended {self.thresholds["window_size_min"]} bytes',
                'suggestions': [
                    'Increase TCP window size in registry',
                    'Enable window scaling',
                    'Review TCP autotuning settings',
                    'Check for application-level window size limitations'
                ]
            })
            
    def _check_mtu_configuration(self, network_info):
        for interface, stats in network_info.get('interface_stats', {}).items():
            mtu = stats.get('mtu', 0)
            if mtu < self.thresholds['mtu_min']:
                self.issues.append({
                    'type': 'configuration',
                    'severity': 'medium',
                    'issue': f'Suboptimal MTU on interface {interface}',
                    'details': f'MTU size: {mtu} bytes is below recommended {self.thresholds["mtu_min"]} bytes',
                    'suggestions': [
                        'Increase MTU size if network supports it',
                        'Enable jumbo frames if available',
                        'Review network adapter settings',
                        'Check switch/router MTU configuration'
                    ]
                })
                
    def _check_dns_resolution(self, network_info):
        dns_info = network_info.get('dns_resolution', {})
        if not dns_info.get('local_hostname'):
            self.issues.append({
                'type': 'configuration',
                'severity': 'high',
                'issue': 'DNS resolution issues detected',
                'details': 'Unable to resolve local hostname',
                'suggestions': [
                    'Verify DNS server configuration',
                    'Check local hosts file',
                    'Review DNS client settings',
                    'Ensure DNS service is running'
                ]
            })
            
    def _check_routing(self, network_info):
        routing = network_info.get('routing_info', {}).get('route_table', '')
        if not routing or 'error' in routing.lower():
            self.issues.append({
                'type': 'configuration',
                'severity': 'high',
                'issue': 'Routing configuration issues detected',
                'details': 'Unable to retrieve or invalid routing information',
                'suggestions': [
                    'Verify network route configuration',
                    'Check default gateway settings',
                    'Review network interface bindings',
                    'Ensure routing service is running'
                ]
            })

class PerformanceOptimizer:
    def __init__(self):
        self.recommendations = []
        
    def analyze_performance(self, metrics, network_info):
        """Generate performance optimization recommendations"""
        self._analyze_network_usage(metrics)
        self._analyze_configuration(network_info)
        self._analyze_protocol_efficiency(metrics)
        return self.recommendations
        
    def _analyze_network_usage(self, metrics):
        if not metrics.rtt_samples:
            return
            
        # Analyze RTT patterns
        avg_rtt = sum(metrics.rtt_samples) / len(metrics.rtt_samples)
        rtt_variance = statistics.variance(metrics.rtt_samples) if len(metrics.rtt_samples) > 1 else 0
        
        if rtt_variance > avg_rtt * 0.5:
            self.recommendations.append({
                'category': 'network_stability',
                'priority': 'high',
                'recommendation': 'High RTT variance detected',
                'details': 'Network latency is unstable',
                'actions': [
                    'Implement QoS policies',
                    'Review network prioritization',
                    'Consider dedicated network path',
                    'Monitor for network congestion patterns'
                ]
            })
            
    def _analyze_configuration(self, network_info):
        for interface, stats in network_info.get('interface_stats', {}).items():
            if not stats.get('speed'):
                continue
                
            if stats['speed'] < 1000:  # Less than 1 Gbps
                self.recommendations.append({
                    'category': 'hardware',
                    'priority': 'medium',
                    'recommendation': f'Slow network interface detected: {interface}',
                    'details': f'Network speed: {stats["speed"]} Mbps',
                    'actions': [
                        'Upgrade network interface to Gigabit or better',
                        'Check cable category rating',
                        'Verify switch port speed',
                        'Review network adapter settings'
                    ]
                })
                
    def _analyze_protocol_efficiency(self, metrics):
        if not metrics.packet_sizes:
            return
            
        avg_packet_size = sum(metrics.packet_sizes) / len(metrics.packet_sizes)
        if avg_packet_size < 1000:  # Small packet sizes
            self.recommendations.append({
                'category': 'protocol_optimization',
                'priority': 'medium',
                'recommendation': 'Suboptimal packet sizes detected',
                'details': f'Average packet size: {avg_packet_size:.0f} bytes',
                'actions': [
                    'Enable packet coalescing',
                    'Review application write patterns',
                    'Adjust TCP_NODELAY settings',
                    'Consider implementing write buffering'
                ]
            })

class MLAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        self.scaler = StandardScaler()
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.historical_data = []
        
    def analyze_anomalies(self, metrics):
        """Detect anomalies using Isolation Forest with rate limit handling"""
        try:
            if not metrics or len(metrics) < 10:
                return []
                
            # Basic anomaly detection without API if rate limited
            if not self.api_key or getattr(self, '_rate_limited', False):
                return self._basic_anomaly_detection(metrics)
                
            try:
                return super().analyze_anomalies(metrics)
            except openai.error.RateLimitError:
                self._rate_limited = True
                self.logger.warning("OpenAI rate limit reached, falling back to basic analysis")
                return self._basic_anomaly_detection(metrics)
                
        except Exception as e:
            self.logger.error(f"Error in anomaly detection: {str(e)}")
            return []
            
    def _basic_anomaly_detection(self, metrics):
        """Basic anomaly detection without using OpenAI API"""
        try:
            anomalies = []
            
            # Calculate basic statistics
            latencies = [m.get('latency', 0) for m in metrics if m.get('latency')]
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                max_latency = max(latencies)
                
                # Flag high latencies
                if max_latency > avg_latency * 3:  # 3x average is suspicious
                    anomalies.append({
                        'type': 'high_latency',
                        'severity': 'medium',
                        'details': f'Latency spike detected: {max_latency:.2f}ms (avg: {avg_latency:.2f}ms)'
                    })
            
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Error in basic anomaly detection: {str(e)}")
            return []
        
    def predict_performance(self, metrics, timeframe_minutes=30):
        """Predict performance trends using OpenAI"""
        if not metrics.rtt_samples:
            return []
            
        # Prepare historical data
        current_stats = self._get_current_stats(metrics)
        self.historical_data.append(current_stats)
        
        # Keep only recent data
        self.historical_data = self._filter_recent_data(timeframe_minutes)
        
        # Generate prediction using OpenAI
        try:
            prediction = self._generate_ai_prediction()
            return prediction
        except Exception as e:
            return [{"error": f"AI prediction failed: {str(e)}"}]
            
    def _format_anomalies(self, df, anomaly_indices):
        """Format detected anomalies"""
        anomalies = []
        for idx in anomaly_indices:
            anomaly = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'type': 'anomaly',
                'metrics': {
                    'rtt': float(df.iloc[idx]['rtt']),
                    'packet_size': float(df.iloc[idx]['packet_size']),
                    'window_size': float(df.iloc[idx]['window_size'])
                },
                'severity': self._calculate_anomaly_severity(df.iloc[idx])
            }
            anomalies.append(anomaly)
        return anomalies
        
    def _calculate_anomaly_severity(self, row):
        """Calculate anomaly severity based on deviation from mean"""
        deviations = abs((row - row.mean()) / row.std())
        max_deviation = deviations.max()
        
        if max_deviation > 3:
            return 'high'
        elif max_deviation > 2:
            return 'medium'
        return 'low'
        
    def _get_current_stats(self, metrics):
        """Get current performance statistics"""
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'avg_rtt': np.mean(metrics.rtt_samples) if metrics.rtt_samples else 0,
            'avg_packet_size': np.mean(metrics.packet_sizes) if metrics.packet_sizes else 0,
            'retransmissions': metrics.retransmissions,
            'avg_window_size': np.mean(metrics.window_sizes) if metrics.window_sizes else 0
        }
        
    def _filter_recent_data(self, timeframe_minutes):
        """Keep only recent data within timeframe"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=timeframe_minutes)
        return [d for d in self.historical_data if d['timestamp'] > cutoff_time]
        
    def _generate_ai_prediction(self):
        """Generate performance predictions using OpenAI"""
        if not self.historical_data:
            return []
            
        # Prepare trend data
        trends = self._calculate_trends()
        
        # Create prompt for OpenAI
        prompt = f"""Analyze the following network performance trends and predict likely issues and recommendations:
Performance Trends:
- RTT: {trends['rtt_trend']}% change
- Packet Size: {trends['packet_size_trend']}% change
- Retransmissions: {trends['retransmission_trend']}% change
- Window Size: {trends['window_size_trend']}% change

Based on these trends, what are the likely performance issues and recommended actions?
Format the response as a JSON array with 'prediction' and 'recommendations' fields."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a network performance analysis expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse and format the response
            prediction = response.choices[0].message.content
            return self._format_ai_prediction(prediction)
        except Exception as e:
            return [{"error": f"AI prediction failed: {str(e)}"}]
            
    def _calculate_trends(self):
        """Calculate trends from historical data"""
        if len(self.historical_data) < 2:
            return {
                'rtt_trend': 0,
                'packet_size_trend': 0,
                'retransmission_trend': 0,
                'window_size_trend': 0
            }
            
        first = self.historical_data[0]
        last = self.historical_data[-1]
        
        def calculate_percentage_change(old, new):
            if old == 0:
                return 0
            return ((new - old) / old) * 100
            
        return {
            'rtt_trend': calculate_percentage_change(first['avg_rtt'], last['avg_rtt']),
            'packet_size_trend': calculate_percentage_change(first['avg_packet_size'], last['avg_packet_size']),
            'retransmission_trend': calculate_percentage_change(first['retransmissions'], last['retransmissions']),
            'window_size_trend': calculate_percentage_change(first['avg_window_size'], last['avg_window_size'])
        }
        
    def _format_ai_prediction(self, prediction_text):
        """Format AI prediction response"""
        try:
            prediction_data = json.loads(prediction_text)
            return [{
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'type': 'ai_prediction',
                'prediction': prediction_data.get('prediction', ''),
                'recommendations': prediction_data.get('recommendations', [])
            }]
        except json.JSONDecodeError:
            return [{
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'type': 'ai_prediction',
                'prediction': prediction_text,
                'recommendations': []
            }]

class ProtocolInfo:
    def __init__(self):
        self.protocol_version = None
        self.backend_hosts = set()
        self.namespace_info = {}
        self.negotiated_features = {}
        self.library_versions = self._get_library_versions()

    def _get_library_versions(self):
        """Get versions of key libraries in use"""
        versions = {}
        try:
            versions['pyshark'] = importlib.metadata.version('pyshark')
            versions['scapy'] = importlib.metadata.version('scapy')
            versions['pandas'] = importlib.metadata.version('pandas')
        except Exception:
            pass
        return versions

    def _get_wireshark_version(self):
        """Get Wireshark version"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['tshark', '--version'], capture_output=True, text=True)
            else:  # Linux/Mac
                result = subprocess.run(['tshark', '--version'], capture_output=True, text=True)
            if result.stdout:
                version_match = re.search(r'TShark .*?(\d+\.\d+\.\d+)', result.stdout)
                if version_match:
                    return version_match.group(1)
        except Exception as e:
            logging.warning(f"Could not determine Wireshark version: {e}")
        return "Unknown"

    def update_from_packet(self, packet):
        """Update protocol information from packet"""
        try:
            # Extract SMB/NFS version information
            if hasattr(packet, 'smb2'):
                self.protocol_version = f"SMB {packet.smb2.dialect}"
                if hasattr(packet.smb2, 'server_component'):
                    self.backend_hosts.add(packet.smb2.server_component)
            elif hasattr(packet, 'smb'):
                self.protocol_version = "SMB1"
            elif hasattr(packet, 'nfs'):
                self.protocol_version = f"NFS v{packet.nfs.version}"

            # Extract namespace information
            if hasattr(packet, 'smb2') and hasattr(packet.smb2, 'tree'):
                share_path = packet.smb2.tree
                if share_path not in self.namespace_info:
                    self.namespace_info[share_path] = {
                        'first_seen': datetime.now(timezone.utc).isoformat(),
                        'access_count': 0
                    }
                self.namespace_info[share_path]['access_count'] += 1

            # Extract negotiated features
            if hasattr(packet, 'smb2') and hasattr(packet.smb2, 'capabilities'):
                self.negotiated_features['capabilities'] = packet.smb2.capabilities
            if hasattr(packet, 'smb2') and hasattr(packet.smb2, 'security_mode'):
                self.negotiated_features['security_mode'] = packet.smb2.security_mode

        except Exception as e:
            logging.error(f"Error updating protocol info: {e}")

    def get_info(self):
        """Get current protocol information"""
        return {
            "protocol_version": self.protocol_version,
            "backend_hosts": list(self.backend_hosts),
            "namespace_info": self.namespace_info,
            "negotiated_features": self.negotiated_features,
            "library_versions": self.library_versions
        }

class ShareAnalyzer:
    def __init__(self, share_path, username, debug_level=0, domain=None, openai_key=None):
        self.share_path = share_path
        # Convert synology to synology-01 in share path if needed
        if '\\\\synology\\' in self.share_path:
            self.share_path = self.share_path.replace('\\\\synology\\', '\\\\synology-01\\')
        self.username = username
        self.domain = domain
        self.debug_level = debug_level
        self.openai_key = openai_key
        self.platform_info = get_platform_info()
        
        # Set Wireshark paths
        self.wireshark_path = r"C:\Program Files\Wireshark"
        os.environ["WIRESHARK_PATH"] = self.wireshark_path
        os.environ["PATH"] = f"{self.wireshark_path};{os.environ.get('PATH', '')}"
        
        # Download manuf file if missing
        manuf_path = os.path.join(self.wireshark_path, 'manuf')
        if not os.path.exists(manuf_path):
            try:
                print("Downloading Wireshark manufacturer database...")
                url = 'https://gitlab.com/wireshark/wireshark/-/raw/master/manuf'
                response = requests.get(url)
                if response.status_code == 200:
                    os.makedirs(os.path.dirname(manuf_path), exist_ok=True)
                    with open(manuf_path, 'wb') as f:
                        f.write(response.content)
                    print("Successfully downloaded manufacturer database")
            except Exception as e:
                print(f"Warning: Could not download manufacturer database: {e}")
        
        # Initialize capture state
        self.capture = None
        self.is_capturing = False
        self._shutdown_requested = False
        self._connected_share = False
        self._authenticated = False
        
        self.metrics = NetworkMetrics()
        self.protocol_info = ProtocolInfo()
        self.issue_detector = IssueDetector()
        self.performance_optimizer = PerformanceOptimizer()
        
        # Initialize ML analyzer if API key provided
        self.ml_analyzer = None
        if openai_key:
            try:
                self.ml_analyzer = MLAnalyzer(openai_key)
            except Exception as e:
                self.logger.warning(f"Failed to initialize ML analyzer: {str(e)}")
        
        self.error_counts = defaultdict(int)
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        self.logs_dir = os.path.join(self.output_dir, "logs")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Set up log files with ISO 8601 timestamp
        timestamp_utc = datetime.now(timezone.utc)
        filename_timestamp = timestamp_utc.strftime("%Y-%m-%dT%H-%M-%S")
        self.output_file = os.path.join(self.output_dir, f"analysis_{filename_timestamp}.log")
        self.debug_log = os.path.join(self.logs_dir, f"debug_analysis_{filename_timestamp}.log")
        
        self.logger = self._setup_logging()
            
    def _setup_logging(self):
        """Set up logging with ISO 8601 timestamps"""
        logger = logging.getLogger('ShareAnalyzer')
        logger.setLevel(logging.DEBUG)
        
        # Remove any existing handlers
        logger.handlers = []
        
        # Create formatter with ISO 8601 timestamps
        formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03dZ - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        
        # File handler for debug log
        debug_handler = logging.FileHandler(self.debug_log)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)
        
        # Console handler for user feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Add timezone info to timestamps
        def custom_time(*args):
            utc_dt = datetime.now(timezone.utc)
            return utc_dt.timetuple()
        
        logging.Formatter.converter = custom_time
        
        return logger

    def authenticate(self, password):
        """Authenticate with the share using provided credentials"""
        if self._authenticated:
            return True
        
        try:
            # For Windows, use net use command
            if self.platform_info['is_windows']:
                # Extract hostname from share path
                hostname = self.share_path.split('\\')[2]
                
                # First check if share exists
                ping_cmd = ['ping', '-n', '1', '-w', '1000', hostname]
                try:
                    self.logger.info(f"Checking connectivity to {hostname}...")
                    result = subprocess.run(ping_cmd, capture_output=True, check=False)
                    if result.returncode != 0:
                        self.logger.error(f"Cannot reach host {hostname}. Please check if the server is online.")
                        return False
                    self.logger.info(f"Successfully pinged {hostname}")
                except Exception as e:
                    self.logger.error(f"Error checking host availability: {str(e)}")
                    return False
            
                # Check if already connected with correct credentials
                check_cmd = ['net', 'use', self.share_path]
                try:
                    result = subprocess.run(check_cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        # Check if the connection is using the correct username
                        if self.username.lower() in result.stdout.lower():
                            self.logger.info(f"Already connected to share {self.share_path}")
                            self._connected_share = True
                            self._authenticated = True
                            return True
                except:
                    pass
            
                # Not connected or wrong credentials, try to connect
                self.logger.info(f"Attempting to connect to {self.share_path}...")
            
                # Only use domain if it's actually set to something
                if self.domain and self.domain.strip():
                    full_username = f"{self.domain}\\{self.username}"
                else:
                    full_username = self.username
            
                # First try to disconnect if already connected
                try:
                    subprocess.run(['net', 'use', self.share_path, '/delete'], 
                                capture_output=True, check=False)
                except:
                    pass
            
                connect_cmd = [
                    'net', 'use', self.share_path,
                    f'/USER:{full_username}', password,
                    '/PERSISTENT:YES'  # Make the connection persistent
                ]
                try:
                    result = subprocess.run(connect_cmd, capture_output=True, check=False)
                    if result.returncode == 0:
                        self.logger.info(f"Successfully connected to share {self.share_path}")
                        self._connected_share = True
                        self._authenticated = True
                        return True
                    else:
                        error_msg = result.stderr.decode() if result.stderr else str(result.returncode)
                        self.logger.error(f"Failed to connect to share: {error_msg}")
                        return False
                except Exception as e:
                    self.logger.error(f"Error during share connection: {str(e)}")
                    return False
                
        # For Unix-like systems, try mount command
        else:
            # Implementation for Unix mount...
            pass
            
    except Exception as e:
        self.logger.error(f"Authentication error: {str(e)}")
        return False

    def analyze_share(self):
        """Analyze the network share"""
        try:
            # Get share type and protocol info
            share_type = self.analyze_share_type(self.share_path)
            self.logger.debug(f"Share type: {share_type}")
            
            # Get security info
            security_info = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "encryption": "enabled",  # Assuming SMB3
                "auth_method": "kerberos"  # Default for domain auth
            }
            self.logger.info(f"SECURITY: {json.dumps(security_info)}")
            
            # Write analysis results
            analysis_data = {
                "share_info": {
                    "path": self.share_path,
                    "type": share_type,
                    "security": security_info
                }
            }
            
            self._write_analysis(analysis_data)
            
        except Exception as e:
            self.logger.error(f"Error during share analysis: {str(e)}")
            raise

    def cleanup(self):
        """Clean up resources before exit"""
        if self.is_capturing and self.capture:
            try:
                self.capture.close()
            except:
                pass
        
        if self._connected_share and not '/PERSISTENT:YES' in self.platform_info['connect_cmd']:
            try:
                subprocess.run(self.platform_info['disconnect_cmd'].format(share_path=self.share_path), shell=True)
            except Exception as e:
                self.logger.warning(f"Failed to disconnect from share: {e}")

def get_platform_info():
    """Get platform-specific information and commands"""
    platform_info = {}
    
    if platform.system() == 'Windows':
        platform_info['connect_cmd'] = 'net use "{share_path}" /user:{domain}\\{username} {password} /PERSISTENT:YES'
        platform_info['disconnect_cmd'] = 'net use "{share_path}" /delete'
        platform_info['path_sep'] = '\\'
    else:
        platform_info['connect_cmd'] = 'mount -t cifs "{share_path}" /mnt/share -o username={username},password={password},domain={domain}'
        platform_info['disconnect_cmd'] = 'umount "{share_path}"'
        platform_info['path_sep'] = '/'
            
    return platform_info

def main():
    try:
        # Load defaults from .env first
        load_dotenv()
        default_share = os.getenv('SHARE_PATH')
        default_username = os.getenv('USERNAME')
        default_debug = os.getenv('DEBUG_LEVEL', '0')
        default_domain = os.getenv('DOMAIN', '').strip()  # Strip whitespace
        default_openai = os.getenv('OPENAI_KEY')
        
        # Use command line args if provided, otherwise use .env defaults
        share_path = sys.argv[1] if len(sys.argv) > 1 else default_share
        username = sys.argv[2] if len(sys.argv) > 2 else default_username
        
        try:
            debug_level = int(sys.argv[3]) if len(sys.argv) > 3 else int(default_debug.split('#')[0].strip())
        except:
            debug_level = 0
            
        domain = sys.argv[4] if len(sys.argv) > 4 else default_domain
        openai_key = sys.argv[5] if len(sys.argv) > 5 else default_openai
            
        # Validate required parameters
        if not share_path or not username:
            print("Error: Share path and username are required. Provide them either in .env file or as command line arguments.")
            print("\nUsage:")
            print("1. Configure in .env file:")
            print("   SHARE_PATH=\\\\server\\share")
            print("   USERNAME=user")
            print("   DOMAIN=domain        (optional)")
            print("   DEBUG_LEVEL=0        (optional, default: 0)")
            print("   OPENAI_KEY=key       (optional)")
            print("\n2. Or provide as command line arguments:")
            print("   python dfs_nfs_analyzer.py [share_path] [username] [debug_level] [domain] [openai_key]")
            sys.exit(1)
            
        analyzer = ShareAnalyzer(share_path, username, debug_level, domain, openai_key)
        
        # Get password securely (only once)
        password = getpass.getpass(f"Enter password for user {username}: ")
        
        # Authenticate and analyze
        if analyzer.authenticate(password):
            analyzer.analyze_share()
        else:
            print("Authentication failed. Please check credentials and try again.")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'analyzer' in locals():
            analyzer.cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
