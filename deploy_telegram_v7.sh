#!/bin/bash

# 🚀 HYPERION ULTRA TELEGRAM BOT v7.0 DEPLOYMENT
# ==============================================
# Deploy ultra-performance Telegram bot with real-time updates

echo "🚀 DEPLOYING HYPERION ULTRA TELEGRAM BOT v7.0..."

# Kill all existing processes
echo "🔥 Stopping all HYPERION processes..."
sudo pkill -f "hyperion" || true
sudo pkill -f "mega_auth" || true
sudo systemctl stop hyperion-ultra-v7 || true
sudo systemctl stop hyperion-ultra-standalone || true
sudo systemctl disable hyperion-ultra-v7 || true
sudo systemctl disable hyperion-ultra-standalone || true

# Clean and update
echo "🧹 Cleaning and updating..."
cd /opt/HYPERION-Elite-Bot || exit 1
git pull origin main

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install python-telegram-bot psutil

# Check for bot token
echo "🔑 Checking bot token..."
if [ ! -f "bot_token.txt" ] || [ ! -s "bot_token.txt" ]; then
    echo ""
    echo "❌ TELEGRAM BOT TOKEN REQUIRED!"
    echo ""
    echo "📱 To get your bot token:"
    echo "1. Open Telegram and message @BotFather"
    echo "2. Send: /newbot"
    echo "3. Follow instructions to create your bot"
    echo "4. Copy the token (looks like: 123456789:ABCdefGhIjKlMnOpQrStUvWxYz)"
    echo ""
    read -p "🔑 Paste your bot token here: " BOT_TOKEN
    
    if [ -z "$BOT_TOKEN" ]; then
        echo "❌ No token provided. Exiting."
        exit 1
    fi
    
    echo "$BOT_TOKEN" > bot_token.txt
    echo "✅ Bot token saved!"
else
    echo "✅ Bot token found!"
fi

# Create service for Telegram bot
echo "🔧 Creating Telegram bot service..."
sudo tee /etc/systemd/system/hyperion-ultra-telegram.service > /dev/null << 'EOF'
[Unit]
Description=HYPERION ULTRA Telegram Bot v7.0
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/HYPERION-Elite-Bot
ExecStart=/usr/bin/python3 /opt/HYPERION-Elite-Bot/hyperion_ultra_telegram_v7.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Performance optimizations
CPUSchedulingPolicy=1
CPUSchedulingPriority=50
IOSchedulingClass=1
IOSchedulingPriority=4
OOMScoreAdjust=-100

# Resource limits
LimitNOFILE=65536
LimitNPROC=65536

# Environment
Environment=PYTHONUNBUFFERED=1
Environment=MALLOC_ARENA_MAX=2

[Install]
WantedBy=multi-user.target
EOF

# Reload and start service
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

echo "🚀 Starting HYPERION ULTRA TELEGRAM BOT v7.0..."
sudo systemctl enable hyperion-ultra-telegram
sudo systemctl start hyperion-ultra-telegram

# Wait for startup
sleep 5

# Check status
echo ""
echo "📊 SERVICE STATUS:"
sudo systemctl status hyperion-ultra-telegram --no-pager -l

echo ""
echo "🎯 FOLLOW BOT LOGS:"
echo "sudo journalctl -u hyperion-ultra-telegram -f"

echo ""
echo "✅ HYPERION ULTRA TELEGRAM BOT v7.0 DEPLOYED!"
echo ""
echo "📱 BOT FEATURES:"
echo "• Upload combo files directly to bot"
echo "• Real-time progress updates every 15 seconds"
echo "• Live CPM, CPU, RAM monitoring"
echo "• Auto-organized hit delivery"  
echo "• 250 thread ultra performance"
echo "• Interactive Telegram interface"
echo ""
echo "🚀 HOW TO USE:"
echo "1. Find your bot in Telegram"
echo "2. Send /start command"
echo "3. Click 'ULTRA CHECK' button"
echo "4. Upload your combo .txt file"
echo "5. Watch real-time progress!"
echo "6. Receive hits automatically!"
echo ""
echo "🔥 Your bot is ready for ultra-speed checking!"

# Show bot info
if [ -f "bot_token.txt" ]; then
    TOKEN=$(cat bot_token.txt)
    BOT_USERNAME=$(curl -s "https://api.telegram.org/bot$TOKEN/getMe" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
    if [ ! -z "$BOT_USERNAME" ]; then
        echo ""
        echo "🤖 YOUR BOT: @$BOT_USERNAME"
        echo "📱 Open Telegram and search for: @$BOT_USERNAME"
    fi
fi