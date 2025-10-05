# 🚀 HYPERION Elite Bot - One-Click Ubuntu Deployment

## 📋 One Command Installation

Copy and paste this **single command** on your Ubuntu VPS:

```bash
curl -fsSL https://raw.githubusercontent.com/varungor365/HYPERION-Elite-Bot/main/ubuntu-deploy.sh | bash
```

### Alternative (if you want to review the script first):
```bash
wget https://raw.githubusercontent.com/varungor365/HYPERION-Elite-Bot/main/ubuntu-deploy.sh
chmod +x ubuntu-deploy.sh
./ubuntu-deploy.sh
```

## 🎯 What This Command Does:

### ✅ **System Setup:**
- Updates Ubuntu packages
- Installs Python 3, Git, Docker, Nginx, UFW
- Configures firewall (SSH, HTTP, HTTPS)

### 🤖 **Bot Installation:**
- Clones HYPERION Elite Bot repository
- Creates Python virtual environment
- Installs all dependencies (fixes tenacity conflict)
- Sets up systemd service for auto-start

### 🔧 **Configuration:**
- Prompts for your Telegram bot token
- Prompts for your Telegram user ID
- Creates secure environment file
- Sets up log rotation and backups

### 🛠️ **Management Scripts:**
- `./hyperion-status.sh` - Check bot status
- `./hyperion-restart.sh` - Restart bot
- `./hyperion-stop.sh` - Stop bot  
- `./hyperion-update.sh` - Update bot
- `./hyperion-backup.sh` - Backup bot

### 🔄 **Automated Maintenance:**
- Health check every 5 minutes
- Daily backups at 2 AM
- Automatic restart if bot crashes
- Log rotation to prevent disk full

## 🎉 After Installation:

1. **Test the bot**: Send `/start` to your Telegram bot
2. **Check status**: `./hyperion-status.sh`  
3. **Upload combos**: Send file to bot and use `/scan`
4. **Start checking**: Use `/check` with auto-optimized threads

## 📱 Bot Features Ready:

- ✅ **Resource Optimizer** - Auto-calculates optimal threads
- ✅ **AI Analyzer** - A-Z sorting + duplicate removal
- ✅ **Dynamic Combo Addition** - `/addcombos` during checking
- ✅ **Real-time Monitoring** - CPU/RAM stats in `/status`
- ✅ **Auto File Delivery** - Hits sent automatically
- ✅ **System Throttling** - Prevents crashes

## 🆘 Troubleshooting:

```bash
# Check service status
sudo systemctl status hyperion-elite-bot

# View logs
sudo journalctl -u hyperion-elite-bot -f

# Restart if needed
sudo systemctl restart hyperion-elite-bot
```

## 🔐 Security Features:

- Dedicated user permissions
- Firewall configured
- Secure environment variables
- System isolation
- Regular backups

---

**Requirements**: Ubuntu 18.04+ VPS with sudo access  
**Time**: ~3-5 minutes for complete installation  
**Result**: Production-ready HYPERION Elite Bot with all optimizations!