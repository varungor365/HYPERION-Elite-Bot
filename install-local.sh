#!/bin/bash

# 🚀 HYPERION Elite Bot - Local VM Installer
# Use this if you've already downloaded the repository

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 HYPERION Elite Bot - Local Installation"
echo "=========================================="
echo "📁 Installing from: $SCRIPT_DIR"

# Check if we're in the right directory
if [[ ! -f "hyperion_headless.py" ]]; then
    echo "❌ Error: This doesn't appear to be the HYPERION Elite Bot directory!"
    echo "📂 Please run this script from the bot directory or download it first."
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found!"
    echo "📦 Please install Python3 first:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "   Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
echo "✅ Virtual environment activated"

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install python-telegram-bot==22.5
pip install aiohttp aiofiles httpx pandas numpy
pip install python-dotenv cryptography PySocks colorama
pip install requests "urllib3<2.0.0,>=1.26.0"
pip install "tenacity>=8.0.0,<9.0.0"
pip install mega.py==1.0.8 --no-deps
pip install pycryptodome pathlib tqdm rich backoff bcrypt loguru psutil

echo "✅ Dependencies installed"

# Test installation
echo "🧪 Testing installation..."
python3 -c "
try:
    from telegram import Bot
    import hyperion_config
    print('✅ All imports successful!')
except Exception as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Make scripts executable
chmod +x *.sh *.py 2>/dev/null || true

# Create run script
cat > run-bot.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
echo "🚀 Starting HYPERION Elite Bot..."
echo "📝 Press Ctrl+C to stop the bot"
python3 hyperion_headless.py
EOF

chmod +x run-bot.sh

echo ""
echo "🎉 Installation Complete!"
echo "========================="
echo ""
echo "🚀 To start the bot:"
echo "   ./run-bot.sh"
echo ""
echo "🔧 To test the bot:"
echo "   ./run_bot_debug.py"
echo ""
echo "📱 Telegram Bot: @megacheckk_bot"
echo "🔑 Bot Token: Pre-configured (no setup needed!)"
echo ""
echo "✨ Your HYPERION Elite Bot is ready!"