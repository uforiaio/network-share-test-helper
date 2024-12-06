"""Tests for network metrics collection."""

import pytest
from unittest.mock import patch, MagicMock
from scapy.layers.inet import IP, TCP
from src.metrics.network_metrics import NetworkMetrics

@pytest.fixture
def network_metrics():
    """Create a NetworkMetrics instance."""
    return NetworkMetrics()

@pytest.fixture
def mock_packet():
    """Create a mock packet with TCP options."""
    packet = MagicMock()
    packet.__contains__ = lambda s, layer: layer in [IP, TCP]
    
    # Add TCP attributes
    tcp = MagicMock()
    tcp.window = 65535
    tcp.flags = MagicMock(R=False)
    tcp.options = [('Timestamp', (12345, 67890))]
    
    packet.__getitem__ = lambda s, layer: tcp if layer == TCP else MagicMock()
    packet.__len__ = lambda s: 1500
    
    return packet

def test_capture_initialization(network_metrics):
    """Test packet capture initialization."""
    with patch('scapy.all.sniff') as mock_sniff:
        with network_metrics.capture_packets(interface='eth0') as success:
            assert success is True
            assert network_metrics._capture_thread is not None
            assert network_metrics._capture_file is not None
            
        # Verify cleanup
        assert network_metrics._capture is None
        assert network_metrics._capture_thread is None
        assert network_metrics._capture_file is None

def test_capture_error_handling(network_metrics):
    """Test error handling during capture."""
    with patch('scapy.all.sniff', side_effect=Exception("Test error")):
        with network_metrics.capture_packets(interface='eth0') as success:
            assert success is True  # Initial setup succeeded
        
        # Verify cleanup after error
        assert network_metrics._capture is None
        assert network_metrics._capture_thread is None
        assert network_metrics._capture_file is None

def test_packet_processing(network_metrics, mock_packet):
    """Test packet processing logic."""
    network_metrics._process_packet(mock_packet)
    
    assert network_metrics.total_packets == 1
    assert network_metrics.packet_sizes == [1500]
    assert network_metrics.window_sizes == [65535]
    assert network_metrics.retransmissions == 0
    assert network_metrics.rtt_samples == [55545]  # 67890 - 12345

def test_packet_processing_retransmission(network_metrics, mock_packet):
    """Test processing of retransmitted packets."""
    # Set retransmission flag
    mock_packet[TCP].flags.R = True
    
    network_metrics._process_packet(mock_packet)
    assert network_metrics.retransmissions == 1

def test_statistics_calculation(network_metrics):
    """Test network statistics calculation."""
    # Add some sample data
    network_metrics.add_rtt_sample(100)
    network_metrics.add_rtt_sample(200)
    network_metrics.add_packet_size(1000)
    network_metrics.add_packet_size(1500)
    network_metrics.add_window_size(65535)
    network_metrics.increment_retransmissions()
    network_metrics.increment_packet_loss()
    network_metrics.increment_total_packets()
    network_metrics.increment_total_packets()
    
    stats = network_metrics.get_statistics()
    
    assert stats['rtt']['min'] == 100
    assert stats['rtt']['max'] == 200
    assert stats['rtt']['avg'] == 150
    assert stats['packet_size']['min'] == 1000
    assert stats['packet_size']['max'] == 1500
    assert stats['packet_size']['avg'] == 1250
    assert stats['window_size']['min'] == 65535
    assert stats['window_size']['max'] == 65535
    assert stats['retransmission_rate'] == 50.0  # 1/2 * 100
    assert stats['packet_loss_rate'] == 50.0  # 1/2 * 100

def test_cleanup_after_timeout(network_metrics):
    """Test cleanup after capture timeout."""
    with patch('scapy.all.sniff') as mock_sniff, \
         patch('scapy.all.wrpcap') as mock_wrpcap:
        with network_metrics.capture_packets(timeout=1):
            pass
            
        # Verify cleanup was called
        assert mock_wrpcap.called
        assert network_metrics._capture is None

def test_reset_metrics(network_metrics):
    """Test metrics reset functionality."""
    # Add some data
    network_metrics.add_rtt_sample(100)
    network_metrics.add_packet_size(1500)
    network_metrics.increment_total_packets()
    
    # Reset
    network_metrics.reset()
    
    # Verify reset
    assert len(network_metrics.rtt_samples) == 0
    assert len(network_metrics.packet_sizes) == 0
    assert network_metrics.total_packets == 0
    assert network_metrics._capture is None
    assert network_metrics._capture_thread is None
    assert network_metrics._capture_file is None
