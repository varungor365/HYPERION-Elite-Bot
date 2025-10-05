#!/bin/bash

# 🚀 HYPERION Elite Bot - Quick VM Installer
# Run this single command to install everything

echo "🚀 HYPERION Elite Bot - Quick Installer"
echo "======================================"

# Download and run the full installer
if command -v curl &> /dev/null; then
    echo "📥 Downloading installer with curl..."
    curl -fsSL https://raw.githubusercontent.com/varungor365/HYPERION-Elite-Bot/main/install-vm.sh | bash
elif command -v wget &> /dev/null; then
    echo "📥 Downloading installer with wget..."
    wget -qO- https://raw.githubusercontent.com/varungor365/HYPERION-Elite-Bot/main/install-vm.sh | bash
else
    echo "❌ Neither curl nor wget found!"
    echo "📦 Please install curl or wget first:"
    echo "   Ubuntu/Debian: sudo apt install curl"
    echo "   CentOS/RHEL: sudo yum install curl"
    echo "   Arch: sudo pacman -S curl"
    exit 1
fi