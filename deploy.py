#!/usr/bin/env python3
"""
Deployment Script for Autonomous QA Agent
Validates system readiness and provides deployment guidance
"""

import os
import sys
import subprocess
import json
import requests
import time
from pathlib import Path


class DeploymentManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_url = None
        
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        print("\n📦 Checking Dependencies...")
        
        required_packages = [
            'fastapi',
            'uvicorn', 
            'requests',
            'python-dotenv',
            'pydantic'
        ]
        
        optional_packages = {
            'chromadb': 'Vector database (recommended)',
            'sentence_transformers': 'Embeddings (recommended)',
            'google.generativeai': 'LLM integration (optional)'
        }
        
        missing_required = []
        missing_optional = []
        
        for package in required_packages:
            try:
                # Handle special cases
                if package == "python-dotenv":
                    from dotenv import load_dotenv
                else:
                    __import__(package)
                print(f"✅ {package}")
            except ImportError:
                print(f"❌ {package} - REQUIRED")
                missing_required.append(package)
        
        for package, description in optional_packages.items():
            try:
                __import__(package)
                print(f"✅ {package} - {description}")
            except ImportError:
                print(f"⚠️  {package} - {description}")
                missing_optional.append(package)
        
        if missing_required:
            print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
            print("💡 Install with: pip install -r requirements.txt")
            return False
        
        if missing_optional:
            print(f"\n⚠️  Missing optional packages: {', '.join(missing_optional)}")
            print("💡 Some features may be limited but deployment should work")
        
        return True

    def validate_local_environment(self):
        """Validate local environment before deployment."""
        print("🔍 Validating Local Environment...")
        issues = []
        
        # Check Python version
        python_version = sys.version_info
        if python_version >= (3, 8):
            print(f"✅ Python {python_version.major}.{python_version.minor} (compatible)")
        else:
            issues.append(f"❌ Python {python_version.major}.{python_version.minor} (need 3.8+)")
        
        # Check required files
        required_files = [
            "requirements.txt",
            "backend/main.py",
            "render.yaml",
            "railway.toml"
        ]
        
        for file in required_files:
            file_path = self.project_root / file
            if file_path.exists():
                print(f"✅ {file}")
            else:
                issues.append(f"❌ Missing: {file}")
        
        # Check environment variables
        env_vars = {
            "GEMINI_API_KEY": "Optional - enables LLM functionality",
            "ENVIRONMENT": "Optional - defaults to development",
            "PORT": "Optional - defaults to 8000"
        }
        
        print("\n🔐 Environment Variables:")
        for var, description in env_vars.items():
            value = os.getenv(var)
            if value:
                print(f"✅ {var}: {'*' * 10}... ({description})")
            else:
                print(f"⚠️  {var}: Not set ({description})")
        
        return issues
    
    def test_local_backend(self):
        """Test the backend locally."""
        print("\n🧪 Testing Local Backend...")
        
        try:
            # Check if backend directory exists
            backend_dir = self.project_root / "backend"
            if not backend_dir.exists():
                print(f"❌ Backend directory not found: {backend_dir}")
                return False
            
            main_file = backend_dir / "main.py"
            if not main_file.exists():
                print(f"❌ Backend main.py not found: {main_file}")
                return False
            
            print("🚀 Starting backend server...")
            
            # Start backend with better error capture
            process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=str(backend_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Wait longer for server to start and check if it's running
            print("⏳ Waiting for server to start (this may take 10-15 seconds)...")
            
            # Check if process started successfully
            for i in range(15):  # Wait up to 15 seconds
                time.sleep(1)
                if process.poll() is not None:
                    # Process has terminated - get error output
                    stdout, stderr = process.communicate()
                    print(f"❌ Backend process terminated unexpectedly:")
                    if stderr:
                        print(f"Error output: {stderr}")
                    if stdout:
                        print(f"Standard output: {stdout}")
                    return False
                
                # Try to connect to see if server is up
                try:
                    response = requests.get("http://localhost:8000/health", timeout=2)
                    if response.status_code == 200:
                        print(f"✅ Backend server started successfully after {i+1} seconds")
                        break
                except requests.RequestException:
                    continue
            else:
                # Server didn't start in time
                print("❌ Backend server failed to start within 15 seconds")
                
                # Get some output for debugging
                try:
                    stdout, stderr = process.communicate(timeout=2)
                    if stderr:
                        print(f"Error output: {stderr[:500]}...")  # Limit output
                    if stdout:
                        print(f"Standard output: {stdout[:500]}...")
                except subprocess.TimeoutExpired:
                    print("⚠️  Server is running but not responding")
                
                process.terminate()
                process.wait()
                return False
            
            # Test endpoints
            print("🔍 Testing API endpoints...")
            base_url = "http://localhost:8000"
            endpoints = [
                "/health",
                "/status", 
                "/config",
                "/analytics",
                "/deployment/validate"
            ]
            
            success_count = 0
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{base_url}{endpoint}", timeout=10)
                    if response.status_code == 200:
                        print(f"✅ {endpoint}: {response.status_code}")
                        success_count += 1
                    else:
                        print(f"⚠️  {endpoint}: {response.status_code}")
                except requests.RequestException as e:
                    error_msg = str(e)
                    if len(error_msg) > 100:
                        error_msg = error_msg[:100] + "..."
                    print(f"❌ {endpoint}: {error_msg}")
            
            # Stop the process gracefully
            print("\n🛑 Stopping backend server...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            
            # Evaluate results
            if success_count >= 3:  # At least 3 endpoints working
                print(f"\n🎉 Backend test successful! ({success_count}/{len(endpoints)} endpoints working)")
                return True
            else:
                print(f"\n⚠️  Backend test partially failed. Only {success_count}/{len(endpoints)} endpoints working.")
                print("💡 This might still work for deployment if core endpoints are functional.")
                return success_count > 0
            
        except Exception as e:
            print(f"❌ Backend test failed with exception: {e}")
            print("\n🔧 Troubleshooting suggestions:")
            print("   1. Check if all dependencies are installed: pip install -r requirements.txt")
            print("   2. Try starting the backend manually: cd backend && python main.py")
            print("   3. Check if port 8000 is available")
            print("   4. Verify Python path and imports")
            return False
    
    def get_deployment_instructions(self):
        """Provide platform-specific deployment instructions."""
        print("\n🚀 Deployment Instructions")
        print("=" * 50)
        
        print("\n📋 Choose Your Deployment Platform:")
        print("1. Railway (Recommended)")
        print("2. Render") 
        print("3. Heroku")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            self._show_railway_instructions()
        elif choice == "2":
            self._show_render_instructions()
        elif choice == "3":
            self._show_heroku_instructions()
        else:
            print("Invalid choice. Showing Railway instructions by default.")
            self._show_railway_instructions()
    
    def _show_railway_instructions(self):
        """Show Railway deployment instructions."""
        print("\n🚄 Railway Deployment Instructions:")
        print("=" * 40)
        
        instructions = """
1. **Prepare Repository:**
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main

2. **Deploy to Railway:**
   • Go to: https://railway.app
   • Sign up with GitHub
   • New Project → Deploy from GitHub repo
   • Select: nimish1402/Autonomous_QA_Generator
   • Railway will auto-detect and deploy

3. **Set Environment Variables:**
   GEMINI_API_KEY = your_api_key_here
   ENVIRONMENT = production
   VECTOR_DB_PATH = /tmp/vectordb

4. **Expected Result:**
   • Backend URL: https://your-project.railway.app
   • Health check: https://your-project.railway.app/health

5. **Test Deployment:**
   curl https://your-project.railway.app/health
   curl https://your-project.railway.app/deployment/validate
        """
        
        print(instructions)
    
    def _show_render_instructions(self):
        """Show Render deployment instructions."""
        print("\n🎨 Render Deployment Instructions:")
        print("=" * 40)
        
        instructions = """
1. **Prepare Repository:**
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main

2. **Deploy to Render:**
   • Go to: https://render.com
   • Sign up with GitHub
   • New → Blueprint
   • Connect: nimish1402/Autonomous_QA_Generator
   • Branch: main
   • Apply Blueprint

3. **Set Environment Variables:**
   GEMINI_API_KEY = your_api_key_here
   ENVIRONMENT = production

4. **Expected Result:**
   • Backend URL: https://your-service.onrender.com
   • Health check: https://your-service.onrender.com/health

5. **Test Deployment:**
   curl https://your-service.onrender.com/health
   curl https://your-service.onrender.com/deployment/validate
        """
        
        print(instructions)
    
    def _show_heroku_instructions(self):
        """Show Heroku deployment instructions."""
        print("\n🟣 Heroku Deployment Instructions:")
        print("=" * 40)
        
        instructions = """
1. **Install Heroku CLI:**
   Download from: https://devcenter.heroku.com/articles/heroku-cli

2. **Deploy to Heroku:**
   heroku create your-qa-agent
   heroku config:set GEMINI_API_KEY=your_api_key_here
   heroku config:set ENVIRONMENT=production
   git push heroku main

3. **Expected Result:**
   • Backend URL: https://your-qa-agent.herokuapp.com
   • Health check: https://your-qa-agent.herokuapp.com/health

4. **Test Deployment:**
   curl https://your-qa-agent.herokuapp.com/health
   heroku logs --tail
        """
        
        print(instructions)
    
    def validate_deployed_backend(self):
        """Validate a deployed backend."""
        print("\n🌐 Validate Deployed Backend")
        print("=" * 30)
        
        backend_url = input("Enter your deployed backend URL: ").strip()
        
        if not backend_url.startswith(("http://", "https://")):
            backend_url = f"https://{backend_url}"
        
        self.backend_url = backend_url
        
        # Test endpoints
        endpoints = {
            "/health": "Basic health check",
            "/status": "Detailed system status", 
            "/deployment/validate": "Deployment validation",
            "/config": "System configuration",
            "/analytics": "System analytics"
        }
        
        print(f"\n🔍 Testing endpoints on: {backend_url}")
        
        all_passed = True
        
        for endpoint, description in endpoints.items():
            try:
                response = requests.get(f"{backend_url}{endpoint}", timeout=30)
                if response.status_code == 200:
                    print(f"✅ {endpoint}: {response.status_code} - {description}")
                else:
                    print(f"⚠️  {endpoint}: {response.status_code} - {description}")
                    all_passed = False
            except requests.RequestException as e:
                print(f"❌ {endpoint}: Error - {str(e)}")
                all_passed = False
        
        if all_passed:
            print(f"\n🎉 Backend deployment successful!")
            print(f"📊 Dashboard: {backend_url}/status")
            print(f"📈 Analytics: {backend_url}/analytics")
            
            # Show validation results
            try:
                validation_response = requests.get(f"{backend_url}/deployment/validate", timeout=30)
                if validation_response.status_code == 200:
                    validation_data = validation_response.json()
                    print(f"\n📋 Deployment Status: {validation_data['deployment_status']}")
                    
                    if validation_data['errors']:
                        print("❌ Errors:", ", ".join(validation_data['errors']))
                    if validation_data['warnings']:
                        print("⚠️  Warnings:", ", ".join(validation_data['warnings']))
            except:
                pass
        else:
            print(f"\n⚠️  Some endpoints failed. Check deployment logs.")
    
    def generate_streamlit_config(self):
        """Generate Streamlit Cloud configuration."""
        if not self.backend_url:
            self.backend_url = input("Enter your backend URL: ").strip()
        
        print(f"\n📝 Streamlit Cloud Configuration")
        print("=" * 35)
        
        config = f"""
For Streamlit Cloud deployment, add these environment variables:

BACKEND_URL = {self.backend_url}
GEMINI_API_KEY = your_api_key_here
ENVIRONMENT = production

Main file: streamlit_cloud_app.py
        """
        
        print(config)
    
    def run_complete_deployment(self):
        """Run complete deployment process."""
        print("🤖 Autonomous QA Agent - Deployment Manager")
        print("=" * 50)
        
        # Step 1: Check dependencies
        deps_ok = self.check_dependencies()
        
        if not deps_ok:
            print("\n❌ Dependency check failed. Please install missing packages.")
            return False
        
        # Step 2: Validate local environment
        issues = self.validate_local_environment()
        
        if issues:
            print(f"\n❌ Issues found:")
            for issue in issues:
                print(f"   {issue}")
            print("\nPlease fix these issues before deployment.")
            return False
        
        # Step 3: Test local backend
        print("\n" + "="*50)
        backend_works = self.test_local_backend()
        
        if not backend_works:
            print("\n❌ Local backend test failed.")
            print("\n🤔 You can still proceed with deployment, but local testing failed.")
            proceed = input("Do you want to continue anyway? (y/N): ").strip().lower()
            if proceed != 'y':
                print("\n⏹️  Deployment cancelled. Fix local issues first.")
                return False
        
        # Step 3: Show deployment instructions
        self.get_deployment_instructions()
        
        # Step 4: Wait for user to deploy
        input("\n⏸️  Press Enter after you've completed the deployment...")
        
        # Step 5: Validate deployed backend
        self.validate_deployed_backend()
        
        # Step 6: Generate frontend config
        self.generate_streamlit_config()
        
        print("\n🎉 Deployment process completed!")
        return True


def main():
    """Main deployment script."""
    manager = DeploymentManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "validate":
            manager.validate_local_environment()
        elif command == "deps" or command == "dependencies":
            manager.check_dependencies()
        elif command == "test":
            deps_ok = manager.check_dependencies()
            if deps_ok:
                manager.test_local_backend()
            else:
                print("\n❌ Cannot test backend - dependencies missing")
        elif command == "instructions":
            manager.get_deployment_instructions()
        elif command == "check":
            manager.validate_deployed_backend()
        elif command == "config":
            manager.generate_streamlit_config()
        else:
            print("Usage: python deploy.py [validate|deps|test|instructions|check|config]")
            print("\nCommands:")
            print("  validate     - Check local environment")
            print("  deps         - Check dependencies")
            print("  test         - Test local backend")
            print("  instructions - Show deployment instructions")
            print("  check        - Validate deployed backend")
            print("  config       - Generate Streamlit config")
    else:
        # Run complete deployment process
        manager.run_complete_deployment()


if __name__ == "__main__":
    main()