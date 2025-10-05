"""
Theme Manager for MEGA Checker
Allows users to load custom color themes from JSON files
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThemeManager:
    """Manages theme loading and switching"""
    
    def __init__(self, theme_dir: str = "themes"):
        self.theme_dir = Path(theme_dir)
        self.themes: Dict[str, dict] = {}
        self.current_theme: Optional[dict] = None
        
    def discover_themes(self) -> int:
        """
        Discover all themes in the themes directory
        
        Returns:
            Number of themes discovered
        """
        if not self.theme_dir.exists():
            logger.warning(f"Theme directory '{self.theme_dir}' does not exist")
            self.theme_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created theme directory: {self.theme_dir}")
            return 0
        
        theme_count = 0
        
        # Scan all .json files in themes directory
        for theme_file in self.theme_dir.glob("*.json"):
            try:
                with open(theme_file, 'r') as f:
                    theme_data = json.load(f)
                
                # Validate theme structure
                if not self.validate_theme(theme_data):
                    logger.warning(f"✗ Invalid theme format: {theme_file.name}")
                    continue
                
                theme_name = theme_data.get('name', theme_file.stem)
                self.themes[theme_name] = theme_data
                theme_count += 1
                
                logger.info(
                    f"✓ Loaded theme: {theme_name} v{theme_data.get('version', '1.0.0')} "
                    f"by {theme_data.get('author', 'Unknown')}"
                )
                
            except json.JSONDecodeError as e:
                logger.error(f"✗ Invalid JSON in {theme_file.name}: {e}")
            except Exception as e:
                logger.error(f"✗ Failed to load theme {theme_file.name}: {e}")
        
        logger.info(f"🎨 Discovered {theme_count} themes")
        return theme_count
    
    def validate_theme(self, theme_data: dict) -> bool:
        """Validate theme structure"""
        required_keys = ['name', 'colors']
        
        # Check required top-level keys
        for key in required_keys:
            if key not in theme_data:
                return False
        
        # Check required color keys
        required_colors = [
            'primary', 'success', 'warning', 'error',
            'bg_main', 'bg_secondary', 'text_primary'
        ]
        
        colors = theme_data['colors']
        for color_key in required_colors:
            if color_key not in colors:
                return False
        
        return True
    
    def load_theme(self, theme_name: str) -> Optional[dict]:
        """
        Load a theme by name
        
        Args:
            theme_name: Name of the theme to load
            
        Returns:
            Theme colors dict or None if not found
        """
        if theme_name not in self.themes:
            logger.warning(f"Theme '{theme_name}' not found")
            return None
        
        self.current_theme = self.themes[theme_name]
        logger.info(f"✓ Loaded theme: {theme_name}")
        return self.current_theme['colors']
    
    def get_theme_list(self) -> List[dict]:
        """Get list of available themes with metadata"""
        theme_list = []
        for theme_name, theme_data in self.themes.items():
            theme_list.append({
                'name': theme_data.get('name', theme_name),
                'author': theme_data.get('author', 'Unknown'),
                'version': theme_data.get('version', '1.0.0'),
                'description': theme_data.get('description', 'No description')
            })
        return theme_list
    
    def get_current_theme_name(self) -> str:
        """Get name of currently loaded theme"""
        if self.current_theme:
            return self.current_theme.get('name', 'Unknown')
        return "Default"
    
    def export_current_theme(self, output_file: str) -> bool:
        """
        Export current theme to a file
        
        Args:
            output_file: Path to output file
            
        Returns:
            True if successful
        """
        if not self.current_theme:
            logger.warning("No theme currently loaded")
            return False
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.current_theme, f, indent=2)
            logger.info(f"✓ Exported theme to: {output_file}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to export theme: {e}")
            return False
    
    def create_theme_template(self, output_file: str = "themes/custom_theme_template.json"):
        """Create a template file for users to create their own themes"""
        template = {
            "name": "Custom Theme Name",
            "author": "Your Name",
            "version": "1.0.0",
            "description": "Description of your theme",
            "colors": {
                "primary": "#1a73e8",
                "primary_hover": "#1557b0",
                "primary_light": "#4285f4",
                "success": "#34a853",
                "warning": "#fbbc04",
                "error": "#ea4335",
                "info": "#4285f4",
                "bg_main": "#0f1419",
                "bg_secondary": "#1a1f2e",
                "bg_elevated": "#232938",
                "bg_input": "#2d3548",
                "text_primary": "#e8eaed",
                "text_secondary": "#9aa0a6",
                "text_tertiary": "#5f6368",
                "border_main": "#3c4043",
                "border_light": "#5f6368",
                "border_focus": "#1a73e8",
                "accent_1": "#667eea",
                "accent_2": "#764ba2"
            }
        }
        
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump(template, f, indent=2)
            
            logger.info(f"✓ Created theme template: {output_file}")
            logger.info("Edit this file to create your own custom theme!")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to create template: {e}")
            return False


# Global theme manager instance
theme_manager = ThemeManager()


if __name__ == "__main__":
    """Test the theme manager"""
    print("🎨 MEGA Checker - Theme Manager Test\n")
    
    # Discover themes
    count = theme_manager.discover_themes()
    
    if count == 0:
        print("No themes found. Creating template...")
        theme_manager.create_theme_template()
    else:
        print(f"\n📋 Available Themes:")
        for theme_info in theme_manager.get_theme_list():
            print(f"\n  {theme_info['name']} v{theme_info['version']}")
            print(f"    Author: {theme_info['author']}")
            print(f"    Description: {theme_info['description']}")
        
        # Load first theme as example
        first_theme = list(theme_manager.themes.keys())[0]
        colors = theme_manager.load_theme(first_theme)
        
        if colors:
            print(f"\n✓ Loaded theme: {first_theme}")
            print("\n  Color Palette:")
            for color_name, color_value in list(colors.items())[:5]:
                print(f"    {color_name}: {color_value}")
            print(f"    ... and {len(colors) - 5} more colors")
