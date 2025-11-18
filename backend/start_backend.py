#!/usr/bin/env python3
"""
Startup script for Autonomous QA Agent Backend
"""

import os
import sys
import logging

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Change to backend directory
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(backend_dir)
        
        logger.info("Starting Autonomous QA Agent Backend...")
        logger.info(f"Backend directory: {backend_dir}")
        logger.info(f"Project root: {project_root}")
        
        # Import and run the main application
        from main import app
        import uvicorn
        
        # Run the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,  # Set to True for development
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Please install required dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting backend: {e}")
        sys.exit(1)