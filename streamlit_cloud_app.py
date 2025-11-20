"""
Cloud-Optimized Streamlit App for Autonomous QA Agent

This version is optimized for Streamlit Cloud deployment with embedded functionality
when backend is not available.
"""

import streamlit as st
import os
import sys
from pathlib import Path
import requests
import json
from typing import Dict, List, Any

# Add project paths
project_root = Path(__file__).parent
for path in [".", "frontend", "backend", "utils", "models", "config"]:
    sys.path.append(str(project_root / path))

# Environment configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

def check_backend_availability():
    """Check if backend is available"""
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Autonomous QA Agent",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check backend availability
    backend_available = check_backend_availability()
    
    if backend_available:
        # Import and run full application
        try:
            from frontend.app import main as app_main
            app_main()
        except ImportError:
            st.error("Frontend module not found. Please check deployment configuration.")
    else:
        # Show cloud deployment message
        show_cloud_deployment_info()

def show_cloud_deployment_info():
    """Show deployment information when backend is not available"""
    st.title("🤖 Autonomous QA Agent")
    st.markdown("## Streamlit Cloud Deployment")
    
    st.warning("""
    **Backend API Not Available**
    
    This Streamlit Cloud deployment requires a separate backend service to function fully.
    """)
    
    st.info("""
    **To complete the deployment:**
    
    1. **Deploy the backend** to Railway, Render, or Heroku
    2. **Set the BACKEND_URL** environment variable in Streamlit Cloud settings
    3. **Restart** the Streamlit app
    
    See the deployment guide in the repository for detailed instructions.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔧 Backend Deployment Options")
        st.markdown("""
        - **Railway**: [railway.app](https://railway.app) (Recommended)
        - **Render**: [render.com](https://render.com)
        - **Heroku**: [heroku.com](https://heroku.com)
        - **Google Cloud Run**: [cloud.google.com/run]
        """)
    
    with col2:
        st.markdown("### ⚙️ Environment Variables Needed")
        st.code("""
BACKEND_URL=https://your-backend.railway.app
GEMINI_API_KEY=your_api_key_here
ENVIRONMENT=production
        """)
    
    # Show current configuration
    st.markdown("### 📊 Current Configuration")
    config_data = {
        "Backend URL": BACKEND_URL,
        "Environment": ENVIRONMENT,
        "Backend Status": "❌ Not Available" if not check_backend_availability() else "✅ Available"
    }
    
    for key, value in config_data.items():
        st.write(f"**{key}**: {value}")
    
    # Test connection button
    if st.button("🔄 Test Backend Connection"):
        with st.spinner("Testing connection..."):
            if check_backend_availability():
                st.success("✅ Backend connection successful!")
                st.experimental_rerun()
            else:
                st.error("❌ Cannot connect to backend. Please check your configuration.")

if __name__ == "__main__":
    main()