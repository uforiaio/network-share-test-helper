"""
Centralized logging configuration for the DFS/NFS Debugger.
Ensures consistent ISO 8601 timestamps and configurable log levels across all modules.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# ISO 8601 format for timestamps
ISO_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

# Mapping of DEBUG_LEVEL env var to logging levels
LOG_LEVEL_MAP = {
    "1": logging.WARNING,  # Basic
    "2": logging.INFO,     # Standard
    "3": logging.DEBUG     # Detailed
}

def get_log_level() -> int:
    """Get logging level from environment variable."""
    debug_level = os.getenv("DEBUG_LEVEL", "2")
    return LOG_LEVEL_MAP.get(debug_level, logging.INFO)

def setup_logger(name: str, log_file: Optional[str] = None, console_output: bool = False) -> logging.Logger:
    """
    Set up a logger with consistent formatting and level.
    
    Args:
        name: Name of the logger (typically __name__)
        log_file: Optional specific log file path
        console_output: Whether to also output to console (default: False)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers if they already exist
    if logger.handlers:
        return logger
        
    logger.setLevel(get_log_level())
    
    # Create formatter with ISO 8601 timestamps
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt=ISO_TIMESTAMP_FORMAT
    )
    
    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if specified or use default log file
    if log_file is None:
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Use current date for log file name
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"dfs_nfs_debugger_{current_date}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Example usage:
# from src.utils.logging import setup_logger
# logger = setup_logger(__name__)
