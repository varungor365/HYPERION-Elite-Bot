"""
Build Script for Creating Standalone Executable
Creates a single .exe file that can run without Python installed
"""

import subprocess
import sys
import os

print("=" * 70)
print("MEGA CHECKER - STANDALONE EXECUTABLE BUILDER")
print("=" * 70)
print()

# Check if PyInstaller is installed
try:
    import PyInstaller
    print("✓ PyInstaller is installed")
except ImportError:
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller installed successfully")

print()
print("Building standalone executable...")
print("This may take a few minutes...")
print()

# PyInstaller command
cmd = [
    "pyinstaller",
    "--name=MegaChecker",
    "--onefile",
    "--windowed",
    "--icon=NONE",
    "--add-data=config.json;.",
    "--hidden-import=mega",
    "--hidden-import=customtkinter",
    "--hidden-import=discord_webhook",
    "--hidden-import=PIL",
    "--hidden-import=requests",
    "--hidden-import=colorama",
    "--collect-all=customtkinter",
    "--noconfirm",
    "mega_checker.py"
]

try:
    subprocess.run(cmd, check=True)
    print()
    print("=" * 70)
    print("✓ BUILD SUCCESSFUL!")
    print("=" * 70)
    print()
    print("Your executable is ready:")
    print("  Location: dist\\MegaChecker.exe")
    print()
    print("To use:")
    print("  1. Copy MegaChecker.exe to any folder")
    print("  2. Create combo.txt in the same folder")
    print("  3. Double-click MegaChecker.exe")
    print()
    print("Note: First run may take a few seconds to start")
    print()
except subprocess.CalledProcessError as e:
    print()
    print("=" * 70)
    print("✗ BUILD FAILED")
    print("=" * 70)
    print(f"Error: {e}")
    print()
    print("Try running manually:")
    print("  pip install pyinstaller")
    print("  pyinstaller mega_checker.spec")
    sys.exit(1)
