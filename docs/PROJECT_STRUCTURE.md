# Project Structure

## Directory Layout

```
dfs-nfs-debugger/
├── docs/               # Project documentation
│   ├── CONFIGURATION.md
│   ├── CONTEXT.md
│   ├── DEPENDENCIES.md
│   ├── GUIDE.md
│   ├── PROJECT_STRUCTURE.md
│   └── TRACKING.md
│
├── logs/              # Application execution logs
│   └── README.md      # Log directory documentation
│
├── output/            # Performance data and analysis
│   └── README.md      # Output directory documentation
│
├── venv/              # Virtual environment (not in repo)
│
├── dfs_nfs_analyzer.py # Main application file
├── version_check.py   # Version and dependency management
├── update.py         # Update script
├── requirements.txt   # Python dependencies
├── setup.py          # Package setup file
├── env.template      # Environment variables template
├── .env              # Environment variables (not in repo)
├── .gitignore        # Git ignore rules
└── README.md         # Project overview
```

## Code Structure

### Core Classes

#### ShareAnalyzer
- Environment management
- Network analysis
- Traffic capture
- Log generation

#### NetworkMetrics
- RTT statistics
- Packet size tracking
- Window size monitoring
- Performance metrics

#### IssueDetector
- Problem identification
- Error categorization
- Threshold monitoring
- Health checks

#### PerformanceOptimizer
- Configuration analysis
- Resource optimization
- Performance tuning
- Improvement suggestions

#### MLAnalyzer
- Anomaly detection
- Performance prediction
- Trend analysis
- AI-powered insights

### Main Components

1. **Configuration Management**
   - Environment variables
   - OpenAI API integration
   - Network settings
   - Logging configuration

2. **Share Analysis**
   - DFS/NFS detection
   - Permission checking
   - Namespace analysis
   - Backend server discovery

3. **Network Monitoring**
   - Packet capture
   - Traffic analysis
   - Performance metrics
   - Connection tracking

4. **Machine Learning**
   - Anomaly detection (Isolation Forest)
   - Predictive analysis (GPT-4)
   - Pattern recognition
   - Trend forecasting

5. **Debug Logging**
   - Emoji-based categorization
   - Structured output
   - Error tracking
   - Performance metrics

6. **Output Generation**
   - JSON formatting
   - Emoji indicators
   - ML insights
   - Recommendations

## Generated Files

### .env
- Share path configuration
- User credentials
- Debug level settings
- OpenAI API key

### output.txt
- Analysis results
- Performance metrics
- ML insights
- Recommendations

### debug_analysis.log
- Detailed debug information
- Error tracking
- Operation timestamps
- System metrics
