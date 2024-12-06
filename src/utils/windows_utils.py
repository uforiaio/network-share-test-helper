"""Windows-specific utilities and information gathering."""

import winreg
from typing import Dict, Any
from .logging import setup_logger

logger = setup_logger(__name__)

def get_windows_info() -> Dict[str, Any]:
    """Get Windows-specific information."""
    info = {}
    try:
        # Get SMB version
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                          r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters") as key:
            try:
                smb2, _ = winreg.QueryValueEx(key, "SMB2")
                info['smb2_enabled'] = bool(smb2)
            except FileNotFoundError:
                info['smb2_enabled'] = True  # Default is enabled
    except WindowsError as e:
        logger.warning(f"Failed to get SMB information: {e}")
        info['smb2_enabled'] = None
    
    return info

def get_network_shares() -> Dict[str, Any]:
    """Get mounted network shares."""
    # TODO: Implement using win32net or subprocess with 'net share' command
    return {}
