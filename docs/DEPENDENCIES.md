# Dependencies

## Core Dependencies

### Package Management
- `setuptools>=65.5.1`: Python package installation
- `packaging==23.2`: Version handling and compatibility
- `python-dotenv==1.0.0`: Environment configuration

### Machine Learning
- `openai==1.3.5`: OpenAI GPT-4 integration
- `scikit-learn==1.3.2`: ML utilities and algorithms
- `numpy==1.26.2`: Numerical computations

### Data Processing
- `pandas==2.1.3`: Data manipulation and analysis
- `matplotlib==3.8.2`: Data visualization
- `seaborn==0.13.0`: Statistical visualization
- `plotly==5.18.0`: Interactive plotting

### Network Analysis
- `scapy==2.5.0`: Network packet manipulation
- `pyshark==0.6.0`: Wireshark/tshark interface
- `psutil==5.9.6`: System and process monitoring
- `netifaces==0.11.0`: Network interface info

### Utilities
- `requests==2.31.0`: HTTP client library
- `emoji==2.8.0`: Emoji support for logging

## System Requirements

### Windows (Primary)
- Python 3.8 or higher
- Wireshark with Npcap
- Administrative privileges
- Network share access

### Linux (Experimental)
- Python 3.8 or higher
- Wireshark/tshark
- tcpdump
- Root privileges
- Samba client
- NFS client

### macOS (Experimental)
- Python 3.8 or higher
- Wireshark/tshark
- tcpdump
- Root privileges
- Samba client
- NFS client

## Installation

### Package Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### Platform-Specific Setup

#### Windows
```bash
# Install Wireshark with Npcap
# Run as administrator
```

#### Linux
```bash
sudo apt-get install wireshark tcpdump samba-client nfs-common
sudo usermod -a -G wireshark $USER
```

#### macOS
```bash
brew install wireshark
brew install samba
```

## Version Management

### Version Checking
- Automatic update checks
- Dependency validation
- Compatibility testing
- Version reporting

### Update Process
- Package updates
- Dependency resolution
- Virtual environment maintenance
- Configuration preservation
