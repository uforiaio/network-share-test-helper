#!/usr/bin/env python3
"""
Update script for DFS/NFS Debugger
This script handles updating the application and its dependencies
"""

import os
import sys
from version_check import check_and_update

def main():
    """Main entry point for the updater."""
    try:
        # Ensure we're in the virtual environment
        if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
            print("❌ Please run this script from within the virtual environment")
            sys.exit(1)
        
        print("🔍 Checking for updates...")
        updated, message = check_and_update()
        print(message)
        
        if updated:
            print("\n✨ Updates completed successfully")
            print("🔄 Please restart the application to use the updated version")
        else:
            print("\n✅ No updates needed")
        
    except KeyboardInterrupt:
        print("\n❌ Update cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Update failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
