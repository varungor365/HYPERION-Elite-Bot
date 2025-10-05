#!/bin/bash

# 🚀 HYPERION Elite Bot - Terminal Runner
# Use this script to run the bot directly in terminal

set -e

echo "🚀 HYPERION Elite Bot - Terminal Runner"
echo "======================================"

# Check if we're in the right directory
if [[ ! -f "hyperion_headless.py" ]]; then
    echo "❌ Error: hyperion_headless.py not found!"
    echo "📁 Please run this from the bot directory:"
    echo "   cd /opt/HYPERION-Elite-Bot"
    echo "   ./run_bot_terminal.sh"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check virtual environment
if [[ -d ".venv" ]]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️ No virtual environment found, using system Python"
fi

# Test the bot first
echo "🧪 Testing bot configuration..."
python3 run_bot_debug.py

if [[ $? -eq 0 ]]; then
    echo ""
    echo "🎯 Starting HYPERION Elite Bot in terminal..."
    echo "📝 Press Ctrl+C to stop the bot"
    echo ""
    
    # Run the bot
    python3 hyperion_headless.py
else
    echo ""
    echo "❌ Bot test failed! Please check the errors above."
    exit 1
fi