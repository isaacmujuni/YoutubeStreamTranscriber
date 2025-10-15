#!/bin/bash

# Stream Transcriber Startup Script

echo "🎵 Starting Stream Transcriber..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed. Audio processing may not work properly."
    echo "   Install FFmpeg:"
    echo "   macOS: brew install ffmpeg"
    echo "   Linux: sudo apt install ffmpeg"
    echo "   Windows: Download from https://ffmpeg.org/download.html"
    echo ""
fi

# Start the Streamlit app
echo "🚀 Starting Streamlit application..."
echo "   The app will open in your default web browser."
echo "   If it doesn't open automatically, go to: http://localhost:8501"
echo ""

# Run streamlit with virtual environment
streamlit run main.py
