# Project Context

## Overview
The DFS/NFS Debugger is a comprehensive network analysis tool designed to help diagnose and optimize network share performance. It supports both Windows DFS/SMB and Unix NFS protocols, providing detailed metrics and insights about network share behavior.

## Core Features

### Network Analysis
- Real-time packet capture and analysis
- Protocol version detection and validation
- Performance metrics collection (ISO 8601 timestamps)
- Latency and throughput measurements
- Connection stability monitoring

### Share Analysis
- Share type detection (DFS/SMB/NFS)
- Protocol-specific metrics
- Backend server identification
- Permission validation
- Access pattern analysis

### Performance Monitoring
- Real-time metrics collection
- Historical data analysis
- Resource utilization tracking
- Bottleneck detection
- Optimization recommendations

### Security Features
- Secure credential handling
- Network traffic sanitization
- Debug log masking
- API key protection
- Access monitoring

## Technical Stack

### Core Technologies
- Python 3.8+: Primary development language
- Wireshark/pyshark: Packet capture and analysis
- OpenAI GPT-4: ML-powered analysis
- Pandas/NumPy: Data processing

### Network Components
- SMB/CIFS Protocol
  - Version detection
  - Share enumeration
  - Performance metrics
  - Access validation

- NFS Protocol
  - Version detection
  - Mount point analysis
  - Performance metrics
  - Access validation

- TCP/IP Analysis
  - Packet inspection
  - Window size optimization
  - MTU configuration
  - Route analysis

### Data Management
- JSON output format
- ISO 8601 timestamps
- Structured logging
- Data sanitization
- Automatic rotation

## Use Cases

### Network Administrators
- Performance monitoring and optimization
- Issue diagnosis and resolution
- Capacity planning and scaling
- Security auditing and compliance

### System Engineers
- Protocol analysis and tuning
- Performance benchmarking
- Security validation
- Deployment verification

### DevOps Teams
- Integration testing
- Performance validation
- Automated monitoring
- Deployment verification

## Best Practices

### Performance Analysis
- Regular baseline measurements
- Trend analysis and tracking
- Alert threshold configuration
- Resource monitoring

### Security
- Regular credential rotation
- Traffic sanitization
- Log file protection
- Access monitoring

### Maintenance
- Regular updates
- Log rotation
- Configuration reviews
- Performance tuning
