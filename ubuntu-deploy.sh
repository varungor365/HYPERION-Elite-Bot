#!/bin/bash

# 🚀 HYPERION Elite Bot - One-Click Ubuntu VPS Deployment
# This script will install and run the bot with minimal user interaction

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo -e "${BLUE}"
echo "████████████████████████████████████████████████████"
echo "█                                                  █"
echo "█    🚀 HYPERION Elite Bot - VPS Auto Deploy      █"
echo "█         One-Click Ubuntu Installation            █"
echo "█                                                  █"
echo "████████████████████████████████████████████████████"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "Please don't run this script as root. Run as regular user with sudo access."
   exit 1
fi

# Get user input for bot credentials
echo -e "\n${YELLOW}📋 Bot Configuration${NC}"
echo "================================================"

if [[ -z "$TELEGRAM_BOT_TOKEN" ]]; then
    echo -e "${BLUE}Enter your Telegram Bot Token (from @BotFather):${NC}"
    read -r TELEGRAM_BOT_TOKEN
fi

if [[ -z "$AUTHORIZED_USER_ID" ]]; then
    echo -e "${BLUE}Enter your Telegram User ID (send /start to @userinfobot):${NC}"
    read -r AUTHORIZED_USER_ID
fi

# Validate inputs
if [[ -z "$TELEGRAM_BOT_TOKEN" ]] || [[ -z "$AUTHORIZED_USER_ID" ]]; then
    print_error "Bot token and user ID are required!"
    exit 1
fi

print_success "Configuration received!"

# Update system
print_status "Updating Ubuntu system..."
sudo apt update -qq
sudo apt upgrade -y -qq

# Install dependencies
print_status "Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl wget htop \
    build-essential libssl-dev libffi-dev python3-dev \
    supervisor nginx ufw

# Install Docker (optional for advanced users)
print_status "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# Create bot directory
BOT_DIR="/opt/HYPERION-Elite-Bot"
print_status "Setting up bot directory: $BOT_DIR"

if [[ -d "$BOT_DIR" ]]; then
    print_warning "Directory exists, updating..."
    cd $BOT_DIR
    sudo git pull origin main
else
    sudo mkdir -p /opt
    cd /opt
    sudo git clone https://github.com/varungor365/HYPERION-Elite-Bot.git
fi

# Change ownership
sudo chown -R $USER:$USER $BOT_DIR
cd $BOT_DIR

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
print_status "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
print_status "Creating environment configuration..."
cat > .env << EOF
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
AUTHORIZED_USER_ID=$AUTHORIZED_USER_ID
LOG_LEVEL=INFO
MAX_WORKERS=50
ENABLE_PROXY_ROTATION=true
EOF

chmod 600 .env

# Create systemd service
print_status "Setting up systemd service..."
sudo tee /etc/systemd/system/hyperion-elite-bot.service > /dev/null << EOF
[Unit]
Description=HYPERION Elite Bot - Advanced MEGA Checker
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$BOT_DIR
Environment=PATH=$BOT_DIR/.venv/bin
EnvironmentFile=$BOT_DIR/.env
ExecStart=$BOT_DIR/.venv/bin/python hyperion_headless.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=hyperion-elite-bot

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$BOT_DIR /tmp
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
sudo mkdir -p /var/log/hyperion
sudo chown $USER:$USER /var/log/hyperion

# Setup log rotation
sudo tee /etc/logrotate.d/hyperion > /dev/null << 'EOF'
/var/log/hyperion/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    copytruncate
    su $USER $USER
}
EOF

# Configure firewall
print_status "Configuring firewall..."
sudo ufw --force enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Test bot functionality
print_status "Testing bot functionality..."
source .venv/bin/activate
export TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
export AUTHORIZED_USER_ID="$AUTHORIZED_USER_ID"

python3 -c "
import sys
sys.path.insert(0, '$BOT_DIR')
try:
    import hyperion_headless
    print('✅ Bot modules loaded successfully')
except Exception as e:
    print(f'❌ Bot test failed: {e}')
    sys.exit(1)
"

if [[ $? -ne 0 ]]; then
    print_error "Bot functionality test failed!"
    exit 1
fi

# Enable and start service
print_status "Starting HYPERION Elite Bot service..."
sudo systemctl daemon-reload
sudo systemctl enable hyperion-elite-bot
sudo systemctl start hyperion-elite-bot

# Wait a moment for service to start
sleep 3

# Check service status
if sudo systemctl is-active --quiet hyperion-elite-bot; then
    print_success "🎉 HYPERION Elite Bot is running!"
else
    print_error "Service failed to start. Checking logs..."
    sudo journalctl -u hyperion-elite-bot --no-pager -l
    exit 1
fi

# Create management scripts
print_status "Creating management scripts..."

# Status script
cat > hyperion-status.sh << 'EOF'
#!/bin/bash
echo "🤖 HYPERION Elite Bot Status"
echo "=================================="
sudo systemctl status hyperion-elite-bot --no-pager -l
echo -e "\n📊 System Resources:"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}')"
echo "RAM: $(free -h | awk 'NR==2{printf "%.1f/%.1fGB (%.2f%%)\n", $3/1024/1024/1024,$2/1024/1024/1024,$3*100/$2 }')"
echo "Disk: $(df -h / | awk 'NR==2{print $3"/"$2" ("$5")"}')"
echo -e "\n📋 Recent Logs:"
sudo journalctl -u hyperion-elite-bot -n 10 --no-pager
EOF

# Restart script  
cat > hyperion-restart.sh << 'EOF'
#!/bin/bash
echo "🔄 Restarting HYPERION Elite Bot..."
sudo systemctl restart hyperion-elite-bot
sleep 2
sudo systemctl status hyperion-elite-bot --no-pager -l
EOF

# Stop script
cat > hyperion-stop.sh << 'EOF'
#!/bin/bash
echo "⏹️ Stopping HYPERION Elite Bot..."
sudo systemctl stop hyperion-elite-bot
sudo systemctl status hyperion-elite-bot --no-pager -l
EOF

# Update script
cat > hyperion-update.sh << 'EOF'
#!/bin/bash
echo "📥 Updating HYPERION Elite Bot..."
cd /opt/HYPERION-Elite-Bot
sudo systemctl stop hyperion-elite-bot
git pull origin main
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
sudo systemctl start hyperion-elite-bot
echo "✅ Update complete!"
./hyperion-status.sh
EOF

chmod +x hyperion-*.sh

# Create backup script
cat > hyperion-backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/opt/hyperion-backup-$DATE.tar.gz"
echo "💾 Creating backup: $BACKUP_FILE"
tar -czf "$BACKUP_FILE" \
    /opt/HYPERION-Elite-Bot \
    /etc/systemd/system/hyperion-elite-bot.service \
    /var/log/hyperion \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude=".venv"
echo "✅ Backup created: $BACKUP_FILE"
# Keep only last 5 backups
find /opt -name "hyperion-backup-*.tar.gz" | sort -r | tail -n +6 | xargs rm -f
EOF

chmod +x hyperion-backup.sh

# Setup cron for health check and backups
print_status "Setting up automated maintenance..."
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/HYPERION-Elite-Bot/hyperion-status.sh > /dev/null 2>&1 || sudo systemctl restart hyperion-elite-bot") | crontab -
(crontab -l 2>/dev/null; echo "0 2 * * * /opt/HYPERION-Elite-Bot/hyperion-backup.sh") | crontab -

# Final success message
echo -e "\n${GREEN}"
echo "████████████████████████████████████████████████████"
echo "█                                                  █"
echo "█            🎉 DEPLOYMENT SUCCESSFUL! 🎉         █"
echo "█                                                  █"
echo "████████████████████████████████████████████████████"
echo -e "${NC}"

echo -e "\n${GREEN}✅ HYPERION Elite Bot is now running on your VPS!${NC}\n"

echo -e "${BLUE}📱 Bot Information:${NC}"
echo "   • Service Status: $(sudo systemctl is-active hyperion-elite-bot)"
echo "   • Bot Token: ${TELEGRAM_BOT_TOKEN:0:20}..."
echo "   • Authorized User: $AUTHORIZED_USER_ID"
echo "   • Installation Path: $BOT_DIR"
echo "   • Log Files: /var/log/hyperion/"

echo -e "\n${BLUE}🛠️ Management Commands:${NC}"
echo "   • Check Status: ./hyperion-status.sh"
echo "   • Restart Bot: ./hyperion-restart.sh" 
echo "   • Stop Bot: ./hyperion-stop.sh"
echo "   • Update Bot: ./hyperion-update.sh"
echo "   • Backup Bot: ./hyperion-backup.sh"

echo -e "\n${BLUE}📋 System Commands:${NC}"
echo "   • View Logs: sudo journalctl -u hyperion-elite-bot -f"
echo "   • Service Status: sudo systemctl status hyperion-elite-bot"
echo "   • Restart Service: sudo systemctl restart hyperion-elite-bot"

echo -e "\n${BLUE}📱 Telegram Bot Commands:${NC}"
echo "   • /start - Initialize bot"
echo "   • /status - System status with resource optimizer"
echo "   • /scan - AI analyze combo file (A-Z sorted)"
echo "   • /check - Start elite checking with optimized threads"
echo "   • /addcombos - Add combos during checking"
echo "   • /stop - Stop and get results"
echo "   • /results - Download hit files"

echo -e "\n${YELLOW}🔔 Next Steps:${NC}"
echo "   1. Open Telegram and send /start to your bot"
echo "   2. Upload a combo file and use /scan"
echo "   3. Use /check to start checking with resource optimization"
echo "   4. Monitor with ./hyperion-status.sh"

echo -e "\n${GREEN}🎖️ Your HYPERION Elite Bot v5.1 is ready for production!${NC}"
echo -e "${BLUE}💡 Features enabled: Resource Optimizer, AI Analyzer, A-Z Sorting, Dynamic Combo Addition${NC}"

# Show current status
print_status "Current bot status:"
sudo systemctl status hyperion-elite-bot --no-pager -l