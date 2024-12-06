#!/usr/bin/env python3
"""CLI entry point for DFS/NFS Debugger updates."""

import sys
import os

# Add src directory to path for imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)

from utils.version.updater import main

if __name__ == "__main__":
    main()
