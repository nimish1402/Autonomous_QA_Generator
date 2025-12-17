"""
LLM Integration Configuration for Autonomous QA Agent

This module provides configuration and integration options for various LLM providers.
Supports OpenAI, Anthropic, local models, and template-based fallback.
"""

import os
from typing import Dict, Any, Optional
from enum import Enum

class LLMProvider(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL_OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    TEMPLATE_BASED = "template"  # Fallback option

class LLMConfig:
    """Configuration class for LLM integration."""
    
    def __init__(self):
        # Try to detect available LLM configurations
        self.provider = self._detect_provider()
        self.config = self._load_config()
    
    def _detect_provider(self) -> LLMProvider:
        """Auto-detect which LLM provider to use based on available API keys."""
        
        # Check for Gemini API key first
        if os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'):
            return LLMProvider.GEMINI
        
        # Check for OpenAI API key
        if os.getenv('OPENAI_API_KEY'):
            return LLMProvider.OPENAI
        
        # Check for Anthropic API key
        if os.getenv('ANTHROPIC_API_KEY'):
            return LLMProvider.ANTHROPIC
        
        # Check for local Ollama installation
        try:
            import requests
            response = requests.get('http://localhost:11434/api/tags', timeout=2)
            if response.status_code == 200:
                return LLMProvider.LOCAL_OLLAMA
        except:
            pass
        
        # Check for HuggingFace token
        if os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HF_TOKEN'):
            return LLMProvider.HUGGINGFACE
        
        # Fallback to template-based
        return LLMProvider.TEMPLATE_BASED
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration based on detected provider."""
        
        configs = {
            LLMProvider.GEMINI: {
                'api_key': os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'),
                'model': os.getenv('GEMINI_MODEL', 'gemini-flash-latest'),
                'base_url': os.getenv('GEMINI_BASE_URL', 'https://generativelanguage.googleapis.com'),
                'max_tokens': int(os.getenv('GEMINI_MAX_TOKENS', '2000')),
                'temperature': float(os.getenv('GEMINI_TEMPERATURE', '0.1')),
                'safety_settings': os.getenv('GEMINI_SAFETY_SETTINGS', 'default')
            },
            LLMProvider.OPENAI: {
                'api_key': os.getenv('OPENAI_API_KEY'),
                'model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                'base_url': os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
                'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '2000')),
                'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.1'))
            },
            LLMProvider.ANTHROPIC: {
                'api_key': os.getenv('ANTHROPIC_API_KEY'),
                'model': os.getenv('ANTHROPIC_MODEL', 'claude-3-sonnet-20240229'),
                'base_url': os.getenv('ANTHROPIC_BASE_URL', 'https://api.anthropic.com'),
                'max_tokens': int(os.getenv('ANTHROPIC_MAX_TOKENS', '2000')),
                'temperature': float(os.getenv('ANTHROPIC_TEMPERATURE', '0.1'))
            },
            LLMProvider.LOCAL_OLLAMA: {
                'base_url': os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
                'model': os.getenv('OLLAMA_MODEL', 'llama2'),
                'temperature': float(os.getenv('OLLAMA_TEMPERATURE', '0.1'))
            },
            LLMProvider.HUGGINGFACE: {
                'token': os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HF_TOKEN'),
                'model': os.getenv('HF_MODEL', 'microsoft/DialoGPT-medium'),
                'base_url': os.getenv('HF_BASE_URL', 'https://api-inference.huggingface.co'),
                'max_tokens': int(os.getenv('HF_MAX_TOKENS', '1000'))
            },
            LLMProvider.TEMPLATE_BASED: {
                'enabled': True,
                'fallback_message': 'Using template-based generation (no LLM API configured)'
            }
        }
        
        return configs.get(self.provider, configs[LLMProvider.TEMPLATE_BASED])
    
    def is_api_available(self) -> bool:
        """Check if a real LLM API is available."""
        return self.provider != LLMProvider.TEMPLATE_BASED
    
    def get_provider_info(self) -> str:
        """Get human-readable provider information."""
        provider_names = {
            LLMProvider.GEMINI: "Google Gemini",
            LLMProvider.OPENAI: "OpenAI GPT",
            LLMProvider.ANTHROPIC: "Anthropic Claude",
            LLMProvider.LOCAL_OLLAMA: "Local Ollama",
            LLMProvider.HUGGINGFACE: "HuggingFace Inference",
            LLMProvider.TEMPLATE_BASED: "Template-based (No API)"
        }
        return provider_names.get(self.provider, "Unknown")

# Global configuration instance
llm_config = LLMConfig()