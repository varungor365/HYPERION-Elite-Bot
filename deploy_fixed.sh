#!/bin/bash

# 🚀 HYPERION Elite Bot - Quick Fix Deployment
# This will replace the problematic version with a working one

echo "🔧 HYPERION Elite Bot - Quick Fix"
echo "=================================="

# Stop current service
echo "⏹️ Stopping current bot service..."
sudo systemctl stop hyperion-elite-bot

# Backup current version
echo "💾 Backing up current version..."
sudo cp /opt/HYPERION-Elite-Bot/hyperion_headless.py /opt/HYPERION-Elite-Bot/hyperion_headless.py.backup

# Install fixed version
echo "🔧 Installing fixed version..."
cd /opt/HYPERION-Elite-Bot

# Create new systemd service for fixed version
echo "📝 Creating new systemd service..."
sudo tee /etc/systemd/system/hyperion-elite-bot-fixed.service > /dev/null << 'EOF'
[Unit]
Description=HYPERION Elite Bot - Fixed Version
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/HYPERION-Elite-Bot
Environment=PATH=/opt/HYPERION-Elite-Bot/.venv/bin
ExecStart=/opt/HYPERION-Elite-Bot/.venv/bin/python hyperion_fixed.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start fixed service
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

echo "🚀 Starting fixed bot service..."
sudo systemctl enable hyperion-elite-bot-fixed
sudo systemctl start hyperion-elite-bot-fixed

# Check status
echo "📊 Service status:"
sudo systemctl status hyperion-elite-bot-fixed --no-pager -l

echo ""
echo "✅ Fixed HYPERION Elite Bot deployed!"
echo ""
echo "🔍 To monitor logs:"
echo "sudo journalctl -u hyperion-elite-bot-fixed -f"
echo ""
echo "🎯 Test the bot now by sending /start to @megacheckk_bot"