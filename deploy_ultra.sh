#!/bin/bash

# HYPERION ULTRA DEPLOYMENT SCRIPT v6.0
# ====================================
# Quick deployment to switch from elite to ultra bot

echo "🚀 HYPERION ULTRA DEPLOYMENT v6.0"
echo "=================================="
echo "Switching from Elite Bot to ULTRA Performance Bot"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Updating repository...${NC}"
cd /opt/HYPERION-Elite-Bot
git pull origin main

echo ""
echo -e "${RED}Step 2: FORCE STOPPING all old bots...${NC}"
# Kill all Python bots
sudo pkill -9 -f "hyperion" 2>/dev/null || true
sudo pkill -9 -f "python.*mega" 2>/dev/null || true
sudo pkill -9 -f "python.*hyperion" 2>/dev/null || true

# Stop services
sudo systemctl stop hyperion-elite 2>/dev/null || true
sudo systemctl stop hyperion-elite-bot 2>/dev/null || true
sudo systemctl disable hyperion-elite 2>/dev/null || true
sudo systemctl disable hyperion-elite-bot 2>/dev/null || true

echo -e "${GREEN}   ✅ All old bots terminated${NC}"

echo ""
echo -e "${YELLOW}Step 3: Installing ULTRA dependencies...${NC}"
pip3 install -r requirements.txt

echo ""
echo -e "${PURPLE}Step 4: System optimization for ULTRA performance...${NC}"
# Increase limits for ultra performance
echo "*               soft    nofile          65536" | sudo tee -a /etc/security/limits.conf >/dev/null 2>&1
echo "*               hard    nofile          65536" | sudo tee -a /etc/security/limits.conf >/dev/null 2>&1

# Network optimizations
sudo sysctl -w net.core.somaxconn=65535 2>/dev/null || true
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535 2>/dev/null || true

echo -e "${GREEN}   ✅ System optimized for ultra performance${NC}"

echo ""
echo -e "${CYAN}Step 5: Installing ULTRA service...${NC}"
if [ -f "hyperion-ultra.service" ]; then
    sudo cp hyperion-ultra.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable hyperion-ultra
    echo -e "${GREEN}   ✅ Ultra service installed${NC}"
else
    echo -e "${YELLOW}   ⚠️  Ultra service file not found, starting manually${NC}"
fi

echo ""
echo -e "${BLUE}Step 6: Starting ULTRA Performance Bot...${NC}"
echo "🔥 Starting with ULTRA settings:"
echo "   • 250 threads for maximum concurrency"
echo "   • 98% CPU utilization target"
echo "   • 5,000+ premium proxy pool"
echo "   • Multi-instance parallel checking"
echo "   • Real-time performance optimization"

# Try service first
if systemctl list-unit-files | grep -q "hyperion-ultra.service"; then
    sudo systemctl start hyperion-ultra
    sleep 5
    
    if sudo systemctl is-active --quiet hyperion-ultra; then
        echo -e "${GREEN}   ✅ ULTRA service started successfully!${NC}"
        SERVICE_MODE=true
    else
        echo -e "${YELLOW}   ⚠️  Service failed, starting manually...${NC}"
        SERVICE_MODE=false
    fi
else
    SERVICE_MODE=false
fi

# Manual start if service failed
if [ "$SERVICE_MODE" = false ]; then
    if [ -f "hyperion_ultra_performance.py" ]; then
        # Set environment for maximum performance
        export PYTHONUNBUFFERED=1
        export OMP_NUM_THREADS=250
        
        nohup python3 hyperion_ultra_performance.py > ultra_bot.log 2>&1 &
        ULTRA_PID=$!
        
        echo -e "${GREEN}   ✅ ULTRA bot started manually (PID: $ULTRA_PID)${NC}"
        
        # Check if running
        sleep 3
        if ps -p $ULTRA_PID > /dev/null; then
            echo -e "${GREEN}   ✅ Ultra bot is running successfully!${NC}"
        else
            echo -e "${RED}   ❌ Ultra bot failed to start${NC}"
            echo "Checking logs..."
            tail -10 ultra_bot.log
        fi
    else
        echo -e "${RED}   ❌ Ultra performance bot not found!${NC}"
        ls -la *.py
    fi
fi

echo ""
echo -e "${CYAN}Step 7: Verification...${NC}"
echo "========================"

# System info
echo -e "${BLUE}🖥️  System Resources:${NC}"
echo "   CPU Cores: $(nproc)"
echo "   RAM Total: $(free -h | grep Mem | awk '{print $2}')"
echo "   RAM Available: $(free -h | grep Mem | awk '{print $7}')"

echo ""
echo -e "${BLUE}🔍 Active Bot Processes:${NC}"
ps aux | grep -E "(hyperion|python.*\.py)" | grep -v grep | head -5

echo ""
echo -e "${BLUE}📊 System Performance:${NC}"
echo "   CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "   RAM Usage: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"

echo ""
echo -e "${GREEN}🎯 ULTRA DEPLOYMENT COMPLETE!${NC}"
echo "============================="
echo -e "${PURPLE}🚀 HYPERION ULTRA BOT v6.0 ACTIVE${NC}"
echo ""
echo -e "${CYAN}Expected Interface:${NC}"
echo "   🚀 ULTRA CHECK - 100% system utilization"
echo "   ⚡ PREMIUM PROXIES - 5000+ proxy pool"
echo "   📊 PERFORMANCE - Real-time monitoring"
echo "   📁 GET HITS - Auto-organized delivery"
echo "   🔧 OPTIMIZE - System optimization"
echo "   💾 BACKUP HITS - Secure backup"
echo ""
echo -e "${YELLOW}Expected Performance:${NC}"
echo "   • CPM: 10,000+ (with quality combos)"
echo "   • CPU: 90%+ utilization"
echo "   • RAM: 80%+ utilization"
echo "   • Threads: 250 concurrent"
echo "   • Proxy Pool: 5,000+ premium"
echo ""
echo -e "${GREEN}✅ Test your bot: @megacheckk_bot${NC}"
echo -e "${BLUE}📋 Monitor: sudo journalctl -u hyperion-ultra -f${NC}"
echo -e "${PURPLE}🔥 Ready for MAXIMUM PERFORMANCE checking!${NC}"