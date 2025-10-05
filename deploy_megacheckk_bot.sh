#!/bin/bash

# 🤖 HYPERION ULTRA TELEGRAM BOT v7.0 - QUICK DEPLOY
# =================================================
# Deploy @megacheckk_bot with ultra performance

echo "🤖 DEPLOYING @megacheckk_bot - HYPERION ULTRA v7.0..."

# Kill all existing processes
echo "🔥 Stopping all HYPERION processes..."
sudo pkill -f "hyperion" || true
sudo pkill -f "mega_auth" || true
sudo systemctl stop hyperion-ultra-v7 || true
sudo systemctl stop hyperion-ultra-standalone || true
sudo systemctl stop hyperion-ultra-telegram || true
sudo systemctl disable hyperion-ultra-v7 || true
sudo systemctl disable hyperion-ultra-standalone || true
sudo systemctl disable hyperion-ultra-telegram || true

# Clean and update
echo "🧹 Updating repository..."
cd /opt/HYPERION-Elite-Bot || exit 1
git pull origin main

# Install dependencies
echo "📦 Installing Telegram bot dependencies..."
pip3 install python-telegram-bot==20.7 psutil requests

# Create bot token file
echo "🔑 Setting up @megacheckk_bot token..."
echo "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM" > bot_token.txt

# Create service for your bot
echo "🔧 Creating @megacheckk_bot service..."
sudo tee /etc/systemd/system/hyperion-ultra-telegram.service > /dev/null << 'EOF'
[Unit]
Description=HYPERION ULTRA Telegram Bot v7.0 (@megacheckk_bot)
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/HYPERION-Elite-Bot
ExecStart=/usr/bin/python3 /opt/HYPERION-Elite-Bot/hyperion_ultra_telegram_v7.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Performance optimizations for ultra speed
CPUSchedulingPolicy=1
CPUSchedulingPriority=50
IOSchedulingClass=1
IOSchedulingPriority=4
OOMScoreAdjust=-100

# High resource limits for 250 threads
LimitNOFILE=65536
LimitNPROC=65536
LimitSTACK=infinity

# Environment variables
Environment=PYTHONUNBUFFERED=1
Environment=MALLOC_ARENA_MAX=4

[Install]
WantedBy=multi-user.target
EOF

# Create directories
echo "📁 Creating organized directories..."
mkdir -p combos hits backups

# Reload systemd and start bot
echo "🔄 Starting @megacheckk_bot..."
sudo systemctl daemon-reload
sudo systemctl enable hyperion-ultra-telegram
sudo systemctl start hyperion-ultra-telegram

# Wait for startup
sleep 8

# Check bot status
echo ""
echo "📊 BOT STATUS:"
sudo systemctl status hyperion-ultra-telegram --no-pager -l

echo ""
echo "🎯 FOLLOW BOT LOGS:"
echo "sudo journalctl -u hyperion-ultra-telegram -f"

echo ""
echo "✅ @megacheckk_bot DEPLOYED SUCCESSFULLY!"
echo ""
echo "🤖 YOUR BOT: @megacheckk_bot"
echo "📱 Open Telegram and search: @megacheckk_bot"
echo ""
echo "🚀 BOT FEATURES:"
echo "• Upload .txt combo files directly"
echo "• Real-time progress every 15 seconds"
echo "• 250 ultra threads for maximum speed"
echo "• Live CPM/CPU/RAM monitoring"
echo "• Auto hit delivery with organized files"
echo "• Interactive buttons and commands"
echo ""
echo "📝 HOW TO USE:"
echo "1. Open Telegram → Search @megacheckk_bot"
echo "2. Send: /start"
echo "3. Click: 🚀 ULTRA CHECK"
echo "4. Upload your combo.txt file"
echo "5. Watch real-time progress updates!"
echo "6. Receive hits automatically!"
echo ""
echo "🔥 Ready for ultra-speed MEGA checking!"

# Test bot connection
echo ""
echo "🔍 Testing bot connection..."
RESPONSE=$(curl -s "https://api.telegram.org/bot7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM/getMe")
if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ Bot connection successful!"
    echo "🤖 Bot is online and ready!"
else
    echo "❌ Bot connection failed. Check token."
fi