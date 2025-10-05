#!/usr/bin/env python3
"""
HYPERION Configuration Manager
Secure configuration loading for production deployment
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class HyperionConfig:
    """Secure configuration manager for HYPERION bot"""
    
    def __init__(self):
        self.config = {}
        self.load_configuration()
    
    def load_configuration(self):
        """Load configuration from environment variables and .env file"""
        # Try to load from .env file first
        env_file = Path('.env')
        if env_file.exists():
            self._load_env_file(env_file)
        
        # Override with environment variables
        self._load_environment_variables()
        
        # Validate required configuration
        self._validate_config()
    
    def _load_env_file(self, env_file: Path):
        """Load configuration from .env file"""
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        self.config[key.strip()] = value.strip()
            logger.info(f"Loaded configuration from {env_file}")
        except Exception as e:
            logger.warning(f"Could not load .env file: {e}")
    
    def _load_environment_variables(self):
        """Load configuration from environment variables"""
        env_vars = {
            'TELEGRAM_BOT_TOKEN': 'telegram_bot_token',
            'AUTHORIZED_USER_ID': 'authorized_user_id',
            'DISCORD_WEBHOOK_URL': 'discord_webhook_url',
            'MAX_THREADS': 'max_threads',
            'DEFAULT_DELAY_MIN': 'default_delay_min',
            'DEFAULT_DELAY_MAX': 'default_delay_max',
            'ENABLE_DEEP_SCAN': 'enable_deep_scan',
            'ENABLE_PROXY_ROTATION': 'enable_proxy_rotation',
            'MAX_RETRIES': 'max_retries',
            'HITS_DIRECTORY': 'hits_directory',
            'LOGS_DIRECTORY': 'logs_directory',
            'TEMP_DIRECTORY': 'temp_directory',
            'DEBUG_MODE': 'debug_mode',
            'PERFORMANCE_LOGGING': 'performance_logging'
        }
        
        for env_var, config_key in env_vars.items():
            value = os.getenv(env_var)
            if value:
                self.config[env_var] = value
    
    def _validate_config(self):
        """Validate required configuration"""
        required_vars = ['TELEGRAM_BOT_TOKEN']
        
        missing_vars = []
        for var in required_vars:
            if not self.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required configuration: {', '.join(missing_vars)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer configuration value"""
        try:
            return int(self.get(key, default))
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean configuration value"""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return default
    
    def get_telegram_token(self) -> str:
        """Get Telegram bot token"""
        token = self.get('TELEGRAM_BOT_TOKEN')
        if not token or token == 'your_bot_token_here':
            raise ValueError("Telegram bot token not configured! Please set TELEGRAM_BOT_TOKEN environment variable.")
        return token
    
    def get_authorized_user_id(self) -> Optional[int]:
        """Get authorized user ID"""
        user_id = self.get('AUTHORIZED_USER_ID')
        if user_id and user_id != 'your_telegram_user_id_here':
            try:
                return int(user_id)
            except ValueError:
                logger.warning(f"Invalid user ID format: {user_id}")
        return None
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance-related settings"""
        return {
            'max_threads': self.get_int('MAX_THREADS', 10),
            'default_delay_min': self.get_int('DEFAULT_DELAY_MIN', 1),
            'default_delay_max': self.get_int('DEFAULT_DELAY_MAX', 3),
            'max_retries': self.get_int('MAX_RETRIES', 3),
            'enable_proxy_rotation': self.get_bool('ENABLE_PROXY_ROTATION', True),
            'enable_deep_scan': self.get_bool('ENABLE_DEEP_SCAN', True)
        }
    
    def get_paths(self) -> Dict[str, str]:
        """Get file paths configuration"""
        return {
            'hits_directory': self.get('HITS_DIRECTORY', './hits'),
            'logs_directory': self.get('LOGS_DIRECTORY', './logs'),
            'temp_directory': self.get('TEMP_DIRECTORY', './temp')
        }
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get_bool('DEBUG_MODE', False)
    
    def is_performance_logging_enabled(self) -> bool:
        """Check if performance logging is enabled"""
        return self.get_bool('PERFORMANCE_LOGGING', True)

# Global configuration instance
config = HyperionConfig()