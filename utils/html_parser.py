"""
HTML Parser Module for Autonomous QA Agent

This module parses HTML content to extract DOM information, selectors,
and UI elements for Selenium script generation.
"""

from typing import Dict, List, Any, Optional
import re
import logging

try:
    from bs4 import BeautifulSoup, Tag, NavigableString
except ImportError:
    BeautifulSoup = None


class HTMLParser:
    """
    Parser for extracting DOM information from HTML content.
    Identifies selectors, form elements, and UI components for test automation.
    """
    
    def __init__(self):
        if BeautifulSoup is None:
            raise ImportError("beautifulsoup4 is required. Install with: pip install beautifulsoup4")
        
        self.logger = logging.getLogger(__name__)
    
    def parse_html(self, html_content: str) -> Dict[str, Any]:
        """
        Parse HTML content and extract DOM information.
        
        Args:
            html_content: Raw HTML content string
            
        Returns:
            Dictionary containing selectors, forms, buttons, inputs, and other UI elements
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            dom_info = {
                'selectors': self._extract_selectors(soup),
                'forms': self._extract_forms(soup),
                'buttons': self._extract_buttons(soup),
                'inputs': self._extract_inputs(soup),
                'links': self._extract_links(soup),
                'text_elements': self._extract_text_elements(soup),
                'structure': self._analyze_structure(soup)
            }
            
            return dom_info
            
        except Exception as e:
            self.logger.error(f"Error parsing HTML: {str(e)}")
            return {}
    
    def _extract_selectors(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """Extract all possible selectors from HTML elements."""
        selectors = {}
        
        # Find all elements with ID attributes
        for element in soup.find_all(attrs={'id': True}):
            element_id = element.get('id')
            if element_id:
                selectors[element_id] = {
                    'type': self._get_element_type(element),
                    'tag': element.name,
                    'selector_type': 'id',
                    'selector_value': element_id,
                    'text': self._get_element_text(element),
                    'attributes': dict(element.attrs),
                    'xpath': self._generate_xpath(element),
                    'css_selector': f'#{element_id}'
                }
        
        # Find all elements with name attributes
        for element in soup.find_all(attrs={'name': True}):
            name = element.get('name')
            if name and name not in selectors:
                selectors[f"name_{name}"] = {
                    'type': self._get_element_type(element),
                    'tag': element.name,
                    'selector_type': 'name',
                    'selector_value': name,
                    'text': self._get_element_text(element),
                    'attributes': dict(element.attrs),
                    'xpath': self._generate_xpath(element),
                    'css_selector': f'[name="{name}"]'
                }
        
        # Find elements with class attributes
        for element in soup.find_all(attrs={'class': True}):
            classes = element.get('class')
            if classes and isinstance(classes, list):
                class_str = ' '.join(classes)
                class_key = f"class_{classes[0]}"
                if class_key not in selectors:
                    selectors[class_key] = {
                        'type': self._get_element_type(element),
                        'tag': element.name,
                        'selector_type': 'class',
                        'selector_value': classes[0],
                        'text': self._get_element_text(element),
                        'attributes': dict(element.attrs),
                        'xpath': self._generate_xpath(element),
                        'css_selector': f'.{classes[0]}'
                    }
        
        return selectors
    
    def _extract_forms(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """Extract form information."""
        forms = {}
        
        for i, form in enumerate(soup.find_all('form')):
            form_id = form.get('id') or f'form_{i}'
            
            # Get form fields
            fields = []
            for input_elem in form.find_all(['input', 'select', 'textarea']):
                field_info = {
                    'tag': input_elem.name,
                    'type': input_elem.get('type', 'text'),
                    'name': input_elem.get('name'),
                    'id': input_elem.get('id'),
                    'required': input_elem.has_attr('required'),
                    'placeholder': input_elem.get('placeholder')
                }
                fields.append(field_info)
            
            forms[form_id] = {
                'action': form.get('action'),
                'method': form.get('method', 'GET'),
                'fields': fields,
                'attributes': dict(form.attrs)
            }
        
        return forms
    
    def _extract_buttons(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """Extract button information."""
        buttons = {}
        
        # Find button elements
        for i, button in enumerate(soup.find_all(['button', 'input'])):
            if button.name == 'input' and button.get('type') not in ['button', 'submit', 'reset']:
                continue
            
            button_id = button.get('id') or button.get('name') or f'button_{i}'
            
            buttons[button_id] = {
                'tag': button.name,
                'type': button.get('type', 'button'),
                'text': self._get_element_text(button) or button.get('value', ''),
                'onclick': button.get('onclick'),
                'class': button.get('class'),
                'attributes': dict(button.attrs)
            }
        
        return buttons
    
    def _extract_inputs(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """Extract input field information."""
        inputs = {}
        
        for input_elem in soup.find_all(['input', 'select', 'textarea']):
            input_id = input_elem.get('id') or input_elem.get('name') or f'input_{len(inputs)}'
            
            inputs[input_id] = {
                'tag': input_elem.name,
                'type': input_elem.get('type', 'text'),
                'name': input_elem.get('name'),
                'placeholder': input_elem.get('placeholder'),
                'required': input_elem.has_attr('required'),
                'value': input_elem.get('value'),
                'class': input_elem.get('class'),
                'attributes': dict(input_elem.attrs)
            }
        
        return inputs
    
    def _extract_links(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """Extract link information."""
        links = {}
        
        for i, link in enumerate(soup.find_all('a')):
            link_id = link.get('id') or f'link_{i}'
            
            links[link_id] = {
                'href': link.get('href'),
                'text': self._get_element_text(link),
                'title': link.get('title'),
                'target': link.get('target'),
                'class': link.get('class'),
                'attributes': dict(link.attrs)
            }
        
        return links
    
    def _extract_text_elements(self, soup: BeautifulSoup) -> Dict[str, Dict]:
        """Extract text elements like headers, paragraphs, etc."""
        text_elements = {}
        
        text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'label']
        
        for tag_name in text_tags:
            for i, element in enumerate(soup.find_all(tag_name)):
                element_id = element.get('id') or f'{tag_name}_{i}'
                text_content = self._get_element_text(element)
                
                if text_content and len(text_content.strip()) > 0:
                    text_elements[element_id] = {
                        'tag': element.name,
                        'text': text_content,
                        'class': element.get('class'),
                        'attributes': dict(element.attrs)
                    }
        
        return text_elements
    
    def _analyze_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze the overall structure of the HTML."""
        structure = {
            'title': soup.title.string if soup.title else 'No Title',
            'has_forms': bool(soup.find('form')),
            'form_count': len(soup.find_all('form')),
            'button_count': len(soup.find_all(['button', 'input[type="button"]', 'input[type="submit"]'])),
            'input_count': len(soup.find_all(['input', 'select', 'textarea'])),
            'link_count': len(soup.find_all('a')),
            'main_containers': []
        }
        
        # Find main containers
        for container in soup.find_all(['div', 'section', 'main', 'article']):
            container_id = container.get('id') or container.get('class')
            if container_id:
                structure['main_containers'].append({
                    'tag': container.name,
                    'id': container.get('id'),
                    'class': container.get('class')
                })
        
        return structure
    
    def _get_element_type(self, element: Tag) -> str:
        """Determine the type of HTML element."""
        if element.name == 'input':
            return element.get('type', 'text')
        elif element.name == 'button':
            return 'button'
        elif element.name in ['select', 'textarea']:
            return element.name
        elif element.name == 'a':
            return 'link'
        elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            return 'heading'
        elif element.name in ['p', 'span', 'div', 'label']:
            return 'text'
        else:
            return element.name
    
    def _get_element_text(self, element: Tag) -> str:
        """Get clean text content from an element."""
        if element.name == 'input':
            return element.get('value', '') or element.get('placeholder', '')
        
        text = element.get_text(strip=True)
        return text if text else ''
    
    def _generate_xpath(self, element: Tag) -> str:
        """Generate XPath for an element."""
        try:
            components = []
            current = element
            
            while current and hasattr(current, 'parent') and current.parent:
                if current.name:
                    siblings = [sibling for sibling in current.parent.find_all(current.name, recursive=False)]
                    if len(siblings) > 1:
                        index = siblings.index(current) + 1
                        components.append(f"{current.name}[{index}]")
                    else:
                        components.append(current.name)
                
                current = current.parent
                
                # Stop at body or html to avoid overly long XPaths
                if current and current.name in ['body', 'html']:
                    break
            
            components.reverse()
            xpath = '//' + '/'.join(components) if components else '//*'
            return xpath
            
        except Exception:
            return '//*'  # Fallback XPath
    
    def find_element_by_text(self, soup: BeautifulSoup, text: str, tag_names: List[str] = None) -> Optional[Dict]:
        """Find element by its text content."""
        if tag_names is None:
            tag_names = ['button', 'a', 'span', 'div', 'p', 'label', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        
        for tag_name in tag_names:
            elements = soup.find_all(tag_name)
            for element in elements:
                element_text = self._get_element_text(element)
                if text.lower() in element_text.lower():
                    return {
                        'element': element,
                        'tag': element.name,
                        'text': element_text,
                        'id': element.get('id'),
                        'class': element.get('class'),
                        'xpath': self._generate_xpath(element)
                    }
        
        return None
    
    def get_best_selector(self, element_info: Dict) -> str:
        """Get the best selector for an element based on reliability."""
        if element_info.get('id'):
            return f"By.ID, '{element_info['id']}'"
        elif element_info.get('name'):
            return f"By.NAME, '{element_info['name']}'"
        elif element_info.get('class') and isinstance(element_info['class'], list):
            return f"By.CLASS_NAME, '{element_info['class'][0]}'"
        elif element_info.get('text') and element_info.get('tag') in ['button', 'a']:
            return f"By.LINK_TEXT, '{element_info['text']}'"
        elif element_info.get('xpath'):
            return f"By.XPATH, '{element_info['xpath']}'"
        else:
            return f"By.TAG_NAME, '{element_info.get('tag', 'div')}'"