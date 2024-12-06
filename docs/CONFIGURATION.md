# Configuration Guide

## Environment Setup

1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt
pip install -e .
```

3. Configure Environment
```bash
# Copy template
copy env.template .env  # Windows
cp env.template .env    # Linux/Mac

# Edit .env with your settings
```

## Environment Variables

The application uses the following environment variables in `.env`:

```ini
# Required Settings
SHARE_PATH=\\server\share
USERNAME=domain\user
DEBUG_LEVEL=INFO

# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here

# ML Analysis Settings
ML_ENABLED=true
ANOMALY_THRESHOLD=0.95
PREDICTION_WINDOW=24
HISTORY_WINDOW=168
MODEL_UPDATE_INTERVAL=24

# Performance Thresholds
MAX_LATENCY_MS=100
MIN_BANDWIDTH_MBPS=100
MAX_PACKET_LOSS=0.1
MIN_TCP_WINDOW=65535

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=logs/application.log
MAX_LOG_SIZE=10485760
LOG_BACKUP_COUNT=5

# Output Configuration
OUTPUT_DIR=output
DATA_RETENTION_DAYS=30
REPORT_RETENTION_DAYS=365
```

## Configuration Options

### Required Settings
- `SHARE_PATH`: Target share path to analyze
- `USERNAME`: User account for access
- `DEBUG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

### OpenAI Configuration
- `OPENAI_API_KEY`: Your OpenAI API key
  - Required for ML features
  - Keep secure and never commit
  - Rate limits apply

### ML Analysis Settings
- `ML_ENABLED`: Enable/disable ML features
- `ANOMALY_THRESHOLD`: Isolation Forest threshold
- `PREDICTION_WINDOW`: Hours to predict ahead
- `HISTORY_WINDOW`: Hours of history to analyze
- `MODEL_UPDATE_INTERVAL`: Hours between updates

### Performance Thresholds
- `MAX_LATENCY_MS`: Maximum acceptable latency
- `MIN_BANDWIDTH_MBPS`: Minimum acceptable bandwidth
- `MAX_PACKET_LOSS`: Maximum acceptable loss rate
- `MIN_TCP_WINDOW`: Minimum TCP window size

## Security Considerations

### API Key Management
- Store OPENAI_API_KEY securely
- Never commit API keys
- Use environment variables
- Rotate keys regularly

### Access Control
- Use least privilege access
- Monitor usage patterns
- Log access attempts
- Sanitize debug output

### Data Privacy
- Mask sensitive data
- Encrypt configuration
- Clean debug logs
- Secure ML data

## Virtual Environment

### Creation
```bash
python -m venv venv
```

### Activation
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Maintenance
```bash
# Update dependencies
python update.py

# Manual dependency update
pip install --upgrade -r requirements.txt
```

## Update Management

### Automatic Updates
- Version checking on startup
- Dependency updates
- Update notifications
- Self-update capability

### Manual Updates
```bash
# Run update script
python update.py

# Check current version
python -m pip show dfs-nfs-debugger
```

## ML Configuration

### Anomaly Detection

```python
ANOMALY_PARAMS = {
    'n_estimators': 100,
    'contamination': 'auto',
    'max_samples': 'auto',
    'random_state': 42
}
```

### Performance Prediction

```python
PREDICTION_PARAMS = {
    'model': 'gpt-4',
    'temperature': 0.7,
    'max_tokens': 150,
    'frequency_penalty': 0,
    'presence_penalty': 0
}
```

## Network Settings

### Capture Configuration

```python
CAPTURE_CONFIG = {
    'timeout': 30,
    'filter': 'port 445 or port 2049',
    'promiscuous': True,
    'snaplen': 65535
}
```

### Analysis Parameters

```python
ANALYSIS_CONFIG = {
    'sample_interval': 60,
    'window_size': 3600,
    'min_samples': 100,
    'max_samples': 1000
}
```

## Optimization

### Resource Limits

```python
RESOURCE_LIMITS = {
    'max_memory_mb': 1024,
    'max_cpu_percent': 50,
    'max_disk_io_mbps': 100,
    'max_network_mbps': 1000
}
```

### Cache Settings

```python
CACHE_CONFIG = {
    'enabled': True,
    'max_size_mb': 100,
    'ttl_seconds': 3600,
    'cleanup_interval': 300
}
```

## Logging

### Output Format

```python
LOG_FORMAT = {
    'timestamp': True,
    'level': True,
    'source': True,
    'message': True,
    'ml_insights': True
}
```

### File Rotation

```python
ROTATION_CONFIG = {
    'max_bytes': 10485760,
    'backup_count': 5,
    'compress': True
}
