#!/bin/bash

# HYPERION ULTRA FORCE RESTART v6.0
# =================================
# Forces ultra-performance bot to run instead of old elite bot

echo "🚀 HYPERION ULTRA FORCE RESTART v6.0"
echo "====================================="
echo "Stopping OLD elite bot and starting ULTRA performance bot"
echo ""

# Step 1: Kill ALL Python processes related to bots
echo "💀 FORCE KILLING all bot processes..."
sudo pkill -9 -f "python" 2>/dev/null || true
sudo pkill -9 -f "hyperion" 2>/dev/null || true
sudo pkill -9 -f "mega" 2>/dev/null || true

# Wait for processes to die
sleep 3

# Step 2: Stop all bot services
echo "🛑 Stopping all bot services..."
sudo systemctl stop hyperion-elite 2>/dev/null || true
sudo systemctl stop hyperion-elite-bot 2>/dev/null || true
sudo systemctl stop hyperion-ultra 2>/dev/null || true
sudo systemctl disable hyperion-elite 2>/dev/null || true
sudo systemctl disable hyperion-elite-bot 2>/dev/null || true

# Step 3: Verify no bots running
echo "🔍 Verifying no bots are running..."
BOT_PROCESSES=$(ps aux | grep -i hyperion | grep -v grep | wc -l)
if [ $BOT_PROCESSES -gt 0 ]; then
    echo "⚠️  Found $BOT_PROCESSES bot processes still running. Force killing..."
    sudo pkill -9 -f "hyperion" 2>/dev/null || true
    sleep 2
fi

# Step 4: Start ULTRA performance bot directly
echo ""
echo "🚀 Starting ULTRA PERFORMANCE BOT..."
echo "====================================="

cd /opt/HYPERION-Elite-Bot

# Check if ultra bot exists
if [ -f "hyperion_ultra_performance.py" ]; then
    echo "✅ Found ultra performance bot"
    
    # Start with maximum performance settings
    echo "🔥 Starting with ULTRA settings:"
    echo "   • 250 threads"
    echo "   • 100% CPU target"
    echo "   • 5000+ proxy pool"
    echo "   • Real-time optimization"
    
    # Set environment for maximum performance
    export PYTHONUNBUFFERED=1
    export OMP_NUM_THREADS=250
    
    # Start ultra bot in background
    nohup python3 hyperion_ultra_performance.py > ultra_bot.log 2>&1 &
    ULTRA_PID=$!
    
    echo "🎯 ULTRA BOT STARTED!"
    echo "   PID: $ULTRA_PID"
    echo "   Log: ultra_bot.log"
    
    # Wait a moment and check if it's running
    sleep 5
    
    if ps -p $ULTRA_PID > /dev/null; then
        echo "✅ ULTRA bot is running successfully!"
        echo "🔥 Expected performance:"
        echo "   • CPM: 10,000+"
        echo "   • CPU: 90%+"
        echo "   • RAM: 80%+"
        echo "   • Threads: 250"
    else
        echo "❌ Ultra bot failed to start. Checking logs..."
        tail -20 ultra_bot.log
    fi
    
else
    echo "❌ Ultra performance bot not found!"
    echo "Available bot files:"
    ls -la *.py
    
    # Fallback to elite bot with warning
    if [ -f "hyperion_elite_bot.py" ]; then
        echo "🔄 Starting elite bot as fallback..."
        nohup python3 hyperion_elite_bot.py > elite_bot.log 2>&1 &
        echo "⚠️  Using old elite bot - performance will be limited"
    fi
fi

echo ""
echo "📊 Current system status:"
echo "========================"
echo "🖥️  CPU Cores: $(nproc)"
echo "🧠 RAM Total: $(free -h | grep Mem | awk '{print $2}')"
echo "🔍 Bot processes:"
ps aux | grep -E "(hyperion|python.*\.py)" | grep -v grep

echo ""
echo "🎯 Bot should now respond with ULTRA interface!"
echo "Expected features:"
echo "  • 🚀 ULTRA CHECK button"
echo "  • ⚡ PREMIUM PROXIES"
echo "  • 📊 PERFORMANCE monitoring"
echo "  • 📁 GET HITS with organization"
echo ""
echo "Test your bot: @megacheckk_bot"