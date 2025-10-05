"""
Proxy Rotator & Anti-Ban System
Handles IP rotation, rate limiting, and intelligent delays to prevent bans
"""

import time
import random
import logging
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ProxyInfo:
    """Proxy server information"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"  # http, https, socks5
    last_used: Optional[datetime] = None
    success_count: int = 0
    fail_count: int = 0
    is_banned: bool = False
    
    def get_proxy_dict(self) -> Dict[str, str]:
        """Get proxy in requests-compatible format"""
        if self.username and self.password:
            auth = f"{self.username}:{self.password}@"
        else:
            auth = ""
        
        proxy_url = f"{self.protocol}://{auth}{self.host}:{self.port}"
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    def get_proxy_string(self) -> str:
        """Get proxy as string (for mega.py if supported)"""
        if self.username and self.password:
            return f"{self.protocol}://{self.username}:{self.password}@{self.host}:{self.port}"
        return f"{self.protocol}://{self.host}:{self.port}"


class AntiBanSystem:
    """
    Intelligent anti-ban system with:
    - Rate limiting
    - Proxy rotation
    - Smart delays
    - Request throttling
    - IP cooldown periods
    """
    
    def __init__(self):
        self.enabled = False
        self.use_proxies = False
        self.proxies: List[ProxyInfo] = []
        self.current_proxy_index = 0
        
        # Rate limiting settings
        self.max_requests_per_minute = 20  # Conservative default
        self.min_delay_between_requests = 3.0  # seconds
        self.max_delay_between_requests = 8.0  # seconds
        self.random_delay = True
        
        # Request tracking
        self.request_times: List[datetime] = []
        self.last_request_time: Optional[datetime] = None
        self.total_requests = 0
        
        # Proxy rotation settings
        self.rotate_after_requests = 10  # Rotate proxy every N requests
        self.requests_with_current_proxy = 0
        self.proxy_cooldown_minutes = 5  # Wait before reusing same proxy
        
        # Ban detection
        self.consecutive_failures = 0
        self.max_failures_before_rotation = 3
        
        # Thread safety
        self.lock = threading.Lock()
        
        logger.info("🛡️ Anti-Ban System initialized")
    
    def enable(self, max_rpm: int = 20, min_delay: float = 3.0, max_delay: float = 8.0):
        """Enable anti-ban protection"""
        self.enabled = True
        self.max_requests_per_minute = max_rpm
        self.min_delay_between_requests = min_delay
        self.max_delay_between_requests = max_delay
        logger.info(f"✅ Anti-Ban enabled: {max_rpm} req/min, {min_delay}-{max_delay}s delays")
    
    def disable(self):
        """Disable anti-ban protection"""
        self.enabled = False
        logger.info("⚠️ Anti-Ban disabled - Use with caution!")
    
    def load_proxies_from_file(self, filepath: str) -> int:
        """
        Load proxies from file
        Format: protocol://host:port or protocol://user:pass@host:port
        Example: http://proxy1.com:8080
        """
        loaded = 0
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    proxy = self._parse_proxy_string(line)
                    if proxy:
                        self.proxies.append(proxy)
                        loaded += 1
            
            if loaded > 0:
                self.use_proxies = True
                logger.info(f"✅ Loaded {loaded} proxies from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading proxies from {filepath}: {e}")
        
        return loaded
    
    def add_proxy(self, host: str, port: int, protocol: str = "http", 
                  username: str = None, password: str = None):
        """Add a proxy manually"""
        proxy = ProxyInfo(
            host=host,
            port=port,
            protocol=protocol,
            username=username,
            password=password
        )
        self.proxies.append(proxy)
        self.use_proxies = True
        logger.info(f"✅ Added proxy: {proxy.get_proxy_string()}")
    
    def _parse_proxy_string(self, proxy_str: str) -> Optional[ProxyInfo]:
        """Parse proxy string into ProxyInfo"""
        try:
            # Format: protocol://[user:pass@]host:port
            if '://' in proxy_str:
                protocol, rest = proxy_str.split('://', 1)
            else:
                protocol = 'http'
                rest = proxy_str
            
            username = None
            password = None
            
            if '@' in rest:
                auth, rest = rest.split('@', 1)
                if ':' in auth:
                    username, password = auth.split(':', 1)
            
            if ':' in rest:
                host, port_str = rest.rsplit(':', 1)
                port = int(port_str)
            else:
                return None
            
            return ProxyInfo(
                host=host,
                port=port,
                protocol=protocol,
                username=username,
                password=password
            )
        except Exception as e:
            logger.error(f"Failed to parse proxy: {proxy_str} - {e}")
            return None
    
    def get_current_proxy(self) -> Optional[ProxyInfo]:
        """Get current proxy for use"""
        if not self.use_proxies or not self.proxies:
            return None
        
        with self.lock:
            # Find a proxy that's not banned and cooled down
            for _ in range(len(self.proxies)):
                proxy = self.proxies[self.current_proxy_index]
                
                # Check if proxy is banned
                if proxy.is_banned:
                    self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
                    continue
                
                # Check cooldown period
                if proxy.last_used:
                    cooldown = timedelta(minutes=self.proxy_cooldown_minutes)
                    if datetime.now() - proxy.last_used < cooldown:
                        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
                        continue
                
                # This proxy is good to use
                proxy.last_used = datetime.now()
                return proxy
            
            # All proxies are banned or on cooldown
            logger.warning("⚠️ All proxies banned or on cooldown!")
            return None
    
    def rotate_proxy(self, force: bool = False):
        """Rotate to next proxy"""
        if not self.use_proxies or not self.proxies:
            return
        
        with self.lock:
            old_index = self.current_proxy_index
            self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
            self.requests_with_current_proxy = 0
            
            logger.info(f"🔄 Rotated proxy: #{old_index} → #{self.current_proxy_index}")
    
    def mark_proxy_failed(self, proxy: ProxyInfo):
        """Mark proxy as failed"""
        if proxy:
            proxy.fail_count += 1
            self.consecutive_failures += 1
            
            # Ban proxy if too many failures
            if proxy.fail_count >= 5:
                proxy.is_banned = True
                logger.warning(f"🚫 Proxy banned: {proxy.get_proxy_string()}")
            
            # Rotate if too many consecutive failures
            if self.consecutive_failures >= self.max_failures_before_rotation:
                self.rotate_proxy(force=True)
                self.consecutive_failures = 0
    
    def mark_proxy_success(self, proxy: ProxyInfo):
        """Mark proxy as successful"""
        if proxy:
            proxy.success_count += 1
            self.consecutive_failures = 0
    
    def wait_if_needed(self) -> float:
        """
        Intelligent delay calculation and enforcement
        Returns the actual delay time used
        """
        if not self.enabled:
            return 0.0
        
        with self.lock:
            now = datetime.now()
            delay = 0.0
            
            # 1. Check rate limit (requests per minute)
            one_minute_ago = now - timedelta(minutes=1)
            self.request_times = [t for t in self.request_times if t > one_minute_ago]
            
            if len(self.request_times) >= self.max_requests_per_minute:
                # Wait until we can make another request
                oldest = self.request_times[0]
                wait_until = oldest + timedelta(minutes=1)
                wait_seconds = (wait_until - now).total_seconds()
                if wait_seconds > 0:
                    logger.info(f"⏸️ Rate limit reached, waiting {wait_seconds:.1f}s")
                    time.sleep(wait_seconds)
                    delay += wait_seconds
            
            # 2. Enforce minimum delay between requests
            if self.last_request_time:
                time_since_last = (now - self.last_request_time).total_seconds()
                
                if self.random_delay:
                    # Random delay between min and max
                    required_delay = random.uniform(
                        self.min_delay_between_requests,
                        self.max_delay_between_requests
                    )
                else:
                    required_delay = self.min_delay_between_requests
                
                if time_since_last < required_delay:
                    wait_time = required_delay - time_since_last
                    time.sleep(wait_time)
                    delay += wait_time
            
            # 3. Record this request
            self.request_times.append(datetime.now())
            self.last_request_time = datetime.now()
            self.total_requests += 1
            self.requests_with_current_proxy += 1
            
            # 4. Check if we should rotate proxy
            if self.use_proxies and self.requests_with_current_proxy >= self.rotate_after_requests:
                self.rotate_proxy()
            
            return delay
    
    def add_random_human_delay(self):
        """Add random human-like delay (2-7 seconds)"""
        if self.enabled:
            delay = random.uniform(2.0, 7.0)
            time.sleep(delay)
            logger.debug(f"🧑 Human-like delay: {delay:.1f}s")
    
    def get_stats(self) -> Dict:
        """Get anti-ban statistics"""
        with self.lock:
            active_proxies = sum(1 for p in self.proxies if not p.is_banned)
            
            return {
                'enabled': self.enabled,
                'total_requests': self.total_requests,
                'requests_this_minute': len(self.request_times),
                'max_rpm': self.max_requests_per_minute,
                'use_proxies': self.use_proxies,
                'total_proxies': len(self.proxies),
                'active_proxies': active_proxies,
                'current_proxy_index': self.current_proxy_index if self.use_proxies else None,
                'requests_with_current_proxy': self.requests_with_current_proxy
            }
    
    def reset_stats(self):
        """Reset statistics"""
        with self.lock:
            self.request_times.clear()
            self.total_requests = 0
            self.requests_with_current_proxy = 0
            self.consecutive_failures = 0
            logger.info("📊 Anti-Ban statistics reset")


# Global instance
anti_ban = AntiBanSystem()


def create_sample_proxy_file():
    """Create a sample proxies.txt file"""
    sample_content = """# MEGA Checker Proxy List
# Format: protocol://host:port or protocol://user:pass@host:port
# Supported protocols: http, https, socks5

# Example proxies (replace with your own):
# http://proxy1.example.com:8080
# http://user:pass@proxy2.example.com:3128
# socks5://proxy3.example.com:1080

# Free proxy lists (use at your own risk):
# https://www.proxy-list.download/
# https://www.proxyscrape.com/
# https://free-proxy-list.net/

# Premium proxy services (recommended):
# - Bright Data (formerly Luminati)
# - Smartproxy
# - Oxylabs
# - ProxyMesh
"""
    
    try:
        with open('proxies.txt', 'w', encoding='utf-8') as f:
            f.write(sample_content)
        logger.info("✅ Created sample proxies.txt file")
    except Exception as e:
        logger.error(f"Error creating sample file: {e}")


if __name__ == "__main__":
    # Test the anti-ban system
    print("🛡️ Testing Anti-Ban System\n")
    
    # Enable anti-ban
    anti_ban.enable(max_rpm=30, min_delay=2.0, max_delay=5.0)
    
    # Test delays
    print("Testing rate limiting...")
    for i in range(5):
        delay = anti_ban.wait_if_needed()
        print(f"Request {i+1}: waited {delay:.2f}s")
    
    # Test proxy loading
    create_sample_proxy_file()
    
    print("\n📊 Statistics:")
    stats = anti_ban.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
