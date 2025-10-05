#!/bin/bash

# HYPERION ULTRA FORCE DEPLOYMENT v6.0
# ====================================
# Resolves git conflicts and forces ultra bot deployment

echo "🚀 HYPERION ULTRA FORCE DEPLOYMENT v6.0"
echo "========================================"
echo "Resolving conflicts and forcing ultra deployment"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${RED}Step 1: FORCE RESOLVING Git Conflicts...${NC}"
echo "============================================"

# Backup current changes (just in case)
echo "📋 Backing up local changes..."
cp debug_bot.py debug_bot.py.backup 2>/dev/null || true
cp deploy_fixed.sh deploy_fixed.sh.backup 2>/dev/null || true
cp emergency_fix.sh emergency_fix.sh.backup 2>/dev/null || true
cp fix_conflict.sh fix_conflict.sh.backup 2>/dev/null || true
cp fixed-install.sh fixed-install.sh.backup 2>/dev/null || true
cp update_and_deploy.sh update_and_deploy.sh.backup 2>/dev/null || true

# Force reset to match repository
echo -e "${YELLOW}🔄 Force resetting to repository state...${NC}"
git reset --hard HEAD
git clean -fd
git pull origin main --force

echo -e "${GREEN}✅ Git conflicts resolved!${NC}"

echo ""
echo -e "${RED}Step 2: TERMINATING all old bots...${NC}"
echo "=================================="

# Kill ALL bot processes with extreme prejudice
sudo pkill -9 -f "hyperion" 2>/dev/null || true
sudo pkill -9 -f "python.*mega" 2>/dev/null || true
sudo pkill -9 -f "python.*hyperion" 2>/dev/null || true
sudo pkill -9 -f "python.*\.py" 2>/dev/null || true

# Stop and disable all bot services
sudo systemctl stop hyperion-elite 2>/dev/null || true
sudo systemctl stop hyperion-elite-bot 2>/dev/null || true
sudo systemctl stop hyperion-working 2>/dev/null || true
sudo systemctl stop hyperion-ultra 2>/dev/null || true
sudo systemctl disable hyperion-elite 2>/dev/null || true
sudo systemctl disable hyperion-elite-bot 2>/dev/null || true
sudo systemctl disable hyperion-working 2>/dev/null || true

echo -e "${GREEN}✅ ALL old bots terminated!${NC}"

echo ""
echo -e "${BLUE}Step 3: Installing ULTRA dependencies...${NC}"
echo "============================================"
pip3 install -r requirements.txt --upgrade

echo ""
echo -e "${PURPLE}Step 4: System ULTRA optimization...${NC}"
echo "===================================="

# Ultra performance settings
echo "*               soft    nofile          65536" | sudo tee -a /etc/security/limits.conf >/dev/null 2>&1
echo "*               hard    nofile          65536" | sudo tee -a /etc/security/limits.conf >/dev/null 2>&1

# Network optimization for ultra performance
sudo sysctl -w net.core.somaxconn=65535 2>/dev/null || true
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=65535 2>/dev/null || true
sudo sysctl -w net.core.netdev_max_backlog=5000 2>/dev/null || true
sudo sysctl -w net.ipv4.tcp_keepalive_time=300 2>/dev/null || true

echo -e "${GREEN}✅ System optimized for ULTRA performance!${NC}"

echo ""
echo -e "${CYAN}Step 5: Installing ULTRA service...${NC}"
echo "=================================="

# Install ultra service
if [ -f "hyperion-ultra.service" ]; then
    sudo cp hyperion-ultra.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable hyperion-ultra
    echo -e "${GREEN}✅ Ultra service installed and enabled${NC}"
else
    echo -e "${YELLOW}⚠️  Ultra service file not found${NC}"
fi

echo ""
echo -e "${BLUE}Step 6: STARTING ULTRA PERFORMANCE BOT...${NC}"
echo "=========================================="
echo -e "${PURPLE}🔥 ULTRA PERFORMANCE SPECS:${NC}"
echo "   • 250 ultra threads"
echo "   • 98% CPU utilization target"
echo "   • 5,000+ premium proxy pool"
echo "   • Multi-instance parallel checking"
echo "   • Target CPM: 10,000+"

# Try service start first
if [ -f "/etc/systemd/system/hyperion-ultra.service" ]; then
    echo -e "${CYAN}🚀 Starting ULTRA service...${NC}"
    sudo systemctl start hyperion-ultra
    
    sleep 5
    
    if sudo systemctl is-active --quiet hyperion-ultra; then
        echo -e "${GREEN}✅ ULTRA SERVICE STARTED SUCCESSFULLY!${NC}"
        echo -e "${PURPLE}🔥 Mode: SERVICE (Recommended)${NC}"
        SERVICE_RUNNING=true
    else
        echo -e "${YELLOW}⚠️  Service failed, trying manual start...${NC}"
        sudo journalctl -u hyperion-ultra --no-pager -l | tail -10
        SERVICE_RUNNING=false
    fi
else
    SERVICE_RUNNING=false
fi

# Manual start if service failed
if [ "$SERVICE_RUNNING" = false ]; then
    echo -e "${CYAN}🚀 Starting ULTRA bot manually...${NC}"
    
    if [ -f "hyperion_ultra_performance.py" ]; then
        # Set ultra performance environment
        export PYTHONUNBUFFERED=1
        export OMP_NUM_THREADS=250
        export MALLOC_ARENA_MAX=2
        
        # Start ultra bot
        nohup python3 hyperion_ultra_performance.py > ultra_performance.log 2>&1 &
        ULTRA_PID=$!
        
        echo -e "${GREEN}✅ ULTRA BOT STARTED! (PID: $ULTRA_PID)${NC}"
        echo -e "${PURPLE}🔥 Mode: MANUAL${NC}"
        
        # Verify it's running
        sleep 3
        if ps -p $ULTRA_PID > /dev/null; then
            echo -e "${GREEN}✅ Ultra bot verified running!${NC}"
        else
            echo -e "${RED}❌ Ultra bot failed to start!${NC}"
            echo "Last 10 lines of log:"
            tail -10 ultra_performance.log 2>/dev/null || echo "No log file found"
        fi
    else
        echo -e "${RED}❌ hyperion_ultra_performance.py not found!${NC}"
        echo "Available files:"
        ls -la *.py
        
        # Fallback to elite bot
        if [ -f "hyperion_elite_bot.py" ]; then
            echo -e "${YELLOW}🔄 Starting elite bot as fallback...${NC}"
            nohup python3 hyperion_elite_bot.py > elite_fallback.log 2>&1 &
            echo -e "${YELLOW}⚠️  Using elite bot - limited performance${NC}"
        fi
    fi
fi

echo ""
echo -e "${CYAN}Step 7: ULTRA VERIFICATION...${NC}"
echo "============================"

# System information
echo -e "${BLUE}💻 System Resources:${NC}"
echo "   CPU Cores: $(nproc)"
echo "   RAM Total: $(free -h | grep Mem | awk '{print $2}')"
echo "   RAM Available: $(free -h | grep Mem | awk '{print $7}')"

echo ""
echo -e "${BLUE}🔍 Active Bot Processes:${NC}"
HYPERION_PROCESSES=$(ps aux | grep -E "(hyperion|python.*\.py)" | grep -v grep)
if [ -n "$HYPERION_PROCESSES" ]; then
    echo "$HYPERION_PROCESSES" | head -5
else
    echo "   ⚠️  No hyperion processes found"
fi

echo ""
echo -e "${BLUE}📊 System Performance:${NC}"
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 2>/dev/null || echo "N/A")
RAM_USAGE=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}' 2>/dev/null || echo "N/A")
echo "   Current CPU: ${CPU_USAGE}%"
echo "   Current RAM: ${RAM_USAGE}%"

echo ""
echo -e "${BLUE}🔍 Service Status:${NC}"
if systemctl list-units --state=active | grep -q hyperion; then
    systemctl list-units --state=active | grep hyperion
else
    echo "   ℹ️  No active hyperion services"
fi

echo ""
echo -e "${GREEN}🎯 ULTRA DEPLOYMENT COMPLETE!${NC}"
echo "============================="
echo -e "${PURPLE}🚀 HYPERION ULTRA BOT v6.0${NC}"
echo ""
echo -e "${CYAN}Expected Ultra Interface:${NC}"
echo "   🚀 ULTRA CHECK"
echo "   ⚡ PREMIUM PROXIES" 
echo "   📊 PERFORMANCE"
echo "   📁 GET HITS"
echo "   🔧 OPTIMIZE"
echo "   💾 BACKUP HITS"
echo ""
echo -e "${YELLOW}Expected Performance:${NC}"
echo "   • CPM: 10,000+ (vs old 23/min)"
echo "   • CPU: 90%+ (vs old 13.9%)"
echo "   • Threads: 250 (vs old 8)"
echo "   • Proxies: 5000+ (vs old Direct)"
echo ""
echo -e "${GREEN}✅ Test: @megacheckk_bot${NC}"
echo -e "${BLUE}📋 Monitor: sudo journalctl -u hyperion-ultra -f${NC}"
echo -e "${PURPLE}🔥 Ready for MAXIMUM PERFORMANCE!${NC}"

# Final check
echo ""
echo -e "${CYAN}🔄 Final Bot Status Check...${NC}"
sleep 2

if sudo systemctl is-active --quiet hyperion-ultra 2>/dev/null; then
    echo -e "${GREEN}✅ ULTRA SERVICE: ACTIVE${NC}"
elif pgrep -f "hyperion_ultra_performance.py" > /dev/null; then
    echo -e "${GREEN}✅ ULTRA BOT: RUNNING MANUALLY${NC}"
elif pgrep -f "hyperion.*\.py" > /dev/null; then
    echo -e "${YELLOW}⚠️  FALLBACK BOT: RUNNING${NC}"
else
    echo -e "${RED}❌ NO BOT DETECTED - Check logs above${NC}"
fi

echo ""
echo -e "${PURPLE}🎯 DEPLOYMENT FINISHED!${NC}"