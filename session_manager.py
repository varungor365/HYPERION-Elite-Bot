"""
Session Management System
Allows users to save and resume checking sessions
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CheckingSession:
    """Data class for a checking session"""
    session_id: str
    created_at: str
    last_updated: str
    combo_file: str
    total_accounts: int
    checked_count: int
    hit_count: int
    fail_count: int
    custom_count: int
    current_position: int
    settings: Dict
    status: str  # 'active', 'paused', 'completed'
    hits_file: Optional[str] = None
    description: Optional[str] = None


class SessionManager:
    """Manages saving and loading checking sessions"""
    
    def __init__(self, sessions_dir: str = "sessions"):
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.current_session: Optional[CheckingSession] = None
        
    def create_session(self, combo_file: str, total_accounts: int, 
                      settings: Dict, description: str = "") -> CheckingSession:
        """
        Create a new checking session
        
        Args:
            combo_file: Path to combo file
            total_accounts: Total number of accounts
            settings: Dictionary of checker settings
            description: Optional description
            
        Returns:
            CheckingSession object
        """
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp = datetime.now().isoformat()
        
        session = CheckingSession(
            session_id=session_id,
            created_at=timestamp,
            last_updated=timestamp,
            combo_file=combo_file,
            total_accounts=total_accounts,
            checked_count=0,
            hit_count=0,
            fail_count=0,
            custom_count=0,
            current_position=0,
            settings=settings,
            status='active',
            description=description
        )
        
        self.current_session = session
        self.save_session(session)
        
        logger.info(f"✓ Created session: {session_id}")
        return session
    
    def save_session(self, session: Optional[CheckingSession] = None) -> bool:
        """
        Save session to file
        
        Args:
            session: Session to save (uses current_session if None)
            
        Returns:
            True if successful
        """
        if session is None:
            session = self.current_session
        
        if session is None:
            logger.warning("No session to save")
            return False
        
        try:
            session.last_updated = datetime.now().isoformat()
            
            session_file = self.sessions_dir / f"{session.session_id}.json"
            with open(session_file, 'w') as f:
                json.dump(asdict(session), f, indent=2)
            
            logger.debug(f"✓ Saved session: {session.session_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to save session: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[CheckingSession]:
        """
        Load a session from file
        
        Args:
            session_id: ID of session to load
            
        Returns:
            CheckingSession object or None if not found
        """
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            logger.warning(f"Session not found: {session_id}")
            return None
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            session = CheckingSession(**session_data)
            self.current_session = session
            
            logger.info(f"✓ Loaded session: {session_id}")
            return session
        except Exception as e:
            logger.error(f"✗ Failed to load session: {e}")
            return None
    
    def update_session_progress(self, checked: int, hits: int, fails: int, 
                               customs: int, position: int) -> bool:
        """Update current session progress"""
        if not self.current_session:
            return False
        
        self.current_session.checked_count = checked
        self.current_session.hit_count = hits
        self.current_session.fail_count = fails
        self.current_session.custom_count = customs
        self.current_session.current_position = position
        
        return self.save_session()
    
    def pause_session(self) -> bool:
        """Pause the current session"""
        if not self.current_session:
            return False
        
        self.current_session.status = 'paused'
        logger.info(f"⏸ Paused session: {self.current_session.session_id}")
        return self.save_session()
    
    def resume_session(self, session_id: str) -> Optional[CheckingSession]:
        """Resume a paused session"""
        session = self.load_session(session_id)
        if session and session.status == 'paused':
            session.status = 'active'
            self.save_session(session)
            logger.info(f"▶ Resumed session: {session_id}")
            return session
        return None
    
    def complete_session(self) -> bool:
        """Mark current session as completed"""
        if not self.current_session:
            return False
        
        self.current_session.status = 'completed'
        logger.info(f"✓ Completed session: {self.current_session.session_id}")
        return self.save_session()
    
    def list_sessions(self, status_filter: Optional[str] = None) -> List[CheckingSession]:
        """
        List all sessions
        
        Args:
            status_filter: Filter by status ('active', 'paused', 'completed')
            
        Returns:
            List of CheckingSession objects
        """
        sessions = []
        
        for session_file in self.sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                session = CheckingSession(**session_data)
                
                if status_filter is None or session.status == status_filter:
                    sessions.append(session)
                    
            except Exception as e:
                logger.error(f"✗ Failed to load session {session_file.name}: {e}")
        
        # Sort by last updated (newest first)
        sessions.sort(key=lambda s: s.last_updated, reverse=True)
        return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session
        
        Args:
            session_id: ID of session to delete
            
        Returns:
            True if successful
        """
        session_file = self.sessions_dir / f"{session_id}.json"
        
        if not session_file.exists():
            logger.warning(f"Session not found: {session_id}")
            return False
        
        try:
            session_file.unlink()
            logger.info(f"✓ Deleted session: {session_id}")
            
            if self.current_session and self.current_session.session_id == session_id:
                self.current_session = None
            
            return True
        except Exception as e:
            logger.error(f"✗ Failed to delete session: {e}")
            return False
    
    def get_session_stats(self, session: Optional[CheckingSession] = None) -> Dict:
        """Get statistics for a session"""
        if session is None:
            session = self.current_session
        
        if session is None:
            return {}
        
        progress_percent = (session.checked_count / session.total_accounts * 100) if session.total_accounts > 0 else 0
        remaining = session.total_accounts - session.checked_count
        
        return {
            'progress': f"{progress_percent:.1f}%",
            'checked': session.checked_count,
            'total': session.total_accounts,
            'remaining': remaining,
            'hits': session.hit_count,
            'fails': session.fail_count,
            'customs': session.custom_count,
            'hit_rate': f"{(session.hit_count / session.checked_count * 100):.2f}%" if session.checked_count > 0 else "0%"
        }
    
    def export_session_report(self, session_id: str, output_file: str) -> bool:
        """Export session data to a readable report"""
        session = self.load_session(session_id)
        if not session:
            return False
        
        try:
            stats = self.get_session_stats(session)
            
            report = f"""
╔═══════════════════════════════════════════════════════════════╗
║           MEGA CHECKER - SESSION REPORT                       ║
╚═══════════════════════════════════════════════════════════════╝

Session ID: {session.session_id}
Status: {session.status.upper()}
Description: {session.description or 'No description'}

Created: {session.created_at}
Last Updated: {session.last_updated}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        PROGRESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checked: {session.checked_count} / {session.total_accounts} ({stats['progress']})
Remaining: {stats['remaining']} accounts
Current Position: {session.current_position}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Hits: {session.hit_count}
✗ Fails: {session.fail_count}
⚡ Customs: {session.custom_count}
📊 Hit Rate: {stats['hit_rate']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                        SETTINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Combo File: {session.combo_file}
"""
            
            for key, value in session.settings.items():
                report += f"{key}: {value}\n"
            
            report += "\n" + "="*63 + "\n"
            
            with open(output_file, 'w') as f:
                f.write(report)
            
            logger.info(f"✓ Exported report to: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to export report: {e}")
            return False


# Global session manager instance
session_manager = SessionManager()


if __name__ == "__main__":
    """Test the session manager"""
    print("💾 MEGA Checker - Session Manager Test\n")
    
    # Create a test session
    settings = {
        'rate_limit': 20,
        'min_delay': 2.0,
        'max_delay': 5.0,
        'use_proxy': True
    }
    
    session = session_manager.create_session(
        combo_file="test_combo.txt",
        total_accounts=1000,
        settings=settings,
        description="Test session for demo"
    )
    
    print(f"✓ Created session: {session.session_id}\n")
    
    # Simulate progress
    session_manager.update_session_progress(
        checked=250,
        hits=15,
        fails=235,
        customs=0,
        position=250
    )
    
    print("✓ Updated progress\n")
    
    # Pause session
    session_manager.pause_session()
    print(f"⏸ Paused session\n")
    
    # List all sessions
    all_sessions = session_manager.list_sessions()
    print(f"📋 Found {len(all_sessions)} session(s):\n")
    
    for s in all_sessions:
        stats = session_manager.get_session_stats(s)
        print(f"  {s.session_id} - {s.status}")
        print(f"    Progress: {stats['progress']}")
        print(f"    Hits: {stats['hits']} | Fails: {stats['fails']}")
        print()
    
    # Export report
    if all_sessions:
        report_file = f"session_report_{session.session_id}.txt"
        session_manager.export_session_report(session.session_id, report_file)
        print(f"✓ Exported report to: {report_file}")
