#!/bin/bash

# Quick Start Script for Google Play Store ETL Pipeline
# This script sets up and runs the pipeline

set -e  # Exit on error

echo "=========================================="
echo "Google Play Store ETL Pipeline Setup"
echo "=========================================="
echo ""

# Check Python version
echo "[1/5] Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "[2/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "[3/5] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "[4/5] Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check for data files
echo ""
echo "[5/5] Checking for data files..."
if [ -f "data/apps_data.csv" ] && [ -f "data/review_data.csv" ]; then
    echo "✓ Data files found"
    
    # Run the pipeline
    echo ""
    echo "=========================================="
    echo "Running ETL Pipeline"
    echo "=========================================="
    echo ""
    
    cd src
    python pipeline.py
    cd ..
    
    echo ""
    echo "=========================================="
    echo "Pipeline Completed Successfully!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "  - Check logs in: logs/"
    echo "  - Query database: sqlite3 data/playstore.db"
    echo "  - Run examples: python examples/usage_examples.py"
    echo ""
else
    echo "✗ Data files not found!"
    echo ""
    echo "Please place the following files in the data/ directory:"
    echo "  - apps_data.csv"
    echo "  - review_data.csv"
    echo ""
    echo "Then run this script again."
    exit 1
fi
