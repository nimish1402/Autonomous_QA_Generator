"""
Vector Database Module for Autonomous QA Agent

This module handles vector database operations using Chroma for storing embeddings
and metadata with semantic similarity search capabilities.
"""

import os
import logging
from typing import Dict, List, Optional, Any
import json
from pathlib import Path

try:
    import chromadb
    from chromadb.config import Settings
    from chromadb.utils import embedding_functions
except ImportError:
    chromadb = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class VectorDatabase:
    """
    Vector database implementation using Chroma for storing document embeddings
    and performing semantic similarity searches.
    """
    
    def __init__(self, 
                 persist_directory: str = "./vectordb",
                 collection_name: str = "qa_documents",
                 embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the vector database.
        
        Args:
            persist_directory: Directory to persist the database
            collection_name: Name of the collection
            embedding_model_name: Name of the sentence transformer model
        """
        if chromadb is None:
            raise ImportError("chromadb is required. Install with: pip install chromadb")
        
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required. Install with: pip install sentence-transformers")
        
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model_name
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize Chroma client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model_name)
        
        # Create embedding function for Chroma
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model_name
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        except ValueError:
            # Collection doesn't exist, create it
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        
        self.logger = logging.getLogger(__name__)
    
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
            # Prepare data for Chroma
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                text = chunk.get('text', '').strip()
                metadata = chunk.get('metadata', {})
                
                if not text:
                    continue
                
                # Generate unique ID
                chunk_id = f"{metadata.get('filename', 'unknown')}_{metadata.get('chunk_index', i)}"
                
                # Ensure metadata values are strings (Chroma requirement)
                clean_metadata = {}
                for key, value in metadata.items():
                    if value is not None:
                        clean_metadata[key] = str(value)
                
                documents.append(text)
                metadatas.append(clean_metadata)
                ids.append(chunk_id)
            
            if not documents:
                return {"success": False, "message": "No valid documents to add", "added_count": 0}
            
            # Add to collection
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Added {len(documents)} chunks to vector database")
            
            return {
                "success": True, 
                "message": f"Successfully added {len(documents)} chunks", 
                "added_count": len(documents)
            }
            
        except Exception as e:
            error_msg = f"Error adding documents to vector database: {str(e)}"
            self.logger.error(error_msg)
            return {"success": False, "message": error_msg, "added_count": 0}
    
    def similarity_search(self, 
                         query: str, 
                         n_results: int = 5,
                         filter_metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Perform semantic similarity search.
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_metadata: Optional metadata filter
            
        Returns:
            List of search results with text, metadata, and similarity scores
        """
        try:
            # Perform search
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            
            if results['documents'] and results['documents'][0]:
                documents = results['documents'][0]
                metadatas = results['metadatas'][0] if results['metadatas'] else []
                distances = results['distances'][0] if results['distances'] else []
                ids = results['ids'][0] if results['ids'] else []
                
                for i in range(len(documents)):
                    result = {
                        'text': documents[i],
                        'metadata': metadatas[i] if i < len(metadatas) else {},
                        'similarity_score': 1 - distances[i] if i < len(distances) else 0.0,
                        'id': ids[i] if i < len(ids) else f"result_{i}"
                    }
                    formatted_results.append(result)
            
            self.logger.info(f"Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
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
            # Get all documents
            results = self.collection.get()
            
            formatted_results = []
            
            if results['documents']:
                documents = results['documents']
                metadatas = results['metadatas'] if results['metadatas'] else []
                ids = results['ids'] if results['ids'] else []
                
                for i in range(len(documents)):
                    result = {
                        'text': documents[i],
                        'metadata': metadatas[i] if i < len(metadatas) else {},
                        'id': ids[i] if i < len(ids) else f"doc_{i}"
                    }
                    formatted_results.append(result)
            
            return formatted_results
            
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
            count = self.collection.count()
            
            # Get sample of documents to analyze
            sample_results = self.collection.get(limit=10)
            
            file_types = set()
            filenames = set()
            
            if sample_results['metadatas']:
                for metadata in sample_results['metadatas']:
                    if 'file_type' in metadata:
                        file_types.add(metadata['file_type'])
                    if 'filename' in metadata:
                        filenames.add(metadata['filename'])
            
            return {
                "total_chunks": count,
                "file_types": list(file_types),
                "sample_filenames": list(filenames),
                "collection_name": self.collection_name,
                "embedding_model": self.embedding_model_name
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
            # Delete the collection and recreate it
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
            
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
            # Query for documents with the specified filename
            results = self.collection.get(
                where={"filename": filename}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                self.logger.info(f"Deleted {len(results['ids'])} chunks from file: {filename}")
                return True
            else:
                self.logger.info(f"No chunks found for file: {filename}")
                return True
                
        except Exception as e:
            error_msg = f"Error deleting chunks for file {filename}: {str(e)}"
            self.logger.error(error_msg)
            return False


class EmbeddingGenerator:
    """
    Standalone embedding generator for cases where direct embedding generation is needed.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required. Install with: pip install sentence-transformers")
        
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")
    
    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text string
            
        Returns:
            Embedding vector
        """
        return self.generate_embeddings([text])[0]