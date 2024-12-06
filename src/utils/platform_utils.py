"""Platform utilities facade module.

This module serves as a facade for platform-specific utilities and information gathering,
re-exporting functionality from specialized modules.
"""

import os
import socket
import platform
import psutil
import winreg
from typing import Dict, Any
from .logging import setup_logger
from .system_info import get_system_info, get_performance_metrics
from .network_utils import get_network_interfaces, get_dns_servers
from .windows_utils import get_windows_info, get_network_shares

__all__ = [
    'get_system_info',
    'get_performance_metrics',
    'get_network_interfaces',
    'get_dns_servers',
    'get_windows_info',
    'get_network_shares'
]

# Initialize logger for any facade-level logging
logger = setup_logger(__name__)

def get_platform_info() -> Dict[str, Any]:
    """Get platform-specific information."""
    info = {
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'hostname': socket.gethostname(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'network_interfaces': get_network_interfaces()
    }
    
    # Windows-specific information
    if platform.system() == 'Windows':
        info.update(get_windows_info())
    
    return info

def get_windows_info() -> Dict[str, Any]:
    """Get Windows-specific information."""
    info = {}
    try:
        # Get SMB version
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                          r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters") as key:
            try:
                smb2, _ = winreg.QueryValueEx(key, "SMB2")
                info['smb2_enabled'] = bool(smb2)
            except FileNotFoundError:
                info['smb2_enabled'] = True  # Default is enabled
                
        # Get DNS servers
        info['dns_servers'] = get_dns_servers()
        
        # Get network shares
        info['network_shares'] = get_network_shares()
        
    except Exception as e:
        logger.error(f"Error getting Windows information: {e}")
    
    return info

def get_network_interfaces() -> Dict[str, Dict[str, Any]]:
    """Get information about network interfaces."""
    interfaces = {}
    try:
        for iface, addrs in psutil.net_if_addrs().items():
            interfaces[iface] = {
                'addresses': [],
                'stats': get_interface_stats(iface)
            }
            for addr in addrs:
                if addr.family == socket.AF_INET:  # IPv4
                    interfaces[iface]['addresses'].append({
                        'ip': addr.address,
                        'netmask': addr.netmask
                    })
    except Exception as e:
        logger.error(f"Error getting network interfaces: {e}")
    
    return interfaces

def get_interface_stats(iface: str) -> Dict[str, Any]:
    """Get statistics for a network interface."""
    try:
        stats = psutil.net_if_stats()[iface]
        return {
            'speed': stats.speed,
            'mtu': stats.mtu,
            'is_up': stats.isup
        }
    except Exception as e:
        logger.error(f"Error getting interface stats for {iface}: {e}")
        return {}

def get_dns_servers() -> list:
    """Get configured DNS servers."""
    dns_servers = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                          r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters") as key:
            try:
                servers, _ = winreg.QueryValueEx(key, "NameServer")
                dns_servers.extend(servers.split(','))
            except FileNotFoundError:
                pass
    except Exception as e:
        logger.error(f"Error getting DNS servers: {e}")
    
    return dns_servers

def get_network_shares() -> list:
    """Get mounted network shares."""
    shares = []
    try:
        output = os.popen('net use').read()
        for line in output.split('\n'):
            if '\\\\' in line:
                parts = line.split()
                if len(parts) >= 2:
                    shares.append(parts[1])
    except Exception as e:
        logger.error(f"Error getting network shares: {e}")
    
    return shares
