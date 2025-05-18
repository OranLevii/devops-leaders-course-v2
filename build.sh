#!/bin/bash

# Exit on any error
set -e

echo "============================"
echo " Building the application"
echo "============================"

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
./run_tests.sh

# Verify the application can start
echo "Verifying application can start..."
uvicorn main:app --host 127.0.0.1 --port 8000 --no-access-log &
APP_PID=$!

# Wait for the application to start
sleep 5

# Check if the application is running
if ps -p $APP_PID > /dev/null; then
    echo "Application started successfully"
    # Kill the application
    kill $APP_PID
else
    echo "Application failed to start"
    exit 1
fi

echo "============================"
echo " Build completed successfully"
echo "============================" 