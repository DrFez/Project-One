import time
from datetime import datetime

class DebugPrint:
    """
    Utility for printing styled debug messages to the console.
    """
    COLORS = {
        'RESET': '\033[0m',
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
    }
    enabled = True

    @classmethod
    def _print(cls, color, message):
        if not cls.enabled:
            return
        ts = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f"{cls.COLORS[color]}DEBUG [{ts}]: {message}{cls.COLORS['RESET']}")

    @classmethod
    def info(cls, msg):    cls._print('BLUE', msg)
    @classmethod
    def warning(cls, msg): cls._print('YELLOW', msg)
    @classmethod
    def error(cls, msg):   cls._print('RED', msg)
    @classmethod
    def success(cls, msg): cls._print('GREEN', msg)
    @classmethod
    def process(cls, msg): cls._print('PURPLE', msg)
    @classmethod
    def database(cls, msg):cls._print('CYAN', msg)
