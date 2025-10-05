#!/bin/bash

# 🔍 HYPERION Bot Emergency Diagnostics & Fix
# Complete bot troubleshooting and webhook removal

echo "🚨 HYPERION Bot Emergency Diagnostics"
echo "====================================="

BOT_TOKEN="7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
API_URL="https://api.telegram.org/bot$BOT_TOKEN"

echo "🔍 Step 1: Testing Bot API Connection..."
curl -s "$API_URL/getMe" | jq '.' || echo "❌ Bot API test failed"

echo ""
echo "🔍 Step 2: Checking Webhook Status..."
WEBHOOK_INFO=$(curl -s "$API_URL/getWebhookInfo")
echo "$WEBHOOK_INFO" | jq '.' || echo "$WEBHOOK_INFO"

# Check if webhook is set
if echo "$WEBHOOK_INFO" | grep -q '"url":"http'; then
    echo "⚠️  WEBHOOK DETECTED - This prevents polling!"
    echo "🔧 Removing webhook..."
    curl -s -X POST "$API_URL/deleteWebhook" | jq '.' || echo "Webhook removal attempted"
    
    echo "🔄 Verifying webhook removal..."
    sleep 2
    curl -s "$API_URL/getWebhookInfo" | jq '.' || echo "Verification failed"
else
    echo "✅ No webhook set (good for polling)"
fi

echo ""
echo "🔍 Step 3: Getting Recent Updates..."
curl -s "$API_URL/getUpdates?limit=5" | jq '.result[] | {update_id, message: .message.text, from: .message.from.username}' || echo "No recent updates"

echo ""
echo "🔍 Step 4: Checking Bot Services..."
echo "Current bot services:"
systemctl list-units --type=service | grep hyperion || echo "No hyperion services found"

echo ""
echo "🔍 Step 5: Service Status Check..."
if systemctl is-active --quiet hyperion-elite-bot-fixed; then
    echo "✅ hyperion-elite-bot-fixed is running"
    echo "📊 Service status:"
    systemctl status hyperion-elite-bot-fixed --no-pager -l
else
    echo "❌ hyperion-elite-bot-fixed is not running"
fi

if systemctl is-active --quiet hyperion-elite-bot; then
    echo "⚠️  Original hyperion-elite-bot is also running (CONFLICT!)"
    echo "🛑 Stopping original service..."
    systemctl stop hyperion-elite-bot
fi

echo ""
echo "🔍 Step 6: Process Check..."
echo "Python processes related to hyperion:"
ps aux | grep hyperion | grep -v grep || echo "No hyperion processes found"

echo ""
echo "🔍 Step 7: Recent Logs..."
echo "Last 20 lines of bot logs:"
journalctl -u hyperion-elite-bot-fixed -n 20 --no-pager || journalctl -u hyperion-elite-bot -n 20 --no-pager || echo "No logs found"

echo ""
echo "🔧 EMERGENCY FIX ACTIONS:"
echo "========================"

echo "🛑 Stopping all bot services..."
systemctl stop hyperion-elite-bot 2>/dev/null || true
systemctl stop hyperion-elite-bot-fixed 2>/dev/null || true

echo "🔪 Killing any remaining bot processes..."
pkill -f hyperion || echo "No processes to kill"

echo "⏳ Waiting 3 seconds..."
sleep 3

echo "🚀 Starting fresh bot instance..."
cd /opt/HYPERION-Elite-Bot

# Start the fixed bot directly for testing
echo "🧪 Testing direct bot execution..."
source .venv/bin/activate
timeout 10 python3 hyperion_fixed.py &
DIRECT_PID=$!

echo "⏳ Waiting 5 seconds for bot to initialize..."
sleep 5

echo "🔍 Checking if direct execution is working..."
if ps -p $DIRECT_PID > /dev/null; then
    echo "✅ Bot is running directly - killing test instance"
    kill $DIRECT_PID 2>/dev/null || true
    
    echo "🔄 Starting as service..."
    systemctl start hyperion-elite-bot-fixed
    sleep 3
    
    if systemctl is-active --quiet hyperion-elite-bot-fixed; then
        echo "✅ Service started successfully!"
    else
        echo "❌ Service failed to start"
    fi
else
    echo "❌ Direct execution failed"
fi

echo ""
echo "🎯 FINAL STATUS:"
echo "==============="
echo "Service status:"
systemctl is-active hyperion-elite-bot-fixed && echo "✅ RUNNING" || echo "❌ NOT RUNNING"

echo ""
echo "📱 TEST NOW:"
echo "Send /start to @megacheckk_bot"
echo ""
echo "🔍 Monitor logs:"
echo "journalctl -u hyperion-elite-bot-fixed -f"