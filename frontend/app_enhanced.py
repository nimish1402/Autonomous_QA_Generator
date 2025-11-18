"""
Enhanced Streamlit Frontend for Autonomous QA Agent
"""

import streamlit as st
import requests
import json
import pandas as pd
from typing import Dict, List, Any
import tempfile
import os
import time
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="🤖 Autonomous QA Agent",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"

# Enhanced CSS with adaptive theming
def inject_enhanced_css():
    """Inject comprehensive modern CSS with adaptive theming"""
    st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --info-color: #3b82f6;
        --bg-light: #ffffff;
        --text-light: #000000;
        --text-secondary: #000000;
        --text-dark: #000000;
        --border-light: #e5e7eb;
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --border-radius: 12px;
        --transition: all 0.3s ease;
    }
    
    /* Hide Streamlit Elements */
    .css-1d391kg {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-1v0mbdj > .block-container {padding-top: 1rem;}
    
    /* Base Typography */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main Container */
    .main .block-container {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius);
        margin: 1rem;
        box-shadow: var(--shadow-lg);
    }
    
    /* Hero Header */
    .hero-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        opacity: 0.9;
    }
    
    /* Interactive Cards */
    .enhanced-card {
        background: var(--bg-light);
        border: 2px solid var(--border-light);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        transition: var(--transition);
        color: #000000 !important;
    }
    
    .enhanced-card h4 {
        color: #000000 !important;
    }
    
    .enhanced-card p {
        color: #000000 !important;
    }
    
    .enhanced-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-color);
    }
    
    /* Status Cards */
    .success-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid var(--success-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        color: #065f46;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid var(--warning-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        color: #000000 !important;
    }
    
    .warning-card h4 {
        color: #000000 !important;
    }
    
    .warning-card p {
        color: #000000 !important;
    }
    
    .error-card {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border-left: 4px solid var(--error-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        color: #991b1b;
    }
    
    /* Test Case Cards */
    .test-case-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #e2e8f0;
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        transition: var(--transition);
        color: #000000 !important;
    }
    
    .test-case-card div {
        color: #000000 !important;
    }
    
    .test-case-card strong {
        color: #000000 !important;
    }
    
    .test-case-card span {
        color: #000000 !important;
    }
    
    .test-case-card:hover {
        transform: translateX(8px);
        border-color: var(--primary-color);
        box-shadow: var(--shadow-lg);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #ffffff !important;
    }
    
    .sidebar .sidebar-content {
        background-color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Sidebar text styling - Force all text to black */
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown div,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4 {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stMetric {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stMetric-value {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stMetric-label {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .element-container {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stAlert {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stSuccess {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stWarning {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stInfo {
        color: #000000 !important;
    }
    
    section[data-testid="stSidebar"] .stError {
        color: #000000 !important;
    }
    
    /* Progress Bar */
    .progress-container {
        background: #e5e7eb;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
        color: white;
    }
    
    .badge-primary { background: var(--primary-color); }
    .badge-success { background: var(--success-color); }
    .badge-warning { background: var(--warning-color); }
    .badge-info { background: var(--info-color); }
    
    /* Global text color overrides */
    .stMarkdown, .stText, .element-container {
        color: #000000 !important;
    }
    
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #000000 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #000000 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: transparent;
        border-radius: 8px;
        gap: 8px;
        padding: 12px 24px;
        font-weight: 500;
        border: 1px solid transparent;
        transition: all 0.3s ease;
        color: #000000 !important;
    }
    
    .stTabs [data-baseweb="tab"] * {
        color: #000000 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(74, 144, 226, 0.3) !important;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2) !important;
        color: #000000 !important;
    }
    
    .stTabs [aria-selected="true"] * {
        color: #000000 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
        color: #000000 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover * {
        color: #000000 !important;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .hero-title { font-size: 2rem; }
        .enhanced-card { padding: 1.5rem; margin: 1rem 0; }
        .main .block-container { margin: 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize CSS
inject_enhanced_css()

def check_backend_status():
    """Check if the backend is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def create_progress_indicator(current_step, total_steps, step_names):
    """Create an animated progress indicator"""
    progress = current_step / total_steps
    st.markdown(f"""
    <div style="margin: 2rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 600; color: #000000;">Progress: Step {current_step} of {total_steps}</span>
            <span style="font-weight: 600; color: var(--primary-color);">{int(progress * 100)}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress * 100}%;"></div>
        </div>
        <div style="font-size: 0.875rem; color: #000000; margin-top: 0.5rem;">
            📍 {step_names[current_step - 1] if current_step <= len(step_names) else 'Complete'}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_feature_showcase():
    """Create an interactive feature showcase"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="enhanced-card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
            <h4 style="color: var(--primary-color); margin-bottom: 0.5rem;">Smart Upload</h4>
            <p style="color: #000000; font-size: 0.875rem;">AI-powered document processing</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="enhanced-card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
            <h4 style="color: var(--success-color); margin-bottom: 0.5rem;">AI Generation</h4>
            <p style="color: #000000; font-size: 0.875rem;">Context-aware test cases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="enhanced-card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h4 style="color: var(--secondary-color); margin-bottom: 0.5rem;">Automation</h4>
            <p style="color: #000000; font-size: 0.875rem;">Ready Selenium scripts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="enhanced-card" style="text-align: center; cursor: pointer;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h4 style="color: var(--info-color); margin-bottom: 0.5rem;">Analytics</h4>
            <p style="color: #000000; font-size: 0.875rem;">Real-time insights</p>
        </div>
        """, unsafe_allow_html=True)

def upload_files_to_backend(uploaded_files, clear_existing=False):
    """Upload files to the backend for processing."""
    files = []
    for uploaded_file in uploaded_files:
        files.append(('files', (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)))
    
    data = {'clear_existing': clear_existing}
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/ingest",
            files=files,
            data=data,
            timeout=60
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error uploading files: {str(e)}")
        return None

def generate_test_cases(query):
    """Generate test cases from a query."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate_testcases",
            json={"query": query},
            timeout=60
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating test cases: {str(e)}")
        return None

def generate_selenium_script(test_case):
    """Generate Selenium script from test case."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate_script",
            json={"test_case": test_case},
            timeout=60
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating script: {str(e)}")
        return None

def display_test_case(test_case, index):
    """Display a test case in an enhanced card"""
    test_type = test_case.get('Type', 'N/A')
    type_color = 'var(--success-color)' if test_type == 'Positive' else 'var(--warning-color)'
    
    st.markdown(f"""
    <div class="test-case-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="color: var(--primary-color); margin: 0;">🧪 Test Case {index}: {test_case.get('Test_ID', 'N/A')}</h4>
            <span class="badge" style="background: {type_color};">{test_type}</span>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>🎯 Feature:</strong> {test_case.get('Feature', 'N/A')}
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>📝 Scenario:</strong><br>
            <span style="color: #000000;">{test_case.get('Test_Scenario', 'N/A')}</span>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <strong>✅ Expected Result:</strong><br>
            <span style="color: #000000;">{test_case.get('Expected_Result', 'N/A')}</span>
        </div>
        
        <div>
            <strong>📚 Source:</strong>
            <code style="background: #f3f4f6; padding: 0.25rem; border-radius: 4px;">{test_case.get('Grounded_In', 'NOT SPECIFIED')}</code>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Steps in expandable section
    steps = test_case.get('Steps', [])
    if steps:
        with st.expander(f"📋 View Test Steps ({len(steps)} steps)"):
            for i, step in enumerate(steps, 1):
                st.write(f"**Step {i}:** {step}")
    
    # Notes
    notes = test_case.get('Notes', '')
    if notes:
        with st.expander("📌 Additional Notes"):
            st.info(notes)

def main():
    """Enhanced main application"""
    
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🤖 Autonomous QA Agent</h1>
        <p class="hero-subtitle">AI-Powered Test Case Generation & Selenium Automation Platform</p>
        <div style="margin-top: 2rem;">
            <span class="badge badge-primary">✨ AI-Powered</span>
            <span class="badge badge-success">🔍 Context-Grounded</span>
            <span class="badge badge-info">⚡ Automated</span>
            <span class="badge badge-warning">📊 Analytics-Ready</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Showcase
    st.markdown("### 🚀 Platform Capabilities")
    create_feature_showcase()
    
    # Backend Status Check
    if not check_backend_status():
        st.markdown("""
        <div class="error-card">
            <h3>🚨 Backend Connection Required</h3>
            <p>The FastAPI backend server is not running. Please start it first:</p>
            <div style="background: #1f2937; color: #f9fafb; padding: 1rem; border-radius: 6px; margin: 1rem 0; font-family: monospace;">
                cd backend && python main.py
            </div>
            <p>Then refresh this page to continue.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Enhanced Sidebar
    with st.sidebar:
        st.markdown("## 📊 System Dashboard")
        
        try:
            status_response = requests.get(f"{BACKEND_URL}/status")
            if status_response.status_code == 200:
                status_data = status_response.json()
                
                st.success("✅ Backend Connected")
                
                db_stats = status_data.get('database', {})
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("📊 Total Chunks", db_stats.get('total_chunks', 0))
                
                with col2:
                    file_types = db_stats.get('file_types', [])
                    st.metric("📁 File Types", len(file_types))
                
                # LLM Status
                llm_status = status_data.get('llm', {})
                provider = llm_status.get('provider', 'Template')
                api_available = llm_status.get('api_available', False)
                
                if api_available:
                    st.success(f"🤖 {provider} Active")
                else:
                    st.warning("⚠️ Template Mode")
                
                # Checkout Status
                checkout_loaded = status_data.get('checkout_html_loaded', False)
                if checkout_loaded:
                    st.success("🌐 Checkout HTML Ready")
                else:
                    st.info("ℹ️ No Checkout HTML")
        except:
            st.error("❌ Backend Connection Failed")
    
    # Interactive Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload Documents", "🧪 Generate Tests", "🤖 Create Scripts", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 📄 Smart Document Processing")
        create_progress_indicator(1, 3, ["Upload Documents", "Generate Tests", "Download Scripts"])
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="enhanced-card">
                <h4 style="color: var(--primary-color);">📋 Upload Requirements</h4>
                <ul style="color: #000000;">
                    <li>✅ 3-5 support documents (MD, TXT, PDF, JSON)</li>
                    <li>🌐 1 checkout.html file (for e-commerce testing)</li>
                    <li>📏 Max file size: 10MB per file</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_files = st.file_uploader(
                "🎯 Drop files here or click to browse",
                type=['md', 'txt', 'pdf', 'json', 'html'],
                accept_multiple_files=True,
                help="Upload your documentation and HTML files"
            )
            
            if uploaded_files:
                st.markdown("### 🔍 File Preview")
                for file in uploaded_files[:3]:
                    file_icon = {'text/markdown': '📝', 'text/plain': '📄', 'application/pdf': '📕', 
                               'application/json': '📊', 'text/html': '🌐'}.get(file.type, '📄')
                    st.info(f"{file_icon} {file.name} ({file.size:,} bytes)")
        
        with col2:
            st.markdown("### ⚙️ Configuration")
            
            clear_existing = st.checkbox("🗑️ Clear Existing Data")
            
            if uploaded_files:
                st.markdown("""
                <div class="success-card">
                    <h4>🚀 Ready to Build</h4>
                    <p>Files loaded and ready to process</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="warning-card">
                    <h4>⚠️ Files Required</h4>
                    <p>Upload documents to continue</p>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🚀 Build Knowledge Base", type="primary", disabled=not uploaded_files):
                with st.spinner("Processing documents..."):
                    result = upload_files_to_backend(uploaded_files, clear_existing)
                
                if result and result.get('success'):
                    st.balloons()
                    st.success("✅ Knowledge base built successfully!")
                    st.session_state.knowledge_base_built = True
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("📊 Chunks", result.get('total_chunks', 0))
                    with col_b:
                        st.metric("📁 Files", len(result.get('files_processed', [])))
                else:
                    st.error("❌ Failed to build knowledge base")
    
    with tab2:
        st.markdown("### 🧪 AI-Powered Test Generation")
        
        kb_built = st.session_state.get('knowledge_base_built', False)
        
        if kb_built:
            create_progress_indicator(2, 3, ["Upload Documents", "Generate Tests", "Download Scripts"])
        
        if not kb_built:
            st.markdown("""
            <div class="warning-card">
                <h4>⚠️ Knowledge Base Required</h4>
                <p>Please upload and process documents first</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            query = st.text_area(
                "Enter your test generation query:",
                placeholder="e.g., Generate positive and negative test cases for the discount code feature",
                height=100
            )
            
            if st.button("🚀 Generate Test Cases", type="primary", disabled=not query):
                with st.spinner("AI is generating test cases..."):
                    result = generate_test_cases(query)
                
                if result and result.get('success'):
                    test_cases = result.get('test_cases', [])
                    st.balloons()
                    st.success(f"✅ Generated {len(test_cases)} test cases")
                    
                    st.session_state.generated_test_cases = test_cases
                    
                    for i, test_case in enumerate(test_cases, 1):
                        display_test_case(test_case, i)
                else:
                    st.error("❌ Failed to generate test cases")
            
            # Show existing test cases
            if st.session_state.get('generated_test_cases'):
                st.markdown("### 📋 Generated Test Cases")
                for i, tc in enumerate(st.session_state.generated_test_cases, 1):
                    display_test_case(tc, i)
    
    with tab3:
        st.markdown("### 🤖 Selenium Script Generation")
        
        test_cases = st.session_state.get('generated_test_cases', [])
        
        if not test_cases:
            st.markdown("""
            <div class="warning-card">
                <h4>⚠️ Test Cases Required</h4>
                <p>Please generate test cases first</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            create_progress_indicator(3, 3, ["Upload Documents", "Generate Tests", "Download Scripts"])
            
            # Test case selection
            test_options = [f"TC{i+1}: {tc.get('Feature', 'Unknown')} - {tc.get('Test_Scenario', 'Unknown')[:50]}" 
                          for i, tc in enumerate(test_cases)]
            
            selected_idx = st.selectbox("Select test case:", range(len(test_options)), 
                                      format_func=lambda x: test_options[x])
            
            selected_tc = test_cases[selected_idx]
            
            # Preview selected test case
            st.markdown("### 👀 Selected Test Case")
            display_test_case(selected_tc, selected_idx + 1)
            
            if st.button("🐍 Generate Selenium Script", type="primary"):
                with st.spinner("Generating Selenium script..."):
                    result = generate_selenium_script(selected_tc)
                
                if result and result.get('success'):
                    st.success("✅ Selenium script generated!")
                    
                    script_content = result.get('script_content', '')
                    filename = result.get('filename', 'test_script.py')
                    
                    st.markdown("### 🐍 Generated Script")
                    st.code(script_content, language='python')
                    
                    st.download_button(
                        "💾 Download Script",
                        script_content,
                        filename,
                        "text/plain"
                    )
                else:
                    st.error("❌ Failed to generate script")
    
    with tab4:
        st.markdown("### 📊 Analytics Dashboard")
        
        try:
            status_response = requests.get(f"{BACKEND_URL}/status")
            if status_response.status_code == 200:
                status_data = status_response.json()
                
                # System metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    db_stats = status_data.get('database', {})
                    st.metric("📊 Knowledge Base", f"{db_stats.get('total_chunks', 0)} chunks")
                
                with col2:
                    test_cases = st.session_state.get('generated_test_cases', [])
                    st.metric("🧪 Test Cases", len(test_cases))
                
                with col3:
                    llm_status = status_data.get('llm', {})
                    provider = llm_status.get('provider', 'Template')
                    st.metric("🤖 LLM Provider", provider)
                
                # Activity log
                st.markdown("### 📋 Session Activity")
                activities = []
                if st.session_state.get('knowledge_base_built'):
                    activities.append("✅ Knowledge base built")
                if test_cases:
                    activities.append(f"🧪 Generated {len(test_cases)} test cases")
                
                if activities:
                    for activity in activities:
                        st.success(activity)
                else:
                    st.info("No activities in current session")
        except:
            st.error("❌ Unable to load analytics")

if __name__ == "__main__":
    # Initialize session state
    if 'knowledge_base_built' not in st.session_state:
        st.session_state.knowledge_base_built = False
    if 'generated_test_cases' not in st.session_state:
        st.session_state.generated_test_cases = []
    
    main()