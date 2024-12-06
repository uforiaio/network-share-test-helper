# Project Structure

## Directory Layout

```
dfs-nfs-debugger/
├── dfs_nfs_analyzer.py   # Main analyzer script
├── requirements.txt      # Python dependencies
├── setup.py             # Installation script
├── env.template         # Environment template
├── README.md           # Project documentation
├── docs/               # Documentation
│   ├── CONFIGURATION.md
│   ├── CONTEXT.md
│   ├── DEPENDENCIES.md
│   ├── GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   └── TRACKING.md
├── logs/               # Application logs
│   ├── debug_*.log     # Debug logs (ISO 8601)
│   ├── error_*.log     # Error logs (ISO 8601)
│   └── stats_*.log     # Statistics (ISO 8601)
└── output/            # Analysis output
    ├── analysis_results.json  # Results (ISO 8601)
    ├── capture_*.pcapng      # Network captures
    ├── analysis_*.log        # Analysis logs (ISO 8601)
    └── README.md            # Output documentation
```

## Core Components

### Main Script (dfs_nfs_analyzer.py)

#### Core Classes
- `ShareAnalyzer`: Share analysis and monitoring
  - Protocol detection
  - Performance metrics
  - Error handling
  - Data collection

- `NetworkMetrics`: Network performance
  - Latency measurement
  - Throughput calculation
  - Packet analysis
  - Connection monitoring

- `ProtocolInfo`: Protocol handling
  - Version detection
  - Feature negotiation
  - Capability checking
  - Backend identification

- `IssueDetector`: Problem detection
  - Error pattern matching
  - Performance analysis
  - Anomaly detection
  - Root cause analysis

- `PerformanceOptimizer`: Optimization
  - Configuration tuning
  - Resource allocation
  - Protocol optimization
  - Performance recommendations

### Configuration

#### Environment Files
- `.env`: Runtime configuration
  - Share paths
  - Credentials
  - Debug levels
  - API keys

- `env.template`: Configuration template
  - Default settings
  - Example values
  - Documentation
  - Security guidelines

### Output Organization

#### Logs Directory
- Debug logs (ISO 8601)
  - Operation tracking
  - Error reporting
  - Performance metrics
  - System state

- Error logs (ISO 8601)
  - Exception details
  - Stack traces
  - Error context
  - Recovery actions

- Statistics (ISO 8601)
  - Performance data
  - Resource usage
  - Operation counts
  - Trend analysis

#### Output Directory
- Analysis results (JSON)
  - Share information
  - Network metrics
  - Protocol data
  - Performance stats
  - All timestamps in ISO 8601

- Network captures
  - Raw packet data
  - Filtered traffic
  - Sanitized content
  - Protocol-specific info

- Analysis logs
  - Detailed analysis
  - ML insights
  - Recommendations
  - ISO 8601 timestamps

## Key Features

### Network Analysis
- Packet capture and analysis
- Protocol version detection
- Performance measurement
- Latency monitoring
- Throughput calculation

### Protocol Support
- SMB/CIFS handling
  - Version detection
  - Feature negotiation
  - Performance tuning
  - Error handling

- NFS support
  - Version detection
  - Mount management
  - Performance tuning
  - Error handling

### Security Features
- Credential protection
- Traffic sanitization
- Log file security
- API key management
- Access monitoring

### Reporting
- JSON output format
- ISO 8601 timestamps
- Performance metrics
- ML-based insights
- Optimization guidance
