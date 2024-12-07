"""Main ShareAnalyzer class for DFS/NFS debugging."""

import os
import sys
import subprocess
import json
from datetime import datetime, timezone, timedelta
import getpass
from dotenv import load_dotenv
from collections import defaultdict
import platform
import requests
import logging
import warnings

# Suppress scapy warnings
warnings.filterwarnings('ignore', message='Wireshark is installed, but cannot read manuf !')

from ..metrics.network_metrics import NetworkMetrics
from ..metrics.protocol_info import ProtocolInfo
from ..detectors.issue_detector import IssueDetector
from ..detectors.performance_optimizer import PerformanceOptimizer
from .ml_analyzer import MLAnalyzer
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class ShareAnalyzer:
    """Main class for analyzing network shares."""
    
    def __init__(self, share_path, username, debug_level=0, domain=None, openai_key=None):
        """Initialize the ShareAnalyzer."""
        # Basic setup
        self.share_path = share_path
        self.username = username
        self.domain = domain
        self.debug_level = debug_level
        self.openai_key = openai_key
        
        # Convert synology to synology-01 in share path if needed
        if '\\\\synology\\' in self.share_path:
            self.share_path = self.share_path.replace('\\\\synology\\', '\\\\synology-01\\')
            logger.info(f"Converted share path to: {self.share_path}")
            
        # Get platform info and setup Wireshark
        self.platform_info = self._get_platform_info()
        self.wireshark_path = self._find_wireshark_path()
        if self.wireshark_path:
            os.environ["WIRESHARK_PATH"] = self.wireshark_path
            os.environ["PATH"] = f"{self.wireshark_path};{os.environ.get('PATH', '')}"
            self._ensure_manuf_file()
        else:
            logger.warning("Wireshark installation not found")
            
        # Setup directories first
        if not self._setup_directories():
            logger.error("Failed to set up output directories")
            raise RuntimeError("Failed to set up output directories")
        self._setup_logging()
        
        # Initialize components with proper paths
        self.metrics = NetworkMetrics()
        if not self.metrics.set_output_dirs(self.pcap_dir):
            logger.error("Failed to set network metrics output directory")
            raise RuntimeError("Failed to set network metrics output directory")
        
        # Initialize remaining components
        self.protocol_info = ProtocolInfo()
        self.issue_detector = IssueDetector()
        self.performance_optimizer = PerformanceOptimizer()
        
        # Initialize ML analyzer if enabled
        self.ml_analyzer = None
        ml_enabled = os.getenv('MACHINE_LEARNING', 'OFF').upper() == 'ON'
        if ml_enabled and self.openai_key:
            try:
                self.ml_analyzer = MLAnalyzer(self.openai_key)
            except Exception as e:
                logger.warning(f"Failed to initialize ML analyzer: {e}")
                
        # Initialize state
        self._init_state()
        
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

    def _find_wireshark_path(self):
        """Find Wireshark installation path."""
        common_paths = [
            r"C:\Program Files\Wireshark",
            r"C:\Program Files (x86)\Wireshark",
        ]
        
        # First check if WIRESHARK_PATH is already set
        if "WIRESHARK_PATH" in os.environ:
            return os.environ["WIRESHARK_PATH"]
            
        # Then check common install locations
        for path in common_paths:
            if os.path.exists(path):
                return path
                
        # On Windows, try registry
        if platform.system() == 'Windows':
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WiresharkGroup") as key:
                    return winreg.QueryValueEx(key, "InstallDir")[0]
            except Exception:
                pass
                
        return None

    def _ensure_manuf_file(self):
        """Ensure Wireshark manufacturer database exists."""
        # First check resources directory
        resource_manuf = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'manuf')
        wireshark_manuf = os.path.join(self.wireshark_path, 'manuf') if self.wireshark_path else None
        
        # Use resource manuf if it exists, otherwise fall back to wireshark path
        manuf_path = resource_manuf if os.path.exists(resource_manuf) else wireshark_manuf
        
        if manuf_path and os.path.exists(manuf_path):
            # Tell Scapy where to find the manuf file
            from scapy.config import conf
            conf.manufdb = manuf_path
            logger.info(f"Using manuf file at: {manuf_path}")
            return
            
        if not manuf_path or not os.path.exists(manuf_path):
            try:
                print("Downloading Wireshark manufacturer database...")
                url = 'https://gitlab.com/wireshark/wireshark/-/raw/master/manuf'
                response = requests.get(url)
                response.raise_for_status()
                # Always save to resources directory
                manuf_path = resource_manuf
                os.makedirs(os.path.dirname(manuf_path), exist_ok=True)
                with open(manuf_path, 'wb') as f:
                    f.write(response.content)
                # Tell Scapy where to find the manuf file
                from scapy.config import conf
                conf.manufdb = manuf_path
                print("Successfully downloaded manufacturer database")
            except Exception as e:
                print(f"Warning: Could not download manufacturer database: {e}")

    def run(self):
        """Run the share analyzer."""
        try:
            logger.info("Starting share analysis...")
            
            # Get password from environment
            password = os.getenv('PASSWORD')
            if not password:
                logger.error("PASSWORD environment variable not set")
                return 1
                
            # Authenticate first
            if not self.authenticate(password):
                logger.error("Authentication failed")
                return 1
                
            # Run the analysis
            results = self.analyze_share()
            if not results:
                logger.error("Analysis failed")
                return 1
                
            # Clean up
            if not self.cleanup():
                logger.warning("Cleanup failed")
                
            return 0
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            return 1

    def _init_state(self):
        """Initialize capture and connection state."""
        self.capture = None
        self.is_capturing = False
        self._shutdown_requested = False
        self._connected_share = False
        self._authenticated = False
        self.error_counts = defaultdict(int)

    def _setup_directories(self):
        """Set up output and log directories.
        
        Returns:
            bool: True if directories were set up successfully, False otherwise
        """
        try:
            # Get base output directory from environment or use default
            base_output_dir = os.getenv('OUTPUT_DIR', 'output')
            self.output_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), base_output_dir))
            
            # Create timestamp and session ID (simpler format)
            timestamp_utc = datetime.now()
            session_id = os.urandom(4).hex()  # Generate a random 8-character session ID
            
            # Format: YYYY-MM-DD-HH.MM.SS-session-id
            dir_timestamp = f"{timestamp_utc.strftime('%Y-%m-%d-%H.%M.%S')}-{session_id}"
            
            # Create session-specific directory
            self.session_dir = os.path.join(self.output_dir, dir_timestamp)
            os.makedirs(self.session_dir, exist_ok=True)
            
            # Create subdirectories for different types of output
            self.logs_dir = os.path.join(self.session_dir, "logs")
            self.pcap_dir = os.path.join(self.session_dir, "pcap")
            self.json_dir = os.path.join(self.session_dir, "json")
            
            # Create all directories with full permissions
            for dir_path in [self.logs_dir, self.pcap_dir, self.json_dir]:
                os.makedirs(dir_path, exist_ok=True)
                # Set directory permissions to allow full access
                os.chmod(dir_path, 0o777)
                if not os.path.exists(dir_path):
                    logger.error(f"Failed to create directory: {dir_path}")
                    return False
                if not os.access(dir_path, os.W_OK):
                    logger.error(f"Directory not writable: {dir_path}")
                    return False
            
            # Set up file paths for this session
            self.session_log = os.path.join(self.logs_dir, "session.log")
            self.debug_log = os.path.join(self.logs_dir, "debug.log")
            self.metrics_json = os.path.join(self.json_dir, "metrics.json")
            self.pcap_file = os.path.join(self.pcap_dir, "capture.pcap")
            
            logger.info(f"Created session directory: {self.session_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up directories: {e}")
            return False

    def _setup_logging(self):
        """Set up component-specific logging configuration."""
        # Configure component-specific log file
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Create a component-specific log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'share_analyzer_{timestamp}.log')
        
        # Set up file handler for this specific analysis session
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        logger.addHandler(file_handler)
        
        # Log initial configuration
        logger.info(f"Initialized ShareAnalyzer for path: {self.share_path}")
        logger.info(f"Platform info: {self.platform_info}")
        logger.info(f"Debug level: {self.debug_level}")

    def _disconnect_all(self):
        """Disconnect all network connections."""
        try:
            # First try to disconnect specific share
            disconnect_cmd = ['net', 'use', self.share_path.rstrip('\\'), '/delete']
            subprocess.run(disconnect_cmd, capture_output=True, text=True)
        except Exception:
            pass
            
        try:
            # Then try to disconnect all connections
            disconnect_all_cmd = ['net', 'use', '*', '/delete', '/y']
            subprocess.run(disconnect_all_cmd, capture_output=True, text=True)
        except Exception:
            pass
            
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
            
            # Ensure share path has correct format
            share_path = self.share_path.rstrip('\\')  # Remove trailing backslash
            logger.debug(f"Using share path: {share_path}")
            
            # First disconnect any existing connections
            self._disconnect_all()
            
            # Format connection command with proper escaping
            if self.platform_info['is_windows']:
                # For Windows, use a list to handle special characters properly
                connect_cmd = ['net', 'use', share_path, '/user:' + self.username, password]
                logger.debug(f"Using Windows connection command format: net use [share_path] /user:[username] [password]")
            else:
                # For Unix, escape special characters in password
                escaped_password = password.replace('"', '\\"').replace("'", "\\'")
                connect_cmd = self.platform_info['connect_cmd'].format(
                    share_path=share_path,
                    username=self.username,
                    password=escaped_password,
                    domain=self.domain or '.'
                )
            
            logger.info(f"Attempting to connect to {share_path}")
            
            # Execute connection command
            if self.platform_info['is_windows']:
                result = subprocess.run(connect_cmd, capture_output=True, text=True)
            else:
                result = subprocess.run(connect_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self._authenticated = True
                self._connected_share = True
                logger.info("Successfully authenticated to share")
                return True
            else:
                logger.error(f"Authentication failed: {result.stderr}")
                if result.stdout:
                    logger.error(f"Command output: {result.stdout}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
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
            logger.error("Not authenticated to share. Call authenticate() first.")
            return None
            
        try:
            # Start network capture
            logger.info(f"Starting network capture for {duration} seconds...")
            self.is_capturing = True
            
            # Ensure pcap directory is set
            if not self.metrics.set_output_dirs(self.pcap_dir):
                logger.error("Failed to set network metrics output directory")
                return None
            
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
                    logger.warning(f"ML analysis failed: {str(e)}")
            
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
            logger.error(f"Analysis failed: {str(e)}")
            return None
        finally:
            self.is_capturing = False
            
    def _log_analysis_summary(self, results):
        """Log a summary of the analysis results."""
        logger.info("=== Analysis Summary ===")
        logger.info(f"Share: {results['share_path']}")
        logger.info(f"Issues found: {len(results['issues'])}")
        logger.info(f"Recommendations: {len(results['recommendations'])}")
        
        if results['issues']:
            logger.info("\nTop issues:")
            for issue in results['issues'][:3]:  # Show top 3 issues
                logger.info(f"- {issue['description']}")

    def cleanup(self):
        """Clean up resources and disconnect from share.
        
        Returns:
            bool: True if cleanup successful, False otherwise.
        """
        success = True
        
        # Disconnect from share
        try:
            if self._connected_share:
                logger.info("Disconnecting from share...")
                if self.platform_info['is_windows']:
                    cmd = ['net', 'use', self.share_path.rstrip('\\'), '/delete']
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode != 0:
                        logger.error(f"Failed to disconnect: {result.stderr.strip()}")
                        success = False
                else:
                    # Unix disconnect command
                    pass  # TODO: Implement Unix disconnect
        except Exception as e:
            logger.error(f"Error disconnecting from share: {e}")
            success = False
            
        # Clean up components
        try:
            if hasattr(self, 'metrics'):
                self.metrics.cleanup()
            if hasattr(self, 'protocol_info'):
                self.protocol_info.reset()
            if hasattr(self, 'issue_detector'):
                self.issue_detector.reset()
            if hasattr(self, 'performance_optimizer'):
                self.performance_optimizer.reset()
            if hasattr(self, 'ml_analyzer') and self.ml_analyzer:
                self.ml_analyzer.cleanup()
        except Exception as e:
            logger.error(f"Error cleaning up components: {e}")
            success = False
            
        return success
