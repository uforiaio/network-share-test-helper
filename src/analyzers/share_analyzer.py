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
