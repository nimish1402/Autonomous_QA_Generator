#!/usr/bin/env python3
"""
Setup script for Autonomous QA Agent LLM integrations
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🤖 Autonomous QA Agent - LLM Integration Setup")
    print("=" * 50)
    
    print("\nChoose your preferred LLM provider:")
    print("1. Google Gemini (Recommended - free tier available)")
    print("2. OpenAI GPT (requires API key)")
    print("3. Anthropic Claude (requires API key)")  
    print("4. Local Ollama (Free - runs locally)")
    print("5. HuggingFace (Free tier available)")
    print("6. Skip LLM setup (use template-based generation)")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        print("\n📦 Installing Google Gemini integration...")
        if install_package("google-generativeai>=0.3.0"):
            print("✅ Google Gemini installed successfully!")
            print("\n📝 Next steps:")
            print("1. Get your API key from: https://makersuite.google.com/app/apikey")
            print("2. Set environment variable: export GEMINI_API_KEY=your_key_here")
            print("3. Restart the backend server")
            print("\n💡 Tip: Gemini offers generous free tier limits!")
        else:
            print("❌ Failed to install Google Gemini package")
    
    elif choice == "2":
        print("\n📦 Installing OpenAI integration...")
        if install_package("openai>=1.0.0"):
            print("✅ OpenAI installed successfully!")
            print("\n📝 Next steps:")
            print("1. Get your API key from: https://platform.openai.com/api-keys")
            print("2. Set environment variable: export OPENAI_API_KEY=your_key_here")
            print("3. Restart the backend server")
        else:
            print("❌ Failed to install OpenAI package")
    
    elif choice == "2":
        print("\n📦 Installing Anthropic integration...")
        if install_package("anthropic>=0.3.0"):
            print("✅ Anthropic installed successfully!")
            print("\n📝 Next steps:")
            print("1. Get your API key from: https://console.anthropic.com/")
            print("2. Set environment variable: export ANTHROPIC_API_KEY=your_key_here")
            print("3. Restart the backend server")
        else:
            print("❌ Failed to install Anthropic package")
    
    elif choice == "3":
        print("\n🖥️  Setting up Local Ollama...")
        print("📝 Ollama installation steps:")
        print("1. Install Ollama from: https://ollama.ai/")
        print("2. Pull a model: ollama pull llama2")
        print("3. Start Ollama service (usually automatic)")
        print("4. Restart the backend server")
        print("\n✅ No additional Python packages needed for Ollama!")
    
    elif choice == "4":
        print("\n📦 Installing HuggingFace integration...")
        if install_package("transformers>=4.21.0"):
            print("✅ HuggingFace transformers installed successfully!")
            print("\n📝 Next steps (optional for free tier):")
            print("1. Get token from: https://huggingface.co/settings/tokens")
            print("2. Set environment variable: export HUGGINGFACE_TOKEN=your_token_here")
            print("3. Restart the backend server")
        else:
            print("❌ Failed to install HuggingFace package")
    
    elif choice == "6":
        print("\n⚡ Using template-based generation")
        print("✅ No additional setup needed!")
        print("The system will work with predefined templates.")
    
    else:
        print("❌ Invalid choice. Please run the script again.")
        return
    
    print("\n🚀 Setup complete! Run 'python run.py' to start the system.")

if __name__ == "__main__":
    main()