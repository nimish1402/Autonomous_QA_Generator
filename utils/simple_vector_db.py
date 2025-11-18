"""
Simple Vector Database Module for Autonomous QA Agent

This module provides a simplified vector database that doesn't require downloading models.
It uses basic text similarity for initial setup and can be upgraded later.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import re
from collections import Counter


class SimpleVectorDatabase:
    """
    Simple vector database implementation using keyword-based similarity.
    This is a lightweight alternative that doesn't require downloading ML models.
    """
    
    def __init__(self, persist_directory: str = "./vectordb", collection_name: str = "qa_documents"):
        """
        Initialize the simple vector database.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.db_file = os.path.join(persist_directory, f"{collection_name}.json")
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Load existing data or initialize empty
        self.documents = self._load_documents()
        
        self.logger = logging.getLogger(__name__)
        
    def _load_documents(self) -> List[Dict]:
        """Load documents from JSON file."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading documents: {e}")
                return []
        return []
    
    def _save_documents(self):
        """Save documents to JSON file."""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Error saving documents: {e}")
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for similarity matching."""
        # Clean and tokenize text
        text = text.lower()
        # Remove special characters and split into words
        words = re.findall(r'\b[a-z]{3,}\b', text)
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords
    
    def _calculate_similarity(self, query_keywords: List[str], doc_keywords: List[str]) -> float:
        """Calculate similarity between keyword lists."""
        if not query_keywords or not doc_keywords:
            return 0.0
        
        # Count matching keywords
        query_counter = Counter(query_keywords)
        doc_counter = Counter(doc_keywords)
        
        # Calculate intersection
        intersection = sum((query_counter & doc_counter).values())
        
        # Calculate union
        union = sum((query_counter | doc_counter).values())
        
        # Jaccard similarity
        if union == 0:
            return 0.0
        
        similarity = intersection / union
        return similarity
    
    def add_documents(self, chunks: List[Dict]) -> Dict[str, Any]:
        """
        Add document chunks to the vector database.
        
        Args:
            chunks: List of chunk dictionaries with 'text' and 'metadata' keys
            
        Returns:
            Dictionary with operation results
        """
        if not chunks:
            return {"success": False, "message": "No chunks provided", "added_count": 0}
        
        try:
            added_count = 0
            
            for i, chunk in enumerate(chunks):
                text = chunk.get('text', '').strip()
                metadata = chunk.get('metadata', {})
                
                if not text:
                    continue
                
                # Generate unique ID
                chunk_id = f"{metadata.get('filename', 'unknown')}_{metadata.get('chunk_index', i)}"
                
                # Extract keywords for similarity matching
                keywords = self._extract_keywords(text)
                
                # Create document entry
                doc_entry = {
                    'id': chunk_id,
                    'text': text,
                    'metadata': metadata,
                    'keywords': keywords
                }
                
                # Check if document already exists (by ID)
                existing_ids = [doc['id'] for doc in self.documents]
                if chunk_id not in existing_ids:
                    self.documents.append(doc_entry)
                    added_count += 1
            
            # Save to file
            self._save_documents()
            
            self.logger.info(f"Added {added_count} chunks to simple vector database")
            
            return {
                "success": True, 
                "message": f"Successfully added {added_count} chunks", 
                "added_count": added_count
            }
            
        except Exception as e:
            error_msg = f"Error adding documents to simple vector database: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "message": error_msg, "added_count": 0}
    
    def similarity_search(self, 
                         query: str, 
                         n_results: int = 5,
                         filter_metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Perform keyword-based similarity search.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of search results with text, metadata, and similarity scores
        """
        try:
            if not self.documents:
                return []
            
            query_keywords = self._extract_keywords(query)
            
            if not query_keywords:
                return []
            
            # Calculate similarities
            results = []
            
            for doc in self.documents:
                # Apply metadata filter if provided
                if filter_metadata:
                    skip = False
                    for key, value in filter_metadata.items():
                        if key not in doc['metadata'] or str(doc['metadata'][key]) != str(value):
                            skip = True
                            break
                    if skip:
                        continue
                
                # Calculate similarity
                similarity = self._calculate_similarity(query_keywords, doc['keywords'])
                
                if similarity > 0:
                    result = {
                        'text': doc['text'],
                        'metadata': doc['metadata'],
                        'similarity_score': similarity,
                        'id': doc['id']
                    }
                    results.append(result)
            
            # Sort by similarity score (descending)
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Return top n_results
            results = results[:n_results]
            
            self.logger.info(f"Found {len(results)} results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            error_msg = f"Error performing similarity search: {str(e)}"
            self.logger.error(error_msg)
            return []
    
    def get_all_documents(self) -> List[Dict]:
        """
        Get all documents from the collection.
        
        Returns:
            List of all documents with metadata
        """
        try:
            return [
                {
                    'text': doc['text'],
                    'metadata': doc['metadata'],
                    'id': doc['id']
                }
                for doc in self.documents
            ]
        except Exception as e:
            error_msg = f"Error getting all documents: {str(e)}"
            self.logger.error(error_msg)
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            file_types = set()
            filenames = set()
            
            for doc in self.documents:
                metadata = doc.get('metadata', {})
                if 'file_type' in metadata:
                    file_types.add(metadata['file_type'])
                if 'filename' in metadata:
                    filenames.add(metadata['filename'])
            
            return {
                "total_chunks": len(self.documents),
                "file_types": list(file_types),
                "sample_filenames": list(filenames),
                "collection_name": self.collection_name,
                "embedding_model": "simple_keyword_based"
            }
            
        except Exception as e:
            error_msg = f"Error getting collection stats: {str(e)}"
            self.logger.error(error_msg)
            return {"error": error_msg}
    
    def clear_collection(self) -> bool:
        """
        Clear all documents from the collection.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.documents = []
            self._save_documents()
            
            self.logger.info(f"Cleared collection: {self.collection_name}")
            return True
            
        except Exception as e:
            error_msg = f"Error clearing collection: {str(e)}"
            self.logger.error(error_msg)
            return False
    
    def delete_by_filename(self, filename: str) -> bool:
        """
        Delete all chunks from a specific file.
        
        Args:
            filename: Name of the file to delete chunks from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            initial_count = len(self.documents)
            
            # Filter out documents with the specified filename
            self.documents = [
                doc for doc in self.documents 
                if doc.get('metadata', {}).get('filename') != filename
            ]
            
            deleted_count = initial_count - len(self.documents)
            
            # Save changes
            self._save_documents()
            
            self.logger.info(f"Deleted {deleted_count} chunks from file: {filename}")
            return True
                
        except Exception as e:
            error_msg = f"Error deleting chunks for file {filename}: {str(e)}"
            self.logger.error(error_msg)
            return False


# Alias for compatibility
VectorDatabase = SimpleVectorDatabase