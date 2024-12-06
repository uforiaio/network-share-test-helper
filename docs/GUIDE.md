# User Guide

## Quick Start

### 1. Installation
```bash
# Clone repository
git clone https://github.com/yourusername/dfs-nfs-debugger.git
cd dfs-nfs-debugger

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Configuration
```bash
# Create environment file
copy env.template .env  # Windows
cp env.template .env    # Linux/Mac

# Edit .env with your settings:
SHARE_PATH=\\server\share
USERNAME=your_username
DEBUG_LEVEL=1  # 0=Basic, 1=Standard, 2=Detailed, 3=Full
OPENAI_KEY=your_openai_key
```

### 3. Basic Usage
```bash
# Run the analyzer
python dfs_nfs_analyzer.py <share_path> <username> <debug_level> <openai_key>

# Example
python dfs_nfs_analyzer.py "\\share\info" "domain\user" "INFO" "sk-your-openai-key"
```

## Features

### Network Analysis
- Share connectivity testing
- Protocol version detection
- Performance metrics (ISO 8601 timestamps)
- Latency measurements
- Throughput analysis

### Share Analysis
- Share type detection
- Protocol-specific metrics
- Backend server identification
- Permission validation
- Access pattern analysis

### Security
- Secure credential handling
- Network traffic sanitization
- Debug log masking
- API key protection
- Access monitoring

### Reporting
- JSON-formatted results
- ISO 8601 timestamps
- Performance metrics
- ML-powered insights
- Optimization recommendations

## Output Files

### Analysis Results
```
output/
├── analysis_results.json    # Latest analysis (ISO 8601)
├── capture_*.pcapng        # Network captures
├── analysis_*.log          # Debug logs (ISO 8601)
└── README.md              # Output documentation
```

### Log Structure
```
logs/
├── debug_*.log    # Debug logs (ISO 8601)
├── error_*.log    # Error logs (ISO 8601)
└── stats_*.log    # Statistics (ISO 8601)
```

## Debug Levels

### Level 0: Basic
- Errors and critical info
- Basic share status
- Connection status
- Essential metrics

### Level 1: Standard
- Level 0 +
- Performance metrics
- Protocol information
- Basic ML insights

### Level 2: Detailed
- Level 1 +
- Packet analysis
- Full ML insights
- Trend analysis
- Optimization suggestions

### Level 3: Full Debug
- Level 2 +
- Raw packet data
- Complete ML analysis
- Resource metrics
- System state

## Best Practices

### Performance
- Regular monitoring
- Baseline comparison
- Trend analysis
- Issue tracking
- Resource monitoring

### Security
- Regular API key rotation
- Network capture sanitization
- Log file protection
- Access monitoring
- Credential management

### Maintenance
- Regular updates
- Log rotation
- Configuration review
- Performance tuning
- Database updates

## Troubleshooting

### Common Issues

1. Share Access
   ```
   Error: Access Denied
   Solution:
   - Verify credentials
   - Check permissions
   - Test connectivity
   - Review share path
   ```

2. Packet Capture
   ```
   Error: Capture Failed
   Solution:
   - Run as administrator
   - Check Wireshark/Npcap
   - Verify interface
   - Review filters
   ```

3. Performance
   ```
   Issue: Slow Analysis
   Solution:
   - Check network load
   - Monitor resources
   - Verify share health
   - Optimize filters
   ```

## Updating

### Automatic Updates
```bash
# The tool checks for updates on startup
# Manual check:
python update.py
```

### Update Process
1. Checks version
2. Downloads updates
3. Updates dependencies
4. Preserves configuration
5. Maintains virtual environment
