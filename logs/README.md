# Logs Directory

This directory contains application execution logs. All logs are sanitized to remove any PII (Personally Identifiable Information) or privileged information.

## Log Types

1. **application.log**
   - Application startup/shutdown
   - Function execution traces
   - Performance metrics
   - Error messages

2. **debug.log**
   - Detailed debugging information
   - Stack traces
   - System metrics
   - Network statistics

## Security Considerations

- All sensitive information is automatically redacted
- No usernames, passwords, or authentication tokens
- No file paths containing user information
- No network addresses or domain names
- No system-specific information

## Log Rotation

Logs are automatically rotated:
- Maximum file size: 10MB
- Maximum backup count: 5
- Compression enabled for archived logs
