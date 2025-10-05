#!/usr/bin/env python3
"""
HYPERION CLI - Command Line Interface
Simple command-line version for testing MEGA authentication without GUI dependencies
"""

import sys
import os
import time
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mega_auth():
    """Test MEGA authentication functionality"""
    try:
        print("🚀 HYPERION CLI - MEGA Authentication Test")
        print("=" * 50)
        
        # Import MEGA authenticator
        from mega_auth import MegaAuthenticator
        
        print("✅ Successfully imported MegaAuthenticator")
        
        # Create authenticator instance
        auth = MegaAuthenticator()
        print("✅ MegaAuthenticator initialized")
        
        # Test with sample credentials (these will fail, but we can test the functionality)
        test_email = "test@example.com"
        test_password = "testpassword"
        
        print(f"\n🔍 Testing authentication with: {test_email}")
        print("⏳ Attempting login...")
        
        # Perform authentication test
        success, account_data, error = auth.login(test_email, test_password)
        
        if success:
            print("✅ Login successful!")
            print(f"📊 Account data: {account_data}")
        else:
            print("❌ Login failed (expected for test credentials)")
            print(f"🔍 Error details: {error}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_checker_engine():
    """Test the checker engine functionality"""
    try:
        print("\n🔧 Testing Checker Engine")
        print("-" * 30)
        
        from checker_engine import CheckerEngine
        
        print("✅ Successfully imported CheckerEngine")
        
        # Create checker instance
        checker = CheckerEngine(thread_count=1)
        print("✅ CheckerEngine initialized")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main CLI function"""
    print("🎯 HYPERION Command Line Interface")
    print("==================================")
    print(f"⏰ Started at: {datetime.now()}")
    print()
    
    # Test core functionality
    mega_ok = test_mega_auth()
    checker_ok = test_checker_engine()
    
    print("\n" + "=" * 50)
    print("📊 SYSTEM STATUS SUMMARY")
    print("=" * 50)
    print(f"🔐 MEGA Authentication: {'✅ READY' if mega_ok else '❌ FAILED'}")
    print(f"🔧 Checker Engine: {'✅ READY' if checker_ok else '❌ FAILED'}")
    
    if mega_ok and checker_ok:
        print("\n🎉 HYPERION Core Systems: OPERATIONAL")
        print("💡 Ready for combo checking operations")
    else:
        print("\n⚠️ Some systems failed - check dependencies")
        
    return mega_ok and checker_ok

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)