"""
Installation Verification Script
Checks if all dependencies are properly installed
"""

import sys

print("=" * 60)
print("MEGA CHECKER - INSTALLATION VERIFICATION")
print("=" * 60)
print()

# Check Python version
print(f"✓ Python Version: {sys.version}")
if sys.version_info < (3, 8):
    print("❌ ERROR: Python 3.8 or higher is required!")
    sys.exit(1)
else:
    print("✓ Python version is compatible")
print()

# Check required packages
required_packages = {
    'mega': 'mega.py',
    'customtkinter': 'customtkinter',
    'discord_webhook': 'discord-webhook',
    'PIL': 'Pillow',
    'requests': 'requests',
    'colorama': 'colorama'
}

all_installed = True
print("Checking required packages:")
print("-" * 60)

for module, package in required_packages.items():
    try:
        __import__(module)
        print(f"✓ {package:20s} - Installed")
    except ImportError:
        print(f"❌ {package:20s} - NOT INSTALLED")
        all_installed = False

print()

if all_installed:
    print("=" * 60)
    print("✅ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("You're ready to run the MEGA Checker!")
    print()
    print("To start:")
    print("  Windows: Double-click run.bat")
    print("  Linux/Mac: ./run.sh")
    print("  Manual: python mega_checker.py")
    print()
else:
    print("=" * 60)
    print("❌ SOME DEPENDENCIES ARE MISSING")
    print("=" * 60)
    print()
    print("To install missing packages:")
    print()
    print("  Windows:")
    print("    Double-click install.bat")
    print()
    print("  Linux/Mac:")
    print("    ./install.sh")
    print()
    print("  Manual:")
    print("    pip install -r requirements.txt")
    print()
    sys.exit(1)

# Check for combo file
import os
if os.path.exists('combo.txt'):
    print("✓ combo.txt file found")
    with open('combo.txt', 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('#')]
        if lines:
            print(f"  Contains {len(lines)} lines")
        else:
            print("  ⚠️  File is empty - add accounts in format: email:password")
else:
    print("⚠️  combo.txt not found - it will be created on first run")

print()
print("=" * 60)
print("Ready to start checking!")
print("=" * 60)
