#!/bin/bash
# HYPERION Elite Bot Quick Start Script for Digital Ocean VPS
# Run with: bash quick_start_elite.sh

echo "🎯 HYPERION ELITE BOT - Quick Deployment"
echo "======================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# System updates
echo "📦 Updating system..."
apt update && apt upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python environment..."
apt install -y python3 python3-pip python3-venv git curl screen htop

# Create elite user
echo "👤 Creating elite user..."
useradd -m -s /bin/bash hyperion-elite || echo "User already exists"

# Create elite directory
ELITE_DIR="/home/hyperion-elite/hyperion_elite"
mkdir -p $ELITE_DIR
chown hyperion-elite:hyperion-elite $ELITE_DIR

# Setup Python environment as elite user
sudo -u hyperion-elite bash << 'EOF'
cd /home/hyperion-elite

echo "🔧 Setting up Elite Python environment..."
python3 -m venv hyperion_elite_env
source hyperion_elite_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install elite requirements
echo "📋 Installing Elite packages..."
pip install requests python-telegram-bot beautifulsoup4 lxml aiofiles

# Create directories
mkdir -p hyperion_elite/elite_results
mkdir -p hyperion_elite/logs
mkdir -p hyperion_elite/config

echo "✅ Elite environment ready"
EOF

# Create systemd service for elite bot
echo "⚙️ Creating Elite Bot service..."
cat > /etc/systemd/system/hyperion-elite-bot.service << 'EOF'
[Unit]
Description=HYPERION Elite Bot - Premium MEGA Checker
After=network.target

[Service]
Type=simple
User=hyperion-elite
Group=hyperion-elite
WorkingDirectory=/home/hyperion-elite/hyperion_elite
Environment=PATH=/home/hyperion-elite/hyperion_elite_env/bin
ExecStart=/home/hyperion-elite/hyperion_elite_env/bin/python hyperion_elite_bot.py
Restart=always
RestartSec=10
StandardOutput=append:/home/hyperion-elite/hyperion_elite/logs/elite_bot.log
StandardError=append:/home/hyperion-elite/hyperion_elite/logs/elite_bot.error.log

# Enhanced security for elite operations
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/hyperion-elite/hyperion_elite

[Install]
WantedBy=multi-user.target
EOF

# Enable elite service
systemctl daemon-reload
systemctl enable hyperion-elite-bot

# Create elite management scripts
echo "📜 Creating Elite management scripts..."

cat > /home/hyperion-elite/hyperion_elite/start_elite.sh << 'EOF'
#!/bin/bash
# Start HYPERION Elite Bot
source /home/hyperion-elite/hyperion_elite_env/bin/activate
cd /home/hyperion-elite/hyperion_elite

echo "🎯 Starting HYPERION Elite Bot..."
echo "Bot: @megacheckk_bot"
echo "Token: 7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
echo ""

python hyperion_elite_bot.py
EOF

cat > /home/hyperion-elite/hyperion_elite/stop_elite.sh << 'EOF'
#!/bin/bash
# Stop HYPERION Elite Bot
echo "⏹️ Stopping HYPERION Elite Bot..."
sudo systemctl stop hyperion-elite-bot
EOF

cat > /home/hyperion-elite/hyperion_elite/status_elite.sh << 'EOF'
#!/bin/bash
# Check HYPERION Elite Bot status
echo "🎯 HYPERION Elite Bot Status:"
sudo systemctl status hyperion-elite-bot --no-pager -l
EOF

cat > /home/hyperion-elite/hyperion_elite/logs_elite.sh << 'EOF'
#!/bin/bash
# View HYPERION Elite Bot logs
echo "📊 HYPERION Elite Bot Logs:"
echo "=========================="
tail -n 100 /home/hyperion-elite/hyperion_elite/logs/elite_bot.log
EOF

cat > /home/hyperion-elite/hyperion_elite/restart_elite.sh << 'EOF'
#!/bin/bash
# Restart HYPERION Elite Bot
echo "🔄 Restarting HYPERION Elite Bot..."
sudo systemctl restart hyperion-elite-bot
sleep 3
sudo systemctl status hyperion-elite-bot --no-pager -l
EOF

# Make all scripts executable
chmod +x /home/hyperion-elite/hyperion_elite/*.sh
chown hyperion-elite:hyperion-elite /home/hyperion-elite/hyperion_elite/*.sh

# Create elite installation guide
cat > /home/hyperion-elite/hyperion_elite/ELITE_GUIDE.md << 'EOF'
# 🎯 HYPERION ELITE BOT - Installation Complete

## Elite Bot Information
- **Bot Username:** @megacheckk_bot  
- **Token:** 7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM
- **Access:** Private (First user gets elite access)

## Quick Start (3 Steps)

### 1. Copy Elite Bot Files
```bash
cd /home/hyperion-elite/hyperion_elite
# Copy hyperion_elite_bot.py and supporting files here
```

### 2. Start Elite Bot
```bash
# Option A: Service mode (recommended)
sudo systemctl start hyperion-elite-bot

# Option B: Manual mode (for testing)
./start_elite.sh
```

### 3. Use Your Elite Bot
1. Message @megacheckk_bot on Telegram
2. Send `/auth` to get elite access (first user only)
3. Send combo file (.txt)
4. Use `/scan` for AI analysis
5. Use `/check --proxy ai` for elite checking

## Elite Management Commands

### Service Control
- **Start:** `sudo systemctl start hyperion-elite-bot`
- **Stop:** `sudo systemctl stop hyperion-elite-bot`  
- **Restart:** `sudo systemctl restart hyperion-elite-bot`
- **Status:** `sudo systemctl status hyperion-elite-bot`

### Quick Scripts
- `./start_elite.sh` - Manual start
- `./stop_elite.sh` - Quick stop
- `./status_elite.sh` - Check status
- `./logs_elite.sh` - View recent logs
- `./restart_elite.sh` - Quick restart

## Elite Features

### 🤖 AI Core Analysis (/scan)
- Format validation & duplicate detection
- Domain quality assessment (gmail.com = high quality)
- Password strength analysis
- Overall quality scoring (0-100)
- Optimization recommendations

### 🚀 Advanced Checking (/check)
```bash
/check                              # Default settings
/check --threads 100                # Custom threads (1-200)
/check --rate 1.5                   # Rate limit in seconds  
/check --proxy fast                 # Fast proxy mode (1000+ proxies)
/check --proxy ai                   # AI-tested proxies (MEGA compatible)
/check --threads 50 --proxy ai      # Combined options
```

### 🌐 Intelligent Proxy System
- **Fast Mode:** Rapid gathering from multiple sources
- **AI Mode:** Quality testing for speed, stability & MEGA compatibility
- **Auto-Management:** Handles proxy rotation and testing

### 📊 Real-time Progress
- Live message updates (no chat spam)
- Progress bars, rates, ETA calculations  
- Immediate hit notifications
- Detailed performance statistics

### 🔒 Elite Security
- Private bot (restricted to your Telegram ID)
- Secure file handling and results delivery
- Auto-cleanup of temporary files
- Professional logging and monitoring

## File Locations
- **Elite Bot:** `/home/hyperion-elite/hyperion_elite/hyperion_elite_bot.py`
- **Logs:** `/home/hyperion-elite/hyperion_elite/logs/`
- **Results:** `/home/hyperion-elite/hyperion_elite/elite_results/`
- **Service:** `/etc/systemd/system/hyperion-elite-bot.service`

## Troubleshooting

### Check Bot Status
```bash
sudo systemctl status hyperion-elite-bot
./logs_elite.sh
```

### Manual Testing
```bash
cd /home/hyperion-elite/hyperion_elite
source /home/hyperion-elite/hyperion_elite_env/bin/activate
python hyperion_elite_bot.py
```

### Common Issues
1. **Bot not responding:** Check token and internet connection
2. **Permission denied:** Ensure files are owned by hyperion-elite user
3. **Import errors:** Verify all requirements are installed

## Elite Operation Examples

### Basic Workflow
1. Upload combo.txt to @megacheckk_bot
2. `/scan` - Get AI analysis and quality score
3. `/check --proxy ai` - Start elite checking with AI proxies
4. Monitor real-time progress updates
5. Receive hits file automatically

### Advanced Usage
```bash
# High-performance checking
/check --threads 150 --rate 0.8 --proxy ai

# Fast bulk checking  
/check --threads 200 --proxy fast

# Conservative checking
/check --threads 20 --rate 3.0 --proxy ai
```

Your HYPERION Elite Bot is ready for premium operations! 🎖️
EOF

# Set permissions
chown -R hyperion-elite:hyperion-elite /home/hyperion-elite/hyperion_elite

# Create quick access alias for root
echo 'alias elite-status="systemctl status hyperion-elite-bot"' >> /root/.bashrc
echo 'alias elite-logs="tail -f /home/hyperion-elite/hyperion_elite/logs/elite_bot.log"' >> /root/.bashrc
echo 'alias elite-restart="systemctl restart hyperion-elite-bot"' >> /root/.bashrc

echo ""
echo "🎯 HYPERION ELITE BOT DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "🤖 Bot Information:"
echo "   Username: @megacheckk_bot"
echo "   Token: 7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
echo ""
echo "📂 Elite Directory: /home/hyperion-elite/hyperion_elite/"
echo "📋 Installation Guide: /home/hyperion-elite/hyperion_elite/ELITE_GUIDE.md"
echo ""
echo "🚀 Next Steps:"
echo "1. Copy hyperion_elite_bot.py to: /home/hyperion-elite/hyperion_elite/"
echo "2. Copy supporting Python files (mega_auth.py, checker_engine.py, etc.)"
echo "3. Start bot: systemctl start hyperion-elite-bot"
echo "4. Message @megacheckk_bot and send /auth for elite access"
echo ""
echo "✅ Your Elite Bot is ready for premium MEGA checking operations!"
echo ""