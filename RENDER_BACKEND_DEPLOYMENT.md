# 🚀 Render Backend Deployment - Complete Guide

## 📋 Overview
This guide provides detailed instructions for deploying the Autonomous QA Agent backend to Render, a cloud platform that offers free hosting for web services.

## 🎯 Prerequisites

### Required Accounts & Tools:
- ✅ GitHub account with your repository
- ✅ Render account (free tier available)
- ✅ Google Gemini API key
- ✅ Git installed locally

### Repository Requirements:
- ✅ Backend code in `backend/` directory
- ✅ `requirements.txt` with all dependencies
- ✅ `render.yaml` configuration file (already created)
- ✅ Environment variables configured

---

## 📂 Step 1: Prepare Repository for Render

### 1.1 Verify Repository Structure
Ensure your repository has this structure:
```
autonomous-qa-agent/
├── backend/
│   ├── main.py              # FastAPI application
│   └── ...
├── requirements.txt         # Python dependencies
├── render.yaml             # Render configuration
├── runtime.txt             # Python version
└── .env                    # Local environment (not deployed)
```

### 1.2 Update render.yaml Configuration
Let me optimize the render.yaml for better deployment:

```yaml
services:
  - type: web
    name: autonomous-qa-backend
    env: python
    plan: free
    region: oregon  # Choose closest region
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
    startCommand: |
      cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
    healthCheckPath: "/status"
    envVars:
      - key: GEMINI_API_KEY
        sync: false  # Will be set manually in Render dashboard
      - key: ENVIRONMENT
        value: production
      - key: DEBUG
        value: "false"
      - key: LOG_LEVEL
        value: "INFO"
      - key: VECTOR_DB_PATH
        value: "/tmp/vectordb"
      - key: MAX_TOKENS
        value: "2000"
      - key: TEMPERATURE
        value: "0.1"
      - key: GEMINI_MODEL
        value: "gemini-2.0-flash"
    disk:
      name: vectordb-storage
      mountPath: /tmp/vectordb
      sizeGB: 1
```

### 1.3 Commit and Push Changes
```bash
# Navigate to your project directory
cd D:/projects/Resume/Testing/autonomous-qa-agent

# Check current status
git status

# Add all changes
git add .

# Commit with descriptive message
git commit -m "Configure backend for Render deployment"

# Push to GitHub
git push origin main
```

---

## 🌐 Step 2: Deploy to Render

### 2.1 Create Render Account
1. **Visit Render**: Go to [render.com](https://render.com)
2. **Sign Up**: Click "Get Started" 
3. **Connect GitHub**: Choose "Sign up with GitHub"
4. **Authorize**: Allow Render to access your repositories

### 2.2 Create New Web Service

#### Option A: Using render.yaml (Recommended)
1. **Dashboard**: Go to [dashboard.render.com](https://dashboard.render.com)
2. **New**: Click "New +" button
3. **Blueprint**: Select "Blueprint"
4. **Connect Repository**: 
   - Choose `nimish1402/Autonomous_QA_Generator`
   - Click "Connect"
5. **Configure Blueprint**:
   - **Name**: `autonomous-qa-backend`
   - **Branch**: `main`
   - Click "Apply"

#### Option B: Manual Configuration
If Blueprint doesn't work, use manual setup:

1. **New Web Service**: Click "New +" → "Web Service"
2. **Connect Repository**: Select your GitHub repository
3. **Configure Service**:
   ```
   Name: autonomous-qa-backend
   Region: Oregon (US West)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### 2.3 Configure Environment Variables

In the Render dashboard, go to your service → Environment:

#### Required Environment Variables:
```bash
# API Configuration
GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24

# Application Settings
ENVIRONMENT = production
DEBUG = false
LOG_LEVEL = INFO

# Vector Database
VECTOR_DB_PATH = /tmp/vectordb

# LLM Configuration  
MAX_TOKENS = 2000
TEMPERATURE = 0.1
GEMINI_MODEL = gemini-2.0-flash

# Backend Configuration
BACKEND_URL = https://your-service-name.onrender.com
```

**⚠️ Security Note**: Never commit API keys to your repository. Set them only in Render's environment variables.

---

## 🔧 Step 3: Configure Advanced Settings

### 3.1 Health Checks
```
Health Check Path: /status
Health Check Grace Period: 300 seconds
```

### 3.2 Auto-Deploy
- ✅ **Enable**: Auto-deploy from main branch
- ✅ **Enable**: PR previews (optional)

### 3.3 Resource Allocation
**Free Tier Limits**:
- RAM: 512 MB
- CPU: Shared
- Disk: 1 GB SSD
- Sleep after 15 mins of inactivity

---

## 🚀 Step 4: Deploy and Monitor

### 4.1 Initiate Deployment
1. **Deploy**: Click "Create Web Service"
2. **Monitor Build**: Watch the build logs in real-time
3. **Wait**: Initial deployment takes 5-10 minutes

### 4.2 Monitor Deployment Logs
Watch for these key indicators:

#### ✅ Successful Build Logs:
```bash
==> Building application
Installing dependencies from requirements.txt
Successfully installed fastapi uvicorn streamlit...

==> Starting application
INFO: Started server process
INFO: Uvicorn running on http://0.0.0.0:10000
INFO: Using ChromaDB with semantic embeddings
```

#### ❌ Common Build Errors:
```bash
# Dependency conflicts
ERROR: pip's dependency resolver does not currently consider...

# Missing files
FileNotFoundError: [Errno 2] No such file or directory: 'backend/main.py'

# Port binding issues  
OSError: [Errno 98] Address already in use
```

### 4.3 Get Your Backend URL
Once deployed, Render provides:
- **URL**: `https://your-service-name.onrender.com`
- **Custom Domain**: Optional (paid plans)

---

## 🧪 Step 5: Test Your Deployment

### 5.1 API Health Check
Test your deployed backend:

```bash
# Test health endpoint
curl https://your-service-name.onrender.com/status

# Expected response:
{
  "status": "healthy",
  "vector_database": {
    "implementation": "ChromaDB (semantic embeddings)",
    "search_method": "semantic similarity"
  },
  "components": {
    "vector_database": "active (ChromaDB (semantic embeddings))"
  }
}
```

### 5.2 Test API Endpoints
```bash
# Test root endpoint
curl https://your-service-name.onrender.com/

# Test document search (should return empty initially)
curl https://your-service-name.onrender.com/search/test
```

### 5.3 Performance Testing
```bash
# Measure response time
time curl https://your-service-name.onrender.com/status

# Should respond in < 5 seconds (cold start may take longer)
```

---

## ⚡ Step 6: Optimization & Troubleshooting

### 6.1 Common Issues & Solutions

#### **Issue: Build Timeout**
```yaml
# Solution: Optimize requirements.txt
# Remove unused dependencies
# Use lighter alternatives where possible
```

#### **Issue: Memory Errors**
```python
# Solution: Reduce model size in backend
GEMINI_MODEL = "gemini-1.5-flash"  # Lighter model
MAX_TOKENS = 1500  # Reduce token limit
```

#### **Issue: Cold Start Delays**
```python
# Solution: Keep service warm (paid plans)
# Or implement health check pinging
```

#### **Issue: Vector Database Persistence**
```bash
# Free tier has ephemeral storage
# Data resets on each deployment
# Consider external vector database for persistence
```

### 6.2 Performance Optimizations

#### Optimize Dependencies:
```txt
# In requirements.txt, use specific versions
fastapi==0.104.1
uvicorn[standard]==0.24.0
# Remove development dependencies
```

#### Add Caching:
```python
# In backend/main.py, add response caching
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_search(query: str):
    return vector_db.similarity_search(query)
```

---

## 📊 Step 7: Monitoring & Maintenance

### 7.1 Render Dashboard Monitoring
Monitor these metrics:
- **Build Status**: Successful/Failed deployments
- **Runtime Logs**: Application errors and info
- **Metrics**: CPU, Memory, Request count
- **Uptime**: Service availability

### 7.2 Set Up Alerts (Paid Plans)
```yaml
# Example alert configuration
alerts:
  - type: service_down
    channels: [email]
  - type: high_cpu
    threshold: 80%
```

### 7.3 Log Monitoring
```bash
# Key logs to monitor:
INFO: Using ChromaDB with semantic embeddings  # ✅ Good
ERROR: API key not valid                       # ❌ Fix API key
WARNING: Memory usage high                     # ⚠️ Monitor resources
```

---

## 🎯 Step 8: Connect to Frontend

Once backend is deployed:

### 8.1 Note Your Backend URL
```
Backend URL: https://autonomous-qa-backend.onrender.com
```

### 8.2 Update Frontend Configuration
Use this URL when deploying your Streamlit frontend:
```bash
# In Streamlit Cloud environment variables:
BACKEND_URL = https://autonomous-qa-backend.onrender.com
```

---

## 📋 Deployment Checklist

### Pre-Deployment:
- [ ] Repository pushed to GitHub
- [ ] render.yaml configured
- [ ] API keys ready (don't commit to repo)
- [ ] Dependencies updated in requirements.txt

### Deployment:
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Web service created
- [ ] Environment variables set
- [ ] Service deployed successfully

### Testing:
- [ ] Health check endpoint responds
- [ ] API endpoints accessible
- [ ] No error logs in dashboard
- [ ] Response times acceptable

### Production:
- [ ] Backend URL documented
- [ ] Frontend configured with backend URL
- [ ] Monitoring set up
- [ ] Performance optimized

---

## 🚨 Important Notes

### Free Tier Limitations:
- **Sleep Mode**: Service sleeps after 15 minutes of inactivity
- **Cold Start**: First request after sleep takes 30+ seconds
- **Storage**: Ephemeral (resets on deployment)
- **Bandwidth**: 100GB/month limit

### Upgrade Considerations:
- **Starter Plan ($7/month)**: No sleep, more resources
- **Pro Plan ($25/month)**: Auto-scaling, custom domains
- **Team Plan ($100/month)**: Team collaboration features

### Security Best Practices:
- Never commit API keys to repository
- Use Render's environment variables
- Enable HTTPS (automatic on Render)
- Regularly update dependencies

---

## 🎉 Success Metrics

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Service starts and stays running  
- ✅ Health check returns 200 OK
- ✅ API endpoints respond correctly
- ✅ No critical errors in logs
- ✅ Response times < 10 seconds

**Expected Total Deployment Time: 15-20 minutes** ⏱️

Your backend will be live at: `https://your-service-name.onrender.com` 🚀