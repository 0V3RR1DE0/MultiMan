# Prompt for admin rights if not already elevated
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires administrative privileges to run."
    Write-Host "Restarting script with elevated privileges..."
    Start-Sleep -s 2
    Start-Process -FilePath powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    Exit
}

# Define variables
$repoUrl = "https://github.com/0V3RR1DE0/Quanta/archive/refs/heads/main.zip"
$installDir = "C:\Program Files\Quanta"
$startMenuShortcut = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Quanta.lnk"
$cmdFile = "$installDir\quanta.cmd"
$requirementsFile = "$installDir\requirements.txt"

# Create a function to log messages
function Log {
    param ([string]$message)
    Write-Output $message
}

# Download and extract the repository
Log "Downloading Quanta from GitHub..."
$zipPath = "$env:TEMP\quanta.zip"
Invoke-WebRequest -Uri $repoUrl -OutFile $zipPath

Log "Extracting Quanta..."
Expand-Archive -Path $zipPath -DestinationPath $env:TEMP

# Move files to the installation directory
Log "Installing Quanta..."
New-Item -Path $installDir -ItemType Directory -Force
Copy-Item -Path "$env:TEMP\Quanta-main\*" -Destination $installDir -Recurse -Force

# Create requirements.txt
Log "Creating requirements.txt..."
@"
argparse
importlib-metadata
setproctitle
"@ | Set-Content -Path $requirementsFile

# Install Python dependencies
Log "Installing Python dependencies..."
& "$env:SYSTEMROOT\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "& {pip install -r '$requirementsFile'}"

# Create the CMD file
Log "Creating CMD file..."
$cmdContent = "@echo off`npython $installDir\quanta.py %*"
Set-Content -Path $cmdFile -Value $cmdContent

# Add the installation directory to PATH
Log "Adding Quanta to PATH..."
$envPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
if ($envPath -notlike "*$installDir*") {
    [System.Environment]::SetEnvironmentVariable("Path", "$envPath;$installDir", [System.EnvironmentVariableTarget]::Machine)
}

# Create a Start Menu shortcut
Log "Creating Start Menu shortcut..."
$wshShell = New-Object -ComObject WScript.Shell
$shortcut = $wshShell.CreateShortcut($startMenuShortcut)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$installDir\quanta.py`""
$shortcut.IconLocation = "powershell.exe,0"
$shortcut.Save()

# Clean up
Log "Cleaning up..."
Remove-Item -Path $zipPath
Remove-Item -Path "$env:TEMP\Quanta-main" -Recurse

Log "Installation complete. You can now run 'quanta' from the command line."

pause
