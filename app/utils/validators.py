from pathlib import Path
from typing import Optional
import re
from app.utils.exceptions import ValidationError

class FileValidator:
    """Validator for file uploads"""
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
        """Validate file extension"""
        if not filename or '.' not in filename:
            return False
        
        extension = filename.rsplit('.', 1)[1].lower()
        return extension in allowed_extensions
    
    @staticmethod
    def validate_file_size(file, max_size: int) -> bool:
        """Validate file size"""
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to beginning
        return size <= max_size
    
    @staticmethod
    def validate_filename(filename: str) -> bool:
        """Validate filename format"""
        if not filename:
            return False
        
        # Check for dangerous characters
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        return not any(char in filename for char in dangerous_chars)

class TextValidator:
    """Validator for text content"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format"""
        if not phone:
            return False
        
        # Remove common separators
        cleaned = re.sub(r'[-()\s+]', '', phone)
        
        # Check if it's all digits and reasonable length
        return cleaned.isdigit() and 10 <= len(cleaned) <= 15
