#!/usr/bin/env python3
"""
DFS/NFS Debugger - Main Entry Point
Analyzes and debugs network share performance issues.
"""

import warnings
# Suppress specific warnings
warnings.filterwarnings('ignore', message='Wireshark is installed, but cannot read manuf !')
warnings.filterwarnings('ignore', message='.*TripleDES has been moved.*')
warnings.filterwarnings('ignore', category=DeprecationWarning)

import os
from dotenv import load_dotenv
from src.analyzers.share_analyzer import ShareAnalyzer
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def main():
    """Main entry point."""
    # Load environment variables
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        logger.error(f".env file not found at {env_path}")
        return 1
        
    if not load_dotenv(env_path):
        logger.error("Failed to load .env file")
        return 1
    
    logger.info("Successfully loaded .env file")
    
    # Get configuration from environment
    share_path = os.getenv('SHARE_PATH')
    username = os.getenv('USERNAME')
    domain = os.getenv('DOMAIN')
    password = os.getenv('PASSWORD')
    debug_level_str = os.getenv('DEBUG_LEVEL', '2')
    debug_level = int(debug_level_str.split('#')[0].strip())  # Handle comments in env var
    openai_key = os.getenv('OPENAI_KEY')
    
    # Debug log environment variables
    logger.debug(f"Environment variables loaded:")
    logger.debug(f"SHARE_PATH: {share_path}")
    logger.debug(f"USERNAME: {username}")
    logger.debug(f"DOMAIN: {domain}")
    logger.debug(f"PASSWORD: {'<set>' if password else '<not set>'}")
    logger.debug(f"DEBUG_LEVEL: {debug_level}")
    
    if not share_path or not username or not password:
        logger.error("Share path, username, and password are required in .env file")
        return 1
    
    try:
        analyzer = ShareAnalyzer(
            share_path=share_path,
            username=username,
            domain=domain,
            debug_level=debug_level,
            openai_key=openai_key
        )
        return analyzer.run()
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == '__main__':
    exit(main())
