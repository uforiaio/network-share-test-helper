# Resource Management Guidelines

## Context Management

### Token Usage Optimization
1. **Checkpoint System**
   - Use temp.md as primary checkpoint storage
   - Update checkpoints before making code changes
   - Keep detailed progress tracking
   - Document test improvements

2. **Context Rotation**
   - Create new context when reaching ~75% of token limit
   - Save current state in markdown files before switching
   - Use clear handoff points between contexts
   - Track async operation state

### Session Structure
1. **Time-Based Chunking**
   - Work in 15-30 minute segments
   - Take 1-2 minute breaks between major changes
   - Plan exit points before starting complex tasks
   - Monitor async operation timeouts

2. **Resource-Aware Development**
   - Limit file sizes to manageable chunks
   - Break large files into modular components
   - Implement core functionality first
   - Use context managers for cleanup

## Code Management

### Change Size Guidelines
1. **Code Changes**
   - Keep changes to 30-50 lines per update
   - Split large classes into multiple commits
   - Focus on one component at a time
   - Implement proper error handling

2. **Documentation Updates**
   - Update docs in small increments
   - Keep temp.md changes focused
   - Document dependencies clearly
   - Track async patterns

### File Organization
1. **Component Structure**
   - One major component per session
   - Complete basic structure before details
   - Test components independently
   - Manage resource lifecycle

2. **Dependency Management**
   - Track dependencies in separate files
   - Update requirements incrementally
   - Document API changes separately
   - Handle external resources

### Module Organization
1. **Code Structure**
   - Separate concerns clearly
   - Use consistent naming
   - Follow platform conventions
   - Implement cleanup handlers

2. **Resource Handling**
   - Use context managers
   - Implement proper cleanup
   - Handle timeouts gracefully
   - Monitor resource usage

## Testing Guidelines

### Test Organization
1. **Test Structure**
   - Mirror source structure
   - Group related tests
   - Include async tests
   - Test cleanup handlers

2. **Test Coverage**
   - Aim for 80%+ coverage
   - Test error cases
   - Test async operations
   - Verify resource cleanup

### Resource Management in Tests
1. **Test Resources**
   - Mock external dependencies
   - Clean up after tests
   - Handle timeouts
   - Track resource usage

2. **Test Environment**
   - Use consistent setup
   - Clean environment after tests
   - Mock system resources
   - Handle platform differences

## Documentation

### Code Documentation
1. **Inline Documentation**
   - Document complex logic
   - Explain resource usage
   - Note cleanup requirements
   - Document async patterns

2. **API Documentation**
   - Clear method signatures
   - Document resource requirements
   - Note cleanup responsibilities
   - Explain async behavior

### Progress Tracking
1. **Checkpoint System**
   - Regular updates to temp.md
   - Track test improvements
   - Note resource issues
   - Monitor async patterns

2. **Issue Tracking**
   - Document known issues
   - Track resource leaks
   - Note timing problems
   - Monitor cleanup failures

## Resource Types

### System Resources
1. **Network Resources**
   - Packet capture handles
   - Network interfaces
   - Socket connections
   - Capture files

2. **File Resources**
   - Log files
   - Capture files
   - Temporary files
   - Configuration files

### Memory Management
1. **Object Lifecycle**
   - Proper initialization
   - Timely cleanup
   - Resource pooling
   - Memory monitoring

2. **Cleanup Patterns**
   - Context managers
   - Try-finally blocks
   - Signal handlers
   - Timeout handlers

## Best Practices

### Error Handling
1. **Resource Errors**
   - Graceful degradation
   - Cleanup on error
   - Error reporting
   - Recovery strategies

2. **Timeout Handling**
   - Set appropriate timeouts
   - Clean up on timeout
   - Report timeout errors
   - Retry strategies

### Performance
1. **Resource Optimization**
   - Minimize resource usage
   - Pool resources
   - Batch operations
   - Monitor performance

2. **Async Operations**
   - Use proper async patterns
   - Handle cancellation
   - Manage timeouts
   - Clean up resources

### Async Operation Best Practices
1. **Operation Lifecycle**
   - Initialize resources asynchronously
   - Use async context managers
   - Implement proper cancellation
   - Handle cleanup in finally blocks
   - Monitor operation timeouts

2. **Resource Management**
   - Use connection pools
   - Implement backoff strategies
   - Handle connection limits
   - Monitor resource usage
   - Clean up on task completion

3. **Error Handling**
   - Implement retry logic
   - Handle timeout exceptions
   - Log async failures
   - Maintain operation state
   - Provide cleanup callbacks

### Network Resource Management
1. **Connection Management**
   - Pool network connections
   - Monitor connection state
   - Implement timeout handling
   - Track resource usage
   - Clean up stale connections

2. **Performance Optimization**
   - Buffer network operations
   - Use async I/O patterns
   - Implement batch processing
   - Monitor network metrics
   - Optimize packet handling

3. **Resource Monitoring**
   - Track connection counts
   - Monitor bandwidth usage
   - Log resource statistics
   - Alert on resource limits
   - Implement usage quotas

## Performance Guidelines

### Resource Optimization
1. **Memory Management**
   - Use connection pooling for network resources
   - Implement proper cleanup handlers
   - Monitor memory usage in long operations
   - Release resources promptly after use
   - Use weak references where appropriate

2. **Network Efficiency**
   - Batch network operations when possible
   - Use async I/O for network operations
   - Implement proper timeout handling
   - Monitor bandwidth utilization
   - Cache frequently accessed data

3. **Operation Scheduling**
   - Prioritize critical operations
   - Implement rate limiting
   - Use appropriate thread pools
   - Balance resource allocation
   - Monitor operation latency

### Best Practices
1. **Resource Lifecycle**
   - Initialize resources lazily
   - Use context managers
   - Implement proper cleanup
   - Monitor resource usage
   - Handle cleanup failures

2. **Error Recovery**
   - Implement graceful degradation
   - Use circuit breakers
   - Handle partial failures
   - Maintain system stability
   - Log recovery actions

## Project Management

### Progress Tracking
1. **Checkpoint System**
   - Use temp.md as primary progress tracker
   - Update temp.md before and after major changes
   - Reference temp.md for current status and next steps
   - Keep temp.md focused on immediate tasks

2. **Resource-Aware Development**
   - Follow guidelines in this document for resource management
   - Update this document with new resource optimization strategies
   - Track resource usage patterns and bottlenecks
   - Document solutions to resource limitations

### Resource Optimization
1. **Code Organization**
   - Break large files into modules (see temp.md for progress)
   - Keep module sizes under 500 lines
   - Use lazy loading for heavy imports
   - Implement cleanup handlers (see src/utils/cleanup.py)

2. **Memory Management**
   - Clear large objects when no longer needed
   - Use generators for large datasets
   - Implement context managers for resource cleanup
   - Monitor memory usage in long operations

3. **Tool Usage**
   - Limit file views to necessary sections
   - Use specific search queries over broad ones
   - Prefer incremental changes over large rewrites
   - Cache frequently accessed data

### Resource Limitations
1. **Common Issues**
   - Token limit reached in long sessions
   - Large file processing delays
   - Memory usage in data analysis
   - Network timeouts in remote operations

2. **Solutions**
   - Break tasks into smaller chunks
   - Use checkpoint system in temp.md
   - Implement progressive loading
   - Add cleanup points between operations

### Best Practices
1. **Development Flow**
   - Check temp.md for current status
   - Follow modular development pattern
   - Test changes incrementally
   - Document resource impacts

2. **Code Changes**
   - Keep changes small (30-50 lines)
   - Update documentation with changes
   - Test resource usage after changes
   - Monitor performance impact

## Testing Strategy

### Testing Strategy
1. **Unit Testing**
   - Use pytest as primary testing framework
   - Create fixtures for common test scenarios
   - Mock external dependencies
   - Test error cases thoroughly

2. **Test Organization**
   - Mirror source code structure in tests
   - Group related test cases
   - Use descriptive test names
   - Document test purpose and setup

3. **Test Coverage**
   - Focus on critical components
   - Test error handling paths
   - Verify resource cleanup
   - Include edge cases

### Testing Progress
1. **Completed Tests**
   - Resource management (cleanup.py)
   - Command line interface (cli.py)
   - Network utilities (network_utils.py)
   - Platform utilities (platform_utils.py)

2. **Pending Tests**
   - System information (system_info.py)
   - Logging configuration (logging.py)
   - Integration scenarios
   - Performance testing

3. **Test Maintenance**
   - Regular test updates
   - Coverage monitoring
   - Performance benchmarks
   - Documentation updates

## Communication Guidelines

### Status Updates
1. **Progress Reports**
   - Keep updates concise
   - Focus on completed items
   - Plan next steps clearly

2. **Error Handling**
   - Document errors immediately
   - Save state on errors
   - Plan recovery steps

### Context Switching
1. **Handoff Process**
   - Save all changes to temp.md
   - Document current task state
   - List next steps clearly

2. **New Context Setup**
   - Load from latest checkpoint
   - Verify file state
   - Resume from clear point

## Emergency Procedures

### Resource Exhaustion
1. **Immediate Actions**
   - Save current state to temp.md
   - Document last successful operation
   - Note any pending changes

2. **Recovery Steps**
   - Start new context
   - Load from last checkpoint
   - Verify state before continuing

### Data Preservation
1. **Backup Strategy**
   - Keep markdown checkpoints
   - Save incomplete changes
   - Document decision points

2. **Restoration Process**
   - Load from latest temp.md
   - Verify file consistency
   - Resume from known state
