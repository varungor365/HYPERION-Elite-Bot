#!/bin/bash

# 🚀 HYPERION Elite Bot - VM Direct Installation
# One-command installation for any Linux VM/VPS

set -e

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

print_header() { echo -e "${BLUE}$1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${PURPLE}ℹ️  $1${NC}"; }

# Banner
echo -e "${BLUE}"
cat << "EOF"
████████████████████████████████████████████████████████████████
█                                                              █
█    🚀 HYPERION ELITE BOT - VM DIRECT INSTALLATION 🚀        █
█                                                              █
█         Zero-Config • Auto-Deploy • Production Ready        █
█                                                              █
████████████████████████████████████████████████████████████████
EOF
echo -e "${NC}"

print_header "🔍 System Detection & Preparation"

# Detect OS
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    print_info "Detected OS: $OS $VER"
else
    print_error "Cannot detect OS version"
    exit 1
fi

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    print_info "Running as root - proceeding with system-wide installation"
    INSTALL_DIR="/opt/HYPERION-Elite-Bot"
    USER_MODE=false
else
    print_info "Running as user - installing in home directory"
    INSTALL_DIR="$HOME/HYPERION-Elite-Bot"
    USER_MODE=true
fi

print_success "Installation directory: $INSTALL_DIR"

# Update system packages
print_header "📦 Updating System Packages"
if command -v apt-get &> /dev/null; then
    if $USER_MODE; then
        print_warning "Please run 'sudo apt update && sudo apt upgrade -y' manually"
        print_info "Press Enter when done..."
        read -r
    else
        apt-get update -qq && apt-get upgrade -y -qq
        print_success "System updated"
    fi
elif command -v yum &> /dev/null; then
    if $USER_MODE; then
        print_warning "Please run 'sudo yum update -y' manually"
        print_info "Press Enter when done..."
        read -r
    else
        yum update -y
        print_success "System updated"
    fi
elif command -v pacman &> /dev/null; then
    if $USER_MODE; then
        print_warning "Please run 'sudo pacman -Syu' manually"
        print_info "Press Enter when done..."
        read -r
    else
        pacman -Syu --noconfirm
        print_success "System updated"
    fi
fi

# Install dependencies
print_header "🔧 Installing Dependencies"

install_deps() {
    local cmd="$1"
    print_info "Using package manager: $cmd"
    
    case $cmd in
        "apt-get")
            local packages="python3 python3-pip python3-venv git curl wget build-essential libssl-dev libffi-dev python3-dev"
            if $USER_MODE; then
                print_warning "Please run: sudo apt-get install -y $packages"
                print_info "Press Enter when done..."
                read -r
            else
                apt-get install -y $packages
            fi
            ;;
        "yum")
            local packages="python3 python3-pip git curl wget gcc openssl-devel libffi-devel python3-devel"
            if $USER_MODE; then
                print_warning "Please run: sudo yum install -y $packages"
                print_info "Press Enter when done..."
                read -r
            else
                yum install -y $packages
            fi
            ;;
        "pacman")
            local packages="python python-pip git curl wget gcc openssl libffi"
            if $USER_MODE; then
                print_warning "Please run: sudo pacman -S $packages"
                print_info "Press Enter when done..."
                read -r
            else
                pacman -S --noconfirm $packages
            fi
            ;;
    esac
}

if command -v apt-get &> /dev/null; then
    install_deps "apt-get"
elif command -v yum &> /dev/null; then
    install_deps "yum"
elif command -v pacman &> /dev/null; then
    install_deps "pacman"
else
    print_error "Unsupported package manager. Please install Python3, pip, git, curl manually."
    exit 1
fi

print_success "Dependencies installed"

# Setup installation directory
print_header "📁 Setting Up Installation Directory"
if [[ -d "$INSTALL_DIR" ]]; then
    print_warning "Directory exists. Backing up..."
    mv "$INSTALL_DIR" "${INSTALL_DIR}.backup.$(date +%s)" 2>/dev/null || true
fi

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
print_success "Directory created: $INSTALL_DIR"

# Clone repository
print_header "📥 Downloading HYPERION Elite Bot"
git clone https://github.com/varungor365/HYPERION-Elite-Bot.git . 2>/dev/null || {
    print_warning "Git clone failed, downloading as ZIP..."
    curl -L https://github.com/varungor365/HYPERION-Elite-Bot/archive/main.zip -o hyperion.zip
    python3 -c "import zipfile; zipfile.ZipFile('hyperion.zip').extractall('.')"
    mv HYPERION-Elite-Bot-main/* . 2>/dev/null || true
    rm -rf HYPERION-Elite-Bot-main hyperion.zip 2>/dev/null || true
}
print_success "Bot files downloaded"

# Create Python virtual environment
print_header "🐍 Setting Up Python Environment"
python3 -m venv .venv
source .venv/bin/activate
print_success "Virtual environment created"

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
print_header "📚 Installing Python Dependencies"
print_info "Installing core packages..."

# Install packages one by one to handle conflicts
pip install python-telegram-bot==22.5
pip install aiohttp>=3.12.0 aiofiles>=23.2.0 httpx>=0.25.0
pip install pandas>=2.1.0 numpy>=1.24.0
pip install python-dotenv>=1.0.0 cryptography>=41.0.0
pip install PySocks>=1.7.1 colorama>=0.4.6
pip install requests>=2.31.0 "urllib3<2.0.0,>=1.26.0"

# Handle tenacity conflict
print_info "Fixing tenacity version conflict..."
pip install "tenacity>=8.0.0,<9.0.0"

# Install mega.py (ignore tenacity warning)
print_info "Installing mega.py..."
pip install mega.py==1.0.8 --no-deps
pip install pycryptodome pathlib

# Install remaining packages
pip install tqdm rich backoff bcrypt loguru psutil

print_success "All dependencies installed"

# Test bot installation
print_header "🧪 Testing Bot Installation"
python3 -c "
import sys
sys.path.insert(0, '$INSTALL_DIR')
try:
    print('Testing imports...')
    from telegram import Bot
    print('✅ Telegram Bot OK')
    import hyperion_config
    print('✅ Hyperion Config OK')
    print('✅ All tests passed!')
except Exception as e:
    print(f'❌ Test failed: {e}')
    sys.exit(1)
"

if [[ $? -ne 0 ]]; then
    print_error "Installation test failed!"
    exit 1
fi

print_success "Installation test passed"

# Make scripts executable
print_header "🔧 Setting Up Scripts"
chmod +x *.sh *.py 2>/dev/null || true
print_success "Scripts made executable"

# Create systemd service (if root)
if ! $USER_MODE; then
    print_header "⚙️  Setting Up System Service"
    
    cat > /etc/systemd/system/hyperion-elite-bot.service << EOF
[Unit]
Description=HYPERION Elite Bot - VM Installation
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/.venv/bin
ExecStart=$INSTALL_DIR/.venv/bin/python hyperion_headless.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable hyperion-elite-bot
    print_success "System service created and enabled"
fi

# Create user-friendly run scripts
print_header "📝 Creating Management Scripts"

# Create start script
cat > start-bot.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
echo "🚀 Starting HYPERION Elite Bot..."
python3 hyperion_headless.py
EOF

# Create debug script  
cat > debug-bot.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
echo "🔧 Testing HYPERION Elite Bot..."
python3 run_bot_debug.py
EOF

# Create service management scripts (if root)
if ! $USER_MODE; then
    cat > service-start.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting HYPERION Elite Bot service..."
systemctl start hyperion-elite-bot
systemctl status hyperion-elite-bot --no-pager -l
EOF

    cat > service-stop.sh << 'EOF'
#!/bin/bash
echo "⏹️ Stopping HYPERION Elite Bot service..."
systemctl stop hyperion-elite-bot
systemctl status hyperion-elite-bot --no-pager -l
EOF

    cat > service-status.sh << 'EOF'
#!/bin/bash
echo "📊 HYPERION Elite Bot Service Status"
echo "===================================="
systemctl status hyperion-elite-bot --no-pager -l
echo ""
echo "📈 System Resources:"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}' 2>/dev/null || echo "N/A")"
echo "RAM: $(free -h | awk 'NR==2{printf "%.1f/%.1fGB (%.2f%%)\n", $3/1024/1024/1024,$2/1024/1024/1024,$3*100/$2 }' 2>/dev/null || echo "N/A")"
echo ""
echo "📋 Recent Logs:"
journalctl -u hyperion-elite-bot -n 10 --no-pager
EOF

    cat > service-logs.sh << 'EOF'
#!/bin/bash
echo "📋 HYPERION Elite Bot Live Logs (Press Ctrl+C to exit)"
journalctl -u hyperion-elite-bot -f
EOF
fi

chmod +x *.sh

print_success "Management scripts created"

# Final success message
print_header "🎉 Installation Complete!"

echo -e "\n${GREEN}"
cat << "EOF"
████████████████████████████████████████████████████████████████
█                                                              █
█           🎉 HYPERION ELITE BOT INSTALLED! 🎉              █
█                                                              █
████████████████████████████████████████████████████████████████
EOF
echo -e "${NC}\n"

print_success "Installation Directory: $INSTALL_DIR"
print_success "Bot Token: 7090420579:AAEmOwaBr... (pre-configured)"
print_success "Telegram Bot: @megacheckk_bot"

echo -e "\n${BLUE}🚀 How to Run the Bot:${NC}"
if $USER_MODE; then
    echo "   • Test configuration: ./debug-bot.sh"
    echo "   • Start in terminal: ./start-bot.sh"
    echo "   • Background run: nohup ./start-bot.sh &"
else
    echo "   • Start service: ./service-start.sh"
    echo "   • Stop service: ./service-stop.sh"
    echo "   • Check status: ./service-status.sh"
    echo "   • View logs: ./service-logs.sh"
    echo "   • Manual start: ./start-bot.sh"
fi

echo -e "\n${BLUE}📱 Telegram Commands:${NC}"
echo "   • /start - Initialize bot"
echo "   • /status - System status"
echo "   • /scan - AI analyze combo files"
echo "   • /check - Start checking accounts"
echo "   • /results - Download hit files"

echo -e "\n${YELLOW}🔔 Next Steps:${NC}"
echo "   1. Open Telegram and find @megacheckk_bot"
echo "   2. Send /start to activate the bot"
echo "   3. Upload combo files for checking"

if ! $USER_MODE; then
    echo "   4. Use ./service-start.sh to run as system service"
else
    echo "   4. Use ./start-bot.sh to run the bot"
fi

echo -e "\n${GREEN}✨ Your HYPERION Elite Bot is ready for production use!${NC}"