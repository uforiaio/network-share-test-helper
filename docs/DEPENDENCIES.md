# Project Dependencies
*Last Updated: 2024-12-06*

## Table of Contents
1. [Core Dependencies](#core-dependencies)
2. [Optional Dependencies](#optional-dependencies)
3. [Development Dependencies](#development-dependencies)
4. [Version Requirements](#version-requirements)

## Core Dependencies

### Package Management
- `setuptools>=65.5.1`: Python package installation
- `packaging==23.2`: Version handling and compatibility
- `python-dotenv==1.0.0`: Environment configuration
- `pip>=23.3.1`: Package installer

### Machine Learning
- `openai==1.3.5`: OpenAI GPT-4 integration
- `scikit-learn==1.3.2`: ML utilities and algorithms
- `numpy==1.26.2`: Numerical computations
- `pandas==2.1.3`: Data manipulation and analysis

### Data Processing
- `pandas==2.1.3`: Data manipulation and analysis
- `matplotlib==3.8.2`: Data visualization
- `seaborn==0.13.0`: Statistical visualization
- `plotly==5.18.0`: Interactive plotting
- `scipy==1.11.4`: Scientific computing

### Network Analysis
- `scapy==2.5.0`: Network packet manipulation
- `pyshark==0.6.0`: Wireshark/tshark interface
- `psutil==5.9.6`: System and process monitoring
- `netifaces==0.11.0`: Network interface info

### Utilities
- `requests==2.31.0`: HTTP client library
- `emoji==2.8.0`: Emoji support for logging
- `colorama==0.4.6`: Terminal color support
- `tqdm==4.66.1`: Progress bars

## System Requirements

### Windows (Primary)
- Python 3.8 or higher
- Wireshark with Npcap
- Administrative privileges
- Network share access
- 4GB RAM minimum
- 1GB disk space

### Linux (Experimental)
- Python 3.8 or higher
- Wireshark/tshark
- tcpdump
- Root privileges
- Samba client
- NFS client
- 4GB RAM minimum
- 1GB disk space

### macOS (Experimental)
- Python 3.8 or higher
- Wireshark/tshark
- tcpdump
- Root privileges
- Samba client
- NFS client
- 4GB RAM minimum
- 1GB disk space

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

### Test Dependencies
- `pytest==7.4.3`: Testing framework
- `pytest-asyncio==0.21.1`: Async test support
- `pytest-cov==4.1.0`: Coverage reporting
- `pytest-mock==3.12.0`: Mocking support
- `pytest-timeout==2.2.0`: Test timeout handling
- `aiohttp==3.9.1`: Async HTTP client/server
- `asynctest==0.13.0`: Async testing utilities
- `coverage==7.3.2`: Code coverage tool
- `mock==5.1.0`: Mocking library

### Version Checking
- Automatic update checks
- Dependency validation
- Compatibility testing
- Version reporting
- Security updates

### Update Process
- Package updates
- Dependency resolution
- Virtual environment maintenance
- Configuration preservation
- Database updates

## Version Compatibility

### Software Versions
- Python: 3.8 - 3.11
- Wireshark: 3.6.x - 4.x
- OpenAI API: v1
- Windows: 10, 11
- Linux: Ubuntu 20.04+
- macOS: 11+
