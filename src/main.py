"""Main entry point for DFS/NFS Debugger."""
from utils.cli import parse_args
from utils.logging import setup_logger

def main():
    """Main entry point."""
    args = parse_args()
    logger = setup_logger(__name__)
    
    # TODO: Implement main analysis logic
    logger.info(f"Analyzing {args.target_path}")
    logger.info(f"Output format: {args.output_format}")

if __name__ == "__main__":
    main()
