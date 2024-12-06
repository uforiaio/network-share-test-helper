"""Tests for the CLI module."""
import pytest
from unittest.mock import patch
from src.utils.cli import parse_args, CliArgs

def test_parse_args_minimal():
    """Test parsing minimal arguments."""
    with patch('sys.argv', ['script.py', '/path/to/analyze']):
        args = parse_args()
        assert isinstance(args, CliArgs)
        assert args.target_path == '/path/to/analyze'
        assert not args.verbose
        assert args.output_format == 'text'

def test_parse_args_verbose():
    """Test parsing with verbose flag."""
    with patch('sys.argv', ['script.py', '/path/to/analyze', '-v']):
        args = parse_args()
        assert args.verbose

def test_parse_args_json_format():
    """Test parsing with JSON output format."""
    with patch('sys.argv', ['script.py', '/path/to/analyze', '-f', 'json']):
        args = parse_args()
        assert args.output_format == 'json'

def test_parse_args_all_options():
    """Test parsing with all options."""
    with patch('sys.argv', [
        'script.py',
        '/path/to/analyze',
        '-v',
        '-f', 'json'
    ]):
        args = parse_args()
        assert args.target_path == '/path/to/analyze'
        assert args.verbose
        assert args.output_format == 'json'

def test_parse_args_invalid_format():
    """Test parsing with invalid format raises error."""
    with patch('sys.argv', ['script.py', '/path/to/analyze', '-f', 'invalid']):
        with pytest.raises(SystemExit):
            parse_args()

def test_parse_args_missing_target():
    """Test parsing without required target path raises error."""
    with patch('sys.argv', ['script.py']):
        with pytest.raises(SystemExit):
            parse_args()
