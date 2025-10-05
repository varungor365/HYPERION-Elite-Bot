# HYPERION Elite Bot - VPS Deployment Guide

🚀 **Production-ready deployment for Virtual Private Servers**

## Quick Start

### 1. One-Line VPS Installation

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/HYPERION-Elite-Bot/main/deploy_vps.sh | sudo bash
```

### 2. Manual Installation

1. **Clone repository:**
```bash
sudo git clone https://github.com/yourusername/HYPERION-Elite-Bot.git /opt/hyperion-elite-bot
cd /opt/hyperion-elite-bot
```

2. **Run deployment script:**
```bash
sudo chmod +x deploy_vps.sh
sudo ./deploy_vps.sh
```

3. **Configure environment:**
```bash
sudo nano /opt/hyperion-elite-bot/.env
```

4. **Start service:**
```bash
sudo systemctl start hyperion-elite-bot
```

## Configuration

### Environment Variables (.env)

```bash
# Required Configuration
TELEGRAM_TOKEN=your_bot_token_here
AUTHORIZED_USERS=796354588,123456789

# Optional Settings
MEGA_TIMEOUT=30
MAX_THREADS=8
LOG_LEVEL=INFO

# Proxy Configuration (optional)
PROXY_ENABLED=false
PROXY_LIST=proxy1:port,proxy2:port
```

### Security Configuration

- ✅ **Environment-based tokens** - No hardcoded secrets
- ✅ **Restricted file permissions** - `.env` has 600 permissions
- ✅ **System user isolation** - Runs as dedicated `hyperion` user
- ✅ **Minimal privileges** - Uses systemd security features
- ✅ **Firewall ready** - Compatible with ufw/iptables

## Server Management

### Service Control

```bash
# Start the bot
sudo systemctl start hyperion-elite-bot

# Stop the bot
sudo systemctl stop hyperion-elite-bot

# Restart the bot
sudo systemctl restart hyperion-elite-bot

# Check status
sudo systemctl status hyperion-elite-bot

# Enable auto-start on boot
sudo systemctl enable hyperion-elite-bot
```

### Monitoring & Logs

```bash
# View live logs
sudo journalctl -u hyperion-elite-bot -f

# View recent logs
sudo journalctl -u hyperion-elite-bot --since "1 hour ago"

# Check log files
tail -f /var/log/hyperion/hyperion_elite.log
tail -f /var/log/hyperion/errors.log
```

### Performance Monitoring

```bash
# Check system resources
htop
free -h
df -h

# Monitor bot performance
sudo systemctl status hyperion-elite-bot
```

## System Requirements

### Minimum Requirements
- **RAM:** 1GB+ recommended
- **CPU:** 1 core (2+ recommended)
- **Disk:** 2GB free space
- **OS:** Ubuntu 18.04+, Debian 9+, CentOS 7+, Alpine Linux

### Recommended for High Performance
- **RAM:** 2-4GB
- **CPU:** 2-4 cores
- **SSD:** 10GB+ free space
- **Network:** Stable internet connection

## Headless Optimizations

### Memory Management
- Automatic garbage collection
- Conservative thread limits for VPS
- Optimized logging with rotation

### Performance Features
- Multi-threaded account checking
- Proxy rotation system
- Real-time performance metrics
- Auto-restart on failures

### Security Features
- No GUI dependencies
- Minimal system footprint
- Secure configuration management
- Process isolation

## Troubleshooting

### Common Issues

**Bot won't start:**
```bash
# Check configuration
sudo nano /opt/hyperion-elite-bot/.env

# Check logs
sudo journalctl -u hyperion-elite-bot --since "10 minutes ago"

# Verify permissions
ls -la /opt/hyperion-elite-bot/.env
```

**High CPU usage:**
```bash
# Reduce thread count in .env
MAX_THREADS=4

# Restart service
sudo systemctl restart hyperion-elite-bot
```

**Memory issues:**
```bash
# Check memory usage
free -h

# Monitor bot memory
sudo systemctl status hyperion-elite-bot
```

### Log Analysis

**Error patterns to watch for:**
- `ConnectionError` - Network/proxy issues
- `AuthenticationError` - Invalid Telegram token
- `PermissionError` - File permission issues
- `ImportError` - Missing dependencies

## Updates & Maintenance

### Updating the Bot

```bash
# Navigate to installation directory
cd /opt/hyperion-elite-bot

# Pull latest changes
sudo -u hyperion git pull

# Install new dependencies (if any)
sudo -u hyperion ./venv/bin/pip install -r requirements.txt

# Restart service
sudo systemctl restart hyperion-elite-bot
```

### Backup Configuration

```bash
# Backup configuration
sudo cp /opt/hyperion-elite-bot/.env /opt/hyperion-elite-bot/.env.backup

# Backup logs
sudo tar -czf hyperion_logs_$(date +%Y%m%d).tar.gz /var/log/hyperion/
```

## Advanced Configuration

### Custom Proxy Setup

```bash
# Edit configuration
sudo nano /opt/hyperion-elite-bot/.env

# Add proxy settings
PROXY_ENABLED=true
PROXY_LIST=proxy1.example.com:8080,proxy2.example.com:3128

# Restart to apply
sudo systemctl restart hyperion-elite-bot
```

### Performance Tuning

```bash
# High-performance settings
MAX_THREADS=16
MEGA_TIMEOUT=15

# Memory optimization
PYTHONOPTIMIZE=1
PYTHONDONTWRITEBYTECODE=1
```

### Multiple Bot Instances

```bash
# Copy service file
sudo cp /etc/systemd/system/hyperion-elite-bot.service /etc/systemd/system/hyperion-elite-bot-2.service

# Edit paths and config
sudo nano /etc/systemd/system/hyperion-elite-bot-2.service

# Enable both services
sudo systemctl enable hyperion-elite-bot-2
sudo systemctl start hyperion-elite-bot-2
```

## Support & Documentation

### File Structure
```
/opt/hyperion-elite-bot/
├── hyperion_headless.py     # Headless server version
├── hyperion_elite_bot.py    # Full-featured Telegram bot
├── requirements.txt         # Production dependencies
├── .env                     # Configuration (create manually)
├── hyperion-elite-bot.service # Systemd service file
└── deploy_vps.sh           # Automated installer
```

### Key Features
- 🤖 **AI-Powered Analysis** - Smart combo detection
- ⚡ **Multi-Threading** - Concurrent account checking
- 🛡️ **Advanced Security** - Environment-based configuration
- 🔄 **Auto-Restart** - Systemd monitoring and recovery
- 📊 **Real-Time Stats** - Live performance monitoring
- 🌐 **Proxy Support** - Anti-ban protection

### Getting Help

1. **Check logs first**: `sudo journalctl -u hyperion-elite-bot -f`
2. **Verify configuration**: Ensure `.env` file is properly configured
3. **Test connectivity**: Check internet and Telegram API access
4. **Review requirements**: Ensure all dependencies are installed

---

## Production Checklist

- [ ] VPS meets minimum requirements
- [ ] Bot token obtained from @BotFather
- [ ] User IDs added to authorized list
- [ ] `.env` file properly configured
- [ ] Service enabled for auto-start
- [ ] Firewall configured (if needed)
- [ ] Log monitoring set up
- [ ] Backup strategy implemented

🎯 **HYPERION Elite Bot - Ready for elite operations!**