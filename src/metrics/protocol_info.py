"""Protocol information collection and analysis."""

import json
from datetime import datetime, timezone
from ..utils.logging import setup_logger

logger = setup_logger(__name__)

class ProtocolInfo:
    """Collects and analyzes protocol-specific information."""
    
    def __init__(self):
        """Initialize protocol information collection."""
        self.protocol_type = None  # SMB or NFS
        self.protocol_version = None
        self.features = {}
        self.capabilities = {}
        self.security_info = {}
        self.dialect_info = {}
        self.connection_info = {}
        
    def set_protocol_type(self, protocol_type, version=None):
        """Set the protocol type and version."""
        self.protocol_type = protocol_type
        if version:
            self.protocol_version = version
            
    def add_feature(self, feature_name, enabled=True):
        """Add protocol feature information."""
        self.features[feature_name] = {
            "enabled": enabled,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_capability(self, capability_name, value):
        """Add protocol capability information."""
        self.capabilities[capability_name] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_security_info(self, key, value):
        """Add security-related information."""
        self.security_info[key] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_dialect_info(self, dialect, negotiated=False):
        """Add SMB dialect information."""
        self.dialect_info[dialect] = {
            "negotiated": negotiated,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def add_connection_info(self, key, value):
        """Add connection-specific information."""
        self.connection_info[key] = {
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
    def get_info(self):
        """Get all protocol information."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "protocol": {
                "type": self.protocol_type,
                "version": self.protocol_version
            },
            "features": self.features,
            "capabilities": self.capabilities,
            "security": self.security_info,
            "dialects": self.dialect_info,
            "connection": self.connection_info
        }
        
    def reset(self):
        """Reset all protocol information."""
        self.__init__()
