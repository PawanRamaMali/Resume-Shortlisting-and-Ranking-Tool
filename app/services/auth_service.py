import hashlib
import secrets
from typing import Optional, Dict, Any
import logging
from app.utils.exceptions import AuthenticationError

logger = logging.getLogger(__name__)

class AuthService:
    """Service for handling authentication"""
    
    def __init__(self):
        # In production, these should be stored in database with proper hashing
        self.users = {
            'admin': {
                'password_hash': self._hash_password('root'),
                'role': 'admin',
                'active': True
            }
        }
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user credentials"""
        try:
            user = self.users.get(username)
            if not user:
                raise AuthenticationError("Invalid username or password")
            
            if not user['active']:
                raise AuthenticationError("Account is deactivated")
            
            if not self._verify_password(password, user['password_hash']):
                raise AuthenticationError("Invalid username or password")
            
            logger.info(f"User authenticated successfully: {username}")
            return {
                'username': username,
                'role': user['role'],
                'authenticated': True
            }
            
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Authentication error for user {username}: {e}")
            raise AuthenticationError("Authentication failed")
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', 
                                          password.encode('utf-8'), 
                                          salt.encode('utf-8'), 
                                          100000)
        return f"{salt}:{password_hash.hex()}"
    
    def _verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        try:
            salt, hash_hex = stored_hash.split(':')
            password_hash = hashlib.pbkdf2_hmac('sha256',
                                              password.encode('utf-8'),
                                              salt.encode('utf-8'),
                                              100000)
            return password_hash.hex() == hash_hex
        except Exception:
            return False