#!/bin/bash
# Sleep Quality Assessment - Quick Start Script for Linux/Mac

echo ""
echo "========================================"
echo "  Sleep Quality Assessment System"
echo "  Quick Start for Linux/Mac"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found"
    echo "Please run this script from the project directory"
    exit 1
fi

echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Dependencies installed successfully"
echo ""

# Check if model exists
if [ ! -f "sleep_model.h5" ]; then
    echo "WARNING: sleep_model.h5 not found"
    echo "The model file is required for predictions"
    echo "Please ensure it's in the project directory"
fi

echo ""
echo "========================================"
echo "  Starting Sleep Quality Assessment"
echo "========================================"
echo ""
echo "Opening browser to: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start Flask app
sleep 2
python3 app.py
