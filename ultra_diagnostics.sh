#!/bin/bash

# HYPERION ULTRA DIAGNOSTICS v6.0
# ===============================
# Diagnose why ultra bot is stuck during checking

echo "🔍 HYPERION ULTRA DIAGNOSTICS v6.0"
echo "==================================="
echo "Diagnosing stuck ultra bot..."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}📊 SYSTEM DIAGNOSTICS${NC}"
echo "===================="

# System resources
echo -e "${CYAN}💻 System Resources:${NC}"
echo "   CPU Cores: $(nproc)"
echo "   RAM Total: $(free -h | grep Mem | awk '{print $2}')"
echo "   RAM Used: $(free -h | grep Mem | awk '{print $3}')"
echo "   RAM Available: $(free -h | grep Mem | awk '{print $7}')"
echo "   Load Average: $(uptime | awk -F'load average:' '{print $2}')"

echo ""
echo -e "${CYAN}🔍 Bot Processes:${NC}"
HYPERION_PROCS=$(ps aux | grep -E "(hyperion|python.*\.py)" | grep -v grep)
if [ -n "$HYPERION_PROCS" ]; then
    echo "$HYPERION_PROCS"
    echo ""
    echo -e "${GREEN}✅ Bot processes found${NC}"
else
    echo -e "${RED}❌ No bot processes running!${NC}"
fi

echo ""
echo -e "${BLUE}📋 SERVICE STATUS${NC}"
echo "================="

# Check services
if systemctl list-units --state=active | grep -q hyperion; then
    echo -e "${GREEN}Active services:${NC}"
    systemctl list-units --state=active | grep hyperion
else
    echo -e "${YELLOW}⚠️  No active hyperion services${NC}"
fi

echo ""
echo -e "${BLUE}📜 LOG ANALYSIS${NC}"
echo "==============="

# Check various log locations
echo -e "${CYAN}🔍 Checking log files:${NC}"

# Service logs
if systemctl list-units | grep -q hyperion-ultra; then
    echo ""
    echo -e "${PURPLE}📋 Service Logs (last 20 lines):${NC}"
    sudo journalctl -u hyperion-ultra --no-pager -n 20
fi

# Manual bot logs
if [ -f "ultra_performance.log" ]; then
    echo ""
    echo -e "${PURPLE}📋 Ultra Performance Log (last 20 lines):${NC}"
    tail -20 ultra_performance.log
elif [ -f "ultra_bot.log" ]; then
    echo ""
    echo -e "${PURPLE}📋 Ultra Bot Log (last 20 lines):${NC}"
    tail -20 ultra_bot.log
fi

# Python error logs
if [ -f "nohup.out" ]; then
    echo ""
    echo -e "${PURPLE}📋 Nohup Output (last 20 lines):${NC}"
    tail -20 nohup.out
fi

echo ""
echo -e "${BLUE}🔍 STUCK POINT ANALYSIS${NC}"
echo "======================="

# Check if mega.py is the issue
echo -e "${CYAN}🧠 Checking MEGA library:${NC}"
python3 -c "
try:
    from mega import Mega
    print('✅ MEGA library imported successfully')
    m = Mega()
    print('✅ MEGA instance created successfully')
except Exception as e:
    print(f'❌ MEGA library error: {e}')
" 2>&1

echo ""
echo -e "${CYAN}📡 Network Connectivity:${NC}"
# Test network
if ping -c 1 google.com > /dev/null 2>&1; then
    echo "✅ Internet connectivity: OK"
else
    echo "❌ Internet connectivity: FAILED"
fi

if ping -c 1 mega.nz > /dev/null 2>&1; then
    echo "✅ MEGA.nz connectivity: OK"
else
    echo "❌ MEGA.nz connectivity: FAILED" 
fi

echo ""
echo -e "${CYAN}🔧 Dependencies Check:${NC}"
# Check critical dependencies
python3 -c "
import sys
deps = ['telegram', 'requests', 'aiohttp', 'psutil', 'mega']
for dep in deps:
    try:
        __import__(dep)
        print(f'✅ {dep}: OK')
    except ImportError as e:
        print(f'❌ {dep}: MISSING - {e}')
"

echo ""
echo -e "${BLUE}🚀 TROUBLESHOOTING STEPS${NC}"
echo "========================"

echo -e "${YELLOW}If bot is stuck at 'ULTRA CHECKING STARTED':${NC}"
echo ""
echo -e "${CYAN}1. Check mega.py initialization:${NC}"
echo "   python3 -c \"from mega import Mega; print('MEGA OK')\""
echo ""
echo -e "${CYAN}2. Monitor real-time logs:${NC}"
echo "   sudo journalctl -u hyperion-ultra -f"
echo "   # OR"
echo "   tail -f ultra_performance.log"
echo ""
echo -e "${CYAN}3. Check system resources:${NC}"
echo "   htop"
echo "   # Look for high CPU/RAM usage or stuck processes"
echo ""
echo -e "${CYAN}4. Force restart ultra bot:${NC}"
echo "   sudo systemctl restart hyperion-ultra"
echo "   # OR manually:"
echo "   pkill -f hyperion_ultra_performance.py"
echo "   python3 hyperion_ultra_performance.py"
echo ""
echo -e "${CYAN}5. Test with smaller combo file:${NC}"
echo "   # Try with 100-1000 combos first"
echo ""
echo -e "${CYAN}6. Check thread limits:${NC}"
echo "   ulimit -u    # Should be high for 250 threads"
echo "   ulimit -n    # Should be 65536 for file descriptors"

echo ""
echo -e "${RED}🔄 QUICK FIX COMMANDS:${NC}"
echo "===================="
echo -e "${YELLOW}# Restart ultra bot service:${NC}"
echo "sudo systemctl restart hyperion-ultra"
echo ""
echo -e "${YELLOW}# OR restart manually:${NC}"
echo "pkill -f hyperion"
echo "cd /opt/HYPERION-Elite-Bot"
echo "python3 hyperion_ultra_performance.py &"
echo ""
echo -e "${YELLOW}# Monitor in real-time:${NC}"
echo "tail -f ultra_performance.log"

echo ""
echo -e "${PURPLE}🎯 Run this script anytime: sudo ./ultra_diagnostics.sh${NC}"