"""
Document Parser Module for Autonomous QA Agent

This module handles parsing of various document formats (MD, TXT, PDF, JSON, HTML)
and extracts clean, readable text for embedding generation.
"""

import json
import os
from typing import Dict, List, Tuple, Union
from pathlib import Path
import re

# Import libraries for document parsing
try:
    import PyPDF2
    from PyPDF2 import PdfReader
except ImportError:
    PyPDF2 = None
    PdfReader = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class DocumentParser:
    """
    Document parser that extracts text from various file formats.
    Maintains strict grounding by preserving source information.
    """
    
    def __init__(self):
        self.supported_formats = ['.md', '.txt', '.pdf', '.json', '.html']
    
    def parse_file(self, file_path: str, file_content: Union[str, bytes] = None) -> Dict:
        """
        Parse a file and extract clean text with metadata.
        
        Args:
            file_path: Path to the file or filename
            file_content: Optional file content (for uploaded files)
            
        Returns:
            Dict containing:
            - text: Extracted clean text
            - metadata: File information
            - file_type: Type of file
            - raw_content: Raw content (for HTML files)
        """
        file_extension = Path(file_path).suffix.lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Get file content if not provided
        if file_content is None:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            mode = 'rb' if file_extension == '.pdf' else 'r'
            encoding = None if file_extension == '.pdf' else 'utf-8'
            
            with open(file_path, mode, encoding=encoding) as f:
                file_content = f.read()
        
        # Parse based on file type
        if file_extension == '.md':
            return self._parse_markdown(file_path, file_content)
        elif file_extension == '.txt':
            return self._parse_text(file_path, file_content)
        elif file_extension == '.pdf':
            return self._parse_pdf(file_path, file_content)
        elif file_extension == '.json':
            return self._parse_json(file_path, file_content)
        elif file_extension == '.html':
            return self._parse_html(file_path, file_content)
    
    def _parse_markdown(self, file_path: str, content: str) -> Dict:
        """Parse Markdown files."""
        # Remove markdown syntax for clean text
        clean_text = re.sub(r'#+\s*', '', content)  # Remove headers
        clean_text = re.sub(r'\*\*(.*?)\*\*', r'\1', clean_text)  # Remove bold
        clean_text = re.sub(r'\*(.*?)\*', r'\1', clean_text)  # Remove italic
        clean_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_text)  # Remove links
        clean_text = re.sub(r'`(.*?)`', r'\1', clean_text)  # Remove code blocks
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)  # Normalize whitespace
        
        return {
            'text': clean_text.strip(),
            'metadata': {
                'filename': os.path.basename(file_path),
                'file_type': 'markdown',
                'source_path': file_path
            },
            'file_type': 'md',
            'raw_content': content
        }
    
    def _parse_text(self, file_path: str, content: str) -> Dict:
        """Parse plain text files."""
        return {
            'text': content.strip(),
            'metadata': {
                'filename': os.path.basename(file_path),
                'file_type': 'text',
                'source_path': file_path
            },
            'file_type': 'txt',
            'raw_content': content
        }
    
    def _parse_pdf(self, file_path: str, content: bytes) -> Dict:
        """Parse PDF files."""
        if PdfReader is None:
            raise ImportError("PyPDF2 is required for PDF parsing.")
        
        try:
            from io import BytesIO
            pdf_file = BytesIO(content) if isinstance(content, bytes) else open(file_path, 'rb')
            
            reader = PdfReader(pdf_file)
            text_content = ""
            
            for page in reader.pages:
                text_content += page.extract_text() + "\n"
            
            if hasattr(pdf_file, 'close'):
                pdf_file.close()
            
            return {
                'text': text_content.strip(),
                'metadata': {
                    'filename': os.path.basename(file_path),
                    'file_type': 'pdf',
                    'source_path': file_path,
                    'num_pages': len(reader.pages)
                },
                'file_type': 'pdf',
                'raw_content': text_content
            }
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _parse_json(self, file_path: str, content: str) -> Dict:
        """Parse JSON files."""
        try:
            json_data = json.loads(content)
            
            # Convert JSON to readable text
            if isinstance(json_data, dict):
                text_content = self._json_dict_to_text(json_data)
            elif isinstance(json_data, list):
                text_content = self._json_list_to_text(json_data)
            else:
                text_content = str(json_data)
            
            return {
                'text': text_content,
                'metadata': {
                    'filename': os.path.basename(file_path),
                    'file_type': 'json',
                    'source_path': file_path
                },
                'file_type': 'json',
                'raw_content': content
            }
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing JSON: {str(e)}")
    
    def _parse_html(self, file_path: str, content: str) -> Dict:
        """Parse HTML files."""
        if BeautifulSoup is None:
            raise ImportError("beautifulsoup4 is required for HTML parsing. Install with: pip install beautifulsoup4")
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text_content = re.sub(r'\s+', ' ', text_content)
        
        return {
            'text': text_content.strip(),
            'metadata': {
                'filename': os.path.basename(file_path),
                'file_type': 'html',
                'source_path': file_path
            },
            'file_type': 'html',
            'raw_content': content,
            'parsed_html': soup  # Keep parsed HTML for DOM extraction
        }
    
    def _json_dict_to_text(self, json_dict: dict, level: int = 0) -> str:
        """Convert JSON dictionary to readable text."""
        text_lines = []
        indent = "  " * level
        
        for key, value in json_dict.items():
            if isinstance(value, dict):
                text_lines.append(f"{indent}{key}:")
                text_lines.append(self._json_dict_to_text(value, level + 1))
            elif isinstance(value, list):
                text_lines.append(f"{indent}{key}:")
                text_lines.append(self._json_list_to_text(value, level + 1))
            else:
                text_lines.append(f"{indent}{key}: {value}")
        
        return "\n".join(text_lines)
    
    def _json_list_to_text(self, json_list: list, level: int = 0) -> str:
        """Convert JSON list to readable text."""
        text_lines = []
        indent = "  " * level
        
        for i, item in enumerate(json_list):
            if isinstance(item, dict):
                text_lines.append(f"{indent}Item {i+1}:")
                text_lines.append(self._json_dict_to_text(item, level + 1))
            elif isinstance(item, list):
                text_lines.append(f"{indent}Item {i+1}:")
                text_lines.append(self._json_list_to_text(item, level + 1))
            else:
                text_lines.append(f"{indent}Item {i+1}: {item}")
        
        return "\n".join(text_lines)


class TextChunker:
    """
    Text chunking utility for creating overlapping chunks suitable for embeddings.
    """
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Split text into overlapping chunks with metadata.
        
        Args:
            text: Text to chunk
            metadata: Metadata to include with each chunk
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        if not text or len(text.strip()) == 0:
            return []
        
        chunks = []
        text_length = len(text)
        
        # If text is smaller than chunk size, return as single chunk
        if text_length <= self.chunk_size:
            chunks.append({
                'text': text,
                'metadata': {
                    **metadata,
                    'chunk_index': 0,
                    'total_chunks': 1,
                    'start_pos': 0,
                    'end_pos': text_length
                }
            })
            return chunks
        
        # Create overlapping chunks
        start = 0
        chunk_index = 0
        
        while start < text_length:
            end = min(start + self.chunk_size, text_length)
            
            # Try to break at word boundaries
            if end < text_length:
                # Look for last space within the chunk
                last_space = text.rfind(' ', start, end)
                if last_space > start:
                    end = last_space
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:  # Only add non-empty chunks
                chunks.append({
                    'text': chunk_text,
                    'metadata': {
                        **metadata,
                        'chunk_index': chunk_index,
                        'start_pos': start,
                        'end_pos': end
                    }
                })
                chunk_index += 1
            
            # Move start position considering overlap
            start = end - self.overlap if end < text_length else text_length
        
        # Update total chunks in all metadata
        for chunk in chunks:
            chunk['metadata']['total_chunks'] = len(chunks)
        
        return chunks