"""
Project Cleanup and Organization Script
Removes unnecessary files and consolidates documentation
"""

import os
import shutil
from pathlib import Path

# Files to keep (essential)
KEEP_FILES = {
    # Core application files
    'mega_pro_elite.py',
    'checker_engine.py',
    'mega_auth.py',
    'proxy_fetcher.py',
    'proxy_rotator.py',
    'discord_notifier.py',
    'plugin_manager.py',
    'theme_manager.py',
    'session_manager.py',
    
    # Configuration and requirements
    'requirements.txt',
    'config.json',
    '.gitignore',
    'LICENSE',
    
    # Documentation (consolidated)
    'README_COMPLETE.md',
    
    # Installation scripts
    'install.bat',
    'install.sh',
    'run.bat',
    'run.sh',
    'verify_install.py',
    
    # Build files (optional)
    'build_exe.py',
    'build_exe.bat',
    
    # Example files
    'proxies_example.txt',
}

# Files to remove (old versions, duplicates, unnecessary)
REMOVE_FILES = {
    # Old GUI versions
    'mega_checker.py',
    'mega_checker_pro.py',
    'mega_checker_ai_pro.py',
    'mega_hacker_pro.py',
    
    # Duplicate documentation
    'DOCUMENTATION.md',
    'README.md',
    'README_FEATURES.md',
    'README_CONTRIBUTORS.md',
    'QUICKSTART.md',
    'QUICK_START.md',
    'BUILD_INSTRUCTIONS.md',
    
    # Generated/test files
    'combo.txt',
    'combo_cleaned.txt',
    'merged_combo.txt',
    'merged_combo_cleaned.txt',
    'hits.txt',
    'hits_empty.txt',
    'hits_free.txt',
    'hits_pro.txt',
    'fetched_proxies.txt',
    'auto_proxies.txt',
    'ai_proxies.txt',
    'ai_proxies_quality.txt',
    'ai_proxies_elite.txt',
    'auto_fetched_proxies.txt',
    
    # Test scripts
    'test_ai_proxies.py',
    
    # Build artifacts
    'mega_checker.spec',
    
    # Obsolete batch files
    'setup_all.bat',
    'run_pro.bat',
}

# Directories to keep
KEEP_DIRS = {
    'plugins',
    'themes',
    'sessions',
    '__pycache__',
}

def cleanup_project():
    """Clean up project by removing unnecessary files"""
    
    print("🧹 MEGA Checker - Project Cleanup")
    print("=" * 60)
    
    base_dir = Path(__file__).parent
    removed_count = 0
    kept_count = 0
    
    # Remove unnecessary files
    print("\n📁 Removing unnecessary files...")
    for file in REMOVE_FILES:
        file_path = base_dir / file
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"  ✓ Removed: {file}")
                removed_count += 1
            except Exception as e:
                print(f"  ✗ Failed to remove {file}: {e}")
        else:
            print(f"  - Not found: {file}")
    
    # Create necessary directories
    print("\n📂 Creating necessary directories...")
    for dir_name in ['plugins', 'themes', 'sessions', 'exports', 'logs']:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
            print(f"  ✓ Created: {dir_name}/")
        else:
            print(f"  - Exists: {dir_name}/")
    
    # Count kept files
    print("\n📝 Counting essential files...")
    for file in KEEP_FILES:
        file_path = base_dir / file
        if file_path.exists():
            kept_count += 1
            print(f"  ✓ Kept: {file}")
    
    # Rename README
    print("\n📄 Setting up main README...")
    readme_complete = base_dir / 'README_COMPLETE.md'
    readme_main = base_dir / 'README.md'
    
    if readme_complete.exists():
        if readme_main.exists():
            readme_main.unlink()
        shutil.copy(readme_complete, readme_main)
        print("  ✓ Created README.md from README_COMPLETE.md")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Cleanup Complete!")
    print(f"  Removed: {removed_count} files")
    print(f"  Kept: {kept_count} essential files")
    print(f"  Project is now organized and clean!")
    print("=" * 60)
    
    # Next steps
    print("\n📌 Next Steps:")
    print("  1. Review README.md for complete documentation")
    print("  2. Run: python verify_install.py")
    print("  3. Run: python mega_pro_elite.py")
    print("\n💡 To undo cleanup, restore from git: git checkout .")

def create_project_structure_doc():
    """Create a document showing the final project structure"""
    
    structure = """
# MEGA Checker - Project Structure

```
CleanMegaChecker/
│
├── 📁 Core Application
│   ├── mega_pro_elite.py          # Main application (Elite UI)
│   ├── checker_engine.py          # Checking logic
│   ├── mega_auth.py               # MEGA authentication
│   ├── proxy_fetcher.py           # Proxy fetching & AI testing
│   ├── proxy_rotator.py           # Proxy rotation & anti-ban
│   ├── discord_notifier.py        # Discord webhook notifications
│   ├── plugin_manager.py          # Plugin system manager
│   ├── theme_manager.py           # Theme management
│   └── session_manager.py         # Session save/load
│
├── 📁 Configuration
│   ├── config.json                # App configuration
│   ├── requirements.txt           # Python dependencies
│   └── proxies_example.txt        # Example proxy format
│
├── 📁 Plugins (Extensible)
│   ├── proxy_source_plugin.py     # Base plugin class
│   └── example_sources.py         # Example plugin implementations
│
├── 📁 Themes (Customizable)
│   ├── professional_dark.json     # Default theme
│   ├── cyberpunk_matrix.json      # Matrix style theme
│   └── midnight_purple.json       # Purple theme
│
├── 📁 Sessions (Auto-created)
│   └── session_*.json             # Saved sessions
│
├── 📁 Exports (Auto-created)
│   └── hits_*.txt                 # Exported results
│
├── 📁 Logs (Auto-created)
│   └── checker_*.log              # Application logs
│
├── 📁 Installation
│   ├── install.bat                # Windows installer
│   ├── install.sh                 # Linux/Mac installer
│   ├── run.bat                    # Windows runner
│   ├── run.sh                     # Linux/Mac runner
│   ├── verify_install.py          # Installation verifier
│   ├── build_exe.py               # Build executable
│   └── build_exe.bat              # Build script (Windows)
│
├── 📄 Documentation
│   ├── README.md                  # Complete documentation
│   └── LICENSE                    # MIT License
│
└── 🔧 Git
    └── .gitignore                 # Git ignore rules
```

## File Descriptions

### Core Application Files

**mega_pro_elite.py**
- Main application entry point
- Professional UI with 3-column layout
- Integrated features: AI proxy, session management, themes

**checker_engine.py**
- Core checking logic
- Account validation
- Result storage

**mega_auth.py**
- MEGA API authentication
- Login functionality
- Proxy support

**proxy_fetcher.py**
- Fetches proxies from 15+ sources
- AI quality testing
- MEGA compatibility checking

**proxy_rotator.py**
- Proxy rotation system
- Anti-ban features
- Rate limiting

**discord_notifier.py**
- Discord webhook integration
- Hit notifications
- Custom messages

**plugin_manager.py**
- Plugin discovery and loading
- Plugin lifecycle management
- API for plugin developers

**theme_manager.py**
- Theme loading and validation
- Color scheme management
- Theme API

**session_manager.py**
- Save/load checking sessions
- Resume functionality
- Session history

### Configuration Files

**config.json**
- Default settings
- API keys
- Preferences

**requirements.txt**
- Python package dependencies
- Version specifications

**proxies_example.txt**
- Example proxy format
- Documentation

### Directory Purposes

**plugins/**
- User-created proxy source plugins
- Automatically loaded by plugin manager
- See README.md for plugin development guide

**themes/**
- User-created color schemes
- JSON format
- See README.md for theme creation guide

**sessions/**
- Automatically created when saving sessions
- JSON format with all state information
- Can be manually edited

**exports/**
- Automatically created for hit exports
- TXT, CSV, JSON formats
- Organized by timestamp

**logs/**
- Application logs
- Debugging information
- Error tracking

## Installation Flow

1. User runs `install.bat` or `install.sh`
2. Script installs requirements.txt
3. User runs `verify_install.py` to check
4. User runs `mega_pro_elite.py` to start app

## Usage Flow

1. Load combo file(s)
2. Configure settings
3. (Optional) Enable proxies & run AI test
4. Start checking
5. (Optional) Save session
6. Export results

## Development Flow

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Plugin Development Flow

1. Create new file in `plugins/`
2. Inherit from `ProxySourcePlugin`
3. Implement `fetch_proxies()` method
4. Plugin auto-loaded on next run

## Theme Development Flow

1. Create new JSON file in `themes/`
2. Define all required color keys
3. Test with theme manager
4. Share with community

---

**Last Updated:** October 5, 2025
"""
    
    with open('PROJECT_STRUCTURE.md', 'w', encoding='utf-8') as f:
        f.write(structure)
    
    print("  ✓ Created PROJECT_STRUCTURE.md")

if __name__ == "__main__":
    try:
        cleanup_project()
        create_project_structure_doc()
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        print("Project remains unchanged.")
