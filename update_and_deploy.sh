#!/bin/bash

# 🚀 HYPERION Elite Bot - Update and Deploy Latest Fixes
# Pull latest changes and deploy the working bot version

echo "🔄 HYPERION Elite Bot - Update & Deploy"
echo "======================================="

# Navigate to bot directory
cd /opt/HYPERION-Elite-Bot

# Pull latest changes
echo "📥 Pulling latest fixes from GitHub..."
git pull origin main

# Make scripts executable
echo "🔧 Setting up permissions..."
chmod +x deploy_fixed.sh
chmod +x debug_bot.py
chmod +x fixed-install.sh

# Deploy the fixed version
echo "🚀 Deploying fixed bot version..."
sudo ./deploy_fixed.sh

echo ""
echo "✅ Update and deployment complete!"
echo ""
echo "🎯 Your bot should now respond to messages!"
echo "📱 Test it: Send /start to @megacheckk_bot"
echo ""
echo "🔍 Monitor logs: sudo journalctl -u hyperion-elite-bot-fixed -f"