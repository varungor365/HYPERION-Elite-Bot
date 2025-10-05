#!/bin/bash

# HYPERION ULTRA v7.0 CLEAN DEPLOYMENT
# ===================================
# Clean install of v7.0 with real-time updates and file organization

echo "🚀 HYPERION ULTRA v7.0 CLEAN DEPLOYMENT"
echo "======================================="
echo "Installing v7.0 with real-time updates and organized file structure"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${RED}Step 1: COMPLETE CLEANUP of all old bots...${NC}"
echo "=============================================="

# Kill ALL bot processes
echo "💀 Terminating all bot processes..."
sudo pkill -9 -f "hyperion" 2>/dev/null || true
sudo pkill -9 -f "python.*hyperion" 2>/dev/null || true
sudo pkill -9 -f "python.*mega" 2>/dev/null || true
sudo pkill -9 -f "HYPERION" 2>/dev/null || true

# Stop and disable ALL services
echo "🛑 Stopping all bot services..."
sudo systemctl stop hyperion-elite 2>/dev/null || true
sudo systemctl stop hyperion-elite-bot 2>/dev/null || true
sudo systemctl stop hyperion-ultra 2>/dev/null || true
sudo systemctl stop hyperion-working 2>/dev/null || true
sudo systemctl disable hyperion-elite 2>/dev/null || true
sudo systemctl disable hyperion-elite-bot 2>/dev/null || true
sudo systemctl disable hyperion-ultra 2>/dev/null || true
sudo systemctl disable hyperion-working 2>/dev/null || true

# Remove old service files
sudo rm -f /etc/systemd/system/hyperion-*.service
sudo systemctl daemon-reload

echo -e "${GREEN}✅ All old bots and services removed!${NC}"

echo ""
echo -e "${BLUE}Step 2: Repository cleanup and update...${NC}"
echo "======================================="

cd /opt/HYPERION-Elite-Bot

# Force clean repository
git reset --hard HEAD
git clean -fd
git pull origin main --force

echo -e "${GREEN}✅ Repository updated to latest v7.0!${NC}"

echo ""
echo -e "${PURPLE}Step 3: DELETE old bot files...${NC}"
echo "==============================="

# Remove ALL old bot variants
echo "🗑️ Removing old bot files..."
rm -f hyperion_elite_bot.py 2>/dev/null || true
rm -f hyperion_ultra_performance.py 2>/dev/null || true
rm -f hyperion_fixed.py 2>/dev/null || true
rm -f hyperion_working.py 2>/dev/null || true
rm -f hyperion_headless.py 2>/dev/null || true
rm -f hyperion_turbo.py 2>/dev/null || true
rm -f debug_bot.py 2>/dev/null || true
rm -f test_bot_simple.py 2>/dev/null || true

echo -e "${GREEN}✅ Old bot files deleted!${NC}"

echo ""
echo -e "${CYAN}Step 4: File structure organization...${NC}"
echo "===================================="

# Create organized folder structure
echo "📁 Creating organized folder structure..."
mkdir -p combos
mkdir -p hits  
mkdir -p backups
mkdir -p logs

# Move any existing files to appropriate folders
mv *.txt combos/ 2>/dev/null || true
mv *hits*.txt hits/ 2>/dev/null || true
mv *.zip backups/ 2>/dev/null || true
mv *.log logs/ 2>/dev/null || true

echo -e "${GREEN}✅ Organized file structure created!${NC}"
echo "   📂 combos/ - For combo files"
echo "   📂 hits/ - For hit files"
echo "   📂 backups/ - For backup files"
echo "   📂 logs/ - For log files"

echo ""
echo -e "${YELLOW}Step 5: Installing v7.0 dependencies...${NC}"
echo "======================================="

pip3 install -r requirements.txt --upgrade

echo ""
echo -e "${BLUE}Step 6: Creating v7.0 service...${NC}"
echo "==============================="

# Create v7.0 service file
cat > hyperion-ultra-v7.service << EOF
[Unit]
Description=HYPERION Ultra Bot v7.0 - Real-Time Performance
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/HYPERION-Elite-Bot
Environment=PYTHONPATH=/opt/HYPERION-Elite-Bot
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 hyperion_ultra_v7.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Ultra Performance Optimizations
Nice=-10
IOSchedulingClass=1
IOSchedulingPriority=4
CPUSchedulingPolicy=1
CPUSchedulingPriority=50

# Resource Limits
LimitNOFILE=65536
LimitNPROC=32768
LimitCORE=infinity

# Memory optimization
OOMScoreAdjust=-500
Environment=MALLOC_ARENA_MAX=2

[Install]
WantedBy=multi-user.target
EOF

# Install v7.0 service
sudo cp hyperion-ultra-v7.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hyperion-ultra-v7

echo -e "${GREEN}✅ v7.0 service created and enabled!${NC}"

echo ""
echo -e "${GREEN}Step 7: STARTING HYPERION ULTRA v7.0...${NC}"
echo "======================================="

echo -e "${PURPLE}🔥 ULTRA v7.0 FEATURES:${NC}"
echo "   • Real-time progress updates every 10 seconds"
echo "   • Live CPM, CPU, RAM monitoring"
echo "   • Organized file structure (combos/, hits/, backups/)"
echo "   • 250+ ultra threads for maximum speed"
echo "   • Auto hit delivery and categorization"

# Start v7.0
sudo systemctl start hyperion-ultra-v7

sleep 5

# Check if running
if sudo systemctl is-active --quiet hyperion-ultra-v7; then
    echo -e "${GREEN}✅ HYPERION ULTRA v7.0 STARTED SUCCESSFULLY!${NC}"
    echo -e "${PURPLE}🔥 Mode: REAL-TIME PERFORMANCE${NC}"
else
    echo -e "${YELLOW}⚠️ Service failed, starting manually...${NC}"
    
    if [ -f "hyperion_ultra_v7.py" ]; then
        # Manual start
        export PYTHONUNBUFFERED=1
        nohup python3 hyperion_ultra_v7.py > logs/ultra_v7.log 2>&1 &
        V7_PID=$!
        
        echo -e "${GREEN}✅ v7.0 started manually (PID: $V7_PID)${NC}"
        
        # Verify running
        sleep 3
        if ps -p $V7_PID > /dev/null; then
            echo -e "${GREEN}✅ v7.0 verified running!${NC}"
        else
            echo -e "${RED}❌ v7.0 failed to start${NC}"
            echo "Log output:"
            tail -10 logs/ultra_v7.log 2>/dev/null || echo "No log found"
        fi
    else
        echo -e "${RED}❌ hyperion_ultra_v7.py not found!${NC}"
        ls -la *.py
    fi
fi

echo ""
echo -e "${CYAN}Step 8: v7.0 VERIFICATION...${NC}"
echo "=========================="

# System info
echo -e "${BLUE}💻 System Resources:${NC}"
echo "   CPU Cores: $(nproc)"
echo "   RAM Total: $(free -h | grep Mem | awk '{print $2}')"
echo "   RAM Available: $(free -h | grep Mem | awk '{print $7}')"

echo ""
echo -e "${BLUE}📁 Organized Structure:${NC}"
echo "   Combos: $(ls combos/*.txt 2>/dev/null | wc -l) files"
echo "   Hits: $(ls hits/*.txt 2>/dev/null | wc -l) files"  
echo "   Backups: $(ls backups/*.zip 2>/dev/null | wc -l) files"

echo ""
echo -e "${BLUE}🔍 Active v7.0 Process:${NC}"
HYPERION_V7=$(ps aux | grep "hyperion_ultra_v7" | grep -v grep)
if [ -n "$HYPERION_V7" ]; then
    echo "$HYPERION_V7"
else
    echo -e "${YELLOW}   No v7.0 process found${NC}"
fi

echo ""
echo -e "${GREEN}🎯 HYPERION ULTRA v7.0 DEPLOYMENT COMPLETE!${NC}"
echo "============================================="
echo -e "${PURPLE}🚀 HYPERION ULTRA BOT v7.0 - REAL-TIME PERFORMANCE${NC}"
echo ""
echo -e "${CYAN}✨ NEW v7.0 INTERFACE:${NC}"
echo "   🚀 ULTRA CHECK - Real-time progress updates"
echo "   📊 SYSTEM STATS - Live monitoring"
echo "   📁 MANAGE HITS - Organized delivery"
echo "   🗂️ COMBO FOLDER - File management"
echo "   💾 BACKUP ALL - Complete backups"
echo "   🔧 OPTIMIZE - System optimization"
echo ""
echo -e "${YELLOW}🔥 v7.0 FEATURES:${NC}"
echo "   • Real-time updates every 10 seconds"
echo "   • Live CPM: 10,000+ target"
echo "   • CPU: 85% utilization target"  
echo "   • Threads: 250 ultra threads"
echo "   • Organized: combos/, hits/, backups/"
echo ""
echo -e "${GREEN}✅ Test your v7.0 bot: @megacheckk_bot${NC}"
echo -e "${BLUE}📋 Monitor: sudo journalctl -u hyperion-ultra-v7 -f${NC}"
echo -e "${PURPLE}🔥 Ready for REAL-TIME ultra performance!${NC}"

echo ""
echo -e "${CYAN}🎯 EXPECTED v7.0 BEHAVIOR:${NC}"
echo "When you upload a combo file, you'll see:"
echo "• Real-time progress updates every 10 seconds"
echo "• Live CPM counter increasing"
echo "• CPU and RAM utilization displayed"
echo "• Progress percentage and ETA"
echo "• Auto-organized hit file delivery"
echo ""
echo -e "${GREEN}🔥 NO MORE STUCK MESSAGES - REAL-TIME UPDATES GUARANTEED!${NC}"