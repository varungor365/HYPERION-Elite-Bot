#!/bin/bash
# HYPERION Server Deployment Script for Digital Ocean / Ubuntu VPS
# Run with: bash deploy.sh

echo "🚀 HYPERION Server Deployment Script"
echo "===================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Update system packages
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install Python and pip if not present
echo "🐍 Installing Python and dependencies..."
apt install -y python3 python3-pip python3-venv git curl screen

# Create hyperion user (non-root for security)
echo "👤 Creating hyperion user..."
useradd -m -s /bin/bash hyperion || echo "User hyperion already exists"

# Create hyperion directory
HYPERION_HOME="/home/hyperion/hyperion_server"
mkdir -p $HYPERION_HOME
chown hyperion:hyperion $HYPERION_HOME

# Switch to hyperion user and setup environment
sudo -u hyperion bash << 'EOF'
cd /home/hyperion

# Create Python virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv hyperion_env
source hyperion_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "📋 Installing Python packages..."
pip install requests python-telegram-bot aiofiles

# Create directories
mkdir -p hyperion_server/server_results
mkdir -p hyperion_server/logs
mkdir -p hyperion_server/config

echo "✅ Environment setup complete"
EOF

# Create systemd service
echo "⚙️ Creating systemd service..."
cat > /etc/systemd/system/hyperion-server.service << 'EOF'
[Unit]
Description=HYPERION MEGA Checker Server
After=network.target

[Service]
Type=simple
User=hyperion
Group=hyperion
WorkingDirectory=/home/hyperion/hyperion_server
Environment=PATH=/home/hyperion/hyperion_env/bin
ExecStart=/home/hyperion/hyperion_env/bin/python hyperion_server.py
Restart=always
RestartSec=10
StandardOutput=append:/home/hyperion/hyperion_server/logs/hyperion.log
StandardError=append:/home/hyperion/hyperion_server/logs/hyperion.error.log

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/home/hyperion/hyperion_server

[Install]
WantedBy=multi-user.target
EOF

# Enable service
systemctl daemon-reload
systemctl enable hyperion-server

# Create log rotation
echo "📝 Setting up log rotation..."
cat > /etc/logrotate.d/hyperion-server << 'EOF'
/home/hyperion/hyperion_server/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
    su hyperion hyperion
}
EOF

# Create startup script
echo "📜 Creating management scripts..."
cat > /home/hyperion/hyperion_server/start.sh << 'EOF'
#!/bin/bash
# Start HYPERION Server
source /home/hyperion/hyperion_env/bin/activate
cd /home/hyperion/hyperion_server

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN environment variable not set!"
    echo "Set it with: export TELEGRAM_BOT_TOKEN='your_bot_token_here'"
    exit 1
fi

echo "🚀 Starting HYPERION Server..."
python hyperion_server.py
EOF

cat > /home/hyperion/hyperion_server/stop.sh << 'EOF'
#!/bin/bash
# Stop HYPERION Server
echo "⏹️ Stopping HYPERION Server..."
sudo systemctl stop hyperion-server
EOF

cat > /home/hyperion/hyperion_server/status.sh << 'EOF'
#!/bin/bash
# Check HYPERION Server status
echo "📊 HYPERION Server Status:"
sudo systemctl status hyperion-server --no-pager -l
EOF

cat > /home/hyperion/hyperion_server/logs.sh << 'EOF'
#!/bin/bash
# View HYPERION Server logs
echo "📋 HYPERION Server Logs (last 50 lines):"
tail -n 50 /home/hyperion/hyperion_server/logs/hyperion.log
EOF

# Make scripts executable
chmod +x /home/hyperion/hyperion_server/*.sh
chown hyperion:hyperion /home/hyperion/hyperion_server/*.sh

# Create environment template
cat > /home/hyperion/hyperion_server/.env.template << 'EOF'
# HYPERION Server Configuration
# Copy this file to .env and fill in your values

# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Server Configuration
HYPERION_PASSWORD=hyperion2025
MAX_THREADS=50
RESULTS_RETENTION_DAYS=30

# Optional: Proxy settings
# HTTP_PROXY=http://proxy:port
# HTTPS_PROXY=https://proxy:port
EOF

chown hyperion:hyperion /home/hyperion/hyperion_server/.env.template

# Create installation info
cat > /home/hyperion/hyperion_server/INSTALLATION.md << 'EOF'
# HYPERION Server Installation Complete

## Quick Start

1. **Get Telegram Bot Token:**
   - Message @BotFather on Telegram
   - Create a new bot with `/newbot`
   - Save the bot token

2. **Configure Server:**
   ```bash
   cd /home/hyperion/hyperion_server
   cp .env.template .env
   nano .env  # Add your bot token
   ```

3. **Copy HYPERION Files:**
   - Copy all Python files from your local HYPERION to this directory
   - Ensure these files are present:
     - hyperion_server.py
     - mega_auth.py
     - checker_engine.py
     - proxy_rotator.py

4. **Start Server:**
   ```bash  
   sudo systemctl start hyperion-server
   sudo systemctl status hyperion-server
   ```

## Management Commands

- **Start:** `sudo systemctl start hyperion-server`
- **Stop:** `sudo systemctl stop hyperion-server`
- **Status:** `sudo systemctl status hyperion-server`
- **Logs:** `tail -f /home/hyperion/hyperion_server/logs/hyperion.log`
- **Auto-start:** Already enabled (starts on boot)

## Manual Operation

```bash
cd /home/hyperion/hyperion_server
source /home/hyperion/hyperion_env/bin/activate
export TELEGRAM_BOT_TOKEN='your_token_here'
python hyperion_server.py
```

## Telegram Bot Usage

1. Start chat with your bot
2. Send `/auth hyperion2025` (change password in code)
3. Send combo file (.txt) or paste combos directly
4. Bot will automatically process and send results

## File Locations

- **Server Code:** `/home/hyperion/hyperion_server/`
- **Logs:** `/home/hyperion/hyperion_server/logs/`
- **Results:** `/home/hyperion/hyperion_server/server_results/`
- **Service:** `/etc/systemd/system/hyperion-server.service`

## Security Notes

- Server runs as non-root user `hyperion`
- Change default password in hyperion_server.py
- Consider firewall rules for production
- Bot token should be kept secret

## Troubleshooting

- Check logs: `tail -f /home/hyperion/hyperion_server/logs/hyperion.log`
- Check service: `systemctl status hyperion-server`
- Test manually: Run commands in "Manual Operation" section
EOF

chown hyperion:hyperion /home/hyperion/hyperion_server/INSTALLATION.md

# Set permissions
chown -R hyperion:hyperion /home/hyperion/hyperion_server

echo ""
echo "✅ HYPERION Server deployment complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Copy your HYPERION Python files to: /home/hyperion/hyperion_server/"
echo "2. Get Telegram bot token from @BotFather"
echo "3. Configure: nano /home/hyperion/hyperion_server/.env"
echo "4. Start server: systemctl start hyperion-server"
echo ""
echo "📖 See /home/hyperion/hyperion_server/INSTALLATION.md for details"
echo ""