"""The main pipeline engine for agentpromptsentinel."""

import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field

from .exceptions import InjectionDetectedError, ScannerTimeoutError
from .scanners.base import BaseScanner

class BastionConfig(BaseModel):
    """Configuration for the Sentinel/Bastion pipeline."""
    timeout_per_scanner_seconds: float = Field(default=5.0, ge=0.1)
    fail_fast: bool = Field(default=True, description="Stop at the first detected injection.")
    fail_closed: bool = Field(default=True, description="Treat scanner timeouts or unhandled failures as an injection.")

class Bastion:
    """
    Main evaluation engine that processes inputs through a pipeline of scanners.
    
    Uses the Strategy Pattern to execute a series of BaseScanner implementations.
    """
    
    def __init__(self, scanners: List[BaseScanner], config: Optional[BastionConfig] = None) -> None:
        self.scanners = scanners
        self.config = config or BastionConfig()
        
    async def evaluate_async(self, prompt: str) -> None:
        detected_issues = []
        for scanner in self.scanners:
            try:
                reason = await asyncio.wait_for(
                    scanner.scan(prompt),
                    timeout=self.config.timeout_per_scanner_seconds
                )
                if reason:
                    if self.config.fail_fast:
                        raise InjectionDetectedError(message=reason, scanner_name=scanner.name)
                    detected_issues.append(f"[{scanner.name}] {reason}")
            except Exception as e:
                # Handle timeouts and arbitrary Hugging Face crashes
                is_timeout = isinstance(e, asyncio.TimeoutError)
                if self.config.fail_closed:
                    if self.config.fail_fast:
                        if is_timeout:
                            raise ScannerTimeoutError(f"Scanner '{scanner.name}' timed out.") from e
                        raise InjectionDetectedError(message=f"Crash: {e}", scanner_name=scanner.name) from e
                    detected_issues.append(f"[{scanner.name}] {'TIMEOUT' if is_timeout else 'ERROR'}")
                
        # If fail_fast is False, aggregate and raise at the end
        if detected_issues and not self.config.fail_fast:
            raise InjectionDetectedError(message=" | ".join(detected_issues), scanner_name="Multiple")\
            
                        
    def evaluate(self, prompt: str) -> None:
        """
        Synchronous wrapper for evaluate_async.
        
        Args:
            prompt: The text string to scan.
        """
        asyncio.run(self.evaluate_async(prompt))