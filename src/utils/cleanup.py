"""Resource cleanup and management utilities."""
import os
import logging
import psutil
from contextlib import contextmanager
from typing import Generator, Optional

logger = logging.getLogger(__name__)

class ResourceManager:
    """Manages cleanup of system resources."""
    
    def __init__(self):
        self.open_files = set()
        self.network_connections = set()
        self.temp_files = set()
    
    def register_file(self, file_path: str) -> None:
        """Register an open file for cleanup."""
        self.open_files.add(file_path)
        
    def register_network_connection(self, connection_id: str) -> None:
        """Register a network connection for cleanup."""
        self.network_connections.add(connection_id)
        
    def register_temp_file(self, temp_path: str) -> None:
        """Register a temporary file for cleanup."""
        self.temp_files.add(temp_path)
        
    def cleanup(self) -> None:
        """Clean up all registered resources."""
        self._cleanup_files()
        self._cleanup_network()
        self._cleanup_temp_files()
        
    def _cleanup_files(self) -> None:
        """Close any open file handles."""
        for file_path in self.open_files:
            try:
                if os.path.exists(file_path):
                    logger.debug(f"Closing file: {file_path}")
                    # Find and close any open handles to this file
                    for proc in psutil.process_iter(['pid', 'open_files']):
                        try:
                            for file in proc.open_files():
                                if file.path == file_path:
                                    os.close(file.fd)
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            continue
            except Exception as e:
                logger.error(f"Error cleaning up file {file_path}: {str(e)}")
        self.open_files.clear()
                
    def _cleanup_network(self) -> None:
        """Clean up network connections."""
        for conn_id in self.network_connections:
            try:
                logger.debug(f"Cleaning up network connection: {conn_id}")
                # Implementation depends on specific network cleanup needs
                pass
            except Exception as e:
                logger.error(f"Error cleaning up connection {conn_id}: {str(e)}")
        self.network_connections.clear()
                
    def _cleanup_temp_files(self) -> None:
        """Remove temporary files."""
        for temp_path in self.temp_files:
            try:
                if os.path.exists(temp_path):
                    logger.debug(f"Removing temp file: {temp_path}")
                    os.remove(temp_path)
            except Exception as e:
                logger.error(f"Error removing temp file {temp_path}: {str(e)}")
        self.temp_files.clear()

@contextmanager
def managed_resource(resource_manager: ResourceManager) -> Generator[ResourceManager, None, None]:
    """Context manager for automatic resource cleanup.
    
    Args:
        resource_manager: ResourceManager instance to use
        
    Yields:
        ResourceManager: The resource manager instance
    """
    try:
        yield resource_manager
    finally:
        resource_manager.cleanup()

# Global resource manager instance
_global_resource_manager: Optional[ResourceManager] = None

def get_resource_manager() -> ResourceManager:
    """Get or create the global resource manager instance."""
    global _global_resource_manager
    if _global_resource_manager is None:
        _global_resource_manager = ResourceManager()
    return _global_resource_manager
