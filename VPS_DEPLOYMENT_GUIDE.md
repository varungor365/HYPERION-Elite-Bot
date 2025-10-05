# 🚀 HYPERION Elite Bot - VPS Deployment Guide

## Prerequisites

### 1. VPS Requirements
- **OS**: Ubuntu 20.04+ or Debian 11+ (recommended) or Alpine Linux
- **RAM**: Minimum 2GB, Recommended 4GB+
- **CPU**: 2+ cores
- **Storage**: 10GB+ free space
- **Network**: Stable internet connection

### 2. Required Software
- Python 3.11+ (Python 3.12 recommended)
- Git
- Pip
- Systemd (for service management)

## 🔧 Installation Methods

### Method 1: Direct Installation (Recommended)

#### Step 1: Update System
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git curl wget

# Alpine Linux (for Docker)
apk update && apk add python3 py3-pip git curl wget
```

#### Step 2: Clone Repository
```bash
cd /opt
sudo git clone https://github.com/varungor365/HYPERION-Elite-Bot.git
sudo chown -R $USER:$USER HYPERION-Elite-Bot
cd HYPERION-Elite-Bot
```

#### Step 3: Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 4: Configure Bot
```bash
# Copy and edit configuration
cp hyperion_config.py.example hyperion_config.py  # If exists
nano hyperion_config.py

# Set your Telegram bot token and user ID
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export AUTHORIZED_USER_ID="your_telegram_user_id"
```

#### Step 5: Test Run
```bash
# Test headless version
python3 hyperion_headless.py

# Or test main bot
python3 hyperion_elite_bot.py
```

### Method 2: Using Systemd Service (Production)

#### Step 1: Create Service File
```bash
sudo nano /etc/systemd/system/hyperion-elite-bot.service
```

```ini
[Unit]
Description=HYPERION Elite Bot
After=network.target

[Service]
Type=simple
User=hyperion
WorkingDirectory=/opt/HYPERION-Elite-Bot
Environment=PATH=/opt/HYPERION-Elite-Bot/.venv/bin
Environment=TELEGRAM_BOT_TOKEN=your_bot_token_here
Environment=AUTHORIZED_USER_ID=your_telegram_user_id
ExecStart=/opt/HYPERION-Elite-Bot/.venv/bin/python hyperion_headless.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Step 2: Setup Service User
```bash
# Create dedicated user
sudo useradd -r -s /bin/false hyperion
sudo chown -R hyperion:hyperion /opt/HYPERION-Elite-Bot

# Create log directory
sudo mkdir -p /var/log/hyperion
sudo chown hyperion:hyperion /var/log/hyperion
```

#### Step 3: Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable hyperion-elite-bot
sudo systemctl start hyperion-elite-bot

# Check status
sudo systemctl status hyperion-elite-bot

# View logs
sudo journalctl -u hyperion-elite-bot -f
```

### Method 3: Docker Deployment

#### Step 1: Build Docker Image
```bash
# Use production Dockerfile
docker build -f Dockerfile.production -t hyperion-elite-bot .
```

#### Step 2: Run Container
```bash
docker run -d \
  --name hyperion-elite-bot \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN="your_bot_token_here" \
  -e AUTHORIZED_USER_ID="your_telegram_user_id" \
  -v /opt/hyperion-data:/app/data \
  hyperion-elite-bot
```

#### Step 3: Using Docker Compose
```bash
# Use production compose file
docker-compose -f docker-compose.production.yml up -d

# Check logs
docker-compose -f docker-compose.production.yml logs -f
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required
export TELEGRAM_BOT_TOKEN="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
export AUTHORIZED_USER_ID="123456789"

# Optional
export LOG_LEVEL="INFO"
export MAX_WORKERS="50"
export ENABLE_PROXY_ROTATION="true"
```

### Bot Configuration
Edit `hyperion_config.py` or set environment variables:
```python
# Telegram Configuration
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
AUTHORIZED_USER_ID = 123456789

# Performance Settings
MAX_THREADS = 100
DEFAULT_RATE_LIMIT = 1.0
ENABLE_AI_FEATURES = True

# Proxy Settings
ENABLE_PROXY_ROTATION = True
MAX_PROXIES = 500
```

## 🚀 Running the Bot

### Start Bot (Production)
```bash
cd /opt/HYPERION-Elite-Bot
source .venv/bin/activate

# Headless mode (recommended for VPS)
python3 hyperion_headless.py

# Or with nohup for background
nohup python3 hyperion_headless.py > bot.log 2>&1 &
```

### Monitor Performance
```bash
# System resources
htop
iotop

# Bot logs
tail -f /var/log/hyperion/hyperion_elite.log

# Service status
sudo systemctl status hyperion-elite-bot
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Fix tenacity version conflict
pip uninstall tenacity
pip install 'tenacity>=8.0.0,<9.0.0'
```

#### 2. Permission Errors
```bash
sudo chown -R hyperion:hyperion /opt/HYPERION-Elite-Bot
sudo chmod +x hyperion_headless.py
```

#### 3. Log Directory Missing
```bash
sudo mkdir -p /var/log/hyperion
sudo chown hyperion:hyperion /var/log/hyperion
```

#### 4. Bot Not Responding
```bash
# Check if bot is running
ps aux | grep hyperion

# Check system resources
free -h
df -h
```

#### 5. Network Issues
```bash
# Test internet connectivity
curl -I https://api.telegram.org
curl -I https://mega.nz

# Check firewall
sudo ufw status
```

### Performance Optimization

#### 1. System Resources
```bash
# Monitor CPU/RAM usage
watch -n 1 'free -h && echo && ps aux | grep hyperion | head -5'

# Optimize thread count based on CPU cores
echo "Cores: $(nproc)"
echo "Recommended threads: $(($(nproc) * 2))"
```

#### 2. Network Optimization
```bash
# Increase network limits
echo 'net.core.somaxconn = 65535' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv4.tcp_max_syn_backlog = 65535' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 📊 Monitoring & Maintenance

### Health Check Script
```bash
cat > /opt/hyperion-health-check.sh << 'EOF'
#!/bin/bash
if ! pgrep -f "hyperion" > /dev/null; then
    echo "Bot not running, restarting..."
    sudo systemctl restart hyperion-elite-bot
fi
EOF

chmod +x /opt/hyperion-health-check.sh

# Add to crontab
echo "*/5 * * * * /opt/hyperion-health-check.sh" | crontab -
```

### Log Rotation
```bash
sudo nano /etc/logrotate.d/hyperion
```

```
/var/log/hyperion/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    copytruncate
}
```

### Backup Script
```bash
cat > /opt/hyperion-backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /opt/hyperion-backup-$DATE.tar.gz \
    /opt/HYPERION-Elite-Bot \
    /var/log/hyperion \
    --exclude="*.pyc" \
    --exclude="__pycache__"
find /opt -name "hyperion-backup-*.tar.gz" -mtime +7 -delete
EOF

chmod +x /opt/hyperion-backup.sh
echo "0 2 * * * /opt/hyperion-backup.sh" | sudo crontab -
```

## 🔐 Security Recommendations

### 1. Firewall Configuration
```bash
sudo ufw allow ssh
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Update System Regularly
```bash
# Create update script
echo "apt update && apt upgrade -y" | sudo tee /etc/cron.weekly/system-updates
sudo chmod +x /etc/cron.weekly/system-updates
```

### 3. Secure Bot Token
```bash
# Use environment files instead of hardcoding
echo "TELEGRAM_BOT_TOKEN=your_token" | sudo tee /opt/HYPERION-Elite-Bot/.env
sudo chown hyperion:hyperion /opt/HYPERION-Elite-Bot/.env
sudo chmod 600 /opt/HYPERION-Elite-Bot/.env
```

## 📱 Bot Usage Commands

Once deployed, use these Telegram commands:

- `/start` - Initialize bot
- `/status` - Check system status with resource optimizer
- `/scan` - Analyze combo file with AI
- `/check` - Start elite checking
- `/addcombos` - Add combos dynamically during checking
- `/stop` - Stop checking and get results
- `/results` - Download hit files

## ✅ Success Indicators

- Bot responds to `/start` command
- System resources shown in `/status`
- AI analyzer working with A-Z sorting
- Resource optimizer calculating optimal threads
- Hit files automatically sent on completion

## 🆘 Support

If you encounter issues:
1. Check logs: `sudo journalctl -u hyperion-elite-bot -f`
2. Verify system resources: `htop`
3. Test network connectivity: `curl -I https://api.telegram.org`
4. Restart service: `sudo systemctl restart hyperion-elite-bot`

## 🎉 Deployment Complete!

Your HYPERION Elite Bot is now running on VPS with:
- ✅ Intelligent resource optimization
- ✅ Real-time CPU/memory monitoring
- ✅ A-Z sorting and duplicate removal
- ✅ Dynamic combo addition
- ✅ Automatic hit file delivery
- ✅ System throttling to prevent crashes
- ✅ Production-ready error handling