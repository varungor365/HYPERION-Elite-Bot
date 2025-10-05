#!/bin/bash

# HYPERION Elite Bot - VPS Deployment Script
# Supports Ubuntu 20.04+, Debian 10+, CentOS 8+

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BOT_USER="hyperion"
BOT_DIR="/opt/hyperion-elite-bot"
SERVICE_NAME="hyperion-elite-bot"

echo -e "${BLUE}🚀 HYPERION Elite Bot VPS Deployment${NC}"
echo "========================================"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ This script must be run as root${NC}"
   exit 1
fi

# Detect OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VERSION=$VERSION_ID
else
    echo -e "${RED}❌ Cannot detect OS version${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Detected OS: $OS $VERSION${NC}"

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    apt update && apt upgrade -y
    apt install -y python3 python3-pip python3-venv git curl wget unzip
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
    yum update -y
    yum install -y python3 python3-pip git curl wget unzip
else
    echo -e "${RED}❌ Unsupported OS: $OS${NC}"
    exit 1
fi

# Create bot user
echo -e "${YELLOW}👤 Creating bot user...${NC}"
if ! id "$BOT_USER" &>/dev/null; then
    useradd -r -s /bin/bash -d $BOT_DIR $BOT_USER
    echo -e "${GREEN}✅ User $BOT_USER created${NC}"
else
    echo -e "${YELLOW}⚠️ User $BOT_USER already exists${NC}"
fi

# Create directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p $BOT_DIR/{logs,data,hits,backups}
chown -R $BOT_USER:$BOT_USER $BOT_DIR

# Clone repository
echo -e "${YELLOW}📥 Cloning HYPERION repository...${NC}"
cd /tmp
if [[ -d "HYPERION-Elite-Bot" ]]; then
    rm -rf HYPERION-Elite-Bot
fi
git clone https://github.com/varungor365/HYPERION-Elite-Bot.git
cp -r HYPERION-Elite-Bot/* $BOT_DIR/
chown -R $BOT_USER:$BOT_USER $BOT_DIR

# Setup Python environment
echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
cd $BOT_DIR
sudo -u $BOT_USER python3 -m venv venv
sudo -u $BOT_USER ./venv/bin/pip install --upgrade pip
sudo -u $BOT_USER ./venv/bin/pip install -r requirements.txt

# Configure environment
echo -e "${YELLOW}⚙️ Configuring environment...${NC}"
if [[ ! -f "$BOT_DIR/.env" ]]; then
    cp $BOT_DIR/.env.example $BOT_DIR/.env
    echo -e "${RED}❗ Please edit $BOT_DIR/.env with your configuration${NC}"
    echo -e "${YELLOW}Required variables:${NC}"
    echo "  - TELEGRAM_BOT_TOKEN"
    echo "  - AUTHORIZED_USER_ID"
    read -p "Press Enter to continue after editing .env file..."
fi

# Create systemd service
echo -e "${YELLOW}🔧 Creating systemd service...${NC}"
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=HYPERION Elite Bot
After=network.target
Wants=network.target

[Service]
Type=simple
User=$BOT_USER
Group=$BOT_USER
WorkingDirectory=$BOT_DIR
Environment=PATH=$BOT_DIR/venv/bin
ExecStart=$BOT_DIR/venv/bin/python hyperion_elite_bot.py
ExecReload=/bin/kill -HUP \$MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=hyperion-elite-bot

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$BOT_DIR

[Install]
WantedBy=multi-user.target
EOF

# Setup log rotation
echo -e "${YELLOW}📝 Setting up log rotation...${NC}"
cat > /etc/logrotate.d/$SERVICE_NAME << EOF
$BOT_DIR/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 $BOT_USER $BOT_USER
    postrotate
        systemctl reload $SERVICE_NAME
    endscript
}
EOF

# Setup firewall (if UFW is available)
if command -v ufw &> /dev/null; then
    echo -e "${YELLOW}🔥 Configuring firewall...${NC}"
    ufw allow ssh
    ufw allow 8080/tcp
    ufw --force enable
fi

# Setup backup script
echo -e "${YELLOW}💾 Setting up backup script...${NC}"
cat > $BOT_DIR/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/hyperion-elite-bot/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="hyperion_backup_$DATE.tar.gz"

# Create backup
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude="venv" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude="logs/*.log" \
    -C /opt hyperion-elite-bot

# Keep only last 7 backups
find "$BACKUP_DIR" -name "hyperion_backup_*.tar.gz" -mtime +7 -delete

echo "Backup created: $BACKUP_FILE"
EOF

chmod +x $BOT_DIR/backup.sh
chown $BOT_USER:$BOT_USER $BOT_DIR/backup.sh

# Setup cron for backups
echo -e "${YELLOW}⏰ Setting up automated backups...${NC}"
crontab -u $BOT_USER -l 2>/dev/null | { cat; echo "0 2 * * * $BOT_DIR/backup.sh"; } | crontab -u $BOT_USER -

# Start and enable service
echo -e "${YELLOW}🚀 Starting HYPERION Elite Bot...${NC}"
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

# Wait for service to start
sleep 5

# Check service status
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✅ HYPERION Elite Bot is running successfully!${NC}"
else
    echo -e "${RED}❌ Failed to start HYPERION Elite Bot${NC}"
    echo "Check logs with: journalctl -u $SERVICE_NAME -f"
    exit 1
fi

# Display useful information
echo ""
echo -e "${BLUE}🎉 HYPERION Elite Bot Deployment Complete!${NC}"
echo "========================================"
echo -e "${GREEN}📍 Installation Directory:${NC} $BOT_DIR"
echo -e "${GREEN}👤 Service User:${NC} $BOT_USER"
echo -e "${GREEN}🔧 Service Name:${NC} $SERVICE_NAME"
echo ""
echo -e "${YELLOW}📋 Useful Commands:${NC}"
echo "  Status:      systemctl status $SERVICE_NAME"
echo "  Start:       systemctl start $SERVICE_NAME"
echo "  Stop:        systemctl stop $SERVICE_NAME"
echo "  Restart:     systemctl restart $SERVICE_NAME"
echo "  Logs:        journalctl -u $SERVICE_NAME -f"
echo "  Edit Config: nano $BOT_DIR/.env"
echo "  Manual Run:  sudo -u $BOT_USER $BOT_DIR/venv/bin/python $BOT_DIR/hyperion_elite_bot.py"
echo ""
echo -e "${GREEN}🔄 The service will automatically start on boot${NC}"
echo -e "${GREEN}💾 Daily backups are configured at 2 AM${NC}"
echo ""
echo -e "${BLUE}🚀 Your HYPERION Elite Bot is ready!${NC}"