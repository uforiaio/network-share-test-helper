# Project Structure

## Directory Layout

```
dfs-nfs-debugger/
├── dfs_nfs_analyzer.py     # Main analyzer script
├── requirements.txt        # Python dependencies
├── setup.py               # Installation script
├── env.template           # Environment variables template
├── README.md             # Project documentation
├── docs/                 # Detailed documentation
│   ├── CONFIGURATION.md  # Configuration guide
│   ├── CONTEXT.md       # Project context
│   ├── DEPENDENCIES.md  # Dependency information
│   ├── GUIDE.md        # User guide
│   ├── PROJECT_STRUCTURE.md  # This file
│   └── TRACKING.md     # Issue tracking
├── logs/                # Debug and analysis logs
└── output/             # Analysis results
```

## Core Components

### Main Script (dfs_nfs_analyzer.py)
- `ShareAnalyzer`: Main class for share analysis
- `NetworkMetrics`: Network performance measurements
- `ProtocolInfo`: Protocol and version information
- `IssueDetector`: Network issue detection
- `PerformanceOptimizer`: Performance recommendations

### Configuration
- `.env`: Runtime configuration
- `env.template`: Configuration template
- Environment variables for:
  - Share paths
  - Credentials
  - Debug levels
  - API keys

### Output Organization
- `logs/`: Debug and analysis logs with ISO 8601 timestamps
- `output/`: Analysis results in JSON format
  - Network metrics
  - Protocol information
  - Performance data
  - Issue reports

## Key Features

### Network Analysis
- Packet capture and analysis
- Protocol version detection
- Performance metrics
- Latency measurements
- Throughput analysis

### Protocol Support
- SMB/CIFS
- NFS
- Cross-platform compatibility
  - Windows (primary)
  - Linux (experimental)
  - macOS (experimental)

### Security
- Secure credential handling
- No password storage
- Sanitized logging
- API key management

### Reporting
- JSON-formatted results
- ISO 8601 timestamps
- Detailed metrics
- Performance recommendations
