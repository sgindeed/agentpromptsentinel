"""Custom exceptions for the agentbastion library."""

class BastionError(Exception):
    """Base exception for all agentbastion errors."""
    pass

class InjectionDetectedError(BastionError):
    """Raised when a prompt injection attack is detected by a scanner."""
    def __init__(self, message: str, scanner_name: str) -> None:
        super().__init__(f"[{scanner_name}] {message}")
        self.scanner_name = scanner_name

class ScannerTimeoutError(BastionError):
    """Raised when an asynchronous scanner exceeds its execution time limit."""
    pass
