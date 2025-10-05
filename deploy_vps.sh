#!/bin/bash

# HYPERION Elite Bot VPS Deployment Script
# ========================================
# Automated deployment for production VPS servers

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
HYPERION_USER="hyperion"
HYPERION_HOME="/opt/hyperion-elite-bot"
LOG_DIR="/var/log/hyperion"
SERVICE_NAME="hyperion-elite-bot"

echo -e "${BLUE}"
echo "🚀 HYPERION ELITE BOT - VPS DEPLOYMENT"
echo "======================================"
echo "Production Server Setup & Configuration"
echo -e "${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

print_status "Starting HYPERION Elite Bot VPS deployment..."

# Update system packages
print_status "Updating system packages..."
if command -v apt-get &> /dev/null; then
    apt-get update && apt-get upgrade -y
    apt-get install -y python3 python3-pip python3-venv git curl wget unzip
elif command -v yum &> /dev/null; then
    yum update -y
    yum install -y python3 python3-pip python3-venv git curl wget unzip
elif command -v apk &> /dev/null; then
    apk update && apk upgrade
    apk add python3 py3-pip python3-dev git curl wget unzip build-base
else
    print_error "Unsupported package manager. Please install manually: python3, pip, git, curl, wget, unzip"
    exit 1
fi

# Create hyperion user
print_status "Creating hyperion system user..."
if ! id "$HYPERION_USER" &>/dev/null; then
    useradd -r -s /bin/bash -d "$HYPERION_HOME" "$HYPERION_USER"
    print_status "User $HYPERION_USER created"
else
    print_warning "User $HYPERION_USER already exists"
fi

# Create directories
print_status "Creating directory structure..."
mkdir -p "$HYPERION_HOME"
mkdir -p "$LOG_DIR"
chown -R "$HYPERION_USER:$HYPERION_USER" "$HYPERION_HOME"
chown -R "$HYPERION_USER:$HYPERION_USER" "$LOG_DIR"

# Clone or update repository
print_status "Setting up HYPERION codebase..."
if [ -d "$HYPERION_HOME/.git" ]; then
    print_status "Updating existing repository..."
    cd "$HYPERION_HOME"
    sudo -u "$HYPERION_USER" git pull
else
    print_status "Cloning repository..."
    sudo -u "$HYPERION_USER" git clone https://github.com/yourusername/HYPERION-Elite-Bot.git "$HYPERION_HOME"
    cd "$HYPERION_HOME"
fi

# Setup Python virtual environment
print_status "Creating Python virtual environment..."
sudo -u "$HYPERION_USER" python3 -m venv "$HYPERION_HOME/venv"

# Install Python dependencies
print_status "Installing Python dependencies..."
sudo -u "$HYPERION_USER" "$HYPERION_HOME/venv/bin/pip" install --upgrade pip
sudo -u "$HYPERION_USER" "$HYPERION_HOME/venv/bin/pip" install -r "$HYPERION_HOME/requirements.txt"

# Setup configuration
print_status "Configuring HYPERION Elite Bot..."
if [ ! -f "$HYPERION_HOME/.env" ]; then
    print_status "Creating environment configuration..."
    cat > "$HYPERION_HOME/.env" << EOF
# HYPERION Elite Bot Configuration
# Replace with your actual values

# Telegram Bot Token (required)
TELEGRAM_TOKEN=your_telegram_token_here

# Authorized Users (comma-separated Telegram user IDs)
AUTHORIZED_USERS=796354588

# Security Settings
MEGA_TIMEOUT=30
MAX_THREADS=8

# Optional: Proxy Configuration
# PROXY_ENABLED=true
# PROXY_LIST=proxy1:port,proxy2:port

# Logging Level
LOG_LEVEL=INFO
EOF
    chown "$HYPERION_USER:$HYPERION_USER" "$HYPERION_HOME/.env"
    print_warning "Please edit $HYPERION_HOME/.env with your actual configuration"
fi

# Install systemd service
print_status "Installing systemd service..."
cp "$HYPERION_HOME/$SERVICE_NAME.service" "/etc/systemd/system/"
systemctl daemon-reload

# Setup logrotate
print_status "Configuring log rotation..."
cat > "/etc/logrotate.d/hyperion-elite-bot" << EOF
$LOG_DIR/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $HYPERION_USER $HYPERION_USER
    postrotate
        systemctl reload-or-restart $SERVICE_NAME
    endscript
}
EOF

# Setup firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    print_status "Configuring firewall..."
    ufw allow ssh
    ufw allow 80/tcp
    ufw allow 443/tcp
    # Add any other ports your bot needs
fi

# Enable and start service
print_status "Enabling and starting HYPERION Elite Bot service..."
systemctl enable "$SERVICE_NAME"

# Final security check
print_status "Applying security settings..."
chmod 600 "$HYPERION_HOME/.env"
chmod +x "$HYPERION_HOME/hyperion_headless.py"

# Installation complete
echo -e "${GREEN}"
echo "✅ HYPERION ELITE BOT DEPLOYMENT COMPLETE!"
echo "=========================================="
echo -e "${NC}"

print_status "Deployment Summary:"
echo "   📁 Install Path: $HYPERION_HOME"
echo "   📝 Log Directory: $LOG_DIR"
echo "   👤 Service User: $HYPERION_USER"
echo "   🔧 Service Name: $SERVICE_NAME"

echo
print_status "Next Steps:"
echo "1. Edit configuration: sudo nano $HYPERION_HOME/.env"
echo "2. Start the service: sudo systemctl start $SERVICE_NAME"
echo "3. Check status: sudo systemctl status $SERVICE_NAME"
echo "4. View logs: sudo journalctl -u $SERVICE_NAME -f"

echo
print_status "Service Management Commands:"
echo "   Start:   sudo systemctl start $SERVICE_NAME"
echo "   Stop:    sudo systemctl stop $SERVICE_NAME"
echo "   Restart: sudo systemctl restart $SERVICE_NAME"
echo "   Status:  sudo systemctl status $SERVICE_NAME"
echo "   Logs:    sudo journalctl -u $SERVICE_NAME -f"

echo
print_warning "IMPORTANT: Configure your .env file before starting the service!"
print_status "Edit: sudo nano $HYPERION_HOME/.env"

echo -e "${BLUE}"
echo "🎯 HYPERION Elite Bot is ready for production!"
echo "Deploy with confidence. Elite performance guaranteed."
echo -e "${NC}"