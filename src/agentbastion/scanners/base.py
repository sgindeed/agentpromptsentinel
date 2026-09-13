"""Abstract base classes for scanners."""

import abc
from typing import Optional

class BaseScanner(abc.ABC):
    """Base class that all scanners must inherit from."""
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The name of the scanner."""
        pass
        
    @abc.abstractmethod
    async def scan(self, prompt: str) -> Optional[str]:
        """
        Scan a prompt for malicious content.
        
        Args:
            prompt: The text prompt to evaluate.
            
        Returns:
            A string containing the reason if an injection is detected, otherwise None.
            
        Raises:
            ScannerTimeoutError: If the scanner times out.
        """
        pass