class RSARTException(Exception):
    """Base exception for RSART application"""
    pass

class ResumeParsingError(RSARTException):
    """Exception raised when resume parsing fails"""
    pass

class MatchingServiceError(RSARTException):
    """Exception raised when matching service fails"""
    pass

class FileServiceError(RSARTException):
    """Exception raised when file operations fail"""
    pass

class AuthenticationError(RSARTException):
    """Exception raised when authentication fails"""
    pass

class ValidationError(RSARTException):
    """Exception raised when validation fails"""
    pass