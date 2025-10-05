"""
MEGA.nz Authentication Module
Handles login, storage checking, and account validation
"""

from mega import Mega
from typing import Dict, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MegaAuthenticator:
    """Handles MEGA.nz account authentication and data retrieval"""
    
    def __init__(self):
        self.mega = Mega()
    
    def login(self, email: str, password: str, proxy: Optional[str] = None) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Attempt to login to MEGA account
        
        Args:
            email: Account email
            password: Account password
            proxy: Optional proxy URL (format: protocol://[user:pass@]host:port)
            
        Returns:
            Tuple of (success, account_data, error_message)
        """
        try:
            # Create MEGA instance with proxy if provided
            if proxy:
                # Note: mega.py library may not natively support proxies
                # This will depend on the underlying requests library
                # If proxies don't work, consider using requests with proxies directly
                mega_instance = Mega()
                try:
                    # Try to set proxy in session if available
                    if hasattr(mega_instance, 'session'):
                        mega_instance.session.proxies = {
                            'http': proxy,
                            'https': proxy
                        }
                except Exception as proxy_error:
                    logger.warning(f"Could not set proxy: {proxy_error}")
                m = mega_instance.login(email, password)
            else:
                # Attempt login without proxy
                m = self.mega.login(email, password)
            
            # Get storage information
            storage = m.get_storage_space(giga=True)
            used_space = round(storage.get("used", 0), 2)
            total_space = storage.get("total", 0)
            
            # Get files information
            files = m.get_files()
            
            # Get detailed file and folder counts
            detailed_counts = self.get_detailed_file_counts(files)
            
            # Get recovery key (master key)
            recovery_key = self.get_recovery_key(m)
            
            # Get user information
            user_info = self.get_user_info(m)
            
            # Prepare account data
            account_data = {
                "email": email,
                "password": password,
                "used_space": used_space,
                "total_space": total_space,
                "file_count": detailed_counts['files'],
                "folder_count": detailed_counts['folders'],
                "recovery_key": recovery_key,
                "user_info": user_info,
                "files": files,
                "mega_instance": m
            }
            
            return True, account_data, None
            
        except Exception as e:
            error_msg = str(e)
            
            # Categorize errors
            if "User blocked" in error_msg or "blocked" in error_msg.lower():
                return False, None, "BLOCKED"
            elif "ENOENT" in error_msg or "does not exist" in error_msg:
                return False, None, "INVALID"
            elif "password" in error_msg.lower() or "credentials" in error_msg.lower():
                return False, None, "INVALID"
            else:
                return False, None, f"ERROR: {error_msg}"
    
    def search_files(self, files: Dict, keyword: str) -> bool:
        """
        Search for keyword in file names
        
        Args:
            files: Dictionary of files from MEGA
            keyword: Keyword to search for
            
        Returns:
            True if keyword found, False otherwise
        """
        if not keyword:
            return False
        
        try:
            keyword_lower = keyword.lower()
            files_str = str(files).lower()
            
            # Search in files dictionary
            if keyword_lower in files_str:
                return True
            
            # Search in individual file names
            for file_id, file_info in files.items():
                if isinstance(file_info, dict):
                    file_name = file_info.get('a', {}).get('n', '').lower()
                    if keyword_lower in file_name:
                        return True
            
            return False
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return False
    
    def get_account_details(self, mega_instance) -> Dict:
        """
        Get detailed account information
        
        Args:
            mega_instance: Logged in MEGA instance
            
        Returns:
            Dictionary with account details
        """
        try:
            user_info = mega_instance.get_user()
            storage = mega_instance.get_storage_space(giga=True)
            
            return {
                "user_info": user_info,
                "storage": storage
            }
        except Exception as e:
            logger.error(f"Error getting account details: {e}")
            return {}
    
    def get_recovery_key(self, mega_instance) -> str:
        """
        Extract recovery key (master key) from MEGA account
        
        Args:
            mega_instance: Logged in MEGA instance
            
        Returns:
            Recovery key string or 'N/A' if unavailable
        """
        try:
            # Try to get the master key (recovery key)
            # This requires access to the MEGA session data
            if hasattr(mega_instance, 'master_key'):
                master_key = mega_instance.master_key
                if master_key:
                    # Convert to base64 format if needed
                    import base64
                    if isinstance(master_key, bytes):
                        return base64.b64encode(master_key).decode('utf-8')
                    return str(master_key)
            
            # Alternative method: try to access session data
            if hasattr(mega_instance, '_get_session_key'):
                session_key = mega_instance._get_session_key()
                if session_key:
                    return session_key
            
            # If direct access fails, try to get from user data
            user_data = mega_instance.get_user()
            if user_data and 'k' in user_data:
                return user_data['k']
                
            return "N/A"
        except Exception as e:
            logger.warning(f"Could not extract recovery key: {e}")
            return "N/A"
    
    def get_user_info(self, mega_instance) -> dict:
        """
        Get detailed user information
        
        Args:
            mega_instance: Logged in MEGA instance
            
        Returns:
            Dictionary with user information
        """
        try:
            user_data = mega_instance.get_user()
            return {
                'user_handle': user_data.get('u', 'N/A'),
                'email': user_data.get('m', 'N/A'),
                'created': user_data.get('ts', 'N/A'),
                'country': user_data.get('c', 'N/A')
            }
        except Exception as e:
            logger.warning(f"Could not get user info: {e}")
            return {'user_handle': 'N/A', 'email': 'N/A', 'created': 'N/A', 'country': 'N/A'}
    
    def get_detailed_file_counts(self, files: dict) -> dict:
        """
        Get accurate file and folder counts
        
        Args:
            files: Files dictionary from MEGA
            
        Returns:
            Dictionary with file and folder counts
        """
        try:
            file_count = 0
            folder_count = 0
            
            for file_id, file_data in files.items():
                if isinstance(file_data, dict):
                    file_type = file_data.get('t')
                    if file_type == 1:  # Folder
                        folder_count += 1
                    elif file_type == 0:  # File
                        file_count += 1
            
            return {
                'files': file_count,
                'folders': folder_count
            }
        except Exception as e:
            logger.error(f"Error counting files: {e}")
            return {'files': 0, 'folders': 0}
    
    def get_account_type(self, used_space: float, total_space: float, file_count: int) -> str:
        """
        Determine account type (Pro/Free/Empty)
        
        Args:
            used_space: Used storage in GB
            total_space: Total storage in GB
            file_count: Number of files
            
        Returns:
            Account type string
        """
        # Empty account detection
        if file_count == 0 or used_space < 0.01:
            return "Empty"
        
        # Pro account detection (more than 50GB = Pro)
        if total_space > 50:
            if total_space <= 400:
                return "Pro Lite"
            elif total_space <= 2000:
                return "Pro I"
            elif total_space <= 8000:
                return "Pro II"
            else:
                return "Pro III"
        
        # Free account
        return "Free"
    
    def deep_check(self, mega_instance) -> Dict:
        """
        Perform deep check to get all files and folders
        
        Args:
            mega_instance: Logged in MEGA instance
            
        Returns:
            Dictionary with detailed file and folder structure
        """
        try:
            files = mega_instance.get_files()
            
            folder_count = 0
            file_count = 0
            file_list = []
            folder_list = []
            
            # Handle both dict and other formats
            if not isinstance(files, dict):
                logger.warning(f"Files data is not dict format: {type(files)}")
                return {
                    'total_files': 0,
                    'total_folders': 0,
                    'file_list': [],
                    'folder_list': [],
                    'success': False,
                    'error': 'Files data format not supported'
                }
            
            for file_id, file_data in files.items():
                if isinstance(file_data, dict):
                    attrs = file_data.get('a', {})
                    file_type = file_data.get('t')
                    
                    # Ensure attrs is a dict
                    if not isinstance(attrs, dict):
                        continue
                        
                    if file_type == 1:  # Folder
                        folder_count += 1
                        folder_name = attrs.get('n', 'Unknown')
                        folder_list.append(folder_name)
                    elif file_type == 0:  # File
                        file_count += 1
                        file_name = attrs.get('n', 'Unknown')
                        file_size = file_data.get('s', 0)
                        file_list.append({
                            'name': file_name,
                            'size': file_size
                        })
            
            return {
                'total_files': file_count,
                'total_folders': folder_count,
                'file_list': file_list,
                'folder_list': folder_list,
                'success': True
            }
        except Exception as e:
            logger.error(f"Error in deep check: {e}")
            return {
                'total_files': 0,
                'total_folders': 0,
                'file_list': [],
                'folder_list': [],
                'success': False,
                'error': str(e)
            }
