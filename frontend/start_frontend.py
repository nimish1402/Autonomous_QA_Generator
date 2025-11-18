#!/usr/bin/env python3
"""
Startup script for Autonomous QA Agent Frontend
"""

import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Change to frontend directory
        frontend_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(frontend_dir)
        
        logger.info("Starting Autonomous QA Agent Frontend...")
        logger.info(f"Frontend directory: {frontend_dir}")
        
        # Run Streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd)
        
    except FileNotFoundError as e:
        logger.error(f"Streamlit not found: {e}")
        logger.error("Please install streamlit: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting frontend: {e}")
        sys.exit(1)