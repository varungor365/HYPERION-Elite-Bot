#!/bin/bash

# HYPERION ULTRA POST-DEPLOYMENT CHECKER v6.0
# ==========================================
# Verify ultra deployment was successful

echo "🔍 HYPERION ULTRA POST-DEPLOYMENT CHECKER v6.0"
echo "==============================================="
echo "Verifying your ultra deployment was successful..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}📊 DEPLOYMENT VERIFICATION${NC}"
echo "=========================="

# Check if ultra bot is running
echo -e "${CYAN}🔍 Checking Ultra Bot Status:${NC}"

if sudo systemctl is-active --quiet hyperion-ultra 2>/dev/null; then
    echo -e "${GREEN}✅ ULTRA SERVICE: ACTIVE${NC}"
    SERVICE_STATUS="ACTIVE"
elif pgrep -f "hyperion_ultra_performance.py" > /dev/null; then
    echo -e "${GREEN}✅ ULTRA BOT: RUNNING MANUALLY${NC}"
    SERVICE_STATUS="MANUAL"
elif pgrep -f "hyperion.*\.py" > /dev/null; then
    echo -e "${YELLOW}⚠️  FALLBACK BOT: RUNNING${NC}"
    SERVICE_STATUS="FALLBACK"
else
    echo -e "${RED}❌ NO BOT DETECTED${NC}"
    SERVICE_STATUS="NONE"
fi

echo ""
echo -e "${CYAN}📋 Current Bot Processes:${NC}"
HYPERION_PROCS=$(ps aux | grep -E "(hyperion|python.*\.py)" | grep -v grep)
if [ -n "$HYPERION_PROCS" ]; then
    echo "$HYPERION_PROCS" | head -3
else
    echo -e "${RED}   No hyperion processes found${NC}"
fi

echo ""
echo -e "${CYAN}💻 System Resources:${NC}"
echo "   CPU Cores: $(nproc)"
echo "   RAM Total: $(free -h | grep Mem | awk '{print $2}')"
echo "   RAM Used: $(free -h | grep Mem | awk '{print $3}')"
echo "   Load: $(uptime | awk -F'load average:' '{print $2}' | xargs)"

echo ""
echo -e "${CYAN}📡 Network Tests:${NC}"
if ping -c 1 -W 3 8.8.8.8 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Internet: Connected${NC}"
else
    echo -e "${RED}❌ Internet: Failed${NC}"
fi

if ping -c 1 -W 3 api.telegram.org > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Telegram API: Reachable${NC}"
else
    echo -e "${RED}❌ Telegram API: Failed${NC}"
fi

echo ""
echo -e "${BLUE}🎯 BOT TESTING INSTRUCTIONS${NC}"
echo "=========================="

if [ "$SERVICE_STATUS" = "ACTIVE" ] || [ "$SERVICE_STATUS" = "MANUAL" ]; then
    echo -e "${GREEN}✅ Your ultra bot is running!${NC}"
    echo ""
    echo -e "${PURPLE}🎮 Test Steps:${NC}"
    echo "1. Go to: @megacheckk_bot"
    echo "2. Send: /start"
    echo "3. Look for: 🚀 HYPERION ULTRA BOT v6.0"
    echo "4. Click: 🚀 ULTRA CHECK"
    echo "5. Upload a small combo file (100-500 lines)"
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
    echo "   • CPM: 5,000-10,000+ (vs old 23/min)"
    echo "   • CPU: 70-90% (vs old 13.9%)" 
    echo "   • Threads: 250 (vs old 8)"
    echo "   • Progress: Real-time updates"
    
elif [ "$SERVICE_STATUS" = "FALLBACK" ]; then
    echo -e "${YELLOW}⚠️  Fallback bot is running${NC}"
    echo ""
    echo -e "${CYAN}To activate ultra bot:${NC}"
    echo "sudo systemctl stop hyperion-elite"
    echo "sudo systemctl start hyperion-ultra"
    
else
    echo -e "${RED}❌ No bot is running!${NC}"
    echo ""
    echo -e "${CYAN}Quick fix commands:${NC}"
    echo "cd /opt/HYPERION-Elite-Bot"
    echo "sudo systemctl start hyperion-ultra"
    echo "# OR manually:"
    echo "python3 hyperion_ultra_performance.py &"
fi

echo ""
echo -e "${BLUE}📜 MONITORING COMMANDS${NC}"
echo "====================="
echo -e "${CYAN}Real-time logs:${NC}"
echo "sudo journalctl -u hyperion-ultra -f"
echo ""
echo -e "${CYAN}System monitoring:${NC}"
echo "htop"
echo ""
echo -e "${CYAN}Bot process check:${NC}"
echo "ps aux | grep hyperion"
echo ""
echo -e "${CYAN}Service status:${NC}"
echo "sudo systemctl status hyperion-ultra"

echo ""
if [ "$SERVICE_STATUS" = "ACTIVE" ] || [ "$SERVICE_STATUS" = "MANUAL" ]; then
    echo -e "${GREEN}🎯 ULTRA DEPLOYMENT SUCCESSFUL!${NC}"
    echo -e "${PURPLE}Your bot is ready for maximum performance checking!${NC}"
else
    echo -e "${YELLOW}⚠️  DEPLOYMENT NEEDS ATTENTION${NC}"
    echo -e "${CYAN}Run the troubleshooting commands above${NC}"
fi

echo ""
echo -e "${BLUE}🔄 Run this checker anytime: curl -s https://raw.githubusercontent.com/varungor365/HYPERION-Elite-Bot/main/post_deploy_check.sh | bash${NC}"