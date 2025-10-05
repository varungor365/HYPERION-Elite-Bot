#!/bin/bash

# 🛑 HYPERION Bot Conflict Resolver
# Stops all bot instances and starts only the elite bot

echo "🛑 HYPERION Bot Conflict Resolver"
echo "================================="

# Stop ALL bot services
echo "⏹️ Stopping all HYPERION bot services..."
sudo systemctl stop hyperion-elite 2>/dev/null || true
sudo systemctl stop hyperion-elite-bot 2>/dev/null || true
sudo systemctl stop hyperion-elite-bot-fixed 2>/dev/null || true
sudo systemctl stop hyperion-working 2>/dev/null || true

# Kill all Python processes related to hyperion
echo "🔪 Killing all HYPERION Python processes..."
sudo pkill -f "hyperion" || echo "No processes to kill"
sudo pkill -f "python.*hyperion" || echo "No Python hyperion processes"

# Wait a moment
echo "⏳ Waiting 5 seconds for cleanup..."
sleep 5

# Disable conflicting services
echo "🚫 Disabling conflicting services..."
sudo systemctl disable hyperion-elite-bot 2>/dev/null || true
sudo systemctl disable hyperion-elite-bot-fixed 2>/dev/null || true
sudo systemctl disable hyperion-working 2>/dev/null || true

# Check if any bot processes are still running
echo "🔍 Checking for remaining bot processes..."
if pgrep -f "hyperion" > /dev/null; then
    echo "⚠️  Found remaining processes:"
    ps aux | grep hyperion | grep -v grep
    echo "🔪 Force killing remaining processes..."
    sudo pkill -9 -f "hyperion"
    sleep 2
fi

# Now start only the elite bot
echo "🚀 Starting HYPERION Elite Bot (single instance)..."
sudo systemctl start hyperion-elite

# Wait for startup
echo "⏳ Waiting for bot to initialize..."
sleep 3

# Check status
echo "📊 Bot Status:"
if sudo systemctl is-active --quiet hyperion-elite; then
    echo "✅ HYPERION Elite Bot is running"
    echo ""
    echo "🔍 Service status:"
    sudo systemctl status hyperion-elite --no-pager -l | head -20
    echo ""
    echo "📱 Bot should now respond without conflicts!"
    echo "   Try: /start in @megacheckk_bot"
else
    echo "❌ Bot failed to start"
    echo ""
    echo "🔍 Recent logs:"
    sudo journalctl -u hyperion-elite -n 10 --no-pager
fi

echo ""
echo "🔧 To monitor logs in real-time:"
echo "sudo journalctl -u hyperion-elite -f"