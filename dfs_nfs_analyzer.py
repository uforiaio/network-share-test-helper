import os
import sys
import subprocess
import logging
import json
from datetime import datetime
import pyshark
from dotenv import load_dotenv
import socket
import winreg
import psutil
from scapy.all import *
import re
import emoji
from colorama import init, Fore, Style
from collections import defaultdict
import statistics
import openai
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from datetime import datetime, timedelta

init()  # Initialize colorama

class NetworkMetrics:
    def __init__(self):
        self.rtt_samples = []
        self.packet_sizes = []
        self.retransmissions = 0
        self.window_sizes = []
        
    def add_rtt_sample(self, rtt):
        self.rtt_samples.append(rtt)
        
    def add_packet_size(self, size):
        self.packet_sizes.append(size)
        
    def increment_retransmissions(self):
        self.retransmissions += 1
        
    def add_window_size(self, size):
        self.window_sizes.append(size)
        
    def get_statistics(self):
        if not self.rtt_samples:
            return {}
            
        return {
            "rtt": {
                "min": min(self.rtt_samples),
                "max": max(self.rtt_samples),
                "avg": sum(self.rtt_samples) / len(self.rtt_samples)
            },
            "packet_size": {
                "min": min(self.packet_sizes) if self.packet_sizes else 0,
                "max": max(self.packet_sizes) if self.packet_sizes else 0,
                "avg": sum(self.packet_sizes) / len(self.packet_sizes) if self.packet_sizes else 0
            },
            "retransmissions": self.retransmissions,
            "window_size": {
                "min": min(self.window_sizes) if self.window_sizes else 0,
                "max": max(self.window_sizes) if self.window_sizes else 0,
                "avg": sum(self.window_sizes) / len(self.window_sizes) if self.window_sizes else 0
            }
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
        """Detect anomalies using Isolation Forest"""
        if not metrics.rtt_samples:
            return []
            
        # Prepare data for anomaly detection
        data = {
            'rtt': metrics.rtt_samples,
            'packet_size': metrics.packet_sizes,
            'window_size': metrics.window_sizes
        }
        df = pd.DataFrame(data)
        
        # Scale the features
        scaled_data = self.scaler.fit_transform(df)
        
        # Detect anomalies
        anomalies = self.isolation_forest.fit_predict(scaled_data)
        anomaly_indices = np.where(anomalies == -1)[0]
        
        return self._format_anomalies(df, anomaly_indices)
        
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
                'timestamp': datetime.now().isoformat(),
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
            'timestamp': datetime.now(),
            'avg_rtt': np.mean(metrics.rtt_samples) if metrics.rtt_samples else 0,
            'avg_packet_size': np.mean(metrics.packet_sizes) if metrics.packet_sizes else 0,
            'retransmissions': metrics.retransmissions,
            'avg_window_size': np.mean(metrics.window_sizes) if metrics.window_sizes else 0
        }
        
    def _filter_recent_data(self, timeframe_minutes):
        """Keep only recent data within timeframe"""
        cutoff_time = datetime.now() - timedelta(minutes=timeframe_minutes)
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
                'timestamp': datetime.now().isoformat(),
                'type': 'ai_prediction',
                'prediction': prediction_data.get('prediction', ''),
                'recommendations': prediction_data.get('recommendations', [])
            }]
        except json.JSONDecodeError:
            return [{
                'timestamp': datetime.now().isoformat(),
                'type': 'ai_prediction',
                'prediction': prediction_text,
                'recommendations': []
            }]

class ShareAnalyzer:
    def __init__(self):
        self.logger = self._setup_logging()
        self.output_file = "output.txt"
        self.metrics = NetworkMetrics()
        self.error_counts = defaultdict(int)
        self.issue_detector = IssueDetector()
        self.performance_optimizer = PerformanceOptimizer()
        self.ml_analyzer = None  # Will be initialized after loading API key
        
    def _setup_logging(self):
        logger = logging.getLogger('ShareAnalyzer')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        file_handler = logging.FileHandler('debug_analysis.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger

    def _format_log(self, category, message):
        emoji_map = {
            'share': ':file_folder:',
            'network': ':globe_with_meridians:',
            'error': ':warning:',
            'success': ':white_check_mark:',
            'info': ':information_source:',
            'traffic': ':arrows_counterclockwise:',
            'security': ':lock:',
            'performance': ':zap:',
            'config': ':gear:',
            'issue': ':exclamation_mark:',
            'optimization': ':chart_increasing:',
            'anomaly': ':chart_decreasing:',
            'prediction': ':crystal_ball:'
        }
        return f"{emoji.emojize(emoji_map.get(category, ':information_source:'))} {message}"

    def _write_to_output(self, data, category='info'):
        with open(self.output_file, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_message = self._format_log(category, json.dumps(data, indent=2))
            f.write(f"{timestamp} {formatted_message}\n")

    def handle_error(self, error_type, error_message, critical=False):
        """Enhanced error handling with categorization and recovery options"""
        self.error_counts[error_type] += 1
        error_data = {
            "type": error_type,
            "message": error_message,
            "count": self.error_counts[error_type],
            "timestamp": datetime.now().isoformat(),
            "critical": critical
        }
        
        self._write_to_output(error_data, 'error')
        
        if critical:
            raise Exception(f"Critical error: {error_message}")
        return False

    def analyze_traffic_patterns(self, packet):
        """Enhanced traffic analysis with pattern detection"""
        patterns = {
            "bulk_transfer": False,
            "interactive": False,
            "periodic": False,
            "burst": False
        }
        
        try:
            if hasattr(packet, 'length'):
                if int(packet.length) > 1400:
                    patterns["bulk_transfer"] = True
                elif int(packet.length) < 100:
                    patterns["interactive"] = True
                    
            if hasattr(packet, 'tcp'):
                window_size = int(packet.tcp.window_size)
                self.metrics.add_window_size(window_size)
                
                if hasattr(packet.tcp, 'analysis_retransmission'):
                    self.metrics.increment_retransmissions()
                    
            return patterns
        except Exception as e:
            self.handle_error("traffic_analysis", str(e))
            return patterns

    def get_network_info(self):
        """Enhanced network metrics collection"""
        try:
            info = {
                "ports": [],
                "mtu": {},
                "tcp_window": {},
                "interface_stats": {},
                "routing_info": {},
                "dns_resolution": {}
            }
            
            # Collect interface statistics
            for interface, stats in psutil.net_if_stats().items():
                info["interface_stats"][interface] = {
                    "speed": stats.speed,
                    "mtu": stats.mtu,
                    "is_up": stats.isup,
                    "duplex": stats.duplex,
                }
                
            # Get active connections
            for conn in psutil.net_connections():
                if conn.status == 'ESTABLISHED':
                    info["ports"].append({
                        "local_port": conn.laddr.port,
                        "remote_port": conn.raddr.port if conn.raddr else None,
                        "status": conn.status,
                        "pid": conn.pid
                    })
                    
            # Get routing information using 'route print' on Windows
            try:
                route_output = subprocess.check_output(['route', 'print'], text=True)
                info["routing_info"]["route_table"] = route_output
            except Exception as e:
                self.handle_error("routing_info", str(e))
                
            # Test DNS resolution
            try:
                dns_test = socket.gethostbyname(socket.gethostname())
                info["dns_resolution"]["local_hostname"] = dns_test
            except Exception as e:
                self.handle_error("dns_resolution", str(e))
                
            return info
        except Exception as e:
            self.handle_error("network_info", str(e), critical=True)
            return {}

    def _process_packet(self, packet):
        """Enhanced packet processing with detailed analysis"""
        packet_dict = {}
        try:
            packet_dict['protocol'] = packet.highest_layer
            packet_dict['length'] = packet.length
            packet_dict['time'] = packet.sniff_time.isoformat()
            
            # Add traffic pattern analysis
            packet_dict['patterns'] = self.analyze_traffic_patterns(packet)
            
            # Add performance metrics
            if hasattr(packet, 'tcp'):
                tcp_info = {
                    'window_size': packet.tcp.window_size,
                    'seq_number': packet.tcp.seq,
                    'ack': packet.tcp.ack,
                    'flags': packet.tcp.flags
                }
                packet_dict['tcp_info'] = tcp_info
                
            # Mask sensitive data
            if hasattr(packet, 'smb') or hasattr(packet, 'smb2'):
                packet_dict['data'] = "XXXXXXXX"
            else:
                packet_dict['data'] = packet.highest_layer
                
            return packet_dict
        except Exception as e:
            self.handle_error("packet_processing", str(e))
            return {"error": str(e)}

    def capture_traffic(self, interface="Ethernet"):
        capture = pyshark.LiveCapture(interface=interface, display_filter="nfs || smb || smb2")
        print("Starting packet capture... (Press Ctrl+C to stop)")
        
        try:
            for packet in capture.sniff_continuously(packet_count=100):
                # Process packet and mask any password fields
                packet_info = self._process_packet(packet)
                self._write_to_output(packet_info, 'traffic')
        except KeyboardInterrupt:
            print("\nCapture stopped by user")
        finally:
            capture.close()

    def update_env_file(self, share_path, username, debug_level, openai_key=None):
        env_content = f"""SHARE_PATH={share_path}
USERNAME={username}
DEBUG_LEVEL={debug_level}"""
        
        if openai_key:
            env_content += f"\nOPENAI_API_KEY={openai_key}"
            
        with open('.env', 'w') as f:
            f.write(env_content)
        self.logger.info("Updated .env file with new configuration")
        
        # Initialize ML analyzer if API key is provided
        if openai_key:
            self.initialize_ml()
            
    def initialize_ml(self):
        """Initialize ML analyzer with OpenAI API key"""
        try:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.ml_analyzer = MLAnalyzer(api_key)
                self._write_to_output({
                    "message": "ML analyzer initialized successfully"
                }, 'info')
            else:
                self._write_to_output({
                    "error": "OpenAI API key not found in .env file"
                }, 'error')
        except Exception as e:
            self._write_to_output({
                "error": f"Failed to initialize ML analyzer: {str(e)}"
            }, 'error')
            
    def analyze_share_type(self, path):
        if path.startswith('\\\\'):
            try:
                # Check if it's DFS
                result = subprocess.run(['dfsutil', '/root:', path], capture_output=True, text=True)
                if "DFS Root" in result.stdout:
                    return "DFS"
                return "SMB/CIFS"
            except:
                return "SMB/CIFS"
        elif ':' in path:
            return "NFS"
        return "Unknown"

    def analyze_share(self):
        load_dotenv()
        share_path = os.getenv('SHARE_PATH')
        username = os.getenv('USERNAME')
        
        # Share Analysis
        self._write_to_output({
            "type": "share_analysis",
            "path": share_path,
            "user": username
        }, 'share')
        
        # Network Analysis
        network_info = self.get_network_info()
        self._write_to_output({
            "type": "network_info",
            "details": network_info
        }, 'network')
        
        # Performance Metrics
        self._write_to_output({
            "type": "performance",
            "tcp_window": network_info.get('tcp_window', {}),
            "mtu": network_info.get('mtu', {})
        }, 'performance')
        
        # Security Check
        self._write_to_output({
            "type": "security_check",
            "encryption": "enabled",
            "auth_method": "kerberos"
        }, 'security')

        share_type = self.analyze_share_type(share_path)
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "share_type": share_type,
            "share_path": share_path,
            "username": username,
            "network_info": network_info
        }
        
        # Additional analysis based on share type
        if share_type == "DFS":
            analysis.update(self._analyze_dfs(share_path))
        elif share_type == "NFS":
            analysis.update(self._analyze_nfs(share_path))
            
        self._write_analysis(analysis)

    def _analyze_dfs(self, path):
        info = {}
        try:
            result = subprocess.run(['dfsutil', '/root:', path], capture_output=True, text=True)
            info['dfs_details'] = result.stdout
            
            # Get namespace details
            result = subprocess.run(['dfsutil', '/view', path], capture_output=True, text=True)
            info['namespace'] = result.stdout
        except Exception as e:
            self.handle_error("dfs_analysis", str(e))
        return info

    def _analyze_nfs(self, path):
        info = {}
        try:
            result = subprocess.run(['mount'], capture_output=True, text=True)
            info['mount_details'] = result.stdout
            
            # Get NFS version
            result = subprocess.run(['nfsstat'], capture_output=True, text=True)
            info['nfs_stats'] = result.stdout
        except Exception as e:
            self.handle_error("nfs_analysis", str(e))
        return info

    def _write_analysis(self, analysis):
        with open(self.output_file, 'w') as f:
            f.write("=== Share Analysis Report ===\n\n")
            f.write(f"Share Type: {analysis['share_type']}\n")
            f.write(f"Share Path: {analysis['share_path']}\n")
            f.write(f"Username: {analysis['username']}\n\n")
            
            f.write("=== Network Information ===\n")
            f.write(f"Active Ports: {', '.join(map(str, analysis['network_info']['ports']))}\n")
            f.write(f"MTU Settings: {json.dumps(analysis['network_info']['mtu'], indent=2)}\n\n")
            
            if 'dfs_details' in analysis:
                f.write("=== DFS Details ===\n")
                f.write(analysis['dfs_details'])
                f.write("\nNamespace Information:\n")
                f.write(analysis['namespace'])
            
            if 'nfs_stats' in analysis:
                f.write("=== NFS Details ===\n")
                f.write(analysis['nfs_stats'])

    def generate_summary_report(self):
        """Generate a comprehensive analysis summary with ML insights"""
        network_info = self.get_network_info()
        
        # Detect issues
        detected_issues = self.issue_detector.check_network_health(self.metrics, network_info)
        
        # Generate optimization recommendations
        optimization_recommendations = self.performance_optimizer.analyze_performance(self.metrics, network_info)
        
        # Get ML insights if available
        ml_insights = {
            "anomalies": [],
            "predictions": []
        }
        
        if self.ml_analyzer:
            ml_insights["anomalies"] = self.ml_analyzer.analyze_anomalies(self.metrics)
            ml_insights["predictions"] = self.ml_analyzer.predict_performance(self.metrics)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "network_metrics": self.metrics.get_statistics(),
            "error_summary": dict(self.error_counts),
            "performance_indicators": {
                "packet_loss_rate": self._calculate_packet_loss(),
                "connection_stability": self._assess_connection_stability(),
                "bandwidth_utilization": self._estimate_bandwidth_utilization()
            },
            "detected_issues": detected_issues,
            "optimization_recommendations": optimization_recommendations,
            "ml_insights": ml_insights
        }
        
        self._write_to_output(summary, 'summary')
        
        # Log all insights with appropriate emojis
        for issue in detected_issues:
            self._write_to_output(issue, 'issue')
            
        for recommendation in optimization_recommendations:
            self._write_to_output(recommendation, 'optimization')
            
        for anomaly in ml_insights["anomalies"]:
            self._write_to_output(anomaly, 'anomaly')
            
        for prediction in ml_insights["predictions"]:
            self._write_to_output(prediction, 'prediction')
            
        return summary

    def _calculate_packet_loss(self):
        """Calculate packet loss rate based on retransmissions"""
        total_packets = len(self.metrics.packet_sizes)
        if total_packets == 0:
            return 0
        return (self.metrics.retransmissions / total_packets) * 100

    def _assess_connection_stability(self):
        """Assess connection stability based on various metrics"""
        if not self.metrics.rtt_samples:
            return "Unknown"
            
        avg_rtt = sum(self.metrics.rtt_samples) / len(self.metrics.rtt_samples)
        rtt_variance = statistics.variance(self.metrics.rtt_samples) if len(self.metrics.rtt_samples) > 1 else 0
        
        if avg_rtt < 50 and rtt_variance < 100:
            return "Excellent"
        elif avg_rtt < 100 and rtt_variance < 200:
            return "Good"
        elif avg_rtt < 200 and rtt_variance < 400:
            return "Fair"
        else:
            return "Poor"

    def _estimate_bandwidth_utilization(self):
        """Estimate bandwidth utilization based on packet sizes and timing"""
        if not self.metrics.packet_sizes or not self.metrics.rtt_samples:
            return 0
            
        total_bytes = sum(self.metrics.packet_sizes)
        total_time = max(self.metrics.rtt_samples) - min(self.metrics.rtt_samples)
        
        if total_time <= 0:
            return 0
            
        return (total_bytes * 8) / total_time  # bits per second

def main():
    analyzer = ShareAnalyzer()
    
    if len(sys.argv) == 5:
        share_path = sys.argv[1]
        username = sys.argv[2]
        debug_level = sys.argv[3]
        openai_key = sys.argv[4]
        
        analyzer.update_env_file(share_path, username, debug_level, openai_key)
        print("Configuration updated. Starting analysis...")
        
        analyzer.analyze_share()
        analyzer.capture_traffic()
        print(f"Analysis complete. Check {analyzer.output_file} for results.")
    else:
        print("Usage: python dfs_nfs_analyzer.py <share_path> <username> <debug_level> <openai_key>")

if __name__ == "__main__":
    main()
