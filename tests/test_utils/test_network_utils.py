"""Tests for network utilities."""
import socket
import pytest
from unittest.mock import Mock, patch
from src.utils.network_utils import (
    get_network_interfaces,
    get_interface_stats,
    get_dns_servers
)

@pytest.fixture
def mock_net_if_addrs():
    """Mock network interface addresses."""
    return {
        'eth0': [
            Mock(
                family=socket.AF_INET,
                address='192.168.1.100',
                netmask='255.255.255.0'
            )
        ],
        'wlan0': [
            Mock(
                family=socket.AF_INET,
                address='192.168.2.100',
                netmask='255.255.255.0'
            )
        ]
    }

@pytest.fixture
def mock_net_if_stats():
    """Mock network interface statistics."""
    return {
        'eth0': Mock(
            speed=1000,
            mtu=1500,
            isup=True
        ),
        'wlan0': Mock(
            speed=300,
            mtu=1500,
            isup=True
        )
    }

def test_get_network_interfaces(mock_net_if_addrs, mock_net_if_stats):
    """Test getting network interface information."""
    with patch('psutil.net_if_addrs', return_value=mock_net_if_addrs), \
         patch('psutil.net_if_stats', return_value=mock_net_if_stats):
        
        interfaces = get_network_interfaces()
        
        assert 'eth0' in interfaces
        assert 'wlan0' in interfaces
        
        eth0 = interfaces['eth0']
        assert len(eth0['addresses']) == 1
        assert eth0['addresses'][0]['ip'] == '192.168.1.100'
        assert eth0['addresses'][0]['netmask'] == '255.255.255.0'
        assert eth0['stats']['speed'] == 1000
        assert eth0['stats']['mtu'] == 1500
        assert eth0['stats']['is_up'] is True

def test_get_interface_stats(mock_net_if_stats):
    """Test getting interface statistics."""
    with patch('psutil.net_if_stats', return_value=mock_net_if_stats):
        stats = get_interface_stats('eth0')
        assert stats['speed'] == 1000
        assert stats['mtu'] == 1500
        assert stats['is_up'] is True

def test_get_interface_stats_nonexistent():
    """Test getting stats for nonexistent interface."""
    with patch('psutil.net_if_stats', return_value={}):
        stats = get_interface_stats('nonexistent')
        assert stats == {}

def test_get_dns_servers():
    """Test getting DNS servers."""
    # Since DNS server detection is platform-specific and not fully implemented,
    # we just verify it returns a list and doesn't raise exceptions
    servers = get_dns_servers()
    assert isinstance(servers, list)
