"""Main ShareAnalyzer class for DFS/NFS debugging."""

import os
import sys
import subprocess
import logging
import json
from datetime import datetime, timezone, timedelta
import getpass
from dotenv import load_dotenv
from collections import defaultdict
import platform
import requests

from ..metrics.network_metrics import NetworkMetrics
from ..metrics.protocol_info import ProtocolInfo
from ..detectors.issue_detector import IssueDetector
from ..detectors.performance_optimizer import PerformanceOptimizer
from .ml_analyzer import MLAnalyzer

logger = logging.getLogger(__name__)

class ShareAnalyzer:
    """Main class for analyzing network shares."""
    
    def __init__(self, share_path, username, debug_level=0, domain=None, openai_key=None):
        """Initialize the ShareAnalyzer."""
        self.share_path = share_path
        # Convert synology to synology-01 in share path if needed
        if '\\\\synology\\' in self.share_path:
            self.share_path = self.share_path.replace('\\\\synology\\', '\\\\synology-01\\')
        self.username = username
        self.domain = domain
        self.debug_level = debug_level
        self.openai_key = openai_key
        self.platform_info = self._get_platform_info()
        
        # Set Wireshark paths
        self.wireshark_path = r"C:\Program Files\Wireshark"
        os.environ["WIRESHARK_PATH"] = self.wireshark_path
        os.environ["PATH"] = f"{self.wireshark_path};{os.environ.get('PATH', '')}"
        
        # Download manuf file if missing
        self._ensure_manuf_file()
        
        # Initialize state
        self._init_state()
        
        # Initialize components
        self._init_components()
        
        # Set up directories and logging
        self._setup_directories()
        self.logger = self._setup_logging()

    def _get_platform_info(self):
        """Get platform-specific information and commands."""
        platform_info = {}
        
        if platform.system() == 'Windows':
            platform_info['is_windows'] = True
            platform_info['connect_cmd'] = 'net use "{share_path}" /user:{domain}\\{username} {password} /PERSISTENT:YES'
            platform_info['disconnect_cmd'] = 'net use "{share_path}" /delete'
            platform_info['path_sep'] = '\\'
        else:
            platform_info['is_windows'] = False
            platform_info['connect_cmd'] = 'mount -t cifs "{share_path}" /mnt/share -o username={username},password={password},domain={domain}'
            platform_info['disconnect_cmd'] = 'umount "{share_path}"'
            platform_info['path_sep'] = '/'
                
        return platform_info

    def _ensure_manuf_file(self):
        """Ensure Wireshark manufacturer database exists."""
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

    def _init_state(self):
        """Initialize capture and connection state."""
        self.capture = None
        self.is_capturing = False
        self._shutdown_requested = False
        self._connected_share = False
        self._authenticated = False
        self.error_counts = defaultdict(int)

    def _init_components(self):
        """Initialize analysis components."""
        self.metrics = NetworkMetrics()
        self.protocol_info = ProtocolInfo()
        self.issue_detector = IssueDetector()
        self.performance_optimizer = PerformanceOptimizer()
        
        # Initialize ML analyzer if API key provided
        self.ml_analyzer = None
        if self.openai_key:
            try:
                self.ml_analyzer = MLAnalyzer(self.openai_key)
            except Exception as e:
                logger.warning(f"Failed to initialize ML analyzer: {str(e)}")

    def _setup_directories(self):
        """Set up output and log directories."""
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
        self.logs_dir = os.path.join(self.output_dir, "logs")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Set up log files with ISO 8601 timestamp
        timestamp_utc = datetime.now(timezone.utc)
        filename_timestamp = timestamp_utc.strftime("%Y-%m-%dT%H-%M-%S")
        self.output_file = os.path.join(self.output_dir, f"analysis_{filename_timestamp}.log")
        self.debug_log = os.path.join(self.logs_dir, f"debug_analysis_{filename_timestamp}.log")

    def authenticate(self, password=None):
        """Authenticate and connect to the network share.
        
        Args:
            password (str, optional): Share password. If not provided, will prompt.
            
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        if self._authenticated:
            return True
            
        try:
            # Get password if not provided
            if not password:
                password = getpass.getpass(f"Enter password for {self.username}: ")
            
            # Format connection command
            connect_cmd = self.platform_info['connect_cmd'].format(
                share_path=self.share_path,
                username=self.username,
                password=password,
                domain=self.domain or '.'
            )
            
            # Execute connection command
            result = subprocess.run(
                connect_cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self._authenticated = True
                self._connected_share = True
                self.logger.info("Successfully authenticated to share")
                return True
            else:
                self.logger.error(f"Authentication failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            return False

    def analyze_share(self, duration=60, capture_filter=None):
        """Analyze the network share for performance and issues.
        
        Args:
            duration (int): Duration in seconds to capture traffic
            capture_filter (str, optional): Custom Wireshark capture filter
            
        Returns:
            dict: Analysis results containing metrics, issues, and recommendations
        """
        if not self._authenticated:
            self.logger.error("Not authenticated to share. Call authenticate() first.")
            return None
            
        try:
            # Start network capture
            self.logger.info(f"Starting network capture for {duration} seconds...")
            self.is_capturing = True
            
            # Collect network metrics
            network_data = self.metrics.collect_metrics(
                self.share_path,
                duration=duration,
                capture_filter=capture_filter
            )
            
            # Analyze protocol information
            protocol_data = self.protocol_info.analyze_protocols(network_data)
            
            # Detect potential issues
            issues = self.issue_detector.detect_issues(network_data, protocol_data)
            
            # Get performance recommendations
            recommendations = self.performance_optimizer.get_recommendations(
                network_data,
                protocol_data,
                issues
            )
            
            # Run ML analysis if available
            ml_insights = None
            if self.ml_analyzer:
                try:
                    ml_insights = self.ml_analyzer.analyze(
                        network_data,
                        protocol_data,
                        issues
                    )
                except Exception as e:
                    self.logger.warning(f"ML analysis failed: {str(e)}")
            
            # Compile results
            results = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'share_path': self.share_path,
                'metrics': network_data,
                'protocols': protocol_data,
                'issues': issues,
                'recommendations': recommendations
            }
            
            if ml_insights:
                results['ml_insights'] = ml_insights
                
            # Log summary
            self._log_analysis_summary(results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return None
        finally:
            self.is_capturing = False
            
    def _log_analysis_summary(self, results):
        """Log a summary of the analysis results."""
        self.logger.info("=== Analysis Summary ===")
        self.logger.info(f"Share: {results['share_path']}")
        self.logger.info(f"Issues found: {len(results['issues'])}")
        self.logger.info(f"Recommendations: {len(results['recommendations'])}")
        
        if results['issues']:
            self.logger.info("\nTop issues:")
            for issue in results['issues'][:3]:  # Show top 3 issues
                self.logger.info(f"- {issue['description']}")

    def cleanup(self):
        """Clean up resources and disconnect from share.
        
        Returns:
            bool: True if cleanup successful, False otherwise.
        """
        success = True
        
        try:
            # Stop any ongoing capture
            if self.is_capturing:
                self.logger.info("Stopping network capture...")
                self.is_capturing = False
            
            # Disconnect from share if connected
            if self._connected_share:
                self.logger.info("Disconnecting from share...")
                try:
                    disconnect_cmd = self.platform_info['disconnect_cmd'].format(
                        share_path=self.share_path
                    )
                    result = subprocess.run(
                        disconnect_cmd,
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        self._connected_share = False
                        self._authenticated = False
                    else:
                        self.logger.error(f"Failed to disconnect: {result.stderr}")
                        success = False
                except Exception as e:
                    self.logger.error(f"Error disconnecting from share: {str(e)}")
                    success = False
            
            # Clean up components
            try:
                self.metrics.cleanup()
                self.protocol_info.cleanup()
                self.issue_detector.cleanup()
                self.performance_optimizer.cleanup()
                if self.ml_analyzer:
                    self.ml_analyzer.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up components: {str(e)}")
                success = False
                
            return success
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")
            return False
