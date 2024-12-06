# User Guide

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the analyzer:
   ```bash
   python dfs_nfs_analyzer.py <share_path> <username> <debug_level> <openai_key>
   ```

## Output Files

### output.txt
Contains detailed analysis with emoji-based categorization:

#### Share Information
- 📁 Share type (DFS/NFS)
- 📁 Path details
- 📁 Access permissions

#### Network Analysis
- 🌐 Connection details
- 🌐 Protocol information
- 🌐 Active ports

#### Performance Metrics
- ⚡ TCP window sizes
- ⚡ MTU settings
- ⚡ Latency measurements

#### Traffic Analysis
- 🔄 Packet information
- 🔄 Protocol details
- 🔄 Masked sensitive data

#### Security Information
- 🔒 Authentication method
- 🔒 Encryption status
- 🔒 Access patterns

#### ML Insights
- 📊 Anomaly detection
- 🔮 Performance predictions
- 📈 Trend analysis
- 🤖 AI recommendations

### debug_analysis.log
- ℹ️ General Information
- ⚠️ Warnings and Errors
- ✅ Success Messages
- ⚙️ Configuration Changes

## Interpreting Results

### Log Categories
Each log entry is prefixed with an emoji indicating its category:
- 📁 Share Operations
- 🌐 Network Activity
- ⚡ Performance Data
- 🔄 Traffic Monitoring
- 🔒 Security Events
- ⚠️ Warnings/Errors
- ℹ️ Information
- ✅ Success
- ⚙️ Configuration
- 📊 Anomalies
- 🔮 Predictions
- 📈 Trends

### Machine Learning Insights

#### Anomaly Detection
The analyzer uses Isolation Forest to detect anomalies in:
- Network latency
- Packet sizes
- Window sizes
- Traffic patterns

#### Performance Prediction
GPT-4 powered analysis provides:
- Future performance trends
- Potential bottlenecks
- Resource utilization forecasts
- Optimization recommendations

### Troubleshooting Common Issues

1. ⚠️ Connection Failures
   - Check network connectivity
   - Verify share permissions
   - Validate credentials

2. ⚡ Performance Problems
   - Review TCP window sizes
   - Check MTU configuration
   - Analyze network latency

3. 🔒 Permission Errors
   - Verify user access rights
   - Check share permissions
   - Validate authentication

4. 🌐 Network Configuration
   - Confirm port availability
   - Check firewall settings
   - Verify DNS resolution

5. 🤖 ML Analysis Issues
   - Verify OpenAI API key
   - Check internet connectivity
   - Ensure sufficient data points
