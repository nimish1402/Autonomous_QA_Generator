"""
Enhanced LLM Client for various providers with fallback to template-based generation
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union
import requests
from config.llm_config import llm_config, LLMProvider

logger = logging.getLogger(__name__)

class LLMClient:
    """Universal LLM client that works with multiple providers."""
    
    def __init__(self):
        self.config = llm_config
        logger.info(f"Initialized LLM client with provider: {self.config.get_provider_info()}")
    
    async def generate_response(self, 
                              system_prompt: str, 
                              user_prompt: str, 
                              max_tokens: int = 2000) -> str:
        """Generate response using the configured LLM provider."""
        
        try:
            if self.config.provider == LLMProvider.GEMINI:
                return await self._gemini_generate(system_prompt, user_prompt, max_tokens)
            elif self.config.provider == LLMProvider.OPENAI:
                return await self._openai_generate(system_prompt, user_prompt, max_tokens)
            elif self.config.provider == LLMProvider.ANTHROPIC:
                return await self._anthropic_generate(system_prompt, user_prompt, max_tokens)
            elif self.config.provider == LLMProvider.LOCAL_OLLAMA:
                return await self._ollama_generate(system_prompt, user_prompt, max_tokens)
            elif self.config.provider == LLMProvider.HUGGINGFACE:
                return await self._huggingface_generate(system_prompt, user_prompt, max_tokens)
            else:
                logger.info("No LLM API configured, using template-based generation")
                return await self._template_fallback(system_prompt, user_prompt)
                
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            logger.info("Falling back to template-based generation")
            return await self._template_fallback(system_prompt, user_prompt)
    
    async def _openai_generate(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """Generate response using OpenAI API."""
        try:
            import openai
            
            client = openai.OpenAI(
                api_key=self.config.config['api_key'],
                base_url=self.config.config.get('base_url')
            )
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = client.chat.completions.create(
                model=self.config.config['model'],
                messages=messages,
                max_tokens=min(max_tokens, self.config.config['max_tokens']),
                temperature=self.config.config['temperature']
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _gemini_generate(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """Generate response using Google Gemini API."""
        try:
            import google.generativeai as genai
            
            # Configure the API key
            genai.configure(api_key=self.config.config['api_key'])
            
            # Initialize the model
            model = genai.GenerativeModel(
                model_name=self.config.config['model'],
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=min(max_tokens, self.config.config['max_tokens']),
                    temperature=self.config.config['temperature']
                )
            )
            
            # Combine system and user prompts
            combined_prompt = f"System Instructions: {system_prompt}\n\nUser Query: {user_prompt}\n\nPlease provide a response following the system instructions exactly."
            
            # Generate response
            response = model.generate_content(combined_prompt)
            
            return response.text
            
        except ImportError:
            logger.error("Google Generative AI library not installed. Install with: pip install google-generativeai")
            raise
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    async def _anthropic_generate(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """Generate response using Anthropic API."""
        try:
            import anthropic
            
            client = anthropic.Anthropic(
                api_key=self.config.config['api_key']
            )
            
            combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
            
            response = client.completions.create(
                model=self.config.config['model'],
                prompt=combined_prompt,
                max_tokens_to_sample=min(max_tokens, self.config.config['max_tokens']),
                temperature=self.config.config['temperature']
            )
            
            return response.completion
            
        except ImportError:
            logger.error("Anthropic library not installed. Install with: pip install anthropic")
            raise
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def _ollama_generate(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """Generate response using local Ollama."""
        try:
            url = f"{self.config.config['base_url']}/api/generate"
            
            payload = {
                "model": self.config.config['model'],
                "prompt": f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:",
                "stream": False,
                "options": {
                    "temperature": self.config.config['temperature'],
                    "num_predict": max_tokens
                }
            }
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
            
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise
    
    async def _huggingface_generate(self, system_prompt: str, user_prompt: str, max_tokens: int) -> str:
        """Generate response using HuggingFace Inference API."""
        try:
            url = f"{self.config.config['base_url']}/models/{self.config.config['model']}"
            
            headers = {
                "Authorization": f"Bearer {self.config.config['token']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:",
                "parameters": {
                    "max_new_tokens": min(max_tokens, self.config.config['max_tokens']),
                    "temperature": 0.1,
                    "return_full_text": False
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            else:
                return str(result)
            
        except Exception as e:
            logger.error(f"HuggingFace API error: {e}")
            raise
    
    async def _template_fallback(self, system_prompt: str, user_prompt: str) -> str:
        """Fallback to template-based generation when no LLM API is available."""
        logger.info("Using template-based fallback generation")
        
        # Simple template-based response for demonstration
        if "test case" in user_prompt.lower():
            return """[
{
    "Test_ID": "TC001",
    "Feature": "Template Generated Feature",
    "Test_Scenario": "Template generated test scenario based on query",
    "Steps": [
        "1. Navigate to the application",
        "2. Perform the required action",
        "3. Verify the expected result"
    ],
    "Expected_Result": "System should behave as specified in requirements",
    "Grounded_In": "Template-based generation (no specific document)",
    "Type": "Positive",
    "Notes": "Generated using template-based approach - configure LLM API for better results"
}]"""
        
        elif "selenium" in user_prompt.lower() or "script" in user_prompt.lower():
            return '''# Template-generated Selenium script
# Configure LLM API for more sophisticated script generation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TemplateGeneratedTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_basic_functionality(self):
        """Template-generated test - configure LLM API for detailed tests"""
        # Navigate to page
        self.driver.get("file:///path/to/checkout.html")
        
        # Basic interaction
        # Add specific steps based on your test case
        
        # Assertion
        self.assertTrue(True)  # Replace with actual assertion
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()'''
        
        else:
            return "Template-based response generated. Configure LLM API key for enhanced AI-powered generation."
    
    def get_status(self) -> Dict[str, Any]:
        """Get current LLM configuration status."""
        return {
            "provider": self.config.get_provider_info(),
            "api_available": self.config.is_api_available(),
            "config": {
                "model": self.config.config.get('model', 'N/A'),
                "max_tokens": self.config.config.get('max_tokens', 'N/A'),
                "temperature": self.config.config.get('temperature', 'N/A')
            }
        }


# Global LLM client instance
llm_client = LLMClient()