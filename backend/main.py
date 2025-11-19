"""
FastAPI Backend for Autonomous QA Agent

This module provides REST API endpoints for document ingestion, test case generation,
and Selenium script generation with strict grounding enforcement.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import json
import os
import tempfile
import asyncio
from pathlib import Path

# Load environment variables from parent directory
from dotenv import load_dotenv
parent_dir = Path(__file__).parent.parent
env_file = parent_dir / '.env'
if env_file.exists():
    load_dotenv(env_file)
    print(f"Loaded environment from {env_file}")

# Import our custom modules
import sys
sys.path.append(str(parent_dir))

from utils.document_parser import DocumentParser, TextChunker
from utils.vector_database import VectorDatabase
from models.llm_agent import TestCaseGenerator, SeleniumScriptGenerator
from utils.html_parser import HTMLParser
try:
    from utils.llm_client import llm_client
    from config.llm_config import llm_config
    LLM_CLIENT_AVAILABLE = True
except ImportError:
    LLM_CLIENT_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Autonomous QA Agent API",
    description="API for generating context-grounded test cases and Selenium automation scripts",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_parser = DocumentParser()
text_chunker = TextChunker(chunk_size=1000, overlap=200)
vector_db = VectorDatabase(persist_directory="./vectordb")

# Log which vector database implementation is being used
vector_db_type = type(vector_db).__name__
if hasattr(vector_db, 'embedding_model_name'):
    logger.info(f"🧠 Using ChromaDB with semantic embeddings (model: {vector_db.embedding_model_name})")
else:
    logger.info(f"🔤 Using SimpleVectorDatabase with keyword matching")

test_case_generator = TestCaseGenerator()
selenium_generator = SeleniumScriptGenerator()
html_parser = HTMLParser()

# Global variables to store checkout HTML
checkout_html_content = None
checkout_dom_info = None


# Pydantic models for request/response
class IngestResponse(BaseModel):
    success: bool
    message: str
    total_chunks: int
    files_processed: List[str]


class GenerateTestCasesRequest(BaseModel):
    query: str


class GenerateTestCasesResponse(BaseModel):
    success: bool
    test_cases: List[Dict[str, Any]]
    grounded_sources: List[str]
    message: str


class GenerateScriptRequest(BaseModel):
    test_case: Dict[str, Any]


class GenerateScriptResponse(BaseModel):
    success: bool
    script_content: str
    filename: str
    message: str


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Autonomous QA Agent API",
        "version": "1.0.0",
        "endpoints": {
            "ingest": "POST /ingest - Upload and process documents",
            "generate_testcases": "POST /generate_testcases - Generate test cases from query",
            "generate_script": "POST /generate_script - Generate Selenium script from test case",
            "status": "GET /status - Get system status"
        }
    }


@app.get("/status")
async def get_status():
    """Get system status and database statistics."""
    try:
        db_stats = vector_db.get_collection_stats()
        
        # Get LLM status
        llm_status = {"provider": "template-based", "api_available": False}
        if LLM_CLIENT_AVAILABLE:
            llm_status = llm_client.get_status()
        
        # Detect vector database type
        vector_db_info = {
            "type": type(vector_db).__name__,
            "implementation": "ChromaDB (semantic embeddings)" if hasattr(vector_db, 'embedding_model_name') else "SimpleVectorDatabase (keyword matching)",
            "model": getattr(vector_db, 'embedding_model_name', 'keyword-based'),
            "search_method": "semantic similarity" if hasattr(vector_db, 'embedding_model_name') else "keyword overlap"
        }

        return {
            "status": "healthy",
            "database": db_stats,
            "vector_database": vector_db_info,
            "checkout_html_loaded": checkout_html_content is not None,
            "llm": llm_status,
            "components": {
                "document_parser": "active",
                "vector_database": f"active ({vector_db_info['implementation']})",
                "test_case_generator": "active",
                "selenium_generator": "active",
                "llm_client": "active" if LLM_CLIENT_AVAILABLE else "template-only"
            }
        }
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }


@app.post("/ingest", response_model=IngestResponse)
async def ingest_documents(
    files: List[UploadFile] = File(...),
    clear_existing: bool = Form(False)
):
    """
    Ingest documents and build knowledge base.
    
    Accepts multiple files (MD, TXT, PDF, JSON, HTML) and one checkout.html file.
    Processes them into chunks and stores in vector database.
    """
    global checkout_html_content, checkout_dom_info
    
    try:
        if clear_existing:
            vector_db.clear_collection()
            logger.info("Cleared existing collection")
        
        all_chunks = []
        processed_files = []
        
        for file in files:
            logger.info(f"Processing file: {file.filename}")
            
            # Read file content
            content = await file.read()
            
            # Handle checkout.html separately
            if file.filename and 'checkout' in file.filename.lower() and file.filename.endswith('.html'):
                checkout_html_content = content.decode('utf-8')
                checkout_dom_info = html_parser.parse_html(checkout_html_content)
                logger.info(f"Loaded checkout HTML with {len(checkout_dom_info['selectors'])} selectors")
                
                # Also process it as a regular document
                parsed_doc = document_parser.parse_file(file.filename, checkout_html_content)
                chunks = text_chunker.chunk_text(parsed_doc['text'], parsed_doc['metadata'])
                all_chunks.extend(chunks)
                processed_files.append(file.filename)
                continue
            
            # Determine file type and process
            file_extension = Path(file.filename).suffix.lower() if file.filename else '.txt'
            
            try:
                if file_extension == '.pdf':
                    parsed_doc = document_parser.parse_file(file.filename or 'uploaded.pdf', content)
                else:
                    content_str = content.decode('utf-8')
                    parsed_doc = document_parser.parse_file(file.filename or f'uploaded{file_extension}', content_str)
                
                # Create chunks
                chunks = text_chunker.chunk_text(parsed_doc['text'], parsed_doc['metadata'])
                all_chunks.extend(chunks)
                processed_files.append(file.filename or f'uploaded{file_extension}')
                
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {str(e)}")
                continue
        
        # Store chunks in vector database
        if all_chunks:
            result = vector_db.add_documents(all_chunks)
            
            if result['success']:
                return IngestResponse(
                    success=True,
                    message=f"Knowledge Base Built Successfully. Processed {len(processed_files)} files.",
                    total_chunks=result['added_count'],
                    files_processed=processed_files
                )
            else:
                raise HTTPException(status_code=500, detail=f"Error storing documents: {result['message']}")
        else:
            raise HTTPException(status_code=400, detail="No valid documents to process")
            
    except Exception as e:
        logger.error(f"Error in ingest_documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_testcases", response_model=GenerateTestCasesResponse)
async def generate_test_cases(request: GenerateTestCasesRequest):
    """
    Generate test cases based on a query.
    
    Retrieves relevant documents from vector database and generates
    structured test cases with strict grounding.
    """
    try:
        if not request.query or request.query.strip() == "":
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Perform semantic search
        search_results = vector_db.similarity_search(request.query, n_results=10)
        
        if not search_results:
            raise HTTPException(status_code=404, detail="No relevant documents found for the query")
        
        # Generate test cases using LLM agent
        test_cases = await test_case_generator.generate_test_cases(
            query=request.query,
            retrieved_chunks=search_results,
            checkout_dom=checkout_dom_info
        )
        
        # If LLM generation fails, always have template fallback
        if not test_cases:
            logger.info("LLM generation failed, using template fallback")
            grounded_info = test_case_generator._extract_grounded_info(search_results)
            ui_elements = test_case_generator._extract_ui_elements(checkout_dom_info) if checkout_dom_info else {}
            test_cases = test_case_generator._generate_test_cases_from_context(
                query=request.query,
                grounded_info=grounded_info,
                ui_elements=ui_elements
            )
        
        if not test_cases:
            raise HTTPException(status_code=500, detail="Failed to generate test cases")
        
        # Extract grounded sources
        grounded_sources = list(set([
            chunk['metadata'].get('filename', 'Unknown')
            for chunk in search_results
        ]))
        
        return GenerateTestCasesResponse(
            success=True,
            test_cases=test_cases,
            grounded_sources=grounded_sources,
            message=f"Generated {len(test_cases)} test cases from {len(grounded_sources)} source documents"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating test cases: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_script", response_model=GenerateScriptResponse)
async def generate_selenium_script(request: GenerateScriptRequest):
    """
    Generate Selenium Python script for a selected test case.
    
    Creates a runnable Selenium script with proper selectors and assertions
    based on the provided test case and checkout.html DOM.
    """
    try:
        if not request.test_case:
            raise HTTPException(status_code=400, detail="Test case cannot be empty")
        
        if not checkout_html_content or not checkout_dom_info:
            raise HTTPException(status_code=400, detail="Checkout HTML not loaded. Please upload checkout.html first.")
        
        # Retrieve relevant context for the test case
        feature = request.test_case.get('Feature', '')
        scenario = request.test_case.get('Test_Scenario', '')
        search_query = f"{feature} {scenario}"
        
        context_results = vector_db.similarity_search(search_query, n_results=5)
        
        # Generate Selenium script
        script_content = await selenium_generator.generate_script(
            test_case=request.test_case,
            checkout_html=checkout_html_content,
            dom_info=checkout_dom_info,
            context_chunks=context_results
        )
        
        if not script_content:
            raise HTTPException(status_code=500, detail="Failed to generate Selenium script")
        
        # Generate filename
        test_id = request.test_case.get('Test_ID', 'test')
        feature = request.test_case.get('Feature', 'feature')
        filename = f"test_{test_id}_{feature.lower().replace(' ', '_')}.py"
        
        return GenerateScriptResponse(
            success=True,
            script_content=script_content,
            filename=filename,
            message=f"Generated Selenium script: {filename}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating Selenium script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/clear_database")
async def clear_database():
    """Clear the vector database."""
    try:
        success = vector_db.clear_collection()
        
        if success:
            return {"success": True, "message": "Database cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear database")
            
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search/{query}")
async def search_documents(query: str, limit: int = 5):
    """Search documents in the vector database."""
    try:
        results = vector_db.similarity_search(query, n_results=limit)
        
        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )