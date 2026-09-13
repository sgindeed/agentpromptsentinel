"""Tier 3: Transformer-based Semantic Evaluator."""

import asyncio
from typing import Optional
from .base import BaseScanner

class TransformerScanner(BaseScanner):
    """Scanner using a Hugging Face transformer to detect complex injections."""
    
    def __init__(
        self, 
        model_name: str = "ProtectAI/deberta-v3-base-prompt-injection-v2",
        threshold: float = 0.35  # Lowered threshold to catch subtle roleplays
    ) -> None:
        """Initialize the scanner and download/load the model."""
        self.threshold = threshold
        print(f"🔄 Initializing TransformerScanner...")
        print(f"⏳ Loading/Downloading model '{model_name}' (this may take a few minutes on the first run)...")
        
        try:
            from transformers import pipeline
        except ImportError:
            raise ImportError("Please install transformers and torch: pip install transformers torch")
            
        # Load the classification pipeline
        self.classifier = pipeline(
            "text-classification", 
            model=model_name,
            truncation=True,
            max_length=512
        )
        print("✅ Transformer model loaded successfully!")
        
    @property
    def name(self) -> str:
        return "TransformerScanner"
        
    async def scan(self, prompt: str) -> Optional[str]:
        """Evaluate the prompt using the transformer model."""
        result = await asyncio.to_thread(self.classifier, prompt)
        
        prediction = result[0]
        if prediction['label'] == 'INJECTION' and prediction['score'] >= self.threshold:
            return f"Transformer detected malicious intent (confidence: {prediction['score']:.2f})"
            
        return None