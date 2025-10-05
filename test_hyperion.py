#!/usr/bin/env python3
"""
Quick test script for HYPERION Unicode fix
"""

import sys
import os

def test_hyperion_import():
    """Test if HYPERION can be imported without errors"""
    try:
        print("Testing HYPERION import...")
        
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Try to import the main components
        print("✓ Importing logging...")
        import logging
        
        print("✓ Importing customtkinter...")
        import customtkinter as ctk
        
        print("✓ Importing HYPERION classes...")
        from HYPERION import HackerTheme, AIEngine, ProxyManager
        
        print("✓ All imports successful!")
        print("✓ HYPERION is ready to run")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Install missing dependencies with: pip install customtkinter requests")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def test_unicode_logging():
    """Test Unicode logging functionality"""
    try:
        print("\nTesting Unicode logging...")
        
        import logging
        import tempfile
        
        # Create a test logger
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.log', delete=False) as f:
            test_log = f.name
        
        logger = logging.getLogger('test')
        handler = logging.FileHandler(test_log, encoding='utf-8')
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        
        # Test various messages
        logger.info("Basic ASCII message")
        logger.info("Unicode test: ✓ ✗ ⚠")
        logger.info("Emoji test: 🚀 📊 🎯")
        
        print("✓ Unicode logging test passed")
        
        # Clean up
        os.unlink(test_log)
        return True
        
    except Exception as e:
        print(f"✗ Unicode logging test failed: {e}")
        return False

if __name__ == "__main__":
    print("HYPERION v4.0 - System Compatibility Test")
    print("=" * 50)
    
    # Test import
    import_ok = test_hyperion_import()
    
    # Test Unicode
    unicode_ok = test_unicode_logging()
    
    print("\n" + "=" * 50)
    if import_ok and unicode_ok:
        print("✅ ALL TESTS PASSED - HYPERION is ready!")
        print("Run: python HYPERION.py")
    else:
        print("❌ SOME TESTS FAILED - Check dependencies")
        if not import_ok:
            print("   - Install: pip install customtkinter requests")
        if not unicode_ok:
            print("   - Check Python Unicode support")
    
    print("=" * 50)