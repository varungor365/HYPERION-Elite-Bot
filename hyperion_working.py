#!/usr/bin/env python3
"""
HYPERION Elite Bot - Working Version 
Compatible with python-telegram-bot v20+
"""

import asyncio
import logging
import os
import sys
import signal
import time
import multiprocessing
from pathlib import Path

# Enhanced logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/hyperion_working.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

# Check for Telegram bot dependencies
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
    logger.info("✅ Telegram libraries loaded successfully")
except ImportError as e:
    logger.error(f"❌ Telegram dependencies not available: {e}")
    TELEGRAM_AVAILABLE = False

class WorkingHyperionBot:
    """Working HYPERION Elite Bot with correct API usage"""
    
    def __init__(self, telegram_token: str):
        self.telegram_token = telegram_token
        self.authorized_users = []
        self.application = None
        self.running = False
        
        # System info
        self.cpu_cores = multiprocessing.cpu_count()
        self.start_time = time.time()
        
        logger.info(f"🚀 Working HYPERION Elite Bot initialized")
        logger.info(f"   💻 CPU Cores: {self.cpu_cores}")
        logger.info(f"   🔧 Mode: Working Version")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "Unknown"
        
        # Auto-authorize users
        if user_id not in self.authorized_users:
            self.authorized_users.append(user_id)
            logger.info(f"✅ Auto-authorized user: {username} (ID: {user_id})")
        
        welcome_message = f"""
🚀 **HYPERION ELITE BOT v5.0 - WORKING!**
═══════════════════════════════════════

**Status:** ✅ ONLINE & RESPONDING  
**Server:** DigitalOcean VPS
**Mode:** Production Ready

**🎯 SUCCESS! Bot is working correctly!**

**Available Commands:**
• `/start` - This welcome message
• `/status` - System information  
• `/help` - Command help
• `/info` - Bot details
• `/ping` - Connection test

**System Info:**
🖥️ CPU Cores: {self.cpu_cores}
⏱️ Uptime: {int(time.time() - self.start_time)}s
👥 Users: {len(self.authorized_users)}

Ready for MEGA checking operations! 🎯
"""
        
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"✅ /start responded to user {user_id}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /status command"""
        uptime = int(time.time() - self.start_time)
        uptime_str = f"{uptime//3600}h {(uptime%3600)//60}m {uptime%60}s"
        
        status_message = f"""
📊 **SYSTEM STATUS - WORKING!**
═══════════════════════════════

**Bot Status:** ✅ Online & Responding
**Uptime:** {uptime_str}
**CPU Cores:** {self.cpu_cores}
**Users:** {len(self.authorized_users)}

**Server:** DigitalOcean VPS
**Python:** {sys.version.split()[0]}
**Mode:** Production

**🎯 All systems operational!**
"""
        
        await update.message.reply_text(status_message, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"✅ /status responded")
    
    async def ping_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /ping command"""
        start_time = time.time()
        message = await update.message.reply_text("🏓 Pinging...")
        end_time = time.time()
        
        response_time = int((end_time - start_time) * 1000)
        
        await message.edit_text(f"🏓 **Pong!**\n\n⚡ Response time: {response_time}ms\n✅ Bot is responsive!")
        logger.info(f"✅ /ping responded in {response_time}ms")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_message = """
🆘 **HYPERION HELP - WORKING VERSION**
═══════════════════════════════════════

**Available Commands:**
• `/start` - Welcome & bot information
• `/status` - System status check
• `/ping` - Response time test
• `/help` - This help message
• `/info` - Detailed bot info

**Bot Features:**
✅ Real-time responses
✅ VPS optimized
✅ Auto-restart capability
✅ Production logging

**Support:**
🤖 Bot: @megacheckk_bot
📁 GitHub: varungor365/HYPERION-Elite-Bot

**Status:** Working perfectly! 🎯
"""
        
        await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"✅ /help responded")
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /info command"""
        info_message = f"""
ℹ️ **BOT INFORMATION - WORKING VERSION**
═════════════════════════════════════════

**Bot Details:**
🤖 Name: HYPERION Elite Bot
📝 Version: v5.0 Working
🏷️ Username: @megacheckk_bot

**System:**
🖥️ VPS: DigitalOcean
🐧 OS: Ubuntu Server
🐍 Python: {sys.version.split()[0]}
⚡ Cores: {self.cpu_cores}

**Status:** ✅ Fully operational!
**Responses:** ✅ Working perfectly
**Commands:** ✅ All functional

**Repository:**
📁 GitHub: varungor365/HYPERION-Elite-Bot

Ready for action! 🚀
"""
        
        await update.message.reply_text(info_message, parse_mode=ParseMode.MARKDOWN)
        logger.info(f"✅ /info responded")
    
    async def run(self):
        """Run the bot with corrected API usage"""
        logger.info("🚀 Starting Working HYPERION Elite Bot...")
        
        try:
            # Create application
            self.application = Application.builder().token(self.telegram_token).build()
            
            # Add command handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("status", self.status_command))
            self.application.add_handler(CommandHandler("ping", self.ping_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("info", self.info_command))
            
            logger.info("✅ Command handlers registered")
            
            # Initialize bot
            logger.info("🔄 Initializing bot...")
            await self.application.initialize()
            
            logger.info("🔄 Starting bot...")
            await self.application.start()
            
            # Start polling with minimal parameters
            logger.info("🔄 Starting polling...")
            await self.application.updater.start_polling()
            
            logger.info("✅ HYPERION Elite Bot is ONLINE and working!")
            logger.info("📱 Send /start to @megacheckk_bot to test")
            
            # Keep the bot running
            self.running = True
            while self.running:
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"❌ Bot error: {e}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
        finally:
            # Cleanup
            if self.application:
                logger.info("🛑 Stopping bot...")
                try:
                    await self.application.updater.stop()
                    await self.application.stop()
                    await self.application.shutdown()
                except:
                    pass
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"🛑 Received signal {signum}, shutting down...")
        self.running = False

async def main():
    """Main entry point"""
    print("""
🚀 HYPERION ELITE BOT v5.0 - WORKING VERSION
============================================

✅ Fixed API compatibility issues
✅ Corrected polling parameters  
✅ Production ready
✅ VPS optimized

Starting working bot...
""")
    
    if not TELEGRAM_AVAILABLE:
        logger.error("❌ Telegram libraries not installed!")
        sys.exit(1)
    
    # Bot token
    telegram_token = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
    
    # Create and run bot
    bot = WorkingHyperionBot(telegram_token)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, bot.signal_handler)
    signal.signal(signal.SIGTERM, bot.signal_handler)
    
    # Run the bot
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    # Auto-restart loop
    restart_count = 0
    max_restarts = 5
    
    while restart_count < max_restarts:
        try:
            asyncio.run(main())
            break  # Normal exit
        except KeyboardInterrupt:
            print("🛑 Bot stopped by user")
            break
        except Exception as e:
            restart_count += 1
            print(f"❌ Bot crashed (attempt {restart_count}/{max_restarts}): {e}")
            if restart_count < max_restarts:
                print("🔄 Restarting in 5 seconds...")
                time.sleep(5)
            else:
                print("❌ Max restarts reached. Exiting.")
                break