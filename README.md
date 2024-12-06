# DFS/NFS Share Analyzer

A powerful command-line utility for analyzing DFS and NFS shares, combining traditional network analysis with advanced machine learning capabilities for comprehensive debugging and performance optimization.

## Features

### Network Analysis
- 🔍 Analyzes share type (DFS/NFS/SMB)
- 📊 Captures network traffic in pcap format
- 🔒 Masks sensitive information
- 📝 Generates detailed debugging logs

### Performance Monitoring
- 📈 Network statistics and configuration
- ⚡ MTU and TCP window optimization
- 🔄 Traffic pattern analysis
- 📉 Resource utilization tracking

### Machine Learning Capabilities
- 🤖 OpenAI GPT-4 powered analysis
- 📊 Anomaly detection with Isolation Forest
- 🔮 Performance prediction
- 📈 Trend analysis and forecasting

### Security
- 🔐 Secure configuration storage
- 🛡️ Network capture masking
- 🔒 Debug log sanitization
- ✅ Access pattern monitoring

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have:
   - Administrative privileges for network capture
   - OpenAI API key for ML features
   - Network access to target shares

## Usage

```bash
python dfs_nfs_analyzer.py <share_path> <username> <debug_level> <openai_key>
```

Example:
```bash
python dfs_nfs_analyzer.py "\\share\info" "domain\user" "INFO" "sk-your-openai-key"
```

## Output Files

- `output.txt`: Detailed analysis including:
  - Share and network configuration
  - Performance metrics
  - ML insights and predictions
  - Optimization recommendations
  
- `debug_analysis.log`: Debug information with:
  - Operation logs
  - Error tracking
  - Performance metrics
  - ML analysis results

## Security

- Passwords are never stored
- Network capture masks sensitive data
- All debug information is sanitized
- API keys are securely managed

## Requirements

- Windows operating system
- Python 3.8 or higher
- Administrative privileges
- Internet connection for ML features
- OpenAI API access

## Documentation

Detailed documentation is available in the `/docs` directory:
- [Configuration Guide](docs/CONFIGURATION.md)
- [User Guide](docs/GUIDE.md)
- [Context & Background](docs/CONTEXT.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Development Tracking](docs/TRACKING.md)

## Project Structure

```
dfs-nfs-debugger/
├── docs/               # Project documentation
├── logs/              # Application execution logs
├── output/            # Performance data and analysis
├── dfs_nfs_analyzer.py # Main application file
├── requirements.txt   # Python dependencies
└── README.md         # Project overview
```

## Contributing

See [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Code submission process
- Documentation standards
- Testing requirements
- ML model improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
