#!/bin/bash

# CCTV Analyzer - Quick Setup Script
# This script sets up the environment and launches the application

echo "🎥 CCTV Analyzer - Setup Script"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8+
required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.8 or higher is required"
    exit 1
fi

echo "✅ Python version is compatible"
echo ""

# Create virtual environment (optional but recommended)
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

echo ""
echo "================================"
echo "🎉 Setup Complete!"
echo "================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Get your Google AI Studio API key:"
echo "   👉 https://aistudio.google.com/"
echo ""
echo "2. Prepare a sample CCTV video (MP4, AVI, MOV, or MKV)"
echo ""
echo "3. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "4. Open your browser at http://localhost:8501"
echo ""
echo "================================"
echo ""

# Ask if user wants to launch now
read -p "Would you like to launch the app now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Launching CCTV Analyzer..."
    streamlit run app.py
fi
