# Dependencies

## Python Requirements

All Python dependencies are listed in `requirements.txt`:

- `python-dotenv`: Environment variable management
- `pyshark`: Network packet capture and analysis
- `psutil`: System and process utilities
- `scapy`: Network packet manipulation

## System Requirements

### Windows Components
- Windows Management Instrumentation (WMI)
- Network Packet Capture capabilities
- Administrative privileges

### Network Requirements
- Access to target shares
- Required ports open on firewalls
- Network interface in promiscuous mode for packet capture

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. System configuration:
   - Enable network packet capture
   - Configure firewall rules
   - Set appropriate share permissions
