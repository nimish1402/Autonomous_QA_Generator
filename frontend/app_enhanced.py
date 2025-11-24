"""
Modern Streamlit Frontend for Autonomous QA Agent
Clean, minimalist UI with enhanced code display
"""

import streamlit as st
import requests
import json
import os

# Configure page
st.set_page_config(
    page_title="🤖 Autonomous QA Agent",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Modern CSS
def inject_modern_css():
    """Inject modern, clean CSS"""
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables */
    :root {
        --primary: #3B82F6;
        --primary-dark: #2563EB;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --text-primary: #000000;
        --text-secondary: #4B5563;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F9FAFB;
        --border: #E5E7EB;
    }
    
    /* Dark mode */
    [data-theme="dark"], 
    .stApp[style*="background-color: rgb(14, 17, 23)"],
    .stApp[style*="background-color: #0e1117"] {
        --primary: #60A5FA;
        --primary-dark: #3B82F6;
        --success: #34D399;
        --warning: #FBBF24;
        --error: #F87171;
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --bg-primary: #1F2937;
        --bg-secondary: #111827;
        --border: #374151;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Base */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg-secondary);
    }
    
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    p, span, div {
        color: var(--text-secondary) !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-primary) !important;
        border-right: 1px solid var(--border);
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: var(--bg-primary) !important;
        padding: 2rem 1rem;
    }
    
    /* Cards */
    .modern-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.2s ease;
    }
    
    .modern-card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Test Case Cards - Enhanced with borders */
    .test-card {
        background: var(--bg-primary);
        border: 2px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .test-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--border);
    }
    
    .test-badge {
        padding: 0.375rem 0.875rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        color: white;
    }
    
    .badge-positive { background: var(--success); }
    .badge-negative { background: var(--warning); }
    
    /* Code Blocks - Enhanced with syntax highlighting appearance */
    .stCodeBlock {
        background: #0D1117 !important;
        border: 2px solid #30363D !important;
        border-radius: 8px !important;
        margin: 1.5rem 0 !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2) !important;
        overflow: hidden !important;
    }
    
    [data-testid="stCodeBlock"] {
        background: #0D1117 !important;
        border: 2px solid #30363D !important;
        border-radius: 8px !important;
        margin: 1.5rem 0 !important;
    }
    
    /* Code header/title bar */
    .stCodeBlock::before {
        content: 'Python Script';
        display: block;
        background: #161B22;
        color: #8B949E;
        padding: 0.5rem 1rem;
        font-size: 0.75rem;
        font-weight: 600;
        border-bottom: 1px solid #30363D;
    }
    
    code {
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
    }
    
    pre {
        background: #0D1117 !important;
        padding: 1.5rem !important;
        border-radius: 0 0 6px 6px !important;
        overflow-x: auto !important;
        margin: 0 !important;
    }
    
    pre code {
        background: transparent !important;
        color: #E6EDF3 !important;
    }
    
    /* Scrollbar for code blocks */
    pre::-webkit-scrollbar {
        height: 8px;
    }
    
    pre::-webkit-scrollbar-track {
        background: #161B22;
        border-radius: 4px;
    }
    
    pre::-webkit-scrollbar-thumb {
        background: #30363D;
        border-radius: 4px;
    }
    
    pre::-webkit-scrollbar-thumb:hover {
        background: #484F58;
    }
    
    /* Inline code */
    :not(pre) > code {
        background: #F6F8FA !important;
        color: #24292F !important;
        padding: 0.2rem 0.5rem !important;
        border-radius: 4px !important;
        border: 1px solid #D0D7DE !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 600 !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: translateY(-1px);
    }
    
    .stButton > button p {
        color: #FFFFFF !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 0 1.5rem;
        font-weight: 500;
        color: var(--text-secondary) !important;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom-color: var(--primary) !important;
        color: var(--primary) !important;
    }
    
    .stTabs [aria-selected="true"] * {
        color: var(--primary) !important;
    }
    
    /* File Uploader */
    .stFileUploader {
        background: var(--bg-secondary);
        border: 2px dashed var(--border);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Metrics */
    .stMetric {
        background: var(--bg-primary);
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid var(--border);
    }
    
    /* Status indicators */
    .status-success {
        background: #ECFDF5;
        border-left: 3px solid var(--success);
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    .status-warning {
        background: #FFFBEB;
        border-left: 3px solid var(--warning);
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    .status-error {
        background: #FEF2F2;
        border-left: 3px solid var(--error);
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    /* Feature Grid */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-item {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .feature-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: var(--primary);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary) !important;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        font-size: 0.875rem;
        color: var(--text-secondary) !important;
    }
    
    /* Workflow */
    .workflow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 2rem;
        background: var(--bg-primary);
        border-radius: 8px;
        border: 1px solid var(--border);
    }
    
    .workflow-step {
        flex: 1;
        text-align: center;
        position: relative;
    }
    
    .workflow-step:not(:last-child)::after {
        content: '→';
        position: absolute;
        right: -20px;
        top: 20px;
        color: var(--primary);
        font-size: 1.5rem;
    }
    
    .workflow-number {
        width: 40px;
        height: 40px;
        background: var(--primary);
        color: white;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Hero */
    .hero {
        text-align: center;
        padding: 3rem 0;
        margin-bottom: 2rem;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary) !important;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .hero-title {
            font-size: 2rem;
        }
        
        .workflow {
            flex-direction: column;
        }
        
        .workflow-step:not(:last-child)::after {
            content: '↓';
            right: auto;
            top: auto;
            bottom: -30px;
        }
    }
</style>
""", unsafe_allow_html=True)

# DO NOT call inject_modern_css() here - it will be called in main()


def check_backend_status():
    """Check if the backend is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=5)
        return response.status_code == 200, response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return False, None

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
    """Display a test case in a modern card with enhanced borders"""
    test_type = test_case.get('Type', 'N/A')
    badge_class = 'badge-positive' if test_type == 'Positive' else 'badge-negative'
    
    st.markdown(f"""
    <div class="test-card">
        <div class="test-card-header">
            <h4 style="margin: 0; color: var(--text-primary); font-size: 1.125rem;">🧪 {test_case.get('Test_ID', 'N/A')} - {test_case.get('Feature', 'N/A')}</h4>
            <span class="test-badge {badge_class}">{test_type}</span>
        </div>
        <div style="margin-bottom: 1rem; padding: 0.75rem; background: var(--bg-secondary); border-radius: 6px; border-left: 3px solid var(--primary);">
            <strong style="color: var(--text-primary); font-size: 0.875rem;">📝 Scenario:</strong>
            <p style="margin: 0.5rem 0 0 0; color: var(--text-primary);">{test_case.get('Test_Scenario', 'N/A')}</p>
        </div>
        <div style="margin-bottom: 1rem; padding: 0.75rem; background: var(--bg-secondary); border-radius: 6px; border-left: 3px solid var(--success);">
            <strong style="color: var(--text-primary); font-size: 0.875rem;">✅ Expected Result:</strong>
            <p style="margin: 0.5rem 0 0 0; color: var(--text-primary);">{test_case.get('Expected_Result', 'N/A')}</p>
        </div>
        <div style="padding: 0.5rem 0.75rem; background: var(--bg-secondary); border-radius: 6px;">
            <strong style="color: var(--text-primary); font-size: 0.875rem;">📚 Source:</strong>
            <code style="background: var(--bg-primary); padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.875rem; margin-left: 0.5rem;">{test_case.get('Grounded_In', 'NOT SPECIFIED')}</code>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Steps in expandable section
    steps = test_case.get('Steps', [])
    if steps:
        with st.expander(f"📋 View Test Steps ({len(steps)} steps)"):
            for i, step in enumerate(steps, 1):
                st.markdown(f"**{i}.** {step}")
    
    # Notes
    notes = test_case.get('Notes', '')
    if notes:
        with st.expander("📌 Additional Notes"):
            st.info(notes)

def render_home_screen():
    """Render the home/welcome screen"""
    st.markdown("""
    <div class="hero">
        <h1 class="hero-title">🤖 Autonomous QA Agent</h1>
        <p class="hero-subtitle">Transform your documentation into comprehensive test cases and automation scripts using AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("### ✨ Key Features")
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-item">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Smart Document Processing</div>
            <div class="feature-desc">Upload MD, TXT, PDF, JSON, and HTML files for intelligent analysis</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI-Powered Generation</div>
            <div class="feature-desc">Context-aware test cases using Google Gemini AI</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Semantic Search</div>
            <div class="feature-desc">Vector database for accurate document retrieval</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">Selenium Automation</div>
            <div class="feature-desc">Ready-to-run Python test scripts generated automatically</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How it works
    st.markdown("### 🔄 How It Works")
    st.markdown("""
    <div class="workflow">
        <div class="workflow-step">
            <div class="workflow-number">1</div>
            <div class="workflow-title">Upload</div>
            <div class="workflow-desc">Add your documentation files</div>
        </div>
        <div class="workflow-step">
            <div class="workflow-number">2</div>
            <div class="workflow-title">Process</div>
            <div class="workflow-desc">AI analyzes and indexes content</div>
        </div>
        <div class="workflow-step">
            <div class="workflow-number">3</div>
            <div class="workflow-title">Generate</div>
            <div class="workflow-desc">Create test cases from queries</div>
        </div>
        <div class="workflow-step">
            <div class="workflow-number">4</div>
            <div class="workflow-title">Automate</div>
            <div class="workflow-desc">Download Selenium scripts</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Getting Started
    st.markdown("### 🚀 Getting Started")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--primary);">📤 Step 1: Upload Documents</h4>
            <p>Use the sidebar to upload your documentation files. Include requirements, user stories, and a checkout.html file for UI testing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--primary);">🧪 Step 2: Generate Tests</h4>
            <p>Navigate to the "Generate Tests" tab and enter a query describing what test cases you need.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--primary);">🤖 Step 3: Create Scripts</h4>
            <p>Select a test case and generate a complete Selenium automation script ready to run.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="modern-card">
            <h4 style="color: var(--primary);">📊 Step 4: Monitor</h4>
            <p>Check the Analytics tab to view system metrics and track your testing progress.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Inject CSS on every run to ensure consistent styling
    inject_modern_css()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📁 File Upload")
        
        # Backend status
        backend_ok, status_data = check_backend_status()
        
        if backend_ok:
            st.markdown('<div class="status-success">✅ Backend Connected</div>', unsafe_allow_html=True)
            
            # Show stats
            if status_data:
                db_stats = status_data.get('database', {})
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("📊 Chunks", db_stats.get('total_chunks', 0))
                with col2:
                    file_types = db_stats.get('file_types', [])
                    st.metric("📁 Types", len(file_types))
        else:
            st.markdown('<div class="status-error">❌ Backend Offline</div>', unsafe_allow_html=True)
            st.error("Please start the backend server:\n```\ncd backend && python main.py\n```")
            return
        
        st.markdown("---")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=['md', 'txt', 'pdf', 'json', 'html'],
            accept_multiple_files=True,
            help="Upload 3-5 documentation files and 1 checkout.html"
        )
        
        if uploaded_files:
            st.info(f"📄 {len(uploaded_files)} file(s) selected")
            
            # Build knowledge base button
            if st.button("🚀 Build Knowledge Base", type="primary"):
                with st.spinner("Processing documents..."):
                    result = upload_files_to_backend(uploaded_files, clear_existing=False)
                
                if result and result.get('success'):
                    st.success(f"✅ Processed {result.get('total_chunks', 0)} chunks from {len(result.get('files_processed', []))} files")
                    st.session_state.knowledge_base_built = True
                else:
                    st.error("❌ Failed to build knowledge base")
        
        st.markdown("---")
        
        # Clear database button
        st.markdown("### 🗑️ Database")
        if st.button("Clear Database", type="secondary"):
            try:
                response = requests.delete(f"{BACKEND_URL}/clear_database")
                if response.status_code == 200:
                    st.success("✅ Database cleared")
                    st.session_state.knowledge_base_built = False
                    st.session_state.generated_test_cases = []
                else:
                    st.error("❌ Failed to clear database")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🧪 Generate Tests", "🤖 Create Scripts", "📊 Analytics"])
    
    with tab1:
        render_home_screen()
    
    with tab2:
        st.markdown("## 🧪 AI-Powered Test Generation")
        
        kb_built = st.session_state.get('knowledge_base_built', False)
        
        if not kb_built:
            st.markdown('<div class="status-warning">⚠️ Please upload and process documents first using the sidebar</div>', unsafe_allow_html=True)
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
        st.markdown("## 🤖 Selenium Script Generation")
        
        test_cases = st.session_state.get('generated_test_cases', [])
        
        if not test_cases:
            st.markdown('<div class="status-warning">⚠️ Please generate test cases first</div>', unsafe_allow_html=True)
        else:
            # Test case selection
            test_options = [f"{tc.get('Test_ID', 'TC')}: {tc.get('Feature', 'Unknown')} - {tc.get('Test_Scenario', 'Unknown')[:50]}" 
                          for tc in test_cases]
            
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
        st.markdown("## 📊 Analytics Dashboard")
        
        backend_ok, status_data = check_backend_status()
        
        if backend_ok and status_data:
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
        else:
            st.error("❌ Unable to load analytics")

if __name__ == "__main__":
    # Initialize session state
    if 'knowledge_base_built' not in st.session_state:
        st.session_state.knowledge_base_built = False
    if 'generated_test_cases' not in st.session_state:
        st.session_state.generated_test_cases = []
    
    main()
