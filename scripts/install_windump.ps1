# Install WinDump script
$ErrorActionPreference = 'Stop'

# Function to safely download a file
function Download-File {
    param(
        [string]$Url,
        [string]$OutFile
    )
    
    # Remove existing file if it exists
    if (Test-Path $OutFile) {
        try {
            Remove-Item $OutFile -Force
        } catch {
            Write-Warning "Could not remove existing file: $_"
            return $false
        }
    }
    
    try {
        Invoke-WebRequest -Uri $Url -OutFile $OutFile
        return $true
    } catch {
        Write-Warning "Failed to download file: $_"
        return $false
    }
}

# Create WinDump directory
$windumpDir = "C:\Program Files\WinDump"
if (-not (Test-Path $windumpDir)) {
    New-Item -ItemType Directory -Path $windumpDir -Force
}

Write-Host "WinPcap is already installed, proceeding with WinDump installation..."

# Download WinDump
$windumpUrl = "https://www.winpcap.org/windump/install/bin/windump_3_9_5/WinDump.exe"
$windumpExe = Join-Path $windumpDir "WinDump.exe"

if (Download-File -Url $windumpUrl -OutFile $windumpExe) {
    Write-Host "WinDump downloaded successfully"
} else {
    Write-Error "Failed to download WinDump"
    exit 1
}

# Add WinDump to PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if (-not $currentPath.Contains($windumpDir)) {
    try {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$windumpDir", "Machine")
        Write-Host "Added WinDump to system PATH"
    } catch {
        Write-Warning "Failed to add WinDump to PATH: $_"
    }
}

Write-Host "WinDump installation complete. Please restart your terminal for PATH changes to take effect."
