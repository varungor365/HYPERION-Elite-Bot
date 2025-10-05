#!/usr/bin/env python3
"""
HYPERION Bot - Ultra Simple Test Version
Just to verify basic Telegram connectivity
"""

import asyncio
import logging
import sys

# Simple logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    print("✅ Telegram libraries imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

BOT_TOKEN = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Simple start command"""
    user = update.effective_user
    message = f"""
🎯 HYPERION TEST BOT RESPONSE

✅ Bot is WORKING!
👤 User: {user.first_name} (@{user.username})
🆔 User ID: {user.id}
📅 Time: {update.message.date}

If you see this message, the bot is responding correctly! 🚀
"""
    
    await update.message.reply_text(message)
    print(f"✅ Responded to {user.username} ({user.id})")

async def test_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test command"""
    await update.message.reply_text("🧪 Test successful! Bot is receiving and responding to commands.")
    print("✅ Test command executed")

async def main():
    """Simple main function"""
    print("🚀 Starting HYPERION Test Bot...")
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("test", test_command))
    
    print("🔧 Handlers added")
    
    try:
        # Initialize and start
        print("🔄 Initializing bot...")
        await app.initialize()
        
        print("🔄 Starting bot...")
        await app.start()
        
        print("🔄 Starting polling...")
        await app.updater.start_polling(
            poll_interval=1.0,
            timeout=10,
            bootstrap_retries=3
        )
        
        print("✅ HYPERION Test Bot is ONLINE!")
        print("📱 Send /start or /test to @megacheckk_bot")
        print("🛑 Press Ctrl+C to stop")
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("🛑 Stopping bot...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        try:
            await app.updater.stop()
            await app.stop() 
            await app.shutdown()
        except:
            pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped")
    except Exception as e:
        print(f"❌ Fatal error: {e}")