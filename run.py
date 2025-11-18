#!/usr/bin/env python3
"""
Main launcher for Autonomous QA Agent
"""

import os
import sys
import subprocess
import time
import signal
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class AutonomousQAAgent:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.frontend_process = None
    
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        logger.info("Checking dependencies...")
        
        required_packages = [
            'fastapi', 'uvicorn', 'streamlit', 'requests',
            'chromadb', 'sentence_transformers', 'selenium',
            'beautifulsoup4', 'PyPDF2'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing packages: {', '.join(missing_packages)}")
            logger.error("Please install dependencies: pip install -r requirements.txt")
            return False
        
        logger.info("✅ All dependencies are installed")
        return True
    
    def start_backend(self):
        """Start the FastAPI backend server."""
        logger.info("Starting FastAPI backend...")
        
        backend_dir = self.project_root / "backend"
        backend_script = backend_dir / "main.py"
        
        if not backend_script.exists():
            logger.error(f"Backend script not found: {backend_script}")
            return False
        
        try:
            # Start backend process
            env = os.environ.copy()
            env['PYTHONPATH'] = str(self.project_root)
            
            self.backend_process = subprocess.Popen(
                [sys.executable, str(backend_script)],
                cwd=str(backend_dir),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                logger.info("✅ Backend started successfully on http://localhost:8000")
                return True
            else:
                logger.error("❌ Backend failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Error starting backend: {e}")
            return False
    
    def start_frontend(self):
        """Start the Streamlit frontend."""
        logger.info("Starting Streamlit frontend...")
        
        frontend_dir = self.project_root / "frontend"
        frontend_script = frontend_dir / "app.py"
        
        if not frontend_script.exists():
            logger.error(f"Frontend script not found: {frontend_script}")
            return False
        
        try:
            # Start frontend process
            self.frontend_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
                cwd=str(frontend_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for server to start
            time.sleep(5)
            
            if self.frontend_process.poll() is None:
                logger.info("✅ Frontend started successfully on http://localhost:8501")
                return True
            else:
                logger.error("❌ Frontend failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Error starting frontend: {e}")
            return False
    
    def stop_services(self):
        """Stop all running services."""
        logger.info("Stopping services...")
        
        if self.backend_process:
            self.backend_process.terminate()
            self.backend_process.wait()
            logger.info("Backend stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            self.frontend_process.wait()
            logger.info("Frontend stopped")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal...")
            self.stop_services()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def show_usage_info(self):
        """Display usage information."""
        print("""
🤖 Autonomous QA Agent Started Successfully!

📊 System URLs:
  • Backend API: http://localhost:8000
  • Frontend Web UI: http://localhost:8501
  • API Documentation: http://localhost:8000/docs

📋 Quick Start Guide:

1. Open the Web UI at http://localhost:8501
2. Upload your support documents (MD, TXT, PDF, JSON, HTML)
3. Include your checkout.html file (sample provided in data/checkout.html)
4. Click "Build Knowledge Base"
5. Enter a query like: "Generate test cases for discount code feature"
6. Select a test case and generate Selenium script
7. Download and run your automated test script!

📁 Sample Files:
  • data/checkout.html - Sample e-commerce checkout page
  • data/requirements.md - Requirements document
  • data/testing-guide.txt - Testing guidelines
  • data/checkout-config.json - Configuration file

🛑 To stop the system: Press Ctrl+C
        """)
    
    def run(self):
        """Run the complete system."""
        try:
            logger.info("🤖 Starting Autonomous QA Agent System...")
            
            # Check dependencies
            if not self.check_dependencies():
                return 1
            
            # Setup signal handlers
            self.setup_signal_handlers()
            
            # Start backend
            if not self.start_backend():
                return 1
            
            # Start frontend
            if not self.start_frontend():
                self.stop_services()
                return 1
            
            # Show usage information
            self.show_usage_info()
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
                    
                    # Check if processes are still running
                    if self.backend_process and self.backend_process.poll() is not None:
                        logger.error("Backend process stopped unexpectedly")
                        break
                    
                    if self.frontend_process and self.frontend_process.poll() is not None:
                        logger.error("Frontend process stopped unexpectedly") 
                        break
                        
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
            
        except Exception as e:
            logger.error(f"System error: {e}")
            return 1
        finally:
            self.stop_services()
        
        return 0


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "backend":
            # Start only backend
            agent = AutonomousQAAgent()
            agent.check_dependencies()
            agent.setup_signal_handlers()
            agent.start_backend()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                agent.stop_services()
            return
        
        elif command == "frontend":
            # Start only frontend
            agent = AutonomousQAAgent()
            agent.check_dependencies()
            agent.setup_signal_handlers() 
            agent.start_frontend()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                agent.stop_services()
            return
        
        elif command == "help":
            print("""
Autonomous QA Agent - Usage:

  python run.py          # Start both backend and frontend
  python run.py backend  # Start only backend server
  python run.py frontend # Start only frontend (requires backend to be running)
  python run.py help     # Show this help message

Requirements:
  - Python 3.8+
  - All dependencies installed (pip install -r requirements.txt)
            """)
            return
    
    # Start full system
    agent = AutonomousQAAgent()
    exit_code = agent.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()