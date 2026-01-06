#!/bin/bash

# Pegasus Info Quick Start Script

echo "=========================================="
echo "PEGASUS INFO - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi
echo "✅ Python is installed"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✅ Dependencies installed"
echo ""

# Run basic tests
echo "Running basic tests..."
python3 test_basic.py
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi
echo ""

# Run example
echo "Running example usage..."
python3 example.py
echo ""

echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To run Pegasus Info:"
echo "  python3 pegasus_info.py"
echo ""
echo "For more options:"
echo "  python3 pegasus_info.py --help"
echo ""
