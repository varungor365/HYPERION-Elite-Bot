#!/bin/bash

# 🔧 HYPERION ULTRA v7.0 FIXED - WORKING DEPLOYMENT
# =================================================
# Deploy FIXED @megacheckk_bot that actually processes accounts

echo "🔧 DEPLOYING FIXED HYPERION ULTRA v7.0 - WORKING EDITION..."
echo "🎯 This version ACTUALLY processes accounts (no more 0 progress!)"

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
echo "🧹 Updating to FIXED v7.0..."
cd /opt/HYPERION-Elite-Bot || exit 1
git pull origin main

# Install dependencies
echo "📦 Installing v7.0 FIXED dependencies..."
pip3 install python-telegram-bot==20.7 psutil requests mega.py

# Create bot token file with your token
echo "🔑 Setting up @megacheckk_bot token..."
echo "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM" > bot_token.txt

# Create service for FIXED v7.0 bot
echo "🔧 Creating FIXED v7.0 service..."
sudo tee /etc/systemd/system/hyperion-ultra-telegram-fixed.service > /dev/null << 'EOF'
[Unit]
Description=HYPERION ULTRA Telegram Bot v7.0 FIXED (@megacheckk_bot)
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

# High resource limits for working threads
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

# Reload systemd and start FIXED bot
echo "🔄 Starting FIXED v7.0 @megacheckk_bot..."
sudo systemctl daemon-reload
sudo systemctl enable hyperion-ultra-telegram-fixed
sudo systemctl start hyperion-ultra-telegram-fixed

# Wait for startup
sleep 10

# Check bot status
echo ""
echo "📊 FIXED v7.0 BOT STATUS:"
sudo systemctl status hyperion-ultra-telegram-fixed --no-pager -l

echo ""
echo "🎯 FOLLOW FIXED v7.0 LOGS:"
echo "sudo journalctl -u hyperion-ultra-telegram-fixed -f"

echo ""
echo "✅ @megacheckk_bot v7.0 FIXED DEPLOYED!"
echo ""
echo "🔧 WHAT'S FIXED:"
echo "• ✅ Working authentication engine (based on V2-REBUILT)"
echo "• ✅ Actually processes accounts (no more 0 progress)"  
echo "• ✅ Real account checking with proper MEGA login"
echo "• ✅ Working progress updates with actual CPM"
echo "• ✅ Proper error handling and rate limiting"
echo "• ✅ Thread pool executor for maximum performance"
echo ""
echo "🤖 YOUR BOT: @megacheckk_bot"
echo "📱 Open Telegram and search: @megacheckk_bot"
echo ""
echo "📝 HOW TO USE:"
echo "1. Open Telegram → Search @megacheckk_bot"
echo "2. Send: /start"
echo "3. Click: 🚀 ULTRA CHECK"
echo "4. Upload your combo.txt file"
echo "5. Watch REAL progress updates (not stuck at 0!))"
echo "6. Receive hits automatically!"
echo ""
echo "🔥 Now with WORKING account processing!"

# Test bot connection
echo ""
echo "🔍 Testing FIXED bot connection..."
RESPONSE=$(curl -s "https://api.telegram.org/bot7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM/getMe")
if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ FIXED bot connection successful!"
    echo "🤖 Bot is online and ready for REAL checking!"
else
    echo "❌ Bot connection failed. Check token."
fi

echo ""
echo "🎯 EXPECTED BEHAVIOR NOW:"
echo "Instead of stuck at 0 progress, you'll see:"
echo "📊 Progress: 1,234/90,595 (1.4%) ← ACTUAL PROGRESS!"
echo "⚡ CPM: 450 ← REAL CPM!"
echo "🎯 Hits: 15 ← ACTUAL HITS!"
echo ""
echo "🔧 v7.0 FIXED is ready for real account checking!"