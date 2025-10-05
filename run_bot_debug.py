#!/usr/bin/env python3
"""
Debug runner for HYPERION Elite Bot
Run this for testing and debugging in terminal
"""

import os
import sys
import asyncio
import logging

# Setup logging for debug
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Debug main function"""
    print("🔧 HYPERION Elite Bot - Debug Mode")
    print("=" * 40)
    
    # Test token first
    token = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
    print(f"✅ Bot Token: {token[:20]}...")
    
    # Test imports
    try:
        from telegram import Bot
        print("✅ Telegram Bot imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Telegram Bot: {e}")
        print("📦 Install with: pip install python-telegram-bot")
        return False
    
    # Test bot creation
    try:
        bot = Bot(token=token)
        print("✅ Bot object created successfully")
    except Exception as e:
        print(f"❌ Failed to create bot: {e}")
        return False
    
    # Test async bot info
    async def test_bot():
        try:
            me = await bot.get_me()
            print(f"✅ Bot authenticated: @{me.username}")
            print(f"✅ Bot ID: {me.id}")
            print(f"✅ Bot Name: {me.first_name}")
            return True
        except Exception as e:
            print(f"❌ Bot authentication failed: {e}")
            return False
        finally:
            await bot.close()
    
    # Run async test
    try:
        result = asyncio.run(test_bot())
        if result:
            print("\n🎉 All tests passed! Bot is ready to run.")
            print("\n🚀 To start the bot, run:")
            print("   python3 hyperion_headless.py")
            return True
        else:
            print("\n❌ Bot test failed!")
            return False
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Debug test interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Debug test error: {e}")
        sys.exit(1)