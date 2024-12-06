"""Integration tests for DFS/NFS Debugger."""
import os
import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from src.analyzers.share_analyzer import ShareAnalyzer
from src.metrics.network_metrics import NetworkMetrics
from src.metrics.protocol_info import ProtocolInfo
from src.detectors.issue_detector import IssueDetector
from src.detectors.performance_optimizer import PerformanceOptimizer
from src.analyzers.ml_analyzer import MLAnalyzer

@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    return {
        'SHARE_PATH': r'\\test-server\share',
        'USERNAME': 'testuser',
        'DOMAIN': 'testdomain',
        'DEBUG_LEVEL': '2',
        'OPENAI_KEY': 'test-key'
    }

@pytest.fixture
def mock_packet():
    """Create a mock network packet."""
    packet = MagicMock()
    packet.__len__ = lambda s: 1500
    return packet

@pytest.fixture
def share_analyzer(mock_env_vars):
    """Create a ShareAnalyzer instance with mocked dependencies."""
    with patch.dict(os.environ, mock_env_vars):
        analyzer = ShareAnalyzer(
            share_path=mock_env_vars['SHARE_PATH'],
            username=mock_env_vars['USERNAME'],
            domain=mock_env_vars['DOMAIN'],
            debug_level=int(mock_env_vars['DEBUG_LEVEL']),
            openai_key=mock_env_vars['OPENAI_KEY']
        )
        return analyzer

@pytest.mark.asyncio
async def test_full_analysis_workflow(share_analyzer, mock_packet):
    """Test the complete analysis workflow with proper async handling."""
    # Mock network metrics collection
    with patch.object(NetworkMetrics, 'capture_packets') as mock_capture:
        mock_capture.return_value.__enter__.return_value = True
        
        # Mock authentication
        with patch.object(ShareAnalyzer, 'authenticate') as mock_auth:
            mock_auth.return_value = True
            
            # Create an event for capture completion
            capture_complete = asyncio.Event()
            
            async def simulate_capture():
                """Simulate packet capture and processing."""
                # Process some mock packets
                for _ in range(5):
                    share_analyzer.metrics._process_packet(mock_packet)
                    await asyncio.sleep(0.1)
                capture_complete.set()
            
            # Start analysis with timeout
            analysis_task = asyncio.create_task(simulate_capture())
            try:
                # Wait for capture with timeout
                await asyncio.wait_for(capture_complete.wait(), timeout=2.0)
                
                # Run the analysis
                results = share_analyzer.analyze_share(duration=1)
                
                # Verify components were initialized
                assert isinstance(share_analyzer.metrics, NetworkMetrics)
                assert isinstance(share_analyzer.protocol_info, ProtocolInfo)
                assert isinstance(share_analyzer.issue_detector, IssueDetector)
                assert isinstance(share_analyzer.performance_optimizer, PerformanceOptimizer)
                assert isinstance(share_analyzer.ml_analyzer, MLAnalyzer)
                
                # Verify metrics were collected
                assert share_analyzer.metrics.total_packets == 5
                assert len(share_analyzer.metrics.packet_sizes) == 5
                assert all(size == 1500 for size in share_analyzer.metrics.packet_sizes)
                
                # Verify results structure
                assert 'metrics' in results
                assert 'issues' in results
                assert 'recommendations' in results
                
            except asyncio.TimeoutError:
                pytest.fail("Analysis timed out")
            finally:
                # Cleanup
                analysis_task.cancel()
                await share_analyzer.cleanup()

@pytest.mark.asyncio
async def test_error_handling(share_analyzer):
    """Test error handling in the async analysis workflow."""
    # Mock authentication failure
    with patch.object(ShareAnalyzer, 'authenticate', side_effect=Exception("Auth failed")):
        with pytest.raises(Exception) as exc_info:
            await asyncio.wait_for(
                asyncio.create_task(share_analyzer.analyze_share()),
                timeout=2.0
            )
        assert "Auth failed" in str(exc_info.value)

@pytest.mark.asyncio
async def test_resource_cleanup(share_analyzer, mock_packet):
    """Test resource cleanup after async analysis."""
    with patch.object(NetworkMetrics, 'capture_packets') as mock_capture:
        mock_capture.return_value.__enter__.return_value = True
        
        # Start capture
        share_analyzer.is_capturing = True
        
        # Process some packets
        for _ in range(3):
            share_analyzer.metrics._process_packet(mock_packet)
        
        # Run cleanup
        await share_analyzer.cleanup()
        
        # Verify cleanup
        assert not share_analyzer.is_capturing
        assert share_analyzer._shutdown_requested
        assert share_analyzer.metrics.total_packets == 3
        
        # Verify metrics were reset
        share_analyzer.metrics.reset()
        assert share_analyzer.metrics.total_packets == 0

@pytest.mark.asyncio
async def test_timeout_handling(share_analyzer):
    """Test handling of analysis timeout."""
    with patch.object(NetworkMetrics, 'capture_packets') as mock_capture:
        mock_capture.return_value.__enter__.return_value = True
        
        # Create a long-running analysis
        async def slow_analysis():
            await asyncio.sleep(2.0)
            return {}
        
        # Mock the analysis method
        with patch.object(ShareAnalyzer, 'analyze_share', side_effect=slow_analysis):
            # Try to run analysis with short timeout
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(
                    asyncio.create_task(share_analyzer.analyze_share()),
                    timeout=1.0
                )
            
            # Verify cleanup was called
            assert share_analyzer._shutdown_requested

@pytest.mark.asyncio
async def test_concurrent_operations(share_analyzer, mock_packet):
    """Test handling of concurrent operations."""
    with patch.object(NetworkMetrics, 'capture_packets') as mock_capture:
        mock_capture.return_value.__enter__.return_value = True
        
        # Create multiple concurrent tasks
        async def process_packets():
            for _ in range(3):
                share_analyzer.metrics._process_packet(mock_packet)
                await asyncio.sleep(0.1)
        
        # Run multiple processing tasks
        tasks = [
            asyncio.create_task(process_packets())
            for _ in range(3)
        ]
        
        # Wait for all tasks with timeout
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=2.0)
        
        # Verify results
        assert share_analyzer.metrics.total_packets == 9  # 3 tasks * 3 packets
        assert len(share_analyzer.metrics.packet_sizes) == 9
        assert all(size == 1500 for size in share_analyzer.metrics.packet_sizes)
