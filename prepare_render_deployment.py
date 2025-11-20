#!/usr/bin/env python3
"""
Render Deployment Preparation Script

This script prepares your repository for Render deployment by:
1. Validating configuration files
2. Checking dependencies  
3. Testing backend locally
4. Providing deployment URLs and instructions
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import requests

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking Prerequisites...")
    
    issues = []
    
    # Check Git repository
    if not Path(".git").exists():
        issues.append("❌ Not a Git repository")
    else:
        print("✅ Git repository found")
    
    # Check required files
    required_files = [
        "requirements.txt",
        "render.yaml", 
        "backend/main.py",
        ".env.example"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} found")
        else:
            issues.append(f"❌ Missing: {file}")
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor} (compatible)")
    else:
        issues.append(f"❌ Python {python_version.major}.{python_version.minor} (need 3.8+)")
    
    return issues

def validate_render_config():
    """Validate render.yaml configuration"""
    print("\n🔧 Validating Render Configuration...")
    
    try:
        import yaml
        with open("render.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        # Check required fields
        service = config["services"][0]
        required_fields = ["name", "type", "env", "buildCommand", "startCommand"]
        
        for field in required_fields:
            if field in service:
                print(f"✅ {field}: {service[field]}")
            else:
                print(f"❌ Missing: {field}")
        
        return True
        
    except ImportError:
        print("⚠️  PyYAML not installed (pip install pyyaml)")
        return False
    except Exception as e:
        print(f"❌ Invalid render.yaml: {e}")
        return False

def check_environment_variables():
    """Check environment variable configuration"""
    print("\n🔐 Checking Environment Variables...")
    
    # Load .env if exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not installed")
    
    # Check required environment variables
    required_vars = {
        "GEMINI_API_KEY": "Google Gemini API key",
        "ENVIRONMENT": "Application environment",
        "GEMINI_MODEL": "Gemini model name"
    }
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:10]}... ({description})")
        else:
            print(f"⚠️  {var}: Not set ({description})")

def test_local_backend():
    """Test backend locally before deployment"""
    print("\n🧪 Testing Backend Locally...")
    
    try:
        # Test import
        sys.path.append("backend")
        from main import app
        print("✅ Backend imports successfully")
        
        # Test basic functionality
        print("✅ FastAPI app created")
        return True
        
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def generate_deployment_info():
    """Generate deployment information and next steps"""
    print("\n🚀 Deployment Information")
    print("=" * 50)
    
    print("📋 Next Steps:")
    print("1. Commit and push changes:")
    print("   git add .")
    print("   git commit -m 'Prepare for Render deployment'")
    print("   git push origin main")
    print()
    print("2. Deploy to Render:")
    print("   • Go to: https://render.com")
    print("   • Sign up with GitHub")
    print("   • New → Blueprint")
    print("   • Connect: nimish1402/Autonomous_QA_Generator")
    print("   • Branch: main")
    print("   • Apply Blueprint")
    print()
    print("3. Set Environment Variables in Render:")
    print("   GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24")
    print("   ENVIRONMENT = production")
    print("   DEBUG = false")
    print()
    print("4. Expected Backend URL:")
    print("   https://autonomous-qa-backend.onrender.com")
    print()
    print("5. Test Deployment:")
    print("   curl https://your-service.onrender.com/status")

def main():
    """Main deployment preparation workflow"""
    print("🤖 Render Backend Deployment Preparation")
    print("=" * 50)
    
    # Check prerequisites
    issues = check_prerequisites()
    
    if issues:
        print("\n❌ Issues Found:")
        for issue in issues:
            print(f"   {issue}")
        print("\nPlease fix these issues before proceeding.")
        return False
    
    # Validate configuration
    config_valid = validate_render_config()
    
    # Check environment variables
    check_environment_variables()
    
    # Test backend
    backend_works = test_local_backend()
    
    # Generate deployment info
    generate_deployment_info()
    
    # Summary
    print("\n" + "=" * 50)
    if config_valid and backend_works:
        print("🎉 Ready for Render Deployment!")
        print("Follow the steps above to deploy your backend.")
    else:
        print("⚠️  Some issues detected. Please review and fix before deployment.")
    
    return config_valid and backend_works

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)