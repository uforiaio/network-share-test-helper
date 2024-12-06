"""CLI interface for version updates."""

import argparse
import logging
from . import checker

logger = logging.getLogger(__name__)

def setup_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="DFS/NFS Debugger Update Utility",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check for updates without installing them"
    )
    return parser

def main():
    """Main entry point for the updater."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if args.check_only:
        current = checker.get_current_version()
        latest = checker.get_latest_version()
        print(f"Current version: {current}")
        print(f"Latest version: {latest or 'unknown'}")
    else:
        updated, message = checker.check_and_update()
        print(message)

if __name__ == "__main__":
    main()
