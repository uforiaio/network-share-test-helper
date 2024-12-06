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
DOMAIN=your_domain      # Optional
DEBUG_LEVEL=1          # 0=Basic, 1=Standard, 2=Detailed, 3=Full
OPENAI_KEY=your_key    # Optional for ML features
```

### 3. Basic Usage
```bash
# Run with all parameters
python dfs_nfs_analyzer.py "\\share\info" "domain\user" 1 "mydomain" "sk-your-openai-key"

# Run with minimal parameters (using .env defaults)
python dfs_nfs_analyzer.py
```

## Features

### Network Analysis
- Share connectivity testing
- Protocol version detection
- Performance metrics (ISO 8601 timestamps)
- Latency measurements
- Throughput analysis
- Persistent connections
- Connection stability monitoring

### Share Analysis
- Share type detection (DFS/SMB/NFS)
- Protocol-specific metrics
- Backend server identification
- Permission validation
- Access pattern analysis
- Connection stability monitoring

### Security
- Secure credential handling
- Network traffic sanitization
- Debug log masking
- API key protection
- Access monitoring
- Persistent connection support

### ML Features (with OpenAI key)
- Performance prediction
- Anomaly detection
- Pattern recognition
- Trend analysis
- Optimization suggestions

### Reporting
- JSON-formatted results
- ISO 8601 timestamps
- Performance metrics
- ML-powered insights
- Optimization recommendations
- Sanitized output

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
- Security events

### Level 1: Standard (Default)
- Level 0 +
- Performance metrics
- Protocol information
- Connection details
- Basic ML insights

### Level 2: Detailed
- Level 1 +
- Packet analysis
- Full ML insights
- Resource usage
- Pattern detection

### Level 3: Full
- Level 2 +
- Raw packet data
- Debug information
- ML model details
- Complete metrics

## Best Practices

### Performance
- Use persistent connections for long sessions
- Monitor resource usage
- Set appropriate debug levels
- Regular baseline measurements
- Review performance metrics

### Security
- Rotate API keys regularly
- Use domain authentication when possible
- Monitor access patterns
- Review sanitized logs
- Keep dependencies updated

### Maintenance
- Regular updates
- Log rotation
- Capture cleanup
- Configuration review
- Database updates
