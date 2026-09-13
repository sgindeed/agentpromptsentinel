"""
agentpromptsentinel - Detect, block, and sanitize prompt injection attacks.
"""

from .core import Bastion, BastionConfig
from .exceptions import BastionError, InjectionDetectedError, ScannerTimeoutError

# Alias for library branding
Sentinel = Bastion
SentinelConfig = BastionConfig

__version__ = "0.1.2"
__all__ = [
    "Bastion", 
    "BastionConfig",
    "Sentinel",
    "SentinelConfig",
    "BastionError", 
    "InjectionDetectedError", 
    "ScannerTimeoutError"
]