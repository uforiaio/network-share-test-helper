# DFS/NFS Share Analyzer /* Do not use, too many bugs. Fixed it well enough to fix a problem with DFS. It's on my todo list. :)

A powerful command-line utility for analyzing DFS and NFS shares, combining traditional network analysis with advanced machine learning capabilities for comprehensive debugging and performance optimization.

## Key Features

### Network Analysis
- 🔍 Analyzes share type (DFS/NFS/SMB)
- 📊 Captures network traffic in pcapng format
- 🔒 Masks sensitive information
- 📝 Generates detailed debugging logs with ISO 8601 timestamps

### Performance Monitoring
- 📈 Network statistics and configuration
- ⚡ MTU and TCP window optimization
- 🔄 Traffic pattern analysis with real-time metrics
- 📉 Resource utilization tracking

### Machine Learning Capabilities
- 🤖 OpenAI GPT-4 powered analysis
- 📊 Anomaly detection with Isolation Forest
- 🔮 Performance prediction and forecasting
- 📈 Historical trend analysis

### Security
- 🔐 Secure configuration storage
- 🛡️ Network capture masking
- 🔒 Debug log sanitization
- ✅ Access pattern monitoring

## Quick Start

1. Clone and setup:
```bash
git clone https://github.com/yourusername/dfs-nfs-debugger.git
cd dfs-nfs-debugger
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .
```

3. Configure environment:
```bash
copy env.template .env  # Windows
cp env.template .env    # Linux/Mac
# Edit .env with your settings
```

4. Run the analyzer:
```bash
python dfs_nfs_analyzer.py <share_path> <username> <debug_level> <openai_key>
```

Example:
```bash
python dfs_nfs_analyzer.py "\\share\info" "domain\user" "INFO" "sk-your-openai-key"
```

## Output Files

### Analysis Results (`output/analysis_results.json`)
- Share and network configuration
- Performance metrics with ISO 8601 timestamps
- ML insights and predictions
- Optimization recommendations

### Debug Logs (`output/analysis_*.log`)
- Operation logs with ISO 8601 timestamps
- Error tracking and diagnostics
- Performance metrics
- ML analysis results

### Network Captures (`output/capture_*.pcapng`)
- Raw network traffic data
- Protocol-specific information
- Sanitized sensitive data
- Performance indicators

## Security Features

- Passwords are never stored
- Network captures are sanitized
- Debug information is masked
- API keys are securely managed
- All timestamps use ISO 8601 format

## Platform Support

### Windows (Primary)
- Full feature support
- Native share access
- Wireshark/Npcap integration
- Administrative tools

### Linux (Experimental)
- Basic share analysis
- Samba/NFS client support
- tcpdump integration
- Root privileges required

### macOS (Experimental)
- Basic share analysis
- Samba/NFS client support
- tcpdump integration
- Root privileges required

## Requirements

- Windows operating system
- Python 3.8 or higher
- Administrative privileges
- Internet connection for ML features
- OpenAI API access

## Documentation

Detailed documentation in `/docs`:
- [Configuration Guide](docs/CONFIGURATION.md)
- [User Guide](docs/GUIDE.md)
- [Context & Background](docs/CONTEXT.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Development Tracking](docs/TRACKING.md)

## Project Structure

```
dfs-nfs-debugger/
├── docs/               # Project documentation
├── output/            # Analysis results and logs
│   ├── *.json        # Analysis results (ISO 8601)
│   ├── *.log         # Debug logs (ISO 8601)
│   └── *.pcapng      # Network captures
├── logs/              # Application logs
├── dfs_nfs_analyzer.py # Main analyzer script
├── requirements.txt   # Python dependencies
├── setup.py          # Installation script
└── env.template      # Environment template
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with:
   - Description of changes
   - Test results
   - Documentation updates
   - ML model improvements (if applicable)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## New Environment Variable

- `MACHINE_LEARNING`: Set to `ON` to enable machine learning features

## New Features

- Real-time network packet capture and analysis
- Protocol-specific metrics and insights
- Performance optimization recommendations
- Issue detection and troubleshooting
- Session-based output organization
- Secure credential handling
