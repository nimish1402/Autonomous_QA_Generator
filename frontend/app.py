"""
Streamlit Frontend for Autonomous QA Agent

This module provides the web interface for document upload, knowledge base building,
test case generation, and Selenium script download functionality.
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
    page_title="Autonomous QA Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:8000"

def inject_modern_css():
    """Inject comprehensive modern CSS with adaptive theming"""
    st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables for Adaptive Theming */
    :root {
        --primary-color: #6366f1;
        --primary-dark: #4f46e5;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --info-color: #3b82f6;
        
        /* Light Theme Colors */
        --bg-light: #ffffff;
        --bg-light-secondary: #f8fafc;
        --text-light: #1f2937;
        --text-light-secondary: #6b7280;
        --border-light: #e5e7eb;
        
        /* Dark Theme Colors */
        --bg-dark: #1f2937;
        --bg-dark-secondary: #374151;
        --text-dark: #f9fafb;
        --text-dark-secondary: #d1d5db;
        --border-dark: #4b5563;
        
        /* Shadows and Effects */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        
        --border-radius: 12px;
        --border-radius-lg: 16px;
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
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
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius-lg);
        margin: 1rem;
        box-shadow: var(--shadow-xl);
    }
    
    /* Animated Header */
    .hero-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        border-radius: var(--border-radius-lg);
        margin-bottom: 2rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmer 3s infinite;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        opacity: 0.9;
        animation: fadeInUp 1s ease-out 0.2s both;
    }
    
    /* Interactive Cards */
    .interactive-card {
        background: var(--bg-light);
        border: 2px solid var(--border-light);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .interactive-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.1), transparent);
        transition: var(--transition);
    }
    
    .interactive-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-color);
    }
    
    .interactive-card:hover::before {
        left: 100%;
    }
    
    /* Status Cards */
    .status-card {
        background: linear-gradient(135deg, var(--bg-light) 0%, var(--bg-light-secondary) 100%);
        border-left: 4px solid var(--info-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-sm);
        color: var(--text-light);
    }
    
    .success-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        color: #065f46 !important;
        animation: slideInRight 0.5s ease-out;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        color: #92400e;
        animation: pulse 2s infinite;
    }
    
    .error-card {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        color: #991b1b;
        animation: shake 0.5s ease-in-out;
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
        position: relative;
        color: var(--text-light);
    }
    
    .test-case-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: var(--border-radius) var(--border-radius) 0 0;
    }
    
    .test-case-card:hover {
        transform: translateX(8px);
        border-color: var(--primary-color);
        box-shadow: var(--shadow-xl);
    }
    
    /* Interactive Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: var(--transition);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg .css-1n76uvr {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: var(--border-radius);
    }
    
    /* Progress Indicators */
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
        animation: pulse-progress 2s infinite;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        text-align: center;
        margin: 0.25rem;
        transition: var(--transition);
    }
    
    .badge-primary {
        background: var(--primary-color);
        color: white;
    }
    
    .badge-success {
        background: var(--success-color);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning-color);
        color: white;
    }
    
    .badge-info {
        background: var(--info-color);
        color: white;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @keyframes pulse-progress {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .interactive-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .main .block-container {
            margin: 0.5rem;
        }
    }
    
    /* File Upload Enhancements */
    .uploadedFile {
        background: var(--bg-light-secondary);
        border: 2px dashed var(--border-light);
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        transition: var(--transition);
    }
    
    .uploadedFile:hover {
        border-color: var(--primary-color);
        background: rgba(99, 102, 241, 0.05);
    }
    
    /* Interactive Elements */
    .stSelectbox > div > div {
        border-radius: var(--border-radius);
        border: 2px solid var(--border-light);
        transition: var(--transition);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .stTextInput > div > div {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        background-color: #ffffff !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        background-color: #ffffff !important;
    }
    
    /* Sidebar Styling - White Background with Black Text */
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
    
    /* Default Font Color - Black for all main content */
    .stApp {
        color: #000000 !important;
    }
    
    .stMarkdown, .stText, .element-container {
        color: #000000 !important;
    }
    
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #000000 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #000000 !important;
    }
    
    /* Input and form elements styling */
    .stTextInput > div > div > input {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: none !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Textarea styling */
    .stTextArea > div > div > textarea {
        color: #000000 !important;
        background-color: #ffffff !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: #9ca3af !important;
    }
    
    /* Tab text styling */
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
    
    /* Dropdown menu styling */
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu-item"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu-item"]:hover {
        background-color: #f3f4f6 !important;
        color: #000000 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div > div {
        background-color: #ffffff !important;
        border: 2px dashed #d1d5db !important;
        border-radius: 12px !important;
        color: #000000 !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #6366f1 !important;
        background-color: #f8fafc !important;
    }
    
    .stFileUploader label {
        color: #000000 !important;
    }
    
    /* Interactive Card Text Override */
    .interactive-card {
        color: #000000 !important;
    }
    
    .interactive-card h1, .interactive-card h2, .interactive-card h3, .interactive-card h4, .interactive-card h5, .interactive-card h6 {
        color: #000000 !important;
    }
    
    .interactive-card p, .interactive-card div, .interactive-card span, .interactive-card li {
        color: #000000 !important;
    }
    
    /* Warning Card Text Override */
    .warning-card {
        color: #000000 !important;
    }
    
    .warning-card h1, .warning-card h2, .warning-card h3, .warning-card h4, .warning-card h5, .warning-card h6 {
        color: #000000 !important;
    }
    
    .warning-card p, .warning-card div, .warning-card span {
        color: #000000 !important;
    }
    
    /* Success and Error Box Styling */
    .success-box {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%) !important;
        border: 1px solid #10b981 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        color: #065f46 !important;
    }
    
    .success-box * {
        color: #065f46 !important;
    }
    
    .error-box {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%) !important;
        border: 1px solid #ef4444 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        color: #991b1b !important;
    }
    
    .error-box * {
        color: #991b1b !important;
    }
    
    /* Code Block Styling */
    .stCode {
        background-color: #1f2937 !important;
        color: #f9fafb !important;
    }
    
    .stCode code {
        color: #f9fafb !important;
    }
    
    /* Ensure proper contrast for light backgrounds */
    pre {
        background-color: #f8fafc !important;
        color: #374151 !important;
        padding: 1rem !important;
        border-radius: 6px !important;
        border: 1px solid #e5e7eb !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize CSS
inject_modern_css()


def check_backend_status():
    """Check if the backend is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/status", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


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
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating test cases: {str(e)}")
        return None


def generate_selenium_script(test_case):
    """Generate Selenium script for a test case."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate_script",
            json={"test_case": test_case},
            timeout=30
        )
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating script: {str(e)}")
        return None


def display_test_case(test_case, index):
    """Display a test case in an enhanced interactive card."""
    test_type = test_case.get('Type', 'N/A')
    type_color = 'var(--success-color)' if test_type == 'Positive' else 'var(--warning-color)' if test_type == 'Negative' else 'var(--info-color)'
    
    with st.container():
        st.markdown(f"""
        <div class="test-case-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h4 style="color: #6366f1; margin: 0; font-size: 1.25rem;">🧪 Test Case {index}: {test_case.get('Test_ID', 'N/A')}</h4>
                <span class="badge" style="background: {type_color}; color: white;">{test_type}</span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <strong style="color: #000000;">🎯 Feature:</strong>
                    <p style="color: #374151; margin: 0.25rem 0;">{test_case.get('Feature', 'N/A')}</p>
                </div>
                <div>
                    <strong style="color: #000000;">📚 Source:</strong>
                    <p style="color: #374151; margin: 0.25rem 0; font-family: monospace; font-size: 0.875rem;">{test_case.get('Grounded_In', 'NOT SPECIFIED')}</p>
                </div>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <strong style="color: #000000;">📝 Scenario:</strong>
                <p style="color: #374151; margin: 0.25rem 0; line-height: 1.6;">{test_case.get('Test_Scenario', 'N/A')}</p>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <strong style="color: #000000;">✅ Expected Result:</strong>
                <p style="color: #374151; margin: 0.25rem 0; line-height: 1.6;">{test_case.get('Expected_Result', 'N/A')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Interactive steps section
        steps = test_case.get('Steps', [])
        if steps:
            with st.expander(f"📋 View Test Steps ({len(steps)} steps)", expanded=False):
                for i, step in enumerate(steps, 1):
                    st.markdown(f"""
                    <div style="padding: 0.75rem; margin: 0.5rem 0; background: #f8fafc; border-left: 3px solid #6366f1; border-radius: 6px;">
                        <strong style="color: #6366f1;">Step {i}:</strong>
                        <span style="color: #000000; margin-left: 0.5rem;">{step}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Interactive notes section
        notes = test_case.get('Notes', '')
        if notes:
            with st.expander("📌 Additional Notes"):
                st.markdown(f"""
                <div class="status-card">
                    {notes}
                </div>
                """, unsafe_allow_html=True)


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
        <div style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">
            📍 {step_names[current_step - 1] if current_step <= len(step_names) else 'Complete'}
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_interactive_metric(icon, label, value, delta=None, help_text=None):
    """Create an interactive metric card"""
    delta_html = f'<div style="color: var(--success-color); font-size: 0.875rem;">↗️ {delta}</div>' if delta else ''
    help_html = f'<div style="color: #6b7280; font-size: 0.75rem; margin-top: 0.25rem;">{help_text}</div>' if help_text else ''
    
    st.markdown(f"""
    <div class="interactive-card" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #000000; margin-bottom: 0.25rem;">{value}</div>
        <div style="font-size: 0.875rem; color: #6b7280;">{label}</div>
        {delta_html}
        {help_html}
    </div>
    """, unsafe_allow_html=True)

# Platform Capabilities feature showcase removed as requested

def main():
    """Main Streamlit application with enhanced interactivity."""
    
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
    
    # Platform capabilities removed as requested
    
    # Check backend status
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
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Status")
        
        # Get backend status
        try:
            status_response = requests.get(f"{BACKEND_URL}/status")
            if status_response.status_code == 200:
                status_data = status_response.json()
                st.success("✅ Backend Connected")
                
                # Display database stats
                if 'database' in status_data:
                    db_stats = status_data['database']
                    st.metric("Total Chunks", db_stats.get('total_chunks', 0))
                    
                    file_types = db_stats.get('file_types', [])
                    if file_types:
                        st.write("**File Types:**", ", ".join(file_types))
                
                # Checkout HTML status
                checkout_loaded = status_data.get('checkout_html_loaded', False)
                if checkout_loaded:
                    st.success("✅ Checkout HTML Loaded")
                else:
                    st.warning("⚠️ Checkout HTML Not Loaded")
                
                # LLM status
                llm_status = status_data.get('llm', {})
                provider = llm_status.get('provider', 'Unknown')
                api_available = llm_status.get('api_available', False)
                
                if api_available:
                    st.success(f"🤖 LLM: {provider}")
                    model = llm_status.get('config', {}).get('model', 'N/A')
                    if model != 'N/A':
                        st.caption(f"Model: {model}")
                else:
                    st.warning("⚠️ LLM: Template-based only")
                    with st.expander("Configure LLM API"):
                        st.markdown("""
                        **To enable AI-powered generation, set environment variables:**
                        
                        **Google Gemini (Recommended - Free Tier):**
                        ```bash
                        pip install google-generativeai
                        export GEMINI_API_KEY=your_key_here
                        # Get free key: https://makersuite.google.com/app/apikey
                        ```
                        
                        **OpenAI:**
                        ```bash
                        export OPENAI_API_KEY=your_key_here
                        export OPENAI_MODEL=gpt-3.5-turbo  # optional
                        ```
                        
                        **Anthropic Claude:**
                        ```bash
                        export ANTHROPIC_API_KEY=your_key_here
                        ```
                        
                        **Local Ollama:**
                        ```bash
                        # Install Ollama and pull a model
                        ollama pull llama2
                        ```
                        
                        **HuggingFace:**
                        ```bash
                        export HUGGINGFACE_TOKEN=your_token_here
                        ```
                        
                        Then restart the backend server.
                        """)
        except:
            st.error("❌ Backend Connection Failed")
    
    # Interactive Tabs Interface
    tab1, tab2, tab3 = st.tabs(["📄 Document Upload", "🧪 Generate Tests", "🤖 Create Scripts"])
    
    with tab1:
        st.markdown("### 📄 Smart Document Processing")
        create_progress_indicator(1, 3, ["Upload Documents", "Generate Tests", "Download Scripts"])
    
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            <div class="interactive-card">
                <h4 style="color: #6366f1; margin-bottom: 1rem;">📋 Upload Requirements</h4>
                <ul style="color: #000000;">
                    <li>✅ 3-5 support documents (MD, TXT, PDF, JSON)</li>
                    <li>🌐 1 checkout.html file (for e-commerce testing)</li>
                    <li>📏 Max file size: 10MB per file</li>
                    <li>🎯 Clear, structured documentation preferred</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            uploaded_files = st.file_uploader(
                "🎯 Drop files here or click to browse",
                type=['md', 'txt', 'pdf', 'json', 'html'],
                accept_multiple_files=True,
                help="Upload your documentation and HTML files"
            )
            
            # Enhanced file preview
            if uploaded_files:
                st.markdown("### 🔍 File Preview")
                for i, file in enumerate(uploaded_files[:3]):
                    file_icon = {'text/markdown': '📝', 'text/plain': '📄', 'application/pdf': '📕', 
                                'application/json': '📊', 'text/html': '🌐'}.get(file.type, '📄')
                    
                    with st.expander(f"{file_icon} {file.name} ({file.size:,} bytes)"):
                        if file.type in ['text/plain', 'text/markdown'] or file.name.endswith('.md'):
                            try:
                                content = str(file.read(), "utf-8")
                                preview = content[:500] + "..." if len(content) > 500 else content
                                st.markdown(f"""
                                <div style="background: #f8fafc; padding: 1rem; border-radius: 6px; border-left: 3px solid #6366f1;">
                                    <pre style="color: #000000; font-size: 0.875rem; white-space: pre-wrap;">{preview}</pre>
                                </div>
                                """, unsafe_allow_html=True)
                                file.seek(0)
                            except:
                                st.info("📄 Text file detected - content will be processed")
                        else:
                            st.info(f"📄 {file.type} file detected - ready for processing")
        
        with col2:
            st.markdown("### ⚙️ Configuration")
            
            clear_existing = st.checkbox(
                "🗑️ Clear Existing Data", 
                help="Remove all previous documents from knowledge base"
            )
            
            # Enhanced build button
            build_disabled = not uploaded_files
            
            st.markdown("""
            <div class="interactive-card" style="text-align: center;">
                <h4 style="color: #10b981;">🚀 Ready to Build</h4>
                <p style="color: #000000; font-size: 0.875rem;">Process documents and create knowledge base</p>
            </div>
            """ if uploaded_files else """
            <div class="warning-card" style="text-align: center;">
                <h4 style="color: #000000;">⚠️ Files Required</h4>
                <p style="color: #000000; font-size: 0.875rem;">Upload documents to continue</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Build Knowledge Base", type="primary", use_container_width=True, disabled=build_disabled):
                if uploaded_files:
                    with st.spinner("Processing documents and building knowledge base..."):
                        result = upload_files_to_backend(uploaded_files, clear_existing)
                    
                    if result and result.get('success'):
                        st.markdown(f"""
                        <div class="success-box">
                            <strong>✅ {result.get('message', 'Success')}</strong><br>
                            📊 Total Chunks: {result.get('total_chunks', 0)}<br>
                            📁 Files Processed: {', '.join(result.get('files_processed', []))}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Store in session state
                        st.session_state.knowledge_base_built = True
                    else:
                        st.markdown("""
                        <div class="error-box">
                            <strong>❌ Failed to build knowledge base</strong><br>
                            Please check your files and try again.
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Please upload files before building the knowledge base.")
    
    # Show uploaded files
    if uploaded_files:
        st.write("**Uploaded Files:**")
        for file in uploaded_files:
            st.write(f"  • {file.name} ({file.type})")
    
    # Section 2: Test Case Generation
    st.markdown('<h2 class="section-header">🧪 Test Case Generation Agent</h2>', unsafe_allow_html=True)
    
    # Check if knowledge base is built
    kb_built = st.session_state.get('knowledge_base_built', False)
    
    if not kb_built:
        st.info("💡 Please build the knowledge base first by uploading documents above.")
    
    query_input = st.text_input(
        "Enter your test case generation query:",
        placeholder="e.g., Generate all positive and negative test cases for the discount code feature",
        disabled=not kb_built,
        help="Describe what test cases you want to generate based on your uploaded documents"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        generate_button = st.button("🚀 Generate Test Cases", type="primary", disabled=not kb_built or not query_input)
    
    # Generate test cases
    if generate_button and query_input:
        with st.spinner("Generating test cases from knowledge base..."):
            result = generate_test_cases(query_input)
        
        if result and result.get('success'):
            test_cases = result.get('test_cases', [])
            grounded_sources = result.get('grounded_sources', [])
            
            st.markdown(f"""
            <div class="success-box">
                <strong>✅ Generated {len(test_cases)} test cases</strong><br>
                📚 Grounded in sources: {', '.join(grounded_sources)}
            </div>
            """, unsafe_allow_html=True)
            
            # Store test cases in session state
            st.session_state.generated_test_cases = test_cases
            
            # Display test cases
            st.markdown("### Generated Test Cases:")
            for i, test_case in enumerate(test_cases, 1):
                display_test_case(test_case, i)
        else:
            st.markdown("""
            <div class="error-box">
                <strong>❌ Failed to generate test cases</strong><br>
                Please check your query and try again.
            </div>
            """, unsafe_allow_html=True)
    
    # Section 3: Selenium Script Generation
    st.markdown('<h2 class="section-header">⚙️ Selenium Script Generation</h2>', unsafe_allow_html=True)
    
    # Check if test cases are available
    test_cases = st.session_state.get('generated_test_cases', [])
    
    if not test_cases:
        st.info("💡 Please generate test cases first using the section above.")
    else:
        # Test case selection
        test_case_options = []
        for i, tc in enumerate(test_cases):
            option_text = f"TC{i+1}: {tc.get('Feature', 'Unknown')} - {tc.get('Test_Scenario', 'Unknown')}"
            test_case_options.append(option_text)
        
        selected_index = st.selectbox(
            "Select a test case to generate Selenium script:",
            range(len(test_case_options)),
            format_func=lambda x: test_case_options[x],
            help="Choose which test case you want to convert into a Selenium Python script"
        )
        
        selected_test_case = test_cases[selected_index]
        
        # Display selected test case
        st.markdown("**Selected Test Case:**")
        display_test_case(selected_test_case, selected_index + 1)
        
        # Generate script button
        if st.button("🐍 Generate Selenium Script", type="primary"):
            with st.spinner("Generating Selenium Python script..."):
                result = generate_selenium_script(selected_test_case)
            
            if result and result.get('success'):
                script_content = result.get('script_content', '')
                filename = result.get('filename', 'test_script.py')
                
                st.markdown(f"""
                <div class="success-box">
                    <strong>✅ Generated Selenium script: {filename}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Display script
                st.markdown("### Generated Selenium Script:")
                st.code(script_content, language='python')
                
                # Download button
                st.download_button(
                    label="💾 Download Selenium Script",
                    data=script_content,
                    file_name=filename,
                    mime='text/plain',
                    help="Download the generated Selenium Python script"
                )
                
                # Instructions
                st.markdown("""
                ### 📝 Instructions to Run the Script:
                
                1. **Update the base URL** in the script to point to your actual checkout.html file
                2. **Install required packages:**
                   ```bash
                   pip install selenium webdriver-manager
                   ```
                3. **Run the script:**
                   ```bash
                   python {filename}
                   ```
                4. **Review and customize** selectors if needed based on your actual HTML structure
                """.format(filename=filename))
                
            else:
                st.markdown("""
                <div class="error-box">
                    <strong>❌ Failed to generate Selenium script</strong><br>
                    Please ensure checkout.html is uploaded and try again.
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        🤖 Autonomous QA Agent v1.0 - Generating context-grounded test automation with strict adherence to provided documentation
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    # Initialize session state
    if 'knowledge_base_built' not in st.session_state:
        st.session_state.knowledge_base_built = False
    if 'generated_test_cases' not in st.session_state:
        st.session_state.generated_test_cases = []
    
    main()