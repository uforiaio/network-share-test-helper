# Configuration Guide

## Environment Setup

### Environment Variables
Create a `.env` file based on `env.template`:
```ini
# Share Configuration
SHARE_PATH=\\server\share
USERNAME=your_username

# Debug Settings
DEBUG_LEVEL=1  # 0=Basic, 1=Standard, 2=Detailed, 3=Full

# API Keys
OPENAI_KEY=your_openai_key

# Output Settings
OUTPUT_DIR=output
LOG_DIR=logs
TIMESTAMP_FORMAT=ISO8601  # All timestamps use ISO 8601
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
2. Grant packet capture permissions

## Debug Levels

- Level 0: Basic (errors and critical info)
- Level 1: Standard (default, includes performance metrics)
- Level 2: Detailed (adds packet info and ML insights)
- Level 3: Full (all available data and analysis)

## Output Configuration

### Log Files
- Located in `logs/` directory
- All timestamps in ISO 8601 format
- Automatic log rotation (30 days)
- Debug level specific content

### Analysis Results
- Stored in `output/` directory
- JSON formatted data
- ISO 8601 timestamps
- Network metrics
- Protocol information
- Performance recommendations

### Network Captures
- Stored in `output/` directory
- pcapng format
- Sanitized sensitive data
- Timestamped filenames

## Security Configuration

### Credentials
- Never stored on disk
- Secure password input
- Session-only authentication
- Access pattern monitoring

### API Keys
- Store in `.env` file
- Not included in logs/captures
- Restricted file permissions
- Regular rotation recommended

## Performance Settings

### Packet Capture
- Buffer size: 1MB default
- Capture duration: Configurable
- Filter optimization
- Interface auto-detection

### Analysis
- ML model parameters
- Performance thresholds
- Alert configurations
- Resource limits

## Troubleshooting

### Common Issues
1. Share Access Denied
   - Verify credentials
   - Check permissions
   - Test connectivity
   - Review share path format

2. Packet Capture Fails
   - Check administrator/root access
   - Verify interface configuration
   - Test Wireshark/tcpdump
   - Review capture filters

3. Missing Manufacturer Database
   - Will be downloaded automatically
   - Check internet connectivity
   - Verify write permissions
   - Temporary warning only
