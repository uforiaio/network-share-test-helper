#!/usr/bin/env python3
"""
DFS/NFS Debugger - Main Entry Point
Analyzes and debugs network share performance issues.
"""

import os
from dotenv import load_dotenv
from src.analyzers.share_analyzer import ShareAnalyzer
from src.utils.logging import setup_logger

logger = setup_logger(__name__)

def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment
    share_path = os.getenv('SHARE_PATH')
    username = os.getenv('USERNAME')
    domain = os.getenv('DOMAIN')
    debug_level = int(os.getenv('DEBUG_LEVEL', '2'))
    openai_key = os.getenv('OPENAI_KEY')
    
    if not share_path or not username:
        logger.error("Share path and username are required in .env file")
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
