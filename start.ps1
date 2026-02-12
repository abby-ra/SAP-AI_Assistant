# SAP AI Assistant - Startup Script
# This script installs dependencies and starts the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SAP AI Assistant - Starting Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Display Python version
$pythonVersion = python --version
Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install/upgrade dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Start the application
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting FastAPI Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Application will be available at:" -ForegroundColor Green
Write-Host "  → http://localhost:8000" -ForegroundColor Cyan
Write-Host "  → API Health: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "  → API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the application
python run_backend.py
