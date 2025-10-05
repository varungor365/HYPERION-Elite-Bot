#!/bin/bash

# 🚀 HYPERION Elite Bot - Zero Input Deployment
# All credentials are hardcoded - just run and go!

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo -e "${BLUE}"
echo "████████████████████████████████████████████████████"
echo "█                                                  █"
echo "█    🚀 HYPERION Elite Bot - Zero Input Deploy    █"
echo "█         All credentials pre-configured          █"
echo "█                                                  █"
echo "████████████████████████████████████████████████████"
echo -e "${NC}"

print_success "Bot credentials are pre-configured - no input needed!"

# Update system
print_status "Updating Ubuntu system..."
apt update -qq && apt upgrade -y -qq

# Install dependencies
print_status "Installing system dependencies..."
apt install -y python3 python3-pip python3-venv git curl wget \
    build-essential libssl-dev libffi-dev python3-dev

# Setup bot directory
BOT_DIR="/opt/HYPERION-Elite-Bot"
print_status "Setting up bot in $BOT_DIR"

# Fix git safe directory issue
git config --global --add safe.directory $BOT_DIR

if [[ -d "$BOT_DIR" ]]; then
    print_status "Updating existing installation..."
    cd $BOT_DIR 
    git pull origin main
else
    print_status "Cloning fresh installation..."
    cd /opt 
    git clone https://github.com/varungor365/HYPERION-Elite-Bot.git
fi

cd $BOT_DIR

# Create virtual environment
print_status "Creating Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages with tenacity conflict fix
print_status "Installing Python packages..."
pip install --upgrade pip

# Install packages one by one to handle conflicts
print_status "Installing core packages..."
pip install python-telegram-bot==22.5
pip install aiohttp>=3.12.0 aiofiles>=23.2.0 httpx>=0.25.0
pip install pandas>=2.1.0 numpy>=1.24.0
pip install python-dotenv>=1.0.0 cryptography>=41.0.0
pip install PySocks>=1.7.1 colorama>=0.4.6
pip install requests>=2.31.0 "urllib3<2.0.0,>=1.26.0"

# Handle tenacity conflict - install compatible version first
print_status "Fixing tenacity version conflict..."
pip install "tenacity>=8.0.0,<9.0.0"

# Install mega.py (it will complain about tenacity but still work)
print_status "Installing mega.py (ignoring tenacity warning)..."
pip install mega.py==1.0.8 --no-deps
pip install pycryptodome pathlib

# Install remaining packages
print_status "Installing remaining packages..."
pip install tqdm rich backoff bcrypt loguru
pip install pytest pytest-asyncio black flake8

# Test bot (no environment variables needed - all hardcoded)
print_status "Testing bot functionality..."
python3 -c "
import sys
sys.path.insert(0, '$BOT_DIR')
try:
    import hyperion_headless
    print('✅ Bot test successful - all credentials hardcoded!')
except Exception as e:
    print(f'❌ Bot test failed: {e}')
    sys.exit(1)
"

if [[ $? -ne 0 ]]; then
    print_error "Bot test failed!"
    exit 1
fi

# Create systemd service (no environment file needed)
print_status "Creating systemd service..."
cat > /etc/systemd/system/hyperion-elite-bot.service << EOF
[Unit]
Description=HYPERION Elite Bot - Auto Configured
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$BOT_DIR
Environment=PATH=$BOT_DIR/.venv/bin
ExecStart=$BOT_DIR/.venv/bin/python hyperion_headless.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create management scripts
print_status "Creating management tools..."

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
echo "📋 HYPERION Elite Bot Live Logs (Press Ctrl+C to exit)"
journalctl -u hyperion-elite-bot -f
EOF

chmod +x hyperion-*.sh

# Start the service
print_status "Starting HYPERION Elite Bot..."
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
echo -e "\n${GREEN}"
echo "████████████████████████████████████████████████████"
echo "█                                                  █"
echo "█        🎉 ZERO-INPUT DEPLOYMENT SUCCESS! 🎉     █"
echo "█                                                  █"
echo "████████████████████████████████████████████████████"
echo -e "${NC}"

echo -e "\n${GREEN}✅ HYPERION Elite Bot is now running with pre-configured credentials!${NC}\n"

echo -e "${BLUE}📱 Bot Information:${NC}"
echo "   • Service Status: $(systemctl is-active hyperion-elite-bot)"
echo "   • Bot Token: 7090420579:AAEmOwa... (pre-configured)"
echo "   • Authorized User: @megacheckk_bot + ID 796354588"
echo "   • Installation Path: $BOT_DIR"

echo -e "\n${BLUE}🛠️ Management Commands:${NC}"
echo "   • Check Status: ./hyperion-status.sh"
echo "   • Start Bot: ./hyperion-start.sh"
echo "   • Stop Bot: ./hyperion-stop.sh"
echo "   • Restart Bot: ./hyperion-restart.sh"
echo "   • View Logs: ./hyperion-logs.sh"

echo -e "\n${BLUE}📱 Telegram Bot Commands:${NC}"
echo "   • /start - Initialize bot (send this first!)"
echo "   • /status - System status with resource optimizer"
echo "   • /scan - AI analyze combo file (A-Z sorted)"
echo "   • /check - Start elite checking with optimization"
echo "   • /addcombos - Add combos during checking"
echo "   • /stop - Stop and get results"
echo "   • /results - Download hit files"

echo -e "\n${GREEN}🎖️ Your HYPERION Elite Bot v5.1 is production-ready!${NC}"
echo -e "${BLUE}💡 All advanced features enabled: Resource Optimizer, AI Analyzer, A-Z Sorting${NC}"

echo -e "\n${YELLOW}🔔 Next Steps:${NC}"
echo "   1. Open Telegram and find your bot"
echo "   2. Send /start to activate"
echo "   3. Upload combo files and use /scan"
echo "   4. Use /check for optimized checking"
echo "   5. Monitor with ./hyperion-status.sh"

# Show current status
print_status "Final status check:"
./hyperion-status.sh

echo -e "\n${GREEN}🚀 Bot is running! No configuration needed - everything is pre-set!${NC}"