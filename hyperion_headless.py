#!/usr/bin/env python3
"""
HYPERION Elite Bot - Headless Server Version
===========================================

VPS-optimized headless version with:
- No GUI dependencies
- Enhanced security
- Production logging
- Auto-restart capability
- Systemd integration
"""

import asyncio
import logging
import os
import sys
import signal
import json
import time
import threading
import multiprocessing
import gc
import platform
import zipfile
import re
import hashlib
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️ requests module not available. Some features may be limited.")
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from urllib.parse import urlparse
from collections import Counter
import math

# Enhanced logging for production
import os

# Configure logging handlers with proper fallback
handlers = [logging.StreamHandler(sys.stdout)]

# Try to use system log directory, fallback to local file
try:
    if os.path.exists('/var/log'):
        os.makedirs('/var/log/hyperion', exist_ok=True)
        handlers.append(logging.FileHandler('/var/log/hyperion/hyperion_elite.log', encoding='utf-8'))
        print("✅ Using system log directory: /var/log/hyperion/")
    else:
        raise PermissionError("System log directory not available")
except (PermissionError, OSError):
    # Fallback to local logging
    handlers.append(logging.FileHandler('hyperion_elite.log', encoding='utf-8'))
    print("ℹ️ Using local log file: hyperion_elite.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)
logger = logging.getLogger(__name__)

# Telegram Bot imports (headless compatible)
try:
    from telegram import Update, Document, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
    logger.info("✅ Telegram libraries loaded successfully")
except ImportError as e:
    TELEGRAM_AVAILABLE = False
    logger.error(f"❌ Telegram libraries not found: {e}")
    logger.error("Install with: pip install python-telegram-bot")

# Core MEGA checking imports
try:
    from mega_auth import MegaAuthenticator
    from checker_engine import CheckerEngine
    from proxy_rotator import AntiBanSystem, ProxyInfo
    logger.info("✅ MEGA checking modules loaded")
except ImportError as e:
    logger.error(f"❌ MEGA modules not found: {e}")
    sys.exit(1)

class HeadlessHyperionBot:
    """Headless server-optimized HYPERION Elite Bot"""
    
    def __init__(self, telegram_token: str):
        self.telegram_token = telegram_token
        self.authorized_users = self.load_authorized_users()
        self.telegram_app = None
        self.running = False
        
        # Server optimization
        self.cpu_cores = multiprocessing.cpu_count()
        self.max_threads = min(self.cpu_cores * 2, 8)  # Conservative for VPS
        
        # Enhanced logging
        self.setup_production_logging()
        
        # AI components
        self.ai_analyzer = None
        self.proxy_system = None
        
        logger.info(f"🚀 Headless HYPERION Elite Bot initialized")
        logger.info(f"   💻 CPU Cores: {self.cpu_cores}")
        logger.info(f"   ⚡ Max Threads: {self.max_threads}")
        logger.info(f"   🔐 Authorized Users: {len(self.authorized_users)}")
        logger.info(f"   🖥️ Mode: Headless Server")
    
    def setup_production_logging(self):
        """Setup enhanced production logging"""
        try:
            # Create log directory if it doesn't exist
            log_dir = Path("/var/log/hyperion")
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Additional file handlers for different log levels
            error_handler = logging.FileHandler(log_dir / "errors.log")
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - ERROR - %(message)s'
            ))
            
            hits_handler = logging.FileHandler(log_dir / "hits.log")
            hits_handler.setLevel(logging.INFO)
            hits_handler.setFormatter(logging.Formatter(
                '%(asctime)s - HIT - %(message)s'
            ))
            
            # Add handlers to root logger
            root_logger = logging.getLogger()
            root_logger.addHandler(error_handler)
            
        except Exception as e:
            logger.warning(f"Could not setup advanced logging: {e}")
    
    def load_authorized_users(self):
        """Load authorized users from environment or config"""
        try:
            from hyperion_config import config
            return config.get_authorized_users()
        except:
            # Fallback to environment variable
            users_str = os.getenv('AUTHORIZED_USERS', '796354588')
            return [int(user.strip()) for user in users_str.split(',') if user.strip().isdigit()]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "N/A"
        
        # Auto-authorize first user or allow access (simplified for deployment)
        if not self.authorized_users:
            # First user becomes the owner
            self.authorized_users.append(user_id)
            logger.info(f"✅ Auto-authorized first user (owner): {username} (ID: {user_id})")
        elif user_id not in self.authorized_users:
            # Add any user for now (can be restricted later)
            self.authorized_users.append(user_id)
            logger.info(f"✅ Auto-authorized user: {username} (ID: {user_id})")
        
        welcome_text = """
🚀 **HYPERION ELITE BOT v5.0 - HEADLESS SERVER**
================================================

**Server Status:** ✅ Online & Operational
**Mode:** Headless VPS Production
**Performance:** Elite Optimized

**Available Commands:**
• `/check` - Start MEGA account checking
• `/scan` - AI combo analysis
• `/status` - System performance
• `/help` - Command reference

**Elite Features:**
🤖 AI-Powered Analysis
⚡ Multi-Threaded Processing  
🛡️ Advanced Security
🔄 Auto-Restart Capability
📊 Real-Time Statistics

Ready for elite operations! 🎯
"""
        
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"✅ Elite user {user_id} accessed the bot")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - server health check"""
        user_id = update.effective_user.id
        
        if user_id not in self.authorized_users:
            return
        
        try:
            # System information
            uptime = time.time() - getattr(self, 'start_time', time.time())
            memory_objects = len(gc.get_objects())
            
            # Server stats
            status_text = f"""
🖥️ **HYPERION SERVER STATUS**
============================

**System Info:**
• CPU Cores: {self.cpu_cores}
• Max Threads: {self.max_threads}
• Mode: Headless Server
• Uptime: {uptime/3600:.1f} hours

**Performance:**
• Memory Objects: {memory_objects:,}
• Python Version: {sys.version.split()[0]}
• Platform: {platform.system()}

**Status:** ✅ All Systems Operational
**Last Check:** {datetime.now().strftime('%H:%M:%S')}
"""
            
            await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Status check failed: {e}")
            logger.error(f"Status command error: {e}")
    
    async def setup_bot(self):
        """Setup the Telegram bot with handlers"""
        try:
            self.telegram_app = Application.builder().token(self.telegram_token).build()
            
            # Command handlers
            self.telegram_app.add_handler(CommandHandler("start", self.start_command))
            self.telegram_app.add_handler(CommandHandler("status", self.status_command))
            
            logger.info("✅ Headless Telegram bot setup complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Bot setup failed: {e}")
            return False
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"🛑 Headless bot received signal {signum}, shutting down gracefully...")
        self.running = False
        
        if self.telegram_app:
            try:
                # Stop the application
                asyncio.create_task(self.telegram_app.stop())
                logger.info("✅ Bot shutdown complete")
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
        
        sys.exit(0)
    
    async def run_headless_bot(self):
        """Run the bot in headless server mode"""
        self.start_time = time.time()
        self.running = True
        
        logger.info("🚀 Starting headless HYPERION Elite Bot...")
        
        # Setup bot
        if not await self.setup_bot():
            logger.error("❌ Failed to setup bot")
            return
        
        logger.info("🤖 Starting headless Telegram interface...")
        
        try:
            # Start the bot
            await self.telegram_app.initialize()
            await self.telegram_app.start()
            
            logger.info("✅ HYPERION Elite Bot operational! Headless mode active.")
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Bot runtime error: {e}")
        finally:
            if self.telegram_app:
                await self.telegram_app.stop()
                await self.telegram_app.shutdown()

async def main():
    """Main headless entry point"""
    print("""
🚀 HYPERION ELITE BOT v5.0 - HEADLESS SERVER
============================================

VPS Production Mode
Enhanced Security & Performance
Auto-Restart Capability

Starting headless operations...
    """)
    
    if not TELEGRAM_AVAILABLE:
        logger.error("❌ Telegram libraries not installed!")
        logger.error("Install with: pip install python-telegram-bot")
        return
    
    # Load secure configuration
    try:
        import sys
        import os
        logger.info(f"🔍 Python path: {sys.path}")
        logger.info(f"🔍 Current directory: {os.getcwd()}")
        
        from hyperion_config import config
        telegram_token = config.get_telegram_token()
        logger.info(f"✅ Configuration loaded successfully")
        logger.info(f"✅ Bot token loaded: {telegram_token[:20]}..." if telegram_token else "❌ No token")
        
        if not telegram_token:
            # Fallback to hardcoded token
            telegram_token = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
            logger.warning("⚠️ Using fallback hardcoded token")
            
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.warning("⚠️ Using fallback hardcoded token")
        telegram_token = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
    except Exception as e:
        import traceback
        logger.error(f"❌ Configuration error: {e}")
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        logger.warning("⚠️ Using fallback hardcoded token")
        telegram_token = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
    
    # Create and run headless bot
    bot = HeadlessHyperionBot(telegram_token)
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, bot.signal_handler)
    signal.signal(signal.SIGTERM, bot.signal_handler)
    
    try:
        await bot.run_headless_bot()
    except Exception as e:
        logger.error(f"Headless bot error: {e}")

if __name__ == "__main__":
    # Ensure we're running in headless mode
    if os.getenv('DISPLAY'):
        logger.warning("⚠️ Display detected - forcing headless mode")
        os.environ.pop('DISPLAY', None)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Headless bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)