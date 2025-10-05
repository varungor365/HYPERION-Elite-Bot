#!/bin/bash

# 🚀 HYPERION Elite Bot - Fixed Dependency Installation
# Resolves mega.py and tenacity version conflicts

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo -e "${BLUE}"
echo "████████████████████████████████████████████████████"
echo "█                                                  █"
echo "█    🚀 HYPERION Elite Bot - Fixed Install        █"
echo "█         Dependency Conflict Resolution          █"
echo "█                                                  █"
echo "████████████████████████████████████████████████████"
echo -e "${NC}"

# Update system
print_status "Updating Ubuntu system..."
apt update -qq && apt upgrade -y -qq

# Install system dependencies
print_status "Installing system dependencies..."
apt install -y python3 python3-pip python3-venv git curl wget \
    build-essential libssl-dev libffi-dev python3-dev

# Setup bot directory
BOT_DIR="/opt/HYPERION-Elite-Bot"
print_status "Setting up bot in $BOT_DIR"

if [[ -d "$BOT_DIR" ]]; then
    cd $BOT_DIR && git pull origin main
else
    cd /opt && git clone https://github.com/varungor365/HYPERION-Elite-Bot.git
fi

cd $BOT_DIR

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Upgrade pip first
print_status "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install core dependencies first (to resolve conflicts)
print_status "Installing core dependencies..."
pip install python-telegram-bot==22.5

# Install mega.py with relaxed constraints
print_status "Installing mega.py with compatible tenacity..."
pip install "tenacity>=5.1.5,<6.0.0"
pip install mega.py==1.0.8

# Install remaining dependencies
print_status "Installing remaining dependencies..."
pip install requests>=2.31.0
pip install urllib3>=1.26.0,<2.0.0
pip install aiohttp>=3.12.0
pip install aiofiles>=23.2.0
pip install httpx>=0.25.0
pip install python-dotenv>=1.0.0
pip install cryptography>=41.0.0
pip install PySocks>=1.7.1
pip install colorama>=0.4.6
pip install tqdm==4.66.1
pip install rich==13.7.0
pip install backoff==2.2.1
pip install bcrypt==4.1.2
pip install loguru==0.7.2

print_success "All dependencies installed successfully!"

# Create configuration
print_status "Setting up configuration..."
if [[ ! -f ".env" ]]; then
    cp config.env.example .env
    print_success "Configuration file created"
fi

# Create systemd service
print_status "Installing systemd service..."
cat > /etc/systemd/system/hyperion-elite-bot.service << 'EOF'
[Unit]
Description=HYPERION Elite Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/HYPERION-Elite-Bot
Environment=PATH=/opt/HYPERION-Elite-Bot/.venv/bin
ExecStart=/opt/HYPERION-Elite-Bot/.venv/bin/python hyperion_headless.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable hyperion-elite-bot
systemctl start hyperion-elite-bot

print_success "HYPERION Elite Bot installed and started!"
print_status "Service status:"
systemctl status hyperion-elite-bot --no-pager -l

print_success "Installation complete! Bot is running."
print_status "To check logs: journalctl -u hyperion-elite-bot -f"
print_status "To restart: systemctl restart hyperion-elite-bot"