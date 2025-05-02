import time
from datetime import datetime

class DebugPrint:
    """
    Utility for printing styled debug messages to the console.
    Provides colored output for different message types.
    """
    COLORS = {
        'RESET': '\033[0m',
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
    }
    
    enabled = True  # Enable or disable debug printing
    
    @classmethod
    def info(cls, message):
        """Print an informational debug message."""
        if cls.enabled:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"{cls.COLORS['BLUE']}DEBUG [{timestamp}]: {message}{cls.COLORS['RESET']}")
    
    @classmethod
    def warning(cls, message):
        """Print a warning debug message."""
        if cls.enabled:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"{cls.COLORS['YELLOW']}DEBUG [{timestamp}]: {message}{cls.COLORS['RESET']}")
    
    @classmethod
    def error(cls, message):
        """Print an error debug message."""
        if cls.enabled:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"{cls.COLORS['RED']}DEBUG [{timestamp}]: {message}{cls.COLORS['RESET']}")
    
    @classmethod
    def success(cls, message):
        """Print a success debug message."""
        if cls.enabled:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"{cls.COLORS['GREEN']}DEBUG [{timestamp}]: {message}{cls.COLORS['RESET']}")
    
    @classmethod
    def process(cls, message):
        """Print a process-related debug message."""
        if cls.enabled:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"{cls.COLORS['PURPLE']}DEBUG [{timestamp}]: {message}{cls.COLORS['RESET']}")
    
    @classmethod
    def database(cls, message):
        """Print a database operation debug message."""
        if cls.enabled:
            timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            print(f"{cls.COLORS['CYAN']}DEBUG [{timestamp}]: {message}{cls.COLORS['RESET']}")
