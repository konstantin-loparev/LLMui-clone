# Check if Python is installed
$pythonInstalled = & python --version 2>$null
if (-not $?) {
    Write-Output "Python is not installed."
    
    # Check CPU architecture
    $arch = if ($env:PROCESSOR_ARCHITECTURE -eq "AMD64") { "amd64" } else { "x86" }

    # Download and install Python silently
    Write-Output "Downloading Python..."
    
    $pythonInstaller = if ($arch -eq "amd64") {
        "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
    } else {
        "https://www.python.org/ftp/python/3.11.5/python-3.11.5.exe"
    }

    Invoke-WebRequest -Uri $pythonInstaller -OutFile "python_installer.exe"

    Write-Output "Installing Python..."
    Start-Process -FilePath "python_installer.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    # Add Python to PATH
    $pythonDir = "C:\Program Files\Python311"
    [Environment]::SetEnvironmentVariable("PATH", "$pythonDir;$pythonDir\Scripts;[System.Environment]::GetEnvironmentVariable('PATH','Machine')", "Machine")
    $env:PATH = "$pythonDir;$pythonDir\Scripts;$env:PATH"

    # Cleanup installer
    Remove-Item -Force "python_installer.exe"
}

# Check if venv folder exists, if not create it
if (-not (Test-Path -Path "venv")) {
    Write-Output "Creating virtual environment..."
    & python -m venv venv
}

# Activate virtual environment
Write-Output "Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# Install requirements if requirements.txt exists
if (Test-Path -Path "requirements.txt") {
    Write-Output "Installing dependencies..."
    & pip install -r requirements.txt
}

# Run the Flask application
Write-Output "Running the Flask application..."
& python app.py

# Open browser to the Flask application URL
# Replace "http://127.0.0.1:5000" with the actual URL if different
Start-Process "http://127.0.0.1:5000"
