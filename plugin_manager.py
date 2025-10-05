"""
Plugin Manager for Dynamic Proxy Source Loading
Automatically discovers and loads proxy source plugins
"""

import os
import importlib.util
import inspect
import logging
from typing import List, Dict
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PluginManager:
    """Manages loading and execution of proxy source plugins"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: List = []
        self.plugin_info: Dict[str, dict] = {}
        
    def discover_plugins(self) -> int:
        """
        Discover all plugins in the plugins directory
        
        Returns:
            Number of plugins discovered
        """
        if not self.plugin_dir.exists():
            logger.warning(f"Plugin directory '{self.plugin_dir}' does not exist")
            self.plugin_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created plugin directory: {self.plugin_dir}")
            return 0
        
        plugin_count = 0
        
        # Import the base class
        try:
            from plugins.proxy_source_plugin import ProxySourcePlugin
        except ImportError:
            logger.error("Could not import ProxySourcePlugin base class")
            return 0
        
        # Scan all .py files in plugins directory
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue  # Skip __init__.py and private files
            
            if plugin_file.name == "proxy_source_plugin.py":
                continue  # Skip base class
            
            try:
                # Load the module
                module_name = plugin_file.stem
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find all classes that inherit from ProxySourcePlugin
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, ProxySourcePlugin) and obj != ProxySourcePlugin:
                        try:
                            # Instantiate the plugin
                            plugin_instance = obj()
                            
                            # Store plugin info
                            info = {
                                'name': plugin_instance.get_name(),
                                'category': plugin_instance.get_category(),
                                'description': plugin_instance.get_description(),
                                'author': plugin_instance.get_author(),
                                'version': plugin_instance.get_version(),
                                'enabled': plugin_instance.is_enabled(),
                                'file': plugin_file.name,
                                'class': name
                            }
                            
                            self.plugins.append(plugin_instance)
                            self.plugin_info[plugin_instance.get_name()] = info
                            plugin_count += 1
                            
                            logger.info(
                                f"✓ Loaded plugin: {info['name']} v{info['version']} "
                                f"by {info['author']} [{info['category']}]"
                            )
                            
                        except Exception as e:
                            logger.error(f"✗ Failed to instantiate {name}: {e}")
                
            except Exception as e:
                logger.error(f"✗ Failed to load plugin {plugin_file.name}: {e}")
        
        logger.info(f"📦 Discovered {plugin_count} plugins")
        return plugin_count
    
    def get_enabled_plugins(self) -> List:
        """Get list of enabled plugins"""
        return [p for p in self.plugins if p.is_enabled()]
    
    def get_plugins_by_category(self, category: str) -> List:
        """Get plugins filtered by category"""
        return [p for p in self.plugins if p.get_category() == category and p.is_enabled()]
    
    def get_plugin_info_list(self) -> List[dict]:
        """Get list of all plugin information"""
        return list(self.plugin_info.values())
    
    def reload_plugins(self) -> int:
        """Reload all plugins"""
        self.plugins.clear()
        self.plugin_info.clear()
        return self.discover_plugins()


# Global plugin manager instance
plugin_manager = PluginManager()
