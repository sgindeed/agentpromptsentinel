"""
promptsentinel - Detect, block, and sanitize prompt injection attacks.
"""

from .core import Bastion, BastionConfig
from .exceptions import BastionError, InjectionDetectedError, ScannerTimeoutError

__version__ = "0.1.0"
__all__ = [
    "Bastion", 
    "BastionConfig", 
    "BastionError", 
    "InjectionDetectedError", 
    "ScannerTimeoutError"
]