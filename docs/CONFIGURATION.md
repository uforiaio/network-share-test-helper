# Configuration Guide

## Environment Setup

### Environment Variables
Create a `.env` file based on `env.template` with the following variables:
```
SHARE_PATH=\\server\share
USERNAME=your_username
DEBUG_LEVEL=1
OPENAI_KEY=your_openai_key
```

### Platform-Specific Setup

#### Windows
1. Install Wireshark with Npcap
2. Run with administrative privileges
3. Ensure network share access permissions

#### Linux (Experimental)
1. Install required packages:
   ```bash
   sudo apt-get install wireshark tcpdump samba-client nfs-common
   ```
2. Add user to wireshark group:
   ```bash
   sudo usermod -a -G wireshark $USER
   ```

#### macOS (Experimental)
1. Install required packages:
   ```bash
   brew install wireshark
   brew install samba
   ```
2. Grant packet capture permissions to Wireshark

## Debug Levels

- Level 0: Basic logging (errors and critical info)
- Level 1: Standard logging (default)
- Level 2: Detailed logging with packet info
- Level 3: Full debug output with ML insights

## Network Configuration

### Share Access
- Ensure proper network share mounting
- Verify user permissions
- Test basic connectivity

### Packet Capture
- Configure network interface
- Set appropriate capture filters
- Verify Wireshark/tcpdump access

## Output Configuration

### Log Files
- Located in `logs/` directory
- ISO 8601 timestamp format
- Debug level specific content
- Automatic log rotation

### Analysis Results
- Stored in `output/` directory
- JSON formatted data
- Network metrics
- Protocol information
- Performance recommendations

## Security Configuration

### Credentials
- Never stored on disk
- Secure password input
- Session-only authentication

### API Keys
- Store in `.env` file
- Not included in logs
- Restricted permissions

## Performance Settings

### Packet Capture
- Buffer size configuration
- Capture duration limits
- Filter optimization

### Analysis
- ML model parameters
- Performance thresholds
- Alert configurations

## Troubleshooting

### Common Issues
1. Share access denied
   - Verify credentials
   - Check permissions
   - Test network connectivity

2. Packet capture fails
   - Check administrator/root access
   - Verify interface configuration
   - Test Wireshark/tcpdump installation

3. Missing manufacturer database
   - Will be downloaded automatically
   - Check internet connectivity
   - Verify write permissions
