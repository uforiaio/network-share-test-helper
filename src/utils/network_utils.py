"""Network-related utilities and information gathering."""

import socket
import psutil
from typing import Dict, Any, List
from .logging import setup_logger

logger = setup_logger(__name__)

def get_network_interfaces() -> Dict[str, Any]:
    """Get information about network interfaces."""
    interfaces = {}
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
    return interfaces

def get_interface_stats(iface: str) -> Dict[str, int]:
    """Get statistics for a network interface."""
    try:
        stats = psutil.net_if_stats()[iface]
        return {
            'speed': stats.speed,
            'mtu': stats.mtu,
            'is_up': stats.isup
        }
    except KeyError:
        logger.warning(f"No stats available for interface {iface}")
        return {}

def get_dns_servers() -> List[str]:
    """Get configured DNS servers."""
    dns_servers = []
    try:
        for _, stats in psutil.net_if_stats().items():
            if stats.isup:
                # TODO: Implement platform-specific DNS server detection
                pass
    except Exception as e:
        logger.warning(f"Failed to get DNS servers: {e}")
    return dns_servers
