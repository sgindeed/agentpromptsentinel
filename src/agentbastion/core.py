"""The main pipeline engine for promptsentinel."""

import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field

from .exceptions import InjectionDetectedError, ScannerTimeoutError
from .scanners.base import BaseScanner

class BastionConfig(BaseModel):
    """Configuration for the Bastion pipeline."""
    timeout_per_scanner_seconds: float = Field(default=5.0, ge=0.1)
    fail_fast: bool = Field(default=True, description="Stop at the first detected injection.")

class Bastion:
    """
    Main evaluation engine that processes inputs through a pipeline of scanners.
    
    Uses the Strategy Pattern to execute a series of BaseScanner implementations.
    """
    
    def __init__(self, scanners: List[BaseScanner], config: Optional[BastionConfig] = None) -> None:
        """
        Initialize the Bastion engine.
        
        Args:
            scanners: A list of instantiated scanners to run.
            config: Configuration object for pipeline behavior.
        """
        self.scanners = scanners
        self.config = config or BastionConfig()
        
    async def evaluate_async(self, prompt: str) -> None:
        """
        Asynchronously evaluate a prompt through all configured scanners.
        
        Args:
            prompt: The text string to scan.
            
        Raises:
            InjectionDetectedError: If any scanner flags the prompt.
            ScannerTimeoutError: If a scanner exceeds the time limit.
        """
        for scanner in self.scanners:
            try:
                # Use asyncio.wait_for to enforce scanner timeouts
                reason = await asyncio.wait_for(
                    scanner.scan(prompt),
                    timeout=self.config.timeout_per_scanner_seconds
                )
                
                if reason:
                    raise InjectionDetectedError(message=reason, scanner_name=scanner.name)
                    
            except asyncio.TimeoutError as e:
                raise ScannerTimeoutError(
                    f"Scanner '{scanner.name}' exceeded timeout of {self.config.timeout_per_scanner_seconds}s"
                ) from e
                
    def evaluate(self, prompt: str) -> None:
        """
        Synchronous wrapper for evaluate_async.
        
        Args:
            prompt: The text string to scan.
            
        Raises:
            InjectionDetectedError: If any scanner flags the prompt.
            ScannerTimeoutError: If a scanner exceeds the time limit.
        """
        asyncio.run(self.evaluate_async(prompt))