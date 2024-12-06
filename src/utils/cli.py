"""Command line interface for DFS/NFS Debugger."""
import argparse
from typing import NamedTuple

class CliArgs(NamedTuple):
    """Structure to hold CLI arguments."""
    target_path: str
    verbose: bool
    output_format: str

def parse_args() -> CliArgs:
    """Parse command line arguments.
    
    Returns:
        CliArgs: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Debug and analyze DFS/NFS issues'
    )
    
    parser.add_argument(
        'target_path',
        help='Path to analyze (file or directory)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    return CliArgs(
        target_path=args.target_path,
        verbose=args.verbose,
        output_format=args.format
    )
