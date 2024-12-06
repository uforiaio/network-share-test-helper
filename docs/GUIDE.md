# User Guide

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
pip install -e .
```

4. Configure environment:
```bash
copy env.template .env  # Windows
cp env.template .env    # Linux/Mac
# Edit .env with your settings
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   - Copy `env.template` to `.env`
   - Set your share path, username, and OpenAI key

3. Run the analyzer:
   ```bash
   python dfs_nfs_analyzer.py <share_path> <username> <debug_level> <openai_key>
   ```

## Features

### Network Analysis
- Share connectivity testing
- Protocol version detection
- Performance metrics
- Latency measurements
- Throughput analysis

### Protocol Support
- SMB/CIFS shares
- NFS mounts
- Cross-platform compatibility

### Security
- Secure password input
- No credential storage
- API key protection
- Sanitized logging

### Reporting
- JSON-formatted results
- ISO 8601 timestamps
- Performance metrics
- ML-powered insights

## Usage Examples

### Basic Analysis
```bash
python dfs_nfs_analyzer.py \\server\share username 1 sk-your-openai-key
```

### Debug Mode
```bash
python dfs_nfs_analyzer.py \\server\share username 2 sk-your-openai-key
```

### Full Analysis
```bash
python dfs_nfs_analyzer.py \\server\share username 3 sk-your-openai-key
```

## Output Files

### Logs Directory
- Debug logs with timestamps
- Error tracking
- Performance data
- System metrics

### Output Directory
- Analysis results (JSON)
- Performance reports
- ML insights
- Recommendations

## Troubleshooting

### Common Issues

1. Share Access
   - Verify credentials
   - Check permissions
   - Test connectivity

2. Packet Capture
   - Run as administrator
   - Check Wireshark/Npcap
   - Verify interface

3. Performance
   - Check network load
   - Monitor system resources
   - Verify share health

### Debug Levels

- Level 0: Errors only
- Level 1: Standard info
- Level 2: Detailed debug
- Level 3: Full analysis

## Best Practices

### Performance
- Regular monitoring
- Baseline comparison
- Trend analysis
- Issue tracking

### Security
- Rotate API keys
- Update regularly
- Monitor access
- Review logs

### Maintenance
- Check updates
- Clean old logs
- Verify configs
- Test regularly

## Updating the Application

The application checks for updates on startup. You can also update manually:

```bash
python update.py
```

This will:
- Check for new versions
- Update dependencies
- Maintain virtual environment
