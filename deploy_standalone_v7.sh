#!/bin/bash

# 🚀 HYPERION ULTRA v7.0 - STANDALONE SERVICE DEPLOYMENT
# =====================================================
# Deploy standalone real-time checker that processes combo files directly

echo "🚀 DEPLOYING HYPERION ULTRA v7.0 STANDALONE..."

# Kill all existing processes
echo "🔥 Stopping all HYPERION processes..."
sudo pkill -f "hyperion" || true
sudo pkill -f "mega_auth" || true
sudo systemctl stop hyperion-ultra-v7 || true
sudo systemctl disable hyperion-ultra-v7 || true

# Clean old files
echo "🧹 Cleaning old installations..."
cd /opt/HYPERION-Elite-Bot || exit 1

# Update from git
echo "📥 Updating from repository..."
git pull origin main

# Create combo file with test data if empty
echo "📁 Setting up combo file..."
if [ ! -s "combo.txt" ] && [ ! -s "combos/combo.txt" ]; then
    echo "Creating test combo file..."
    mkdir -p combos
    cat > combos/combo.txt << 'EOF'
test1@mega.nz:testpass123
test2@mega.nz:testpass456  
test3@mega.nz:testpass789
example1@protonmail.com:password123
example2@gmail.com:password456
testuser@outlook.com:mypassword
demo@yahoo.com:demopass
sample@mega.nz:samplepass
EOF
    echo "✅ Created test combo file with 8 test accounts"
    echo "📝 Edit combos/combo.txt with your real accounts!"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create new service for standalone version
echo "🔧 Creating standalone service..."
sudo tee /etc/systemd/system/hyperion-ultra-standalone.service > /dev/null << 'EOF'
[Unit]
Description=HYPERION ULTRA v7.0 Standalone Real-Time Checker
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/HYPERION-Elite-Bot
ExecStart=/usr/bin/python3 /opt/HYPERION-Elite-Bot/hyperion_ultra_v7_standalone.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Performance optimizations
CPUSchedulingPolicy=1
CPUSchedulingPriority=50
IOSchedulingClass=1
IOSchedulingPriority=4
OOMScoreAdjust=-100

# Resource limits
LimitNOFILE=65536
LimitNPROC=65536

# Environment
Environment=PYTHONUNBUFFERED=1
Environment=MALLOC_ARENA_MAX=2

[Install]
WantedBy=multi-user.target
EOF

# Reload and start service
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

echo "🚀 Starting HYPERION ULTRA v7.0 Standalone..."
sudo systemctl enable hyperion-ultra-standalone
sudo systemctl start hyperion-ultra-standalone

# Wait a moment
sleep 3

# Check status
echo ""
echo "📊 SERVICE STATUS:"
sudo systemctl status hyperion-ultra-standalone --no-pager -l

echo ""
echo "🎯 FOLLOW REAL-TIME LOGS:"
echo "sudo journalctl -u hyperion-ultra-standalone -f"

echo ""
echo "✅ HYPERION ULTRA v7.0 STANDALONE DEPLOYED!"
echo "🔥 Real-time progress updates every 10 seconds"
echo "📁 Organized file structure: combos/, hits/, backups/"
echo "⚡ Maximum performance with 250 threads"
echo ""
echo "📝 To add your combo file:"
echo "nano /opt/HYPERION-Elite-Bot/combos/combo.txt"
echo ""
echo "🔄 To restart after adding combos:"
echo "sudo systemctl restart hyperion-ultra-standalone"