"""Tests for platform utilities."""
import socket
import platform
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.utils.platform_utils import (
    get_platform_info,
    get_windows_info,
    get_network_interfaces,
    get_interface_stats
)

@pytest.fixture
def mock_platform_info():
    """Mock platform information."""
    return {
        'system': 'Windows',
        'version': '10.0.19041',
        'machine': 'AMD64',
        'python_version': '3.9.0'
    }

@pytest.fixture
def mock_psutil_info():
    """Mock psutil information."""
    return {
        'cpu_count': 8,
        'memory_total': 16000000000,
        'net_if_addrs': {
            'eth0': [
                Mock(
                    family=socket.AF_INET,
                    address='192.168.1.100',
                    netmask='255.255.255.0'
                )
            ]
        },
        'net_if_stats': {
            'eth0': Mock(
                speed=1000,
                mtu=1500,
                isup=True
            )
        }
    }

@pytest.fixture
def mock_windows_registry():
    """Mock Windows registry."""
    mock_key = MagicMock()
    mock_key.__enter__.return_value = mock_key
    mock_key.QueryValueEx.return_value = (1, 'REG_DWORD')
    return mock_key

def test_get_platform_info(mock_platform_info, mock_psutil_info):
    """Test getting platform information."""
    with patch.multiple(
        platform,
        system=Mock(return_value=mock_platform_info['system']),
        version=Mock(return_value=mock_platform_info['version']),
        machine=Mock(return_value=mock_platform_info['machine']),
        python_version=Mock(return_value=mock_platform_info['python_version'])
    ), patch.multiple(
        psutil,
        cpu_count=Mock(return_value=mock_psutil_info['cpu_count']),
        virtual_memory=Mock(return_value=Mock(total=mock_psutil_info['memory_total'])),
        net_if_addrs=Mock(return_value=mock_psutil_info['net_if_addrs']),
        net_if_stats=Mock(return_value=mock_psutil_info['net_if_stats'])
    ), patch('socket.gethostname', return_value='test-host'):
        
        info = get_platform_info()
        
        assert info['os'] == 'Windows'
        assert info['os_version'] == '10.0.19041'
        assert info['architecture'] == 'AMD64'
        assert info['python_version'] == '3.9.0'
        assert info['hostname'] == 'test-host'
        assert info['cpu_count'] == 8
        assert info['memory_total'] == 16000000000
        assert 'network_interfaces' in info

def test_get_windows_info(mock_windows_registry):
    """Test getting Windows-specific information."""
    with patch('winreg.OpenKey', return_value=mock_windows_registry), \
         patch('src.utils.platform_utils.get_dns_servers', return_value=['8.8.8.8']), \
         patch('src.utils.platform_utils.get_network_shares', return_value=[]):
        
        info = get_windows_info()
        
        assert 'smb2_enabled' in info
        assert 'dns_servers' in info
        assert 'network_shares' in info
        assert info['smb2_enabled'] is True
        assert info['dns_servers'] == ['8.8.8.8']
        assert info['network_shares'] == []

def test_get_network_interfaces(mock_psutil_info):
    """Test getting network interface information."""
    with patch('psutil.net_if_addrs', return_value=mock_psutil_info['net_if_addrs']), \
         patch('psutil.net_if_stats', return_value=mock_psutil_info['net_if_stats']):
        
        interfaces = get_network_interfaces()
        
        assert 'eth0' in interfaces
        eth0 = interfaces['eth0']
        assert len(eth0['addresses']) == 1
        assert eth0['addresses'][0]['ip'] == '192.168.1.100'
        assert eth0['stats']['speed'] == 1000

def test_get_interface_stats(mock_psutil_info):
    """Test getting interface statistics."""
    with patch('psutil.net_if_stats', return_value=mock_psutil_info['net_if_stats']):
        stats = get_interface_stats('eth0')
        assert stats['speed'] == 1000
        assert stats['mtu'] == 1500
        assert stats['is_up'] is True

def test_get_interface_stats_error():
    """Test getting interface statistics with error."""
    with patch('psutil.net_if_stats', side_effect=Exception('Test error')):
        stats = get_interface_stats('eth0')
        assert stats == {'speed': None, 'mtu': None, 'is_up': None}
