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

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dfs-nfs-debugger.git
cd dfs-nfs-debugger
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

5. Create environment configuration:
```bash
# Copy the template
copy env.template .env
# Edit .env with your settings
```

6. Ensure you have:
   - Administrative privileges for network capture
   - OpenAI API key for ML features
   - Network access to target shares

## Usage

### Running the Application

```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the application
python dfs_nfs_analyzer.py <share_path> <username> <debug_level> <openai_key>
```

Example:
```bash
python dfs_nfs_analyzer.py "\\share\info" "domain\user" "INFO" "sk-your-openai-key"
```

### Updating the Application

The application automatically checks for updates on startup. You can also manually check and update:

```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run the update script
python update.py
```

This will:
- Check for new versions of the application
- Update dependencies if needed
- Maintain virtual environment isolation

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

## Platform Support

This tool was primarily developed and tested on Windows systems. While basic support for Linux and macOS has been added, it should be considered experimental and untested. The following features may have limited functionality on non-Windows systems:

- Network share access (different path formats and mounting mechanisms)
- Packet capture (requires different privileges and setup)
- Performance measurements (system-specific commands and tools)

### Prerequisites by Platform

#### Windows
- Python 3.8 or higher
- Wireshark with Npcap
- Administrative privileges for packet capture
- Network share access permissions

#### Linux (Experimental)
- Python 3.8 or higher
- Wireshark/tshark
- tcpdump
- Root privileges for packet capture
- Samba client for SMB access
- NFS client for NFS access

#### macOS (Experimental)
- Python 3.8 or higher
- Wireshark/tshark
- tcpdump
- Root privileges for packet capture
- Samba client for SMB access
- NFS client for NFS access

### Platform-Specific Notes

#### Windows
- Default configuration and full feature support
- Uses Windows-native share access mechanisms
- Requires Npcap for packet capture

#### Linux
- Share paths should use forward slashes
- May require manual mounting of shares
- Uses tcpdump for packet capture
- Some performance metrics may differ from Windows

#### macOS
- Share paths should use forward slashes
- May require manual mounting of shares
- Uses tcpdump for packet capture
- Some performance metrics may differ from Windows

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
├── venv/              # Virtual environment
├── dfs_nfs_analyzer.py # Main application file
├── requirements.txt   # Python dependencies
├── setup.py          # Package setup file
├── env.template      # Environment variables template
├── .env              # Environment variables
├── .gitignore        # Git ignore rules
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
