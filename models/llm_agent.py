"""
LLM Agent Module for Autonomous QA Agent

This module contains agents for generating test cases and Selenium scripts
with strict grounding enforcement and structured output generation.
"""

import json
import logging
from typing import Dict, List, Any, Optional
import re
import asyncio
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.llm_client import llm_client
    from config.llm_config import llm_config
    LLM_AVAILABLE = True
except ImportError as e:
    logging.warning(f"LLM client not available: {e}")
    LLM_AVAILABLE = False


class TestCaseGenerator:
    """
    Agent for generating structured test cases with grounding enforcement.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def generate_test_cases(self, 
                                  query: str, 
                                  retrieved_chunks: List[Dict], 
                                  checkout_dom: Optional[Dict] = None) -> List[Dict]:
        """
        Generate test cases based on query and retrieved context.
        
        Args:
            query: User query for test case generation
            retrieved_chunks: Retrieved document chunks from vector DB
            checkout_dom: Parsed DOM information from checkout.html
            
        Returns:
            List of structured test cases in JSON format
        """
        try:
            # Extract relevant information from chunks
            grounded_info = self._extract_grounded_info(retrieved_chunks)
            
            # Extract UI elements from DOM if available
            ui_elements = self._extract_ui_elements(checkout_dom) if checkout_dom else {}
            
            # Try LLM-powered generation first, fallback to template-based
            if LLM_AVAILABLE and llm_config.is_api_available():
                self.logger.info(f"Using {llm_config.get_provider_info()} for test case generation")
                test_cases = await self._generate_with_llm(query, grounded_info, ui_elements, retrieved_chunks)
            else:
                self.logger.info("Using template-based test case generation")
                test_cases = self._generate_test_cases_from_context(
                    query=query,
                    grounded_info=grounded_info,
                    ui_elements=ui_elements
                )
            
            return test_cases
            
        except Exception as e:
            self.logger.error(f"Error generating test cases: {str(e)}")
            # Fallback to template-based generation
            return self._generate_test_cases_from_context(query, self._extract_grounded_info(retrieved_chunks), {})
    
    def _extract_grounded_info(self, chunks: List[Dict]) -> Dict[str, Any]:
        """Extract and organize information from retrieved chunks."""
        grounded_info = {
            'features': [],
            'business_rules': [],
            'ui_elements': [],
            'workflows': [],
            'validations': [],
            'sources': []
        }
        
        for chunk in chunks:
            text = chunk.get('text', '').lower()
            metadata = chunk.get('metadata', {})
            source = metadata.get('filename', 'Unknown')
            
            # Extract features
            if any(keyword in text for keyword in ['feature', 'functionality', 'capability']):
                grounded_info['features'].append({
                    'text': chunk.get('text', ''),
                    'source': source
                })
            
            # Extract business rules
            if any(keyword in text for keyword in ['rule', 'policy', 'requirement', 'must', 'should']):
                grounded_info['business_rules'].append({
                    'text': chunk.get('text', ''),
                    'source': source
                })
            
            # Extract UI elements
            if any(keyword in text for keyword in ['button', 'field', 'input', 'form', 'dropdown', 'checkbox']):
                grounded_info['ui_elements'].append({
                    'text': chunk.get('text', ''),
                    'source': source
                })
            
            # Extract workflows
            if any(keyword in text for keyword in ['step', 'process', 'workflow', 'procedure']):
                grounded_info['workflows'].append({
                    'text': chunk.get('text', ''),
                    'source': source
                })
            
            # Extract validations
            if any(keyword in text for keyword in ['validation', 'error', 'message', 'warning', 'check']):
                grounded_info['validations'].append({
                    'text': chunk.get('text', ''),
                    'source': source
                })
            
            # Track all sources
            if source not in grounded_info['sources']:
                grounded_info['sources'].append(source)
        
        return grounded_info
    
    def _extract_ui_elements(self, checkout_dom: Dict) -> Dict[str, Any]:
        """Extract UI elements from checkout DOM."""
        if not checkout_dom:
            return {}
        
        return {
            'selectors': checkout_dom.get('selectors', {}),
            'forms': checkout_dom.get('forms', {}),
            'buttons': checkout_dom.get('buttons', {}),
            'inputs': checkout_dom.get('inputs', {}),
            'links': checkout_dom.get('links', {})
        }
    
    def _generate_test_cases_from_context(self, 
                                          query: str, 
                                          grounded_info: Dict, 
                                          ui_elements: Dict) -> List[Dict]:
        """Generate test cases based on context and query."""
        test_cases = []
        
        # Determine query intent
        query_lower = query.lower()
        
        # Feature-specific test case generation
        if 'discount' in query_lower or 'coupon' in query_lower:
            test_cases.extend(self._generate_discount_test_cases(grounded_info, ui_elements))
        
        if 'checkout' in query_lower or 'purchase' in query_lower or 'payment' in query_lower:
            test_cases.extend(self._generate_checkout_test_cases(grounded_info, ui_elements))
        
        if 'form' in query_lower or 'validation' in query_lower:
            test_cases.extend(self._generate_form_test_cases(grounded_info, ui_elements))
        
        if 'login' in query_lower or 'authentication' in query_lower:
            test_cases.extend(self._generate_login_test_cases(grounded_info, ui_elements))
        
        # If no specific feature detected, generate general test cases
        if not test_cases:
            test_cases.extend(self._generate_general_test_cases(grounded_info, ui_elements))
        
        return test_cases
    
    def _generate_discount_test_cases(self, grounded_info: Dict, ui_elements: Dict) -> List[Dict]:
        """Generate test cases for discount/coupon functionality."""
        test_cases = []
        
        # Find discount-related information
        discount_info = []
        for item in grounded_info['features'] + grounded_info['business_rules']:
            if 'discount' in item['text'].lower() or 'coupon' in item['text'].lower():
                discount_info.append(item)
        
        sources = list(set([item['source'] for item in discount_info]))
        
        # Positive test cases
        test_cases.append({
            "Test_ID": "TC001",
            "Feature": "Discount Code",
            "Test_Scenario": "Apply valid discount code",
            "Steps": [
                "1. Navigate to checkout page",
                "2. Enter valid discount code in coupon field",
                "3. Click Apply button",
                "4. Verify discount is applied to total"
            ],
            "Expected_Result": "Discount should be applied and total price should be reduced",
            "Grounded_In": sources[0] if sources else "NOT SPECIFIED",
            "Type": "Positive",
            "Notes": "Based on discount functionality requirements"
        })
        
        # Negative test cases
        test_cases.append({
            "Test_ID": "TC002", 
            "Feature": "Discount Code",
            "Test_Scenario": "Apply invalid discount code",
            "Steps": [
                "1. Navigate to checkout page",
                "2. Enter invalid discount code in coupon field", 
                "3. Click Apply button",
                "4. Verify error message is displayed"
            ],
            "Expected_Result": "Error message should be displayed: 'Invalid discount code'",
            "Grounded_In": sources[0] if sources else "NOT SPECIFIED",
            "Type": "Negative",
            "Notes": "Testing invalid input handling"
        })
        
        return test_cases
    
    def _generate_checkout_test_cases(self, grounded_info: Dict, ui_elements: Dict) -> List[Dict]:
        """Generate test cases for checkout functionality."""
        test_cases = []
        
        # Find checkout-related information
        checkout_info = []
        for item in grounded_info['features'] + grounded_info['workflows']:
            if 'checkout' in item['text'].lower() or 'payment' in item['text'].lower():
                checkout_info.append(item)
        
        sources = list(set([item['source'] for item in checkout_info]))
        
        test_cases.append({
            "Test_ID": "TC003",
            "Feature": "Checkout Process",
            "Test_Scenario": "Complete checkout with valid information",
            "Steps": [
                "1. Fill in billing information",
                "2. Select payment method",
                "3. Enter payment details",
                "4. Click Place Order button"
            ],
            "Expected_Result": "Order should be processed successfully",
            "Grounded_In": sources[0] if sources else "NOT SPECIFIED",
            "Type": "Positive",
            "Notes": "End-to-end checkout workflow"
        })
        
        return test_cases
    
    def _generate_form_test_cases(self, grounded_info: Dict, ui_elements: Dict) -> List[Dict]:
        """Generate test cases for form validation."""
        test_cases = []
        
        # Find validation-related information
        validation_info = []
        for item in grounded_info['validations'] + grounded_info['business_rules']:
            validation_info.append(item)
        
        sources = list(set([item['source'] for item in validation_info]))
        
        test_cases.append({
            "Test_ID": "TC004",
            "Feature": "Form Validation",
            "Test_Scenario": "Submit form with empty required fields",
            "Steps": [
                "1. Navigate to form",
                "2. Leave required fields empty",
                "3. Click submit button",
                "4. Verify validation messages are displayed"
            ],
            "Expected_Result": "Validation messages should be displayed for required fields",
            "Grounded_In": sources[0] if sources else "NOT SPECIFIED",
            "Type": "Negative",
            "Notes": "Required field validation testing"
        })
        
        return test_cases
    
    def _generate_login_test_cases(self, grounded_info: Dict, ui_elements: Dict) -> List[Dict]:
        """Generate test cases for login functionality."""
        test_cases = []
        
        test_cases.append({
            "Test_ID": "TC005",
            "Feature": "User Authentication",
            "Test_Scenario": "Login with valid credentials",
            "Steps": [
                "1. Navigate to login page",
                "2. Enter valid username",
                "3. Enter valid password",
                "4. Click login button"
            ],
            "Expected_Result": "User should be logged in and redirected to dashboard",
            "Grounded_In": "NOT SPECIFIED",
            "Type": "Positive",
            "Notes": "Standard login functionality"
        })
        
        return test_cases
    
    def _generate_general_test_cases(self, grounded_info: Dict, ui_elements: Dict) -> List[Dict]:
        """Generate general test cases when no specific feature is identified."""
        test_cases = []
        
        # Extract any available features
        available_features = []
        for item in grounded_info['features']:
            available_features.append(item['text'][:100] + "..." if len(item['text']) > 100 else item['text'])
        
        sources = grounded_info['sources']
        
        if available_features:
            test_cases.append({
                "Test_ID": "TC006",
                "Feature": "General Functionality",
                "Test_Scenario": "Verify main functionality works as expected",
                "Steps": [
                    "1. Navigate to main page",
                    "2. Interact with primary elements",
                    "3. Verify expected behavior"
                ],
                "Expected_Result": "Functionality should work as described in requirements",
                "Grounded_In": sources[0] if sources else "NOT SPECIFIED",
                "Type": "Positive",
                "Notes": f"Based on available features: {', '.join(available_features[:3])}"
            })
        else:
            test_cases.append({
                "Test_ID": "TC007",
                "Feature": "Basic Functionality",
                "Test_Scenario": "Verify page loads correctly",
                "Steps": [
                    "1. Navigate to application URL",
                    "2. Verify page loads without errors",
                    "3. Check for presence of key elements"
                ],
                "Expected_Result": "Page should load successfully with all key elements visible",
                "Grounded_In": "NOT SPECIFIED",
                "Type": "Positive",
                "Notes": "Basic smoke test - no specific requirements found in documents"
            })
        
        return test_cases
    
    async def _generate_with_llm(self, query: str, grounded_info: Dict, ui_elements: Dict, retrieved_chunks: List[Dict]) -> List[Dict]:
        """
        Generate test cases using LLM API with proper grounding.
        """
        try:
            # Create context from retrieved chunks
            context_text = "\n\n".join([
                f"Source: {chunk.get('metadata', {}).get('filename', 'Unknown')}\n{chunk.get('text', '')}"
                for chunk in retrieved_chunks[:5]  # Limit context size
            ])
            
            # Create UI elements summary
            ui_summary = ""
            if ui_elements:
                selectors = ui_elements.get('selectors', {})
                ui_summary = f"Available UI elements: {', '.join(list(selectors.keys())[:10])}"
            
            system_prompt = """
You are an expert QA automation engineer. Generate EXACTLY 2-3 structured test cases in valid JSON format.

CRITICAL: Your response must be ONLY a valid JSON array, no other text before or after.

GROUNDING RULES:
1. Only use information from the provided context documents
2. Reference source document filename in "Grounded_In" field
3. Generate both positive and negative test cases

REQUIRED JSON FORMAT (respond with ONLY this JSON, no explanation):
[
  {
    "Test_ID": "TC001",
    "Feature": "exact feature name from context",
    "Test_Scenario": "specific scenario description",
    "Steps": ["step 1", "step 2", "step 3"],
    "Expected_Result": "expected outcome",
    "Grounded_In": "filename.ext",
    "Type": "Positive",
    "Notes": "brief note"
  },
  {
    "Test_ID": "TC002",
    "Feature": "exact feature name from context", 
    "Test_Scenario": "negative scenario description",
    "Steps": ["step 1", "step 2", "step 3"],
    "Expected_Result": "expected error or validation",
    "Grounded_In": "filename.ext",
    "Type": "Negative",
    "Notes": "brief note"
  }
]

CRITICAL: Ensure all strings are properly quoted and escaped. No trailing commas.
"""
            
            user_prompt = f"""
Query: {query}

Context Documents:
{context_text}

{ui_summary}

Generate test cases based on this query and context. Ensure strict grounding to the provided information.
"""
            
            response = await llm_client.generate_response(system_prompt, user_prompt)
            
            # Parse JSON response
            try:
                # Clean up response (remove markdown formatting if present)
                clean_response = response.strip()
                if clean_response.startswith('```json'):
                    clean_response = clean_response[7:]
                if clean_response.startswith('```'):
                    clean_response = clean_response[3:]
                if clean_response.endswith('```'):
                    clean_response = clean_response[:-3]
                clean_response = clean_response.strip()
                
                # Try to extract JSON from response if it contains extra text
                start_idx = clean_response.find('[')
                end_idx = clean_response.rfind(']')
                
                if start_idx != -1 and end_idx != -1:
                    json_part = clean_response[start_idx:end_idx+1]
                    test_cases = json.loads(json_part)
                else:
                    test_cases = json.loads(clean_response)
                
                # Validate structure
                if isinstance(test_cases, list) and len(test_cases) > 0:
                    return test_cases
                else:
                    self.logger.warning("LLM response not in expected list format or empty")
                    # Fallback to template generation
                    return self._generate_test_cases_from_context(query, grounded_info, ui_elements)
                    
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse LLM JSON response: {e}")
                self.logger.error(f"Raw response length: {len(response)}")
                self.logger.error(f"Full raw response: {response}")
                # Fallback to template generation
                self.logger.info("Falling back to template-based generation")
                return self._generate_test_cases_from_context(query, grounded_info, ui_elements)
                
        except Exception as e:
            self.logger.error(f"Error in LLM generation: {e}")
            return []


class SeleniumScriptGenerator:
    """
    Agent for generating runnable Selenium Python scripts.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def generate_script(self, 
                              test_case: Dict, 
                              checkout_html: str,
                              dom_info: Dict,
                              context_chunks: List[Dict]) -> str:
        """
        Generate Selenium Python script for a test case.
        
        Args:
            test_case: Test case dictionary
            checkout_html: Raw HTML content
            dom_info: Parsed DOM information
            context_chunks: Relevant context chunks
            
        Returns:
            Complete Selenium Python script as string
        """
        try:
            # Try LLM-powered generation first, fallback to template-based
            if LLM_AVAILABLE and llm_config.is_api_available():
                self.logger.info(f"Using {llm_config.get_provider_info()} for script generation")
                script_content = await self._generate_script_with_llm(test_case, dom_info, context_chunks)
            else:
                self.logger.info("Using template-based script generation")
                script_content = self._generate_script_template(
                    test_id=test_case.get('Test_ID', 'test'),
                    feature=test_case.get('Feature', 'feature'),
                    scenario=test_case.get('Test_Scenario', 'scenario'),
                    steps=test_case.get('Steps', []),
                    expected_result=test_case.get('Expected_Result', ''),
                    selectors=dom_info.get('selectors', {})
                )
            
            return script_content
            
        except Exception as e:
            self.logger.error(f"Error generating Selenium script: {str(e)}")
            return ""
    
    def _generate_script_template(self, 
                                  test_id: str,
                                  feature: str, 
                                  scenario: str,
                                  steps: List[str],
                                  expected_result: str,
                                  selectors: Dict) -> str:
        """Generate the complete Selenium script template."""
        
        # Create step implementations
        step_implementations = self._generate_step_implementations(steps, selectors)
        
        script = f'''"""
Test Script: {test_id}
Feature: {feature}
Scenario: {scenario}

Auto-generated Selenium test script for Autonomous QA Agent
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import unittest


class Test{test_id.replace("TC", "")}(unittest.TestCase):
    """
    Test Case: {test_id}
    Feature: {feature}
    Scenario: {scenario}
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Initialize WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
        # Set implicit wait
        self.driver.implicitly_wait(10)
        
        # Set explicit wait
        self.wait = WebDriverWait(self.driver, 10)
        
        # Base URL - UPDATE THIS TO YOUR ACTUAL URL
        self.base_url = "file:///path/to/checkout.html"  # Update this path
    
    def tearDown(self):
        """Clean up after each test method."""
        self.driver.quit()
    
    def test_{test_id.lower().replace("tc", "")}(self):
        """
        Test: {scenario}
        Expected Result: {expected_result}
        """
        try:
            # Navigate to the checkout page
            self.driver.get(self.base_url)
            print("✓ Navigated to checkout page")
            
{step_implementations}
            
            # Final assertion based on expected result
            {self._generate_final_assertion(expected_result, selectors)}
            
            print("✓ Test completed successfully")
            
        except Exception as e:
            self.fail(f"Test failed: {{str(e)}}")


if __name__ == "__main__":
    # Run the test
    unittest.main(verbosity=2)
'''
        
        return script
    
    def _generate_step_implementations(self, steps: List[str], selectors: Dict) -> str:
        """Generate implementations for test steps."""
        implementations = []
        
        for i, step in enumerate(steps, 1):
            step_lower = step.lower()
            implementation = f"            # Step {i}: {step}\n"
            
            if 'navigate' in step_lower or 'open' in step_lower:
                implementation += "            # Navigation already handled in setUp\n"
                implementation += "            time.sleep(1)\n"
            
            elif 'enter' in step_lower or 'input' in step_lower or 'type' in step_lower:
                # Find relevant input field
                field_selector = self._find_input_selector(step, selectors)
                if field_selector:
                    implementation += f"            # Enter data into field\n"
                    implementation += f"            element = self.wait.until(EC.presence_of_element_located({field_selector}))\n"
                    implementation += f"            element.clear()\n"
                    implementation += f"            element.send_keys('test_data')  # UPDATE WITH ACTUAL DATA\n"
                else:
                    implementation += "            # INPUT FIELD NOT FOUND IN HTML - UPDATE SELECTOR\n"
                    implementation += "            # element = self.driver.find_element(By.ID, 'UPDATE_SELECTOR')\n"
                    implementation += "            # element.send_keys('test_data')\n"
            
            elif 'click' in step_lower:
                # Find relevant button or clickable element
                button_selector = self._find_button_selector(step, selectors)
                if button_selector:
                    implementation += f"            # Click button/element\n"
                    implementation += f"            element = self.wait.until(EC.element_to_be_clickable({button_selector}))\n"
                    implementation += f"            element.click()\n"
                else:
                    implementation += "            # BUTTON NOT FOUND IN HTML - UPDATE SELECTOR\n"
                    implementation += "            # element = self.driver.find_element(By.ID, 'UPDATE_SELECTOR')\n"
                    implementation += "            # element.click()\n"
            
            elif 'verify' in step_lower or 'check' in step_lower:
                implementation += "            # Verification step\n"
                implementation += "            # Add appropriate assertion based on what needs to be verified\n"
                implementation += "            time.sleep(2)  # Wait for elements to load\n"
            
            else:
                implementation += "            # Generic step - implement based on requirements\n"
                implementation += "            time.sleep(1)\n"
            
            implementation += f"            print('✓ Step {i} completed')\n"
            implementations.append(implementation)
        
        return "\n".join(implementations)
    
    def _find_input_selector(self, step: str, selectors: Dict) -> Optional[str]:
        """Find appropriate input selector for a step."""
        step_lower = step.lower()
        
        # Check for specific field types
        if 'discount' in step_lower or 'coupon' in step_lower:
            for sel_id, sel_info in selectors.items():
                if 'coupon' in sel_id.lower() or 'discount' in sel_id.lower():
                    return f"(By.ID, '{sel_id}')"
        
        if 'email' in step_lower:
            for sel_id, sel_info in selectors.items():
                if 'email' in sel_id.lower():
                    return f"(By.ID, '{sel_id}')"
        
        if 'name' in step_lower:
            for sel_id, sel_info in selectors.items():
                if 'name' in sel_id.lower() and sel_info.get('type') == 'input':
                    return f"(By.ID, '{sel_id}')"
        
        # Return first input field as fallback
        for sel_id, sel_info in selectors.items():
            if sel_info.get('type') == 'input':
                return f"(By.ID, '{sel_id}')"
        
        return None
    
    def _find_button_selector(self, step: str, selectors: Dict) -> Optional[str]:
        """Find appropriate button selector for a step."""
        step_lower = step.lower()
        
        # Check for specific button types
        if 'apply' in step_lower:
            for sel_id, sel_info in selectors.items():
                if 'apply' in sel_id.lower():
                    return f"(By.ID, '{sel_id}')"
        
        if 'submit' in step_lower or 'place order' in step_lower:
            for sel_id, sel_info in selectors.items():
                if 'submit' in sel_id.lower() or 'order' in sel_id.lower():
                    return f"(By.ID, '{sel_id}')"
        
        # Return first button as fallback
        for sel_id, sel_info in selectors.items():
            if sel_info.get('type') == 'button':
                return f"(By.ID, '{sel_id}')"
        
        return None
    
    def _generate_final_assertion(self, expected_result: str, selectors: Dict) -> str:
        """Generate final assertion based on expected result."""
        expected_lower = expected_result.lower()
        
        if 'discount' in expected_lower or 'price' in expected_lower:
            return '''# Verify discount was applied (update selector as needed)
            # total_element = self.driver.find_element(By.ID, 'total')
            # self.assertTrue("discount applied" in total_element.text.lower())'''
        
        elif 'error' in expected_lower or 'message' in expected_lower:
            return '''# Verify error/success message is displayed
            # message_element = self.driver.find_element(By.CLASS_NAME, 'message')
            # self.assertTrue(message_element.is_displayed())'''
        
        elif 'successful' in expected_lower or 'complete' in expected_lower:
            return '''# Verify successful completion
            # success_indicator = self.driver.find_element(By.CLASS_NAME, 'success')
            # self.assertTrue(success_indicator.is_displayed())'''
        
        else:
            return '''# Add appropriate assertion based on expected result
            # self.assertTrue(True)  # Replace with actual assertion'''
    
    async def _generate_script_with_llm(self, test_case: Dict, dom_info: Dict, context_chunks: List[Dict]) -> str:
        """
        Generate Selenium script using LLM API with proper selector grounding.
        """
        try:
            # Extract available selectors
            selectors = dom_info.get('selectors', {})
            selector_info = "\n".join([
                f"- {sel_id}: {info.get('type', 'unknown')} element, selector: {info.get('css_selector', 'N/A')}"
                for sel_id, info in list(selectors.items())[:15]  # Limit to prevent token overflow
            ])
            
            # Create context
            context_text = "\n".join([
                f"Source: {chunk.get('metadata', {}).get('filename', 'Unknown')}\n{chunk.get('text', '')}"
                for chunk in context_chunks[:3]
            ])
            
            system_prompt = """
You are an expert Selenium automation engineer. Generate a complete, runnable Python Selenium test script based on the provided test case and available UI selectors.

CRITICAL REQUIREMENTS:
1. Use ONLY selectors that exist in the provided selector list
2. Generate complete, executable Python code with proper imports
3. Use WebDriverWait for robust element handling
4. Include proper setUp and tearDown methods
5. Add detailed comments explaining selector choices
6. Use unittest framework structure
7. If a selector doesn't exist, add a comment explaining the missing element

Required imports and structure:
- selenium webdriver and related classes
- webdriver_manager for Chrome driver
- unittest framework
- Proper exception handling
"""
            
            user_prompt = f"""
Test Case:
{json.dumps(test_case, indent=2)}

Available UI Selectors:
{selector_info}

Context Documentation:
{context_text}

Generate a complete Selenium Python script for this test case using only the provided selectors. Include proper comments for any missing selectors.
"""
            
            response = await llm_client.generate_response(system_prompt, user_prompt)
            
            # Clean up response (remove markdown if present)
            clean_response = response.strip()
            if clean_response.startswith('```python'):
                clean_response = clean_response[9:]
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:]
            if clean_response.endswith('```'):
                clean_response = clean_response[:-3]
            
            return clean_response.strip()
            
        except Exception as e:
            self.logger.error(f"Error in LLM script generation: {e}")
            # Fallback to template generation
            return self._generate_script_template(
                test_id=test_case.get('Test_ID', 'test'),
                feature=test_case.get('Feature', 'feature'),
                scenario=test_case.get('Test_Scenario', 'scenario'),
                steps=test_case.get('Steps', []),
                expected_result=test_case.get('Expected_Result', ''),
                selectors=dom_info.get('selectors', {})
            )