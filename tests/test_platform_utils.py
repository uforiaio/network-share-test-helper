"""Tests for platform utilities facade module."""

import pytest
from unittest.mock import patch, MagicMock
import platform
import socket
import psutil
import winreg
from src.utils.platform_utils import (
    get_platform_info,
    get_windows_info,
    get_network_interfaces,
    get_interface_stats
)

# Mock data
MOCK_NET_IF_ADDRS = {
    'Ethernet': [
        MagicMock(
            family=socket.AF_INET,
            address='192.168.1.100',
            netmask='255.255.255.0',
            broadcast='192.168.1.255'
        )
    ]
}

MOCK_NET_IF_STATS = {
    'Ethernet': MagicMock(
        isup=True,
        speed=1000,
        mtu=1500
    )
}

MOCK_VIRTUAL_MEMORY = MagicMock(
    total=17179869184  # 16GB
)

@pytest.fixture
def mock_platform():
    with patch('platform.system', return_value='Windows'), \
         patch('platform.version', return_value='10.0.19041'), \
         patch('platform.machine', return_value='AMD64'), \
         patch('platform.python_version', return_value='3.9.0'):
        yield

@pytest.fixture
def mock_system():
    with patch('socket.gethostname', return_value='TEST-PC'), \
         patch('psutil.cpu_count', return_value=8), \
         patch('psutil.virtual_memory', return_value=MOCK_VIRTUAL_MEMORY):
        yield

@pytest.fixture
def mock_network():
    with patch('psutil.net_if_addrs', return_value=MOCK_NET_IF_ADDRS), \
         patch('psutil.net_if_stats', return_value=MOCK_NET_IF_STATS):
        yield

@pytest.fixture
def mock_windows():
    mock_key = MagicMock()
    mock_key.__enter__ = MagicMock(return_value=mock_key)
    mock_key.__exit__ = MagicMock(return_value=None)
    
    with patch('winreg.OpenKey', return_value=mock_key), \
         patch('winreg.QueryValueEx', return_value=(1, 1)), \
         patch('src.utils.platform_utils.get_dns_servers', return_value=['8.8.8.8']), \
         patch('src.utils.platform_utils.get_network_shares', return_value=['\\\\server\\share']):
        yield

def test_get_platform_info(mock_platform, mock_system, mock_network, mock_windows):
    """Test getting complete platform information."""
    info = get_platform_info()
    
    assert info['os'] == 'Windows'
    assert info['os_version'] == '10.0.19041'
    assert info['architecture'] == 'AMD64'
    assert info['python_version'] == '3.9.0'
    assert info['hostname'] == 'TEST-PC'
    assert info['cpu_count'] == 8
    assert info['memory_total'] == 17179869184
    assert 'network_interfaces' in info
    assert 'smb2_enabled' in info
    assert 'dns_servers' in info
    assert 'network_shares' in info

def test_get_windows_info(mock_windows):
    """Test getting Windows-specific information."""
    info = get_windows_info()
    
    assert info['smb2_enabled'] is True
    assert info['dns_servers'] == ['8.8.8.8']
    assert info['network_shares'] == ['\\\\server\\share']

def test_get_network_interfaces(mock_network):
    """Test getting network interface information."""
    interfaces = get_network_interfaces()
    
    assert 'Ethernet' in interfaces
    assert len(interfaces['Ethernet']['addresses']) == 1
    assert interfaces['Ethernet']['addresses'][0]['ip'] == '192.168.1.100'
    assert interfaces['Ethernet']['addresses'][0]['netmask'] == '255.255.255.0'
    assert interfaces['Ethernet']['stats']['speed'] == 1000
    assert interfaces['Ethernet']['stats']['mtu'] == 1500
    assert interfaces['Ethernet']['stats']['is_up'] is True

def test_get_interface_stats(mock_network):
    """Test getting network interface statistics."""
    stats = get_interface_stats('Ethernet')
    
    assert stats['speed'] == 1000
    assert stats['mtu'] == 1500
    assert stats['is_up'] is True

def test_get_interface_stats_error():
    """Test handling error when getting interface statistics."""
    with patch('psutil.net_if_stats', side_effect=Exception('Test error')):
        stats = get_interface_stats('NonExistentInterface')
        assert stats == {'speed': None, 'mtu': None, 'is_up': False}
