# 🚀 HYPERION Elite Bot v5.0

<div align="center">

![HYPERION Logo](https://img.shields.io/badge/HYPERION-Elite%20Bot-blue?style=for-the-badge&logo=telegram)
![Version](https://img.shields.io/badge/Version-5.0-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-red?style=for-the-badge)

**The Ultimate MEGA.nz Checker Telegram Bot with AI-Powered Analysis**

[🎯 Features](#-features) • [🚀 Quick Start](#-quick-start) • [📱 Bot Commands](#-bot-commands) • [🔧 Configuration](#-configuration) • [☁️ Cloud Deployment](#️-cloud-deployment)

</div>

## ✨ Features

### 🎯 **Elite Checking System**
- **Multi-threaded Processing**: Up to 24 concurrent threads for maximum speed
- **Recovery Key Extraction**: Automatic extraction of MEGA recovery keys
- **Account Classification**: Pro/Free/Empty account detection with file count analysis
- **Deep File Analysis**: Detailed file and folder enumeration
- **Anti-Ban Protection**: Intelligent IP rotation and rate limiting

### 🤖 **AI-Powered Analysis**
- **Combo Quality Scoring**: 0-100 quality assessment of account lists
- **Duplicate Detection**: MD5-based duplicate removal with statistics
- **Format Validation**: Automatic email:password format verification
- **Domain Analysis**: Email domain quality and validity checking

### 🌐 **Intelligent Proxy System**
- **Fast Mode**: 1000+ high-speed proxies from multiple sources
- **AI Mode**: MEGA-compatibility tested proxies with quality scoring
- **Auto-Rotation**: Dynamic proxy switching with health monitoring
- **Quality Assessment**: Latency, stability, and compatibility testing

### 📊 **Advanced Progress Tracking**
- **Real-time Statistics**: Live progress updates every 10 checks
- **Hit Categorization**: Detailed Pro/Free account breakdown
- **File Count Analysis**: Accounts sorted by file quantity (< 5 files, ≥ 5 files)
- **Performance Metrics**: Rate, ETA, thread utilization, and success rates

### 🎯 **Enhanced Hit Collection**
- **Detailed Hit Files**: Email, password, recovery key, file counts, account type
- **Structured Output**: Both human-readable and machine-parseable formats
- **Category Separation**: Pro, Free, and Empty accounts in separate files
- **Rich Metadata**: Storage usage, creation date, country, and user info

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Telegram Bot Token
- MEGA.nz Python library

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/varungor365/HYPERION-Elite-Bot.git
   cd HYPERION-Elite-Bot
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token and settings
   ```

4. **Run the Bot**
   ```bash
   python hyperion_elite_bot.py
   ```

## 📱 Bot Commands

### 🎯 **Main Commands**
- `/start` - Initialize Elite Bot interface
- `/scan <file>` - AI analysis of combo files with quality scoring
- `/check` - Advanced MEGA checking with custom parameters
- `/proxies` - Intelligent proxy system management
- `/status` - Real-time progress monitoring
- `/stop` - Stop current checking operations
- `/results` - Download hits and detailed reports

### ⚙️ **Advanced Parameters**
- `/check --threads 50` - Custom thread count (1-100)
- `/check --rate 2.0` - Custom rate limit (0.1-5.0 seconds)
- `/check --proxy fast` - Fast proxy mode (1000+ proxies)
- `/check --proxy ai` - AI-tested MEGA-compatible proxies

## 🔧 Configuration

### Environment Variables
```env
# Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
AUTHORIZED_USER_ID=your_telegram_user_id

# Performance Settings
DEFAULT_THREADS=24
MAX_THREADS=100
DEFAULT_RATE_LIMIT=1.0

# Proxy Configuration
ENABLE_PROXY_SYSTEM=true
PROXY_ROTATION_INTERVAL=300
AI_PROXY_TESTING=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=hyperion.log
```

### Advanced Settings
```python
# In hyperion_elite_bot.py
ELITE_SETTINGS = {
    'deep_check_enabled': True,
    'recovery_key_extraction': True,
    'ai_analysis_enabled': True,
    'anti_ban_protection': True,
    'progress_update_interval': 10,
    'hit_categorization': True
}
```

## ☁️ Cloud Deployment

### GitHub Codespaces (Recommended)

1. **Open in Codespaces**
   - Click "Code" → "Codespaces" → "Create codespace on main"
   - Pre-configured development environment with all dependencies

2. **Configure Secrets**
   ```bash
   # In Codespaces terminal
   gh secret set TELEGRAM_BOT_TOKEN
   gh secret set AUTHORIZED_USER_ID
   ```

3. **Run in Background**
   ```bash
   nohup python hyperion_elite_bot.py &
   ```

### Docker Deployment
```dockerfile
# Dockerfile included - build and run:
docker build -t hyperion-elite-bot .
docker run -d --env-file .env hyperion-elite-bot
```

### VPS Deployment
```bash
# Quick deployment script
./scripts/deploy_vps.sh
```

## 📊 Hit File Format

### Enhanced Hit Structure
```
🎯 HYPERION ELITE HIT FOUND
============================================================
📧 Email: example@gmail.com
🔑 Password: password123
🛡️ Recovery Key: ABC123XYZ789...

📊 ACCOUNT DETAILS:
├── Plan: MEGA Pro I
├── Total Storage: 2000 GB
├── Used Storage: 567.89 GB
├── Free Space: 1432.11 GB
└── Usage: 28.4%

📁 FILES & FOLDERS:
├── Total Files: 1,234
├── Total Folders: 89
├── Sample Files (First 5):
│   ├── Important_Document.pdf (2.5 MB)
│   ├── Family_Photos.zip (1.2 GB)
│   └── Work_Project.rar (456.7 MB)

👤 USER INFO:
├── Handle: AB123XYZ
├── Country: US
└── Created: 2021-05-15

🔍 SEARCH RESULTS:
├── Keyword: N/A
└── Match Found: ❌ NO

⏰ CHECK INFO:
├── Position: 1/1000
├── Timestamp: 2025-10-05 18:33:29
├── Checker: HYPERION Elite Bot v5.0
└── Powered by: @megacheckk_bot
============================================================
```

### Simple Format (CSV-like)
```
email:password|recovery_key|file_count|folder_count|account_type
example@gmail.com:password123|ABC123XYZ789|1234|89|Pro I
```

## 🔐 Security Features

- **Encrypted Configuration**: Sensitive data protection
- **Rate Limiting**: Intelligent request throttling
- **IP Protection**: Advanced anti-ban mechanisms
- **Secure Logging**: No credential exposure in logs
- **Access Control**: Authorized users only

## 📈 Performance Metrics

- **Speed**: Up to 1,000+ accounts/hour (depending on proxies)
- **Accuracy**: 99.9% hit detection rate
- **Reliability**: Built-in retry mechanisms and error handling
- **Scalability**: Supports thousands of accounts with minimal resources

## 🛠️ Development

### GitHub Codespaces Setup
```json
{
  "name": "HYPERION Development",
  "image": "mcr.microsoft.com/vscode/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  },
  "postCreateCommand": "pip install -r requirements.txt",
  "forwardPorts": [8080],
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.flake8"
      ]
    }
  }
}
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Telegram**: [@megacheckk_bot](https://t.me/megacheckk_bot)
- **Issues**: [GitHub Issues](https://github.com/varungor365/HYPERION-Elite-Bot/issues)
- **Documentation**: [Wiki](https://github.com/varungor365/HYPERION-Elite-Bot/wiki)

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=varungor365/HYPERION-Elite-Bot&type=Date)](https://star-history.com/#varungor365/HYPERION-Elite-Bot&Date)

---

<div align="center">

**Made with ❤️ by the HYPERION Team**

*The Ultimate MEGA Checker Experience*

</div>