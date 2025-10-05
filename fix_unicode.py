"""
HYPERION v4.1 - Windows Compatibility Fix
Fixed Unicode encoding issues for Windows systems
"""

# Check if we're on Windows and configure console appropriately
import sys
import os

def setup_windows_unicode():
    """Setup Unicode support for Windows console"""
    if sys.platform.startswith('win'):
        try:
            # Try to enable UTF-8 mode
            if hasattr(sys.stdout, 'reconfigure'):
                sys.stdout.reconfigure(encoding='utf-8', errors='replace')
                sys.stderr.reconfigure(encoding='utf-8', errors='replace')
            
            # Set environment variable for UTF-8
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            
            # For older Python versions on Windows
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'replace')
            
        except Exception:
            # Fallback: just ignore Unicode errors
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'ignore')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'ignore')

# Apply Windows Unicode fix
setup_windows_unicode()

print("✅ HYPERION v4.1 - Windows Unicode Fix Applied")
print("Now run: python HYPERION.py")
print("The Unicode encoding error should be resolved!")