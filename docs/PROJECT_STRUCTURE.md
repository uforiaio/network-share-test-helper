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
│   ├── CONFIGURATION.md  # Configuration guide
│   ├── CONTEXT.md       # Project context
│   ├── DEPENDENCIES.md  # Dependencies list
│   ├── GUIDE.md        # User guide
│   ├── PROJECT_STRUCTURE.md  # This file
│   └── TRACKING.md     # Development tracking
├── logs/               # Application logs
│   ├── debug_*.log     # Debug logs (ISO 8601)
│   ├── error_*.log     # Error logs (ISO 8601)
│   └── stats_*.log     # Statistics (ISO 8601)
├── output/            # Analysis output
│   ├── analysis_*.json  # Results (ISO 8601)
│   ├── capture_*.pcapng # Network captures
│   └── README.md       # Output documentation
└── src/               # Source code
    ├── analyzer/
    │   ├── __init__.py
    │   ├── share_analyzer.py
    │   ├── network_metrics.py
    │   ├── protocol_info.py
    │   └── issue_detector.py
    ├── async/
    │   ├── __init__.py
    │   ├── capture.py
    │   ├── metrics.py
    │   └── resource.py
    ├── utils/
    │   ├── __init__.py
    │   ├── cleanup.py
    │   ├── metrics.py
    │   └── async_helpers.py
    └── tests/
        ├── __init__.py
        ├── test_analyzer/
        ├── test_async/
        └── test_utils/
```

## Core Components

### Source Structure
```
src/
├── analyzer/
│   ├── __init__.py
│   ├── share_analyzer.py
│   ├── network_metrics.py
│   ├── protocol_info.py
│   └── issue_detector.py
├── async/
│   ├── __init__.py
│   ├── capture.py
│   ├── metrics.py
│   └── resource.py
├── utils/
│   ├── __init__.py
│   ├── cleanup.py
│   ├── metrics.py
│   └── async_helpers.py
└── tests/
    ├── __init__.py
    ├── test_analyzer/
    ├── test_async/
    └── test_utils/
```

### Main Script (dfs_nfs_analyzer.py)

#### Core Classes
- `ShareAnalyzer`: Share analysis and monitoring
  - Protocol detection and analysis
  - Performance metrics collection
  - Error handling and recovery
  - ML integration (with OpenAI)
  - Security features
  - Persistent connections

- `NetworkMetrics`: Network performance
  - Latency measurement
  - Throughput calculation
  - Packet analysis
  - Connection monitoring
  - Resource tracking
  - Performance prediction

- `ProtocolInfo`: Protocol handling
  - Version detection
  - Feature negotiation
  - Capability checking
  - Backend identification
  - Connection management
  - Authentication tracking

- `IssueDetector`: Problem detection
  - Error pattern matching
  - Performance analysis
  - Anomaly detection
  - Root cause analysis
  - ML-powered insights
  - Trend analysis

- `PerformanceOptimizer`: Optimization
  - Configuration tuning
  - Resource allocation
  - Protocol optimization
  - Performance recommendations
  - ML suggestions
  - Automated fixes

### Output Files

#### Logs (ISO 8601)
- Debug logs
  - Operation tracking
  - Error reporting
  - Performance metrics
  - ML insights
  - Security events

- Error logs
  - Exception details
  - Stack traces
  - Error context
  - Recovery actions
  - Impact analysis

- Statistics
  - Performance data
  - Resource usage
  - Operation counts
  - Trend analysis
  - ML predictions

#### Analysis Results
- Network metrics
- Protocol data
- Performance stats
- ML insights
- Security findings
- Recommendations

### Documentation
- Installation guide
- Configuration help
- Usage examples
- API reference
- Security notes
- Best practices
