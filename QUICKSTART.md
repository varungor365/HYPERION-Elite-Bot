# 🚀 HYPERION Elite Bot v5.0 - Quick Start Guide

## ⚡ One-Click GitHub Codespaces Setup

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YourUsername/HYPERION-Elite-Bot)

### Step 1: Open in Codespaces
1. Click the "Open in GitHub Codespaces" badge above
2. Wait for the environment to initialize (2-3 minutes)
3. All dependencies will be automatically installed

### Step 2: Configure Your Bot
```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Required configuration:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
AUTHORIZED_USER_ID=your_telegram_user_id
```

### Step 3: Run Your Bot
```bash
# Start the bot
python hyperion_elite_bot.py
```

That's it! Your HYPERION Elite Bot is now running in the cloud! 🎉

## 📱 Using Your Bot

### Basic Commands
- Send `/start` to your bot to initialize
- Upload a combo file (email:password format)
- Use `/scan` to analyze the file with AI
- Use `/check` to start the advanced checking process

### Advanced Features
- `/check --threads 50` - Custom thread count
- `/check --proxy ai` - AI-tested proxies
- `/proxies` - Proxy management
- `/status` - Real-time progress
- `/results` - Download hits

## 📊 Enhanced Progress Display

Your bot will show:
```
🚀 HYPERION ELITE CHECKING

Progress: ████████████████████ 100.0%
Checked: 1,000 / 1,000
✅ Hits: 45
❌ Fails: 955
⚠️ Errors: 0

Performance:
• Rate: 150/min
• Threads: 24
• Elapsed: 400s
• ETA: Complete

Hit Categories:
🎯 Pro Accounts: 25
  ├─ < 5 files: 10
  └─ ≥ 5 files: 15
🆓 Free Accounts: 18
  ├─ < 5 files: 12
  └─ ≥ 5 files: 6
📭 Empty: 2

System:
• Proxies: AI Mode
• Mode: Elite
• Status: Running 🟢
```

## 🎯 Enhanced Hit Files

Each hit includes:
- 📧 Email & Password
- 🛡️ Recovery Key  
- 📊 Storage Details (Used/Total)
- 📁 File & Folder Counts
- 👤 User Information
- 🌍 Country & Creation Date

## 🔧 Troubleshooting

### Bot Not Responding?
```bash
# Check logs
tail -f hyperion.log

# Restart service
systemctl restart hyperion-elite-bot
```

### Need More Performance?
```bash
# Edit configuration
nano .env

# Increase threads
DEFAULT_THREADS=50
```

### Proxy Issues?
```bash
# Test proxy system
python -c "from proxy_rotator import test_proxies; test_proxies()"
```

## 📚 Advanced Documentation

- 📖 [Full Documentation](docs/README.md)
- 🔧 [Configuration Guide](docs/configuration.md)
- 🐳 [Docker Deployment](docs/docker.md)
- 🔐 [Security Guide](docs/security.md)

## 🚀 Production Deployment

### VPS Deployment
```bash
# One-line deployment
curl -sSL https://raw.githubusercontent.com/YourUsername/HYPERION-Elite-Bot/main/scripts/deploy_vps.sh | sudo bash
```

### Docker Deployment
```bash
# Clone and run
git clone https://github.com/YourUsername/HYPERION-Elite-Bot.git
cd HYPERION-Elite-Bot
docker-compose up -d
```

## 🆘 Support

- 🤖 Telegram: [@megacheckk_bot](https://t.me/megacheckk_bot)
- 📧 Issues: [GitHub Issues](https://github.com/YourUsername/HYPERION-Elite-Bot/issues)
- 📖 Wiki: [Documentation](https://github.com/YourUsername/HYPERION-Elite-Bot/wiki)

---

**🎉 Welcome to the HYPERION Elite Experience!**