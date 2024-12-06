# Resource Management Guidelines

## Context Management

### Token Usage Optimization
1. **Checkpoint System**
   - Use temp.md as primary checkpoint storage
   - Update checkpoints before making code changes
   - Keep detailed progress tracking

2. **Context Rotation**
   - Create new context when reaching ~75% of token limit
   - Save current state in markdown files before switching
   - Use clear handoff points between contexts

### Session Structure
1. **Time-Based Chunking**
   - Work in 15-30 minute segments
   - Take 1-2 minute breaks between major changes
   - Plan exit points before starting complex tasks

2. **Resource-Aware Development**
   - Limit file sizes to manageable chunks
   - Break large files into modular components
   - Implement core functionality first

## Code Management

### Change Size Guidelines
1. **Code Changes**
   - Keep changes to 30-50 lines per update
   - Split large classes into multiple commits
   - Focus on one component at a time

2. **Documentation Updates**
   - Update docs in small increments
   - Keep temp.md changes focused
   - Document dependencies clearly

### File Organization
1. **Component Structure**
   - One major component per session
   - Complete basic structure before details
   - Test components independently

2. **Dependency Management**
   - Track dependencies in separate files
   - Update requirements incrementally
   - Document API changes separately

## Best Practices

### Development Flow
1. **Pre-Change**
   - Review current state in temp.md
   - Plan changes in small chunks
   - Verify resource availability

2. **During Change**
   - Make incremental updates
   - Test each component
   - Document progress

3. **Post-Change**
   - Update checkpoint files
   - Verify file integrity
   - Plan next session

### Resource Monitoring
1. **Token Usage**
   - Monitor context size regularly
   - Plan context switches ahead
   - Save state before limits

2. **Performance**
   - Keep file operations minimal
   - Batch similar changes together
   - Use efficient search patterns

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
