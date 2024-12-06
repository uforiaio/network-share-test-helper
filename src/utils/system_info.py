"""System information gathering utilities."""

import platform
import psutil
from typing import Dict, Any
from .logging import setup_logger
from .network_utils import get_network_interfaces
from .windows_utils import get_windows_info

logger = setup_logger(__name__)

def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information."""
    info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'hostname': platform.node(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'network_interfaces': get_network_interfaces()
    }
    
    # Add Windows-specific information if on Windows
    if platform.system() == 'Windows':
        info.update(get_windows_info())
    
    return info

def get_performance_metrics() -> Dict[str, float]:
    """Get current system performance metrics."""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage_percent': psutil.disk_usage('/').percent
    }
