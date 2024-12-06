import pkg_resources
import requests
import subprocess
import sys
from packaging import version
import json
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

def get_current_version() -> str:
    """Get the current version of the package."""
    try:
        return pkg_resources.get_distribution('dfs-nfs-debugger').version
    except pkg_resources.DistributionNotFound:
        return "0.0.0"

def get_latest_version() -> Optional[str]:
    """Check PyPI for the latest version of the package."""
    try:
        response = requests.get(
            "https://pypi.org/pypi/dfs-nfs-debugger/json",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()['info']['version']
    except Exception as e:
        logger.warning(f"Failed to check for latest version: {str(e)}")
    return None

def check_dependencies() -> Tuple[bool, list]:
    """
    Check if any dependencies need updating.
    Returns (needs_update: bool, outdated_packages: list)
    """
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json'],
            capture_output=True,
            text=True,
            check=True
        )
        outdated = json.loads(result.stdout)
        our_dependencies = pkg_resources.get_distribution('dfs-nfs-debugger').requires()
        our_dep_names = {dep.name for dep in our_dependencies}
        
        relevant_updates = [
            pkg for pkg in outdated
            if pkg['name'] in our_dep_names
        ]
        
        return bool(relevant_updates), relevant_updates
    except Exception as e:
        logger.warning(f"Failed to check dependencies: {str(e)}")
        return False, []

def update_dependencies() -> bool:
    """Update all dependencies to their latest versions."""
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', '-r', 'requirements.txt'],
            check=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to update dependencies: {str(e)}")
        return False

def update_application() -> bool:
    """Update the application to the latest version."""
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', 'dfs-nfs-debugger'],
            check=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to update application: {str(e)}")
        return False

def check_and_update() -> Tuple[bool, str]:
    """
    Check for updates and update if necessary.
    Returns (updated: bool, message: str)
    """
    current = get_current_version()
    latest = get_latest_version()
    
    if not latest:
        return False, "⚠️ Could not check for updates"
    
    needs_update = version.parse(latest) > version.parse(current)
    deps_need_update, outdated_deps = check_dependencies()
    
    if not needs_update and not deps_need_update:
        return False, "✅ Application and dependencies are up to date"
    
    messages = []
    if needs_update:
        messages.append(f"📦 Updating application from {current} to {latest}")
        if update_application():
            messages.append("✅ Application updated successfully")
        else:
            messages.append("❌ Failed to update application")
    
    if deps_need_update:
        dep_list = ", ".join(f"{pkg['name']} ({pkg['version']} → {pkg['latest_version']})"
                           for pkg in outdated_deps)
        messages.append(f"📚 Updating dependencies: {dep_list}")
        if update_dependencies():
            messages.append("✅ Dependencies updated successfully")
        else:
            messages.append("❌ Failed to update dependencies")
    
    return True, "\n".join(messages)

if __name__ == "__main__":
    updated, message = check_and_update()
    print(message)
