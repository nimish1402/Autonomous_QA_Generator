# 🚀 Streamlit Cloud Deployment Guide

This guide explains how to deploy the Autonomous QA Agent to Streamlit Cloud.

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a public GitHub repository
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🔧 Pre-Deployment Setup

### 1. Repository Structure ✅
Your repository should have this structure:
```
autonomous-qa-agent/
├── streamlit_app.py          # ✅ Main entry point (created)
├── requirements.txt          # ✅ Dependencies (updated)
├── .streamlit/
│   └── config.toml          # ✅ Streamlit config (created)
├── frontend/
│   └── app.py               # ✅ Updated for cloud deployment
├── backend/                 # Backend files (not deployed to Streamlit Cloud)
├── utils/                   # Utility modules
├── models/                  # LLM integration
└── config/                  # Configuration files
```

### 2. Environment Variables
You'll need to configure these in Streamlit Cloud:
```
GEMINI_API_KEY=your_actual_api_key_here
BACKEND_URL=your_backend_api_url_here
ENVIRONMENT=production
```

## 🌐 Deployment Options

### **Option A: Frontend-Only Deployment (Recommended)**

Deploy just the Streamlit frontend to Streamlit Cloud, with backend hosted separately.

#### Steps:
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `streamlit_app.py`
   - Configure environment variables

3. **Deploy Backend Separately**:
   - **Railway**: [railway.app](https://railway.app)
   - **Render**: [render.com](https://render.com)
   - **Heroku**: [heroku.com](https://heroku.com)
   - **Google Cloud Run**: [cloud.google.com](https://cloud.google.com/run)

### **Option B: Standalone Mode (Limited Features)**

Deploy with embedded backend simulation (no real-time processing).

## 📝 Streamlit Cloud Configuration

### 1. App Settings
```
Repository: your-username/Autonomous_QA_Generator
Branch: main
Main file path: streamlit_app.py
```

### 2. Environment Variables
In Streamlit Cloud app settings, add:
```
GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
BACKEND_URL = https://your-backend-app.railway.app
ENVIRONMENT = production
LOG_LEVEL = INFO
```

### 3. Advanced Settings
```
Python version: 3.11
```

## 🔧 Backend Deployment (Separate Service)

### Railway Deployment (Recommended)

1. **Create railway.json**:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python main.py",
    "healthcheckPath": "/status"
  }
}
```

2. **Deploy Steps**:
   - Connect GitHub to Railway
   - Select your repository
   - Deploy backend service
   - Get the deployment URL
   - Add URL to Streamlit Cloud environment variables

### Render Deployment

1. **Create render.yaml**:
```yaml
services:
  - type: web
    name: qa-agent-backend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "cd backend && python main.py"
    healthCheckPath: "/status"
```

## 🚨 Important Considerations

### **Limitations of Streamlit Cloud**:
- ✅ **Works**: Document upload, UI display, basic processing
- ⚠️ **Limited**: Vector database (memory only), no persistent storage
- ❌ **Not Supported**: Background FastAPI server, file persistence

### **Recommended Architecture**:
```
Streamlit Cloud (Frontend) ←→ Railway/Render (Backend API) ←→ External Vector DB
```

### **Security Notes**:
- Store API keys in Streamlit Cloud secrets (not in code)
- Use HTTPS for backend communication
- Validate all user inputs

## 🔄 Deployment Process

### Step 1: Prepare Repository
```bash
# Ensure all files are ready
git status
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### Step 2: Deploy Backend (if using separate backend)
1. Deploy to Railway/Render/Heroku
2. Note the deployment URL
3. Test the `/status` endpoint

### Step 3: Deploy Frontend to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Configure settings and environment variables
5. Deploy

### Step 4: Test Deployment
1. Visit your Streamlit Cloud URL
2. Test document upload
3. Verify API connectivity
4. Generate test cases
5. Check Selenium script generation

## 🐛 Troubleshooting

### Common Issues:

**1. Import Errors**
```
Solution: Ensure all dependencies in requirements.txt
Check: Module imports in streamlit_app.py
```

**2. Backend Connection Failed**
```
Solution: Verify BACKEND_URL environment variable
Check: Backend service is running and accessible
```

**3. API Key Invalid**
```
Solution: Check Streamlit Cloud environment variables
Verify: API key is correct and active
```

**4. Memory/Resource Limits**
```
Solution: Use lightweight vector database options
Consider: External vector database service
```

## 📊 Post-Deployment Checklist

- [ ] Frontend loads without errors
- [ ] Document upload works
- [ ] Backend API connectivity verified
- [ ] Test case generation functional
- [ ] Selenium script download works
- [ ] Error handling displays properly
- [ ] Performance is acceptable

## 🎯 Next Steps After Deployment

1. **Monitor Performance**: Use Streamlit Cloud analytics
2. **Set Up Monitoring**: Add logging and error tracking
3. **Scale Backend**: Consider auto-scaling for high traffic
4. **Add Authentication**: Implement user management if needed
5. **Custom Domain**: Configure custom domain for professional use

---

**Ready to Deploy?** Follow the steps above and your Autonomous QA Agent will be live on Streamlit Cloud! 🚀