#!/bin/bash
# HYPERION Elite Bot - VPS Quick Start Script

set -e

echo "🚀 HYPERION Elite Bot - VPS Deployment Starting..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}==== $1 ====${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   print_status "Please run as a regular user with sudo privileges"
   exit 1
fi

print_header "System Information"
echo "OS: $(lsb_release -d 2>/dev/null | cut -f2 || echo "$(uname -s) $(uname -r)")"
echo "Architecture: $(uname -m)"
echo "CPU Cores: $(nproc)"
echo "Memory: $(free -h | grep '^Mem:' | awk '{print $2}')"
echo "Disk Space: $(df -h / | tail -1 | awk '{print $4}') available"

print_header "Step 1: Installing System Dependencies"

# Detect package manager
if command -v apt-get &> /dev/null; then
    print_status "Detected Debian/Ubuntu system"
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv git curl wget htop
elif command -v yum &> /dev/null; then
    print_status "Detected RHEL/CentOS system"
    sudo yum update -y
    sudo yum install -y python3 python3-pip git curl wget htop
elif command -v dnf &> /dev/null; then
    print_status "Detected Fedora system"
    sudo dnf update -y
    sudo dnf install -y python3 python3-pip git curl wget htop
elif command -v apk &> /dev/null; then
    print_status "Detected Alpine Linux system"
    sudo apk update
    sudo apk add python3 py3-pip git curl wget htop gcc musl-dev
else
    print_error "Unsupported package manager. Please install Python 3, pip, and git manually."
    exit 1
fi

print_header "Step 2: Python Version Check"
PYTHON_VERSION=$(python3 --version | cut -d" " -f2 | cut -d"." -f1-2)
print_status "Python version: $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION >= 3.11" | bc -l 2>/dev/null || echo "0") -eq 1 ]] || [[ "$PYTHON_VERSION" == "3.11" ]] || [[ "$PYTHON_VERSION" == "3.12" ]]; then
    print_status "Python version is compatible ✓"
else
    print_warning "Python 3.11+ recommended. Current: $PYTHON_VERSION"
fi

print_header "Step 3: Setting up HYPERION Elite Bot"

# Create installation directory
INSTALL_DIR="/opt/HYPERION-Elite-Bot"
if [ ! -d "$INSTALL_DIR" ]; then
    print_status "Creating installation directory: $INSTALL_DIR"
    sudo mkdir -p "$INSTALL_DIR"
    sudo chown "$USER:$USER" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Clone or update repository
if [ -d ".git" ]; then
    print_status "Updating existing installation..."
    git pull origin main
else
    print_status "Cloning repository..."
    git clone https://github.com/varungor365/HYPERION-Elite-Bot.git .
fi

print_header "Step 4: Setting up Python Virtual Environment"

# Create virtual environment
if [ ! -d ".venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv .venv
fi

print_status "Activating virtual environment..."
source .venv/bin/activate

print_status "Upgrading pip..."
pip install --upgrade pip

print_header "Step 5: Installing Python Dependencies"
print_status "Installing dependencies from requirements.txt..."

# Install dependencies with timeout and retries
pip install --timeout 300 --retries 3 -r requirements.txt

print_header "Step 6: Configuration Setup"

# Create environment file template
if [ ! -f ".env" ]; then
    print_status "Creating environment configuration file..."
    cat > .env << 'EOF'
# HYPERION Elite Bot Configuration
# Copy this file and set your actual values

# Required: Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Required: Your Telegram user ID (get from @userinfobot)
AUTHORIZED_USER_ID=your_telegram_user_id_here

# Optional: Performance settings
MAX_THREADS=100
DEFAULT_RATE_LIMIT=1.0
LOG_LEVEL=INFO

# Optional: Proxy settings
ENABLE_PROXY_ROTATION=true
MAX_PROXIES=500
EOF
    chmod 600 .env
    print_warning "Please edit .env file with your bot token and user ID!"
fi

# Create systemd service
print_header "Step 7: Setting up System Service"

SERVICE_FILE="/etc/systemd/system/hyperion-elite-bot.service"
print_status "Creating systemd service..."

sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=HYPERION Elite Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/.venv/bin
EnvironmentFile=$INSTALL_DIR/.env
ExecStart=$INSTALL_DIR/.venv/bin/python hyperion_headless.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
print_status "Setting up logging..."
sudo mkdir -p /var/log/hyperion
sudo chown "$USER:$USER" /var/log/hyperion

print_header "Step 8: Testing Installation"

print_status "Testing Python imports..."
.venv/bin/python -c "
import sys
sys.path.insert(0, '$INSTALL_DIR')

modules = ['mega_auth', 'checker_engine', 'hyperion_elite_bot']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module} imported successfully')
    except Exception as e:
        print(f'❌ {module} error: {e}')
        
print('✅ Import test complete!')
"

print_header "Step 9: Service Management"

print_status "Reloading systemd daemon..."
sudo systemctl daemon-reload

print_status "Enabling HYPERION Elite Bot service..."
sudo systemctl enable hyperion-elite-bot

print_header "🎉 Installation Complete!"

echo ""
echo -e "${GREEN}✅ HYPERION Elite Bot has been successfully installed!${NC}"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Edit configuration: nano $INSTALL_DIR/.env"
echo "2. Add your Telegram bot token and user ID"
echo "3. Start the bot: sudo systemctl start hyperion-elite-bot"
echo "4. Check status: sudo systemctl status hyperion-elite-bot"
echo "5. View logs: sudo journalctl -u hyperion-elite-bot -f"
echo ""
echo -e "${BLUE}🔧 Useful Commands:${NC}"
echo "• Start bot: sudo systemctl start hyperion-elite-bot"
echo "• Stop bot: sudo systemctl stop hyperion-elite-bot"
echo "• Restart bot: sudo systemctl restart hyperion-elite-bot"
echo "• Check status: sudo systemctl status hyperion-elite-bot"
echo "• View logs: sudo journalctl -u hyperion-elite-bot -f"
echo "• Update bot: cd $INSTALL_DIR && git pull && sudo systemctl restart hyperion-elite-bot"
echo ""
echo -e "${BLUE}📊 System Resources:${NC}"
echo "• Monitor resources: htop"
echo "• Check disk space: df -h"
echo "• Check memory: free -h"
echo ""
echo -e "${YELLOW}⚠️ Important:${NC}"
echo "• Configure your bot token in $INSTALL_DIR/.env"
echo "• The bot is set to auto-start on system boot"
echo "• Resource optimizer will automatically adjust threads based on your system"
echo "• All features include A-Z sorting, duplicate removal, and intelligent monitoring"
echo ""
echo -e "${GREEN}🚀 Ready to deploy! Configure your bot token and start the service.${NC}"