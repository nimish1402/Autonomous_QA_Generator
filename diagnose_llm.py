"""
Diagnostic script to test the LLM integration and identify template generation issue
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment
parent_dir = Path(__file__).parent
env_file = parent_dir / '.env'
load_dotenv(env_file)

# Add parent to path
sys.path.append(str(parent_dir))

print("="*70)
print("DIAGNOSTIC: Testing LLM Integration")
print("="*70)

# Check environment variables
print("\n1. Environment Variables:")
print(f"   GEMINI_API_KEY: {os.getenv('GEMINI_API_KEY')[:15]}..." if os.getenv('GEMINI_API_KEY') else "   GEMINI_API_KEY: NOT SET")
print(f"   GEMINI_MODEL: {os.getenv('GEMINI_MODEL', 'NOT SET')}")

# Test LLM Config
print("\n2. Testing LLM Config:")
try:
    from config.llm_config import llm_config
    print(f"   Provider: {llm_config.get_provider_info()}")
    print(f"   API Available: {llm_config.is_api_available()}")
    print(f"   Model: {llm_config.config.get('model', 'N/A')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test LLM Client
print("\n3. Testing LLM Client:")
try:
    from utils.llm_client import llm_client
    status = llm_client.get_status()
    print(f"   Provider: {status['provider']}")
    print(f"   API Available: {status['api_available']}")
    print(f"   Model: {status['config']['model']}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test direct Gemini API call
print("\n4. Testing Direct Gemini API Call:")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model_name = os.getenv('GEMINI_MODEL', 'gemini-flash-latest')
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say 'API Working' in exactly 2 words")
    print(f"   Model: {model_name}")
    print(f"   Response: {response.text}")
    print(f"   Status: ✓ SUCCESS")
except Exception as e:
    print(f"   ERROR: {e}")
    print(f"   Status: ✗ FAILED")

# Test LLM Client generate_response
print("\n5. Testing LLM Client generate_response:")
async def test_llm_client():
    try:
        from utils.llm_client import llm_client
        response = await llm_client.generate_response(
            system_prompt="You are a test assistant.",
            user_prompt="Say 'LLM Client Working' in exactly 3 words.",
            max_tokens=50
        )
        print(f"   Response: {response}")
        if "template" in response.lower():
            print(f"   Status: ✗ TEMPLATE FALLBACK TRIGGERED")
        else:
            print(f"   Status: ✓ AI RESPONSE")
    except Exception as e:
        print(f"   ERROR: {e}")
        print(f"   Status: ✗ FAILED")

asyncio.run(test_llm_client())

# Test TestCaseGenerator
print("\n6. Testing TestCaseGenerator:")
async def test_test_case_generator():
    try:
        from models.llm_agent import TestCaseGenerator
        generator = TestCaseGenerator()
        
        # Create mock data
        mock_chunks = [
            {
                'text': 'The login page should accept email and password.',
                'metadata': {'filename': 'requirements.md'}
            }
        ]
        
        test_cases = await generator.generate_test_cases(
            query="test login functionality",
            retrieved_chunks=mock_chunks,
            checkout_dom=None
        )
        
        if test_cases:
            print(f"   Generated {len(test_cases)} test case(s)")
            if test_cases[0].get('Feature') == 'Template Generated Feature':
                print(f"   Status: ✗ TEMPLATE GENERATED")
                print(f"   Test Case: {test_cases[0]}")
            else:
                print(f"   Status: ✓ AI GENERATED")
                print(f"   Feature: {test_cases[0].get('Feature', 'N/A')}")
        else:
            print(f"   Status: ✗ NO TEST CASES GENERATED")
    except Exception as e:
        print(f"   ERROR: {e}")
        import traceback
        traceback.print_exc()
        print(f"   Status: ✗ FAILED")

asyncio.run(test_test_case_generator())

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)
