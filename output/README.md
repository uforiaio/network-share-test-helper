# Output Directory

This directory contains performance data and analysis results from DFS/NFS share monitoring.

## File Types

1. **Analysis Results** (`analysis_results.json`)
   - Share configuration and status
   - Network performance metrics
   - Protocol information
   - Timestamps in ISO 8601 format
   - ML-based insights

2. **Packet Captures** (`capture_YYYYMMDD_HHMMSS.pcapng`)
   - Raw network traffic data
   - Filtered for share protocols
   - Sanitized sensitive information
   - Timestamped filenames

3. **Analysis Logs** (`analysis_YYYY-MM-DDTHH-MM-SS.log`)
   - Detailed operation logs
   - Error tracking
   - Performance metrics
   - ISO 8601 formatted timestamps

## Data Categories

1. **Share Performance**
   - Response times
   - Bandwidth usage
   - Operation counts
   - Error rates
   - Protocol-specific metrics

2. **Network Analysis**
   - Packet statistics
   - TCP window sizes
   - MTU configurations
   - Routing information
   - Connection stability

3. **ML Insights**
   - Anomaly detection results
   - Performance predictions
   - Trend analysis
   - Optimization recommendations
   - Resource utilization forecasts

## Data Retention

- Raw packet captures: 7 days
- Performance data: 30 days
- Aggregated statistics: 90 days
- Analysis reports: 1 year
- All data automatically sanitized

## File Organization

- `analysis_results.json`: Latest analysis results
- `capture_*.pcapng`: Network capture files
- `analysis_*.log`: Detailed analysis logs
- All timestamps in ISO 8601 format
