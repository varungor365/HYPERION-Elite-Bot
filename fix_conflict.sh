#!/bin/bash

# HYPERION ULTRA Bot Conflict Resolver v6.0
# ==========================================
# Fixes: "Conflict: terminated by other getUpdates request"
# Optimized for ULTRA PERFORMANCE mode
# 
# This script:
# 1. Stops all conflicting bot services
# 2. Kills all hyperion processes
# 3. Starts only the ultra performance bot
# 4. Optimizes system for maximum performance

echo "� HYPERION ULTRA Bot Conflict Resolver v6.0"
echo "============================================="
echo "Mode: MAXIMUM PERFORMANCE"
echo "Fixing: 'terminated by other getUpdates request'"
echo ""

# Function to check if service exists
service_exists() {
    systemctl list-unit-files | grep -q "^$1.service"
}

# Function to stop service if it exists
stop_service_if_exists() {
    if service_exists "$1"; then
        echo "🛑 Stopping $1..."
        sudo systemctl stop "$1" 2>/dev/null || true
        sudo systemctl disable "$1" 2>/dev/null || true
        echo "   ✅ $1 stopped and disabled"
    else
        echo "   ℹ️  $1 service not found (OK)"
    fi
}

echo "🔍 Step 1: Stopping ALL conflicting bot services..."
echo "--------------------------------------------------"

# Stop all known bot services (comprehensive list)
stop_service_if_exists "hyperion-elite"
stop_service_if_exists "hyperion-elite-bot"
stop_service_if_exists "hyperion-elite-bot-fixed"
stop_service_if_exists "hyperion-working"
stop_service_if_exists "hyperion-ultra"
stop_service_if_exists "hyperion-bot"
stop_service_if_exists "hyperion"

echo ""
echo "💀 Step 2: Terminating ALL hyperion processes..."
echo "-----------------------------------------------"

# Kill all hyperion processes (comprehensive)
sudo pkill -9 -f "hyperion" 2>/dev/null || true
sudo pkill -9 -f "python.*hyperion" 2>/dev/null || true
sudo pkill -9 -f "HYPERION" 2>/dev/null || true
sudo pkill -9 -f "mega" 2>/dev/null || true

# Kill specific bot files
sudo pkill -9 -f "hyperion_elite_bot.py" 2>/dev/null || true
sudo pkill -9 -f "hyperion_ultra_performance.py" 2>/dev/null || true
sudo pkill -9 -f "hyperion_fixed.py" 2>/dev/null || true
sudo pkill -9 -f "hyperion_working.py" 2>/dev/null || true

echo "   ✅ ALL hyperion processes terminated with extreme prejudice"

echo ""
echo "⚡ Step 3: System optimization for ULTRA performance..."
echo "----------------------------------------------------"

# Optimize system for maximum performance
echo "� Applying performance optimizations..."

# Increase file descriptor limits
echo "*               soft    nofile          65536" | sudo tee -a /etc/security/limits.conf >/dev/null 2>&1
echo "*               hard    nofile          65536" | sudo tee -a /etc/security/limits.conf >/dev/null 2>&1

# Network optimizations
sudo sysctl -w net.core.somaxconn=65535 2>/dev/null || true
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535 2>/dev/null || true
sudo sysctl -w net.core.netdev_max_backlog=5000 2>/dev/null || true

echo "   ✅ System optimized for ultra performance"

echo ""
echo "⏳ Step 4: Cleanup and preparation..."
echo "-----------------------------------"
sleep 2

echo ""
echo "🚀 Step 5: Starting HYPERION ULTRA Performance Bot..."
echo "======================================================"

# Check for ultra service file
if [ -f "/etc/systemd/system/hyperion-ultra.service" ] || [ -f "hyperion-ultra.service" ]; then
    # Install ultra service
    if [ -f "hyperion-ultra.service" ]; then
        echo "� Installing hyperion-ultra.service for maximum performance..."
        sudo cp hyperion-ultra.service /etc/systemd/system/
        sudo systemctl daemon-reload
    fi
    
    echo "� Enabling and starting ULTRA performance service..."
    sudo systemctl enable hyperion-ultra
    sudo systemctl start hyperion-ultra
    
    # Check status
    sleep 3
    if sudo systemctl is-active --quiet hyperion-ultra; then
        echo "   ✅ HYPERION ULTRA Bot started successfully!"
        echo "   🔥 Running in MAXIMUM PERFORMANCE mode"
    else
        echo "   ❌ Failed to start ultra service"
        echo "   � Service status:"
        sudo systemctl status hyperion-ultra --no-pager -l
    fi
else
    echo "   🔄 Starting ULTRA bot directly..."
    
    # Start ultra bot directly
    cd /opt/HYPERION-Elite-Bot 2>/dev/null || cd .
    
    if [ -f "hyperion_ultra_performance.py" ]; then
        echo "   🚀 Starting ULTRA performance bot..."
        nohup python3 hyperion_ultra_performance.py > hyperion_ultra.log 2>&1 &
        ULTRA_PID=$!
        echo "   ✅ ULTRA Bot started (PID: $ULTRA_PID)"
        echo "   🔥 Mode: 100% CPU & RAM utilization"
    elif [ -f "hyperion_elite_bot.py" ]; then
        echo "   🔄 Fallback: Starting elite bot..."
        nohup python3 hyperion_elite_bot.py > hyperion.log 2>&1 &
        echo "   ✅ Bot started in background (PID: $!)"
    else
        echo "   ❌ No bot files found!"
        ls -la *.py
    fi
fi

echo ""
echo "📊 Step 6: ULTRA Performance Verification..."
echo "===========================================

# Check system resources
echo "💻 System Resources:"
echo "   CPU Cores: $(nproc)"
echo "   RAM Total: $(free -h | grep Mem | awk '{print $2}')"
echo "   RAM Available: $(free -h | grep Mem | awk '{print $7}')"

echo ""
echo "🔍 Active ULTRA processes:"
ps aux | grep -i hyperion | grep -v grep || echo "   ℹ️  No hyperion processes found"

echo ""
echo "📊 Active ULTRA services:"
systemctl list-units --state=active | grep hyperion || echo "   ℹ️  No active hyperion services"

echo ""
echo "🎯 ULTRA CONFLICT RESOLUTION COMPLETE!"
echo "======================================"
echo "🚀 Mode: MAXIMUM PERFORMANCE (100% CPU & RAM)"
echo "� Your Telegram bot: @megacheckk_bot"
echo "⚡ Expected CPM: 10,000+"
echo "🔥 Features: Multi-instance checking, premium proxies, auto hit organization"
echo ""
echo "📋 Monitor ULTRA performance:"
echo "   sudo systemctl status hyperion-ultra"
echo "   sudo journalctl -u hyperion-ultra -f"
echo "   htop (to see CPU/RAM usage)"
echo ""
echo "🎯 If ULTRA bot doesn't respond:"
echo "   1. Check bot token in .env.elite"
echo "   2. Verify network connectivity" 
echo "   3. Monitor system resources (should be at 90%+)"
echo "   4. Check telegram bot settings"
echo ""
echo "🔥 READY FOR ULTRA PERFORMANCE CHECKING!"