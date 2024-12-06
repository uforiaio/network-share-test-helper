"""Tests for the cleanup module."""
import os
import pytest
from unittest.mock import Mock, patch
from src.utils.cleanup import ResourceManager, managed_resource, get_resource_manager

@pytest.fixture
def resource_manager():
    """Fixture providing a fresh ResourceManager instance."""
    return ResourceManager()

def test_register_file(resource_manager):
    """Test registering a file for cleanup."""
    test_file = "test.txt"
    resource_manager.register_file(test_file)
    assert test_file in resource_manager.open_files

def test_register_network_connection(resource_manager):
    """Test registering a network connection for cleanup."""
    conn_id = "test_conn_1"
    resource_manager.register_network_connection(conn_id)
    assert conn_id in resource_manager.network_connections

def test_register_temp_file(resource_manager):
    """Test registering a temporary file for cleanup."""
    temp_file = "temp.txt"
    resource_manager.register_temp_file(temp_file)
    assert temp_file in resource_manager.temp_files

@pytest.mark.parametrize("temp_file_exists", [True, False])
def test_cleanup_temp_files(resource_manager, temp_file_exists, tmp_path):
    """Test cleanup of temporary files."""
    # Create a temporary file if it should exist
    temp_file = tmp_path / "temp.txt"
    if temp_file_exists:
        temp_file.write_text("test content")
    
    # Register the temp file
    resource_manager.register_temp_file(str(temp_file))
    
    # Run cleanup
    resource_manager.cleanup()
    
    # Verify temp files set is cleared
    assert len(resource_manager.temp_files) == 0
    # Verify file is removed if it existed
    assert not temp_file.exists()

def test_managed_resource_context():
    """Test the managed_resource context manager."""
    manager = ResourceManager()
    
    # Mock the cleanup method
    manager.cleanup = Mock()
    
    # Use the context manager
    with managed_resource(manager):
        manager.register_file("test.txt")
    
    # Verify cleanup was called
    manager.cleanup.assert_called_once()

def test_get_resource_manager_singleton():
    """Test that get_resource_manager returns a singleton instance."""
    manager1 = get_resource_manager()
    manager2 = get_resource_manager()
    assert manager1 is manager2  # Same instance

@patch('psutil.process_iter')
def test_cleanup_files_with_psutil(mock_process_iter, resource_manager):
    """Test file cleanup using psutil."""
    # Mock process with open files
    mock_proc = Mock()
    mock_file = Mock()
    mock_file.path = "test.txt"
    mock_file.fd = 123
    mock_proc.open_files.return_value = [mock_file]
    mock_process_iter.return_value = [mock_proc]
    
    # Mock os.path.exists and os.close
    with patch('os.path.exists', return_value=True), \
         patch('os.close') as mock_close:
        
        # Register and cleanup a file
        resource_manager.register_file("test.txt")
        resource_manager.cleanup()
        
        # Verify os.close was called with the correct file descriptor
        mock_close.assert_called_once_with(123)
