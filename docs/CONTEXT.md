# Project Context

## Overview
The DFS/NFS Debugger is a network analysis tool designed to help diagnose and optimize network share performance. It supports both Windows DFS/SMB and Unix NFS protocols, providing detailed metrics and insights about network share behavior.

## Purpose
- Analyze network share performance
- Detect protocol-specific issues
- Measure latency and throughput
- Provide optimization recommendations
- Generate detailed performance reports

## Key Features

### Network Analysis
- Real-time packet capture
- Protocol version detection
- Performance metrics collection
- Latency measurements
- Throughput analysis

### Cross-Platform Support
- Windows (Primary)
  - Native SMB/CIFS support
  - Wireshark/Npcap integration
  - Administrative tools
- Linux (Experimental)
  - Samba client support
  - tcpdump integration
  - NFS client tools
- macOS (Experimental)
  - Samba client support
  - tcpdump integration
  - NFS client tools

### Security Features
- Secure password handling
- No credential storage
- Sanitized logging
- API key protection

### Machine Learning
- Performance prediction
- Anomaly detection
- Trend analysis
- Optimization suggestions

## Technical Stack

### Core Technologies
- Python 3.8+
- Wireshark/pyshark
- OpenAI GPT-4 API
- Pandas/NumPy

### Network Protocols
- SMB/CIFS
- NFS
- TCP/IP analysis
- Network metrics

### Output Formats
- JSON data
- ISO 8601 timestamps
- Structured logs
- Performance reports

## Use Cases

### Network Administrators
- Performance monitoring
- Issue diagnosis
- Optimization planning
- Capacity planning

### System Engineers
- Protocol analysis
- Performance tuning
- Security auditing
- Troubleshooting

### DevOps Teams
- Integration testing
- Performance validation
- Automated monitoring
- Deployment verification
