#!/usr/bin/env python3
"""
HYPERION Bot Debug and Test Script
Quick verification of bot functionality
"""

import asyncio
import requests
import json
import sys

# Bot credentials
BOT_TOKEN = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
BOT_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

async def test_bot_api():
    """Test bot API connectivity"""
    print("🔍 Testing HYPERION Bot API...")
    
    try:
        # Test getMe
        response = requests.get(f"{BOT_API_URL}/getMe", timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                print(f"✅ Bot API working: @{bot_info['result']['username']}")
                print(f"   Bot ID: {bot_info['result']['id']}")
                print(f"   Bot Name: {bot_info['result']['first_name']}")
                return True
            else:
                print(f"❌ Bot API error: {bot_info}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

async def check_webhook():
    """Check webhook status"""
    print("\n🔍 Checking webhook status...")
    
    try:
        response = requests.get(f"{BOT_API_URL}/getWebhookInfo", timeout=10)
        if response.status_code == 200:
            webhook_info = response.json()
            if webhook_info['ok']:
                webhook_data = webhook_info['result']
                if webhook_data['url']:
                    print(f"⚠️  Webhook is set: {webhook_data['url']}")
                    print("   This might prevent polling. Removing webhook...")
                    
                    # Remove webhook
                    remove_response = requests.post(f"{BOT_API_URL}/deleteWebhook", timeout=10)
                    if remove_response.status_code == 200:
                        print("✅ Webhook removed successfully")
                    else:
                        print("❌ Failed to remove webhook")
                else:
                    print("✅ No webhook set (good for polling)")
                return True
        
    except Exception as e:
        print(f"❌ Webhook check error: {e}")
        return False

async def get_updates():
    """Get recent updates"""
    print("\n🔍 Checking for recent messages...")
    
    try:
        response = requests.get(f"{BOT_API_URL}/getUpdates", timeout=10)
        if response.status_code == 200:
            updates = response.json()
            if updates['ok']:
                if updates['result']:
                    print(f"✅ Found {len(updates['result'])} recent updates")
                    for update in updates['result'][-3:]:  # Show last 3
                        if 'message' in update:
                            msg = update['message']
                            user = msg.get('from', {})
                            text = msg.get('text', 'No text')
                            print(f"   📝 {user.get('username', 'N/A')}: {text}")
                else:
                    print("ℹ️  No recent messages found")
                return True
        
    except Exception as e:
        print(f"❌ Updates check error: {e}")
        return False

async def send_test_message():
    """Send a test message to check if bot can send messages"""
    print("\n🔍 Testing bot message sending...")
    
    # You'll need to replace this with your actual chat ID
    # You can get this by messaging the bot and checking getUpdates
    TEST_CHAT_ID = "796354588"  # Replace with your Telegram user ID
    
    try:
        test_data = {
            'chat_id': TEST_CHAT_ID,
            'text': '🤖 HYPERION Bot Test Message\n\nIf you see this, the bot can send messages!',
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(f"{BOT_API_URL}/sendMessage", json=test_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result['ok']:
                print("✅ Test message sent successfully!")
                return True
            else:
                print(f"❌ Send message error: {result}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Send message error: {e}")
        return False

async def main():
    """Main debug function"""
    print("🚀 HYPERION Bot Debug Tool")
    print("=" * 40)
    
    # Test API connectivity
    if not await test_bot_api():
        print("❌ Bot API test failed - check your token")
        return
    
    # Check webhook
    await check_webhook()
    
    # Check for updates
    await get_updates()
    
    # Optionally send test message
    print("\n💡 To test message sending, uncomment the send_test_message() call")
    # await send_test_message()
    
    print("\n" + "=" * 40)
    print("🔧 TROUBLESHOOTING TIPS:")
    print("1. Make sure your bot service is running: sudo systemctl status hyperion-elite-bot")
    print("2. Check bot logs: sudo journalctl -u hyperion-elite-bot -f")
    print("3. Try restarting the bot: sudo systemctl restart hyperion-elite-bot")
    print("4. Test bot commands in Telegram: /start")

if __name__ == "__main__":
    asyncio.run(main())