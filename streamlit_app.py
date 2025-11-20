"""
Streamlit Cloud Entry Point for Autonomous QA Agent

This file serves as the main entry point for Streamlit Cloud deployment.
It imports and runs the main Streamlit application from the frontend directory.
"""

import sys
import os
from pathlib import Path

# Add project directories to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "frontend"))
sys.path.append(str(project_root / "backend"))
sys.path.append(str(project_root / "utils"))
sys.path.append(str(project_root / "models"))
sys.path.append(str(project_root / "config"))

# Import and run the main Streamlit app
from frontend.app import main

if __name__ == "__main__":
    main()