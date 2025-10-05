#!/usr/bin/env python3
"""
Test the fixed HYPERION system 
Verify no more duplicate hits and proper CheckerEngine integration
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from HYPERION import MEGAChecker, CheckResult

def test_fixed_hyperion():
    """Test the integrated CheckerEngine in HYPERION"""
    print("🔥 HYPERION v4.0 - Integration Test")
    print("=" * 50)
    
    # Test with a small combo list
    test_combos = [
        "test1@invalid.com:password123",
        "test2@invalid.com:password456", 
        "test3@invalid.com:password789"
    ]
    
    # Track results
    results_log = []
    progress_log = []
    
    def log_callback(message, level):
        """Track log messages"""
        results_log.append(f"[{level.upper()}] {message}")
        print(f"LOG: {message}")
    
    def progress_callback(checked, total, result):
        """Track progress updates"""
        progress_log.append(f"Progress: {checked}/{total} - Status: {result.status}")
        print(f"PROGRESS: {checked}/{total} - Status: {result.status}")
    
    # Initialize checker with callbacks
    print("\n🧪 Testing CheckerEngine integration...")
    checker = MEGAChecker(progress_callback=progress_callback, log_callback=log_callback)
    
    print(f"🎯 Testing {len(test_combos)} accounts...")
    
    # Start time
    start_time = time.time()
    
    try:
        # This should now use CheckerEngine properly, no duplicates
        checker.check_combo_list(test_combos, use_proxies=False, threads=2)
        
        # Wait a moment for completion
        time.sleep(2)
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Test completed in {elapsed:.1f}s")
        print(f"📊 Results logged: {len(results_log)}")
        print(f"📈 Progress updates: {len(progress_log)}")
        
        # Check for duplicates
        email_counts = {}
        for log in results_log:
            if "[HIT]" in log or "[FAIL]" in log:
                email = log.split("] ")[-1] if "] " in log else log
                email_counts[email] = email_counts.get(email, 0) + 1
        
        duplicates = {email: count for email, count in email_counts.items() if count > 1}
        
        if duplicates:
            print(f"❌ DUPLICATES DETECTED: {duplicates}")
            print("🚨 The threading fix did not work properly!")
        else:
            print("✅ No duplicate results detected")
            print("🎯 Threading fix successful!")
        
        print(f"\n📋 Final CheckerEngine stats:")
        if hasattr(checker, 'checker_engine') and checker.checker_engine:
            engine = checker.checker_engine
            print(f"   Checked: {engine.checked}")
            print(f"   Hits: {engine.hits}")
            print(f"   Fails: {engine.fails}")
            print(f"   Customs: {engine.customs}")
        
    except Exception as e:
        print(f"⚠️ Test error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ HYPERION Integration Test Complete")

if __name__ == "__main__":
    test_fixed_hyperion()