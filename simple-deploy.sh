#!/bin/bash

# 🚀 HYPERION Elite Bot - Simple Root-Compatible Deployment
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

echo -e "${BLUE}🚀 HYPERION Elite Bot - VPS Deployment${NC}"
echo "=================================================="

# Get bot credentials
if [[ -z "$TELEGRAM_BOT_TOKEN" ]]; then
    echo -e "${BLUE}Enter your Telegram Bot Token:${NC}"
    read -r TELEGRAM_BOT_TOKEN
fi

if [[ -z "$AUTHORIZED_USER_ID" ]]; then
    echo -e "${BLUE}Enter your Telegram User ID:${NC}"
    read -r AUTHORIZED_USER_ID
fi

if [[ -z "$TELEGRAM_BOT_TOKEN" ]] || [[ -z "$AUTHORIZED_USER_ID" ]]; then
    print_error "Bot token and user ID are required!"
    exit 1
fi

# Update system
print_status "Updating system packages..."
apt update -qq && apt upgrade -y -qq

# Install dependencies
print_status "Installing dependencies..."
apt install -y python3 python3-pip python3-venv git curl wget \
    build-essential libssl-dev libffi-dev python3-dev

# Setup bot
BOT_DIR="/opt/HYPERION-Elite-Bot"
print_status "Setting up bot in $BOT_DIR"

if [[ -d "$BOT_DIR" ]]; then
    cd $BOT_DIR && git pull origin main
else
    cd /opt && git clone https://github.com/varungor365/HYPERION-Elite-Bot.git
fi

cd $BOT_DIR

# Create virtual environment
print_status "Creating Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install packages
print_status "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create environment file
print_status "Creating configuration..."
cat > .env << EOF
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
AUTHORIZED_USER_ID=$AUTHORIZED_USER_ID
LOG_LEVEL=INFO
EOF

# Test bot
print_status "Testing bot..."
export TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
export AUTHORIZED_USER_ID="$AUTHORIZED_USER_ID"

python3 -c "
import sys
sys.path.insert(0, '$BOT_DIR')
try:
    import hyperion_headless
    print('✅ Bot test successful')
except Exception as e:
    print(f'❌ Bot test failed: {e}')
    sys.exit(1)
"

if [[ $? -ne 0 ]]; then
    print_error "Bot test failed!"
    exit 1
fi

# Create systemd service
print_status "Creating systemd service..."
cat > /etc/systemd/system/hyperion-elite-bot.service << EOF
[Unit]
Description=HYPERION Elite Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$BOT_DIR
Environment=PATH=$BOT_DIR/.venv/bin
EnvironmentFile=$BOT_DIR/.env
ExecStart=$BOT_DIR/.venv/bin/python hyperion_headless.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create management scripts
print_status "Creating management scripts..."

cat > hyperion-start.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting HYPERION Elite Bot..."
systemctl start hyperion-elite-bot
systemctl status hyperion-elite-bot --no-pager -l
EOF

cat > hyperion-stop.sh << 'EOF'
#!/bin/bash
echo "⏹️ Stopping HYPERION Elite Bot..."
systemctl stop hyperion-elite-bot
systemctl status hyperion-elite-bot --no-pager -l
EOF

cat > hyperion-status.sh << 'EOF'
#!/bin/bash
echo "📊 HYPERION Elite Bot Status"
echo "================================"
systemctl status hyperion-elite-bot --no-pager -l
echo -e "\n📈 System Resources:"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}' 2>/dev/null || echo "N/A")"
echo "RAM: $(free -h | awk 'NR==2{printf "%.1f/%.1fGB (%.2f%%)\n", $3/1024/1024/1024,$2/1024/1024/1024,$3*100/$2 }' 2>/dev/null || echo "N/A")"
echo "Disk: $(df -h / | awk 'NR==2{print $3"/"$2" ("$5")"}' 2>/dev/null || echo "N/A")"
echo -e "\n📋 Recent Logs:"
journalctl -u hyperion-elite-bot -n 5 --no-pager
EOF

cat > hyperion-restart.sh << 'EOF'
#!/bin/bash
echo "🔄 Restarting HYPERION Elite Bot..."
systemctl restart hyperion-elite-bot
sleep 2
systemctl status hyperion-elite-bot --no-pager -l
EOF

cat > hyperion-logs.sh << 'EOF'
#!/bin/bash
echo "📋 HYPERION Elite Bot Logs (Press Ctrl+C to exit)"
journalctl -u hyperion-elite-bot -f
EOF

chmod +x hyperion-*.sh

# Start service
print_status "Starting bot service..."
systemctl daemon-reload
systemctl enable hyperion-elite-bot
systemctl start hyperion-elite-bot

sleep 3

if systemctl is-active --quiet hyperion-elite-bot; then
    print_success "🎉 HYPERION Elite Bot is running!"
else
    print_error "Service failed to start. Checking logs..."
    journalctl -u hyperion-elite-bot --no-pager -l
    exit 1
fi

# Success message
echo -e "\n${GREEN}✅ DEPLOYMENT SUCCESSFUL!${NC}"
echo -e "\n${BLUE}📱 Bot Information:${NC}"
echo "   • Service: hyperion-elite-bot"
echo "   • Status: $(systemctl is-active hyperion-elite-bot)"
echo "   • Location: $BOT_DIR"
echo "   • Token: ${TELEGRAM_BOT_TOKEN:0:20}..."
echo "   • User ID: $AUTHORIZED_USER_ID"

echo -e "\n${BLUE}🛠️ Management Commands:${NC}"
echo "   • Start: ./hyperion-start.sh"
echo "   • Stop: ./hyperion-stop.sh"
echo "   • Status: ./hyperion-status.sh"
echo "   • Restart: ./hyperion-restart.sh"
echo "   • Logs: ./hyperion-logs.sh"

echo -e "\n${BLUE}📋 Direct Commands:${NC}"
echo "   • Service Status: systemctl status hyperion-elite-bot"
echo "   • View Logs: journalctl -u hyperion-elite-bot -f"
echo "   • Restart: systemctl restart hyperion-elite-bot"

echo -e "\n${BLUE}📱 Telegram Commands:${NC}"
echo "   • /start - Initialize bot"
echo "   • /status - System status with resource optimizer"
echo "   • /scan - AI analyze combo file"
echo "   • /check - Start checking with auto-optimization"
echo "   • /addcombos - Add combos during checking"

echo -e "\n${GREEN}🎖️ Your bot is ready! Send /start in Telegram.${NC}"

# Show current status
./hyperion-status.sh