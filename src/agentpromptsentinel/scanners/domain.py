"""Tier 4: Custom Domain Guardrail (Zero-Shot Topic Scanner)."""

import asyncio
from typing import List, Optional
from .base import BaseScanner

class DomainScanner(BaseScanner):
    """Ensures prompts stay within user-defined allowed topics."""
    
    def __init__(
        self, 
        allowed_topics: List[str],
        model_name: str = "facebook/bart-large-mnli",
        threshold: float = 0.45
    ) -> None:
        self.allowed_topics = allowed_topics
        self.threshold = threshold
        
        print(f"🔄 Initializing DomainScanner...")
        try:
            from transformers import pipeline
        except ImportError:
            raise ImportError("Please install transformers and torch")
            
        self.classifier = pipeline(
            "zero-shot-classification", 
            model=model_name
        )
        print("✅ Domain classification model loaded!")
        
    @property
    def name(self) -> str:
        return "DomainScanner"
        
    async def scan(self, prompt: str) -> Optional[str]:
        result = await asyncio.to_thread(
            self.classifier, 
            prompt, 
            self.allowed_topics, 
            multi_label=True
        )
        
        best_score = result['scores'][0]
        if best_score < self.threshold:
            return f"Prompt is off-topic. Must be related to: {', '.join(self.allowed_topics)}"
            
        return None