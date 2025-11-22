# 🎨 Complete Render Deployment Guide
## Autonomous QA Agent Backend

This comprehensive guide will walk you through deploying your Autonomous QA Agent backend to Render step-by-step.

---

## 📋 **Prerequisites**

Before starting, ensure you have:

- ✅ **GitHub Account**: Your code must be pushed to GitHub
- ✅ **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
- ✅ **Google Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- ✅ **Local Testing**: Your backend works locally

---

## 🔧 **Step 1: Prepare Your Repository**

### 1.1 Validate Your Local Setup
```bash
cd "d:\projects\Resume\Testing\autonomous-qa-agent"
python deploy.py validate
```

**Expected Output:**
```
🔍 Validating Local Environment...
✅ Python 3.12 (compatible)
✅ requirements.txt
✅ backend/main.py
✅ render.yaml
✅ railway.toml
```

### 1.2 Test Backend Locally
```bash
python deploy.py test
```

This will:
- Start the backend server
- Test all endpoints (/health, /status, /config, etc.)
- Verify everything works correctly

### 1.3 Commit and Push Changes
```bash
# Navigate to project directory
cd "d:\projects\Resume\Testing\autonomous-qa-agent"

# Check current status
git status

# Add all files
git add .

# Commit changes
git commit -m "Ready for Render deployment - Added deployment endpoints"

# Push to GitHub
git push origin main
```

**Important**: Ensure your repository is public or you have a paid GitHub plan for private repos.

---

## 🌐 **Step 2: Create Render Account & Connect GitHub**

### 2.1 Sign Up for Render
1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub repositories

### 2.2 Verify Account
- Check your email for verification link
- Complete account setup
- Navigate to the Render Dashboard

---

## 🚀 **Step 3: Deploy Using Blueprint (Recommended Method)**

### 3.1 Create New Blueprint
1. **In Render Dashboard**: Click **"New +"** button
2. **Select**: **"Blueprint"**
3. **Connect Repository**:
   - Choose **"Connect a repository"**
   - Select `nimish1402/Autonomous_QA_Generator`
   - Click **"Connect"**

### 3.2 Configure Blueprint
1. **Repository**: `nimish1402/Autonomous_QA_Generator`
2. **Branch**: `main`
3. **Blueprint file**: `render.yaml` (should be auto-detected)
4. **Service name**: `autonomous-qa-backend` (or your preferred name)

### 3.3 Review Configuration
Render will show you the configuration from your `render.yaml` file:

```yaml
services:
  - type: web
    name: autonomous-qa-backend
    env: python
    plan: free
    region: oregon
    pythonVersion: 3.11.7
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
    startCommand: |
      python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers 1
    healthCheckPath: "/health"
```

### 3.4 Apply Blueprint
1. Review the configuration
2. Click **"Apply"**
3. Render will start the deployment process

---

## ⚙️ **Step 4: Configure Environment Variables**

### 4.1 Set Required Environment Variables
While the deployment is in progress, set up environment variables:

1. **In Render Dashboard**: Go to your service
2. **Click**: **"Environment"** tab
3. **Add the following variables**:

```bash
# Required Variables
GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
ENVIRONMENT = production
DEBUG = false
LOG_LEVEL = INFO

# Optional Variables (with defaults)
VECTOR_DB_PATH = /tmp/vectordb
MAX_TOKENS = 2000
TEMPERATURE = 0.1
GEMINI_MODEL = gemini-2.0-flash
```

### 4.2 Save Configuration
- Click **"Save Changes"**
- This will trigger a redeploy with the new environment variables

---

## 📊 **Step 5: Monitor Deployment**

### 5.1 Watch Build Logs
1. **Go to**: **"Logs"** tab in your service
2. **Monitor**: Build and deployment progress

**Expected Build Output:**
```bash
==> Building application
Installing dependencies from requirements.txt
Successfully installed fastapi uvicorn streamlit chromadb...

==> Starting application
INFO: Using ChromaDB with semantic embeddings
🚀 Starting Autonomous QA Agent Backend
🔢 Environment: production
🌐 Port: 10000
📁 Vector DB Path: /tmp/vectordb
🤖 LLM Available: True
INFO: Uvicorn running on http://0.0.0.0:10000
```

### 5.2 Check Service Status
Once deployment completes:
- **Status**: Should show **"Live"** in green
- **URL**: Will be provided (e.g., `https://autonomous-qa-backend.onrender.com`)

---

## 🧪 **Step 6: Test Your Deployment**

### 6.1 Test Health Check
```bash
curl https://your-service-name.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-22",
  "service": "autonomous-qa-agent"
}
```

### 6.2 Test All Endpoints
```bash
# System status
curl https://your-service-name.onrender.com/status

# Deployment validation
curl https://your-service-name.onrender.com/deployment/validate

# System configuration
curl https://your-service-name.onrender.com/config

# Analytics
curl https://your-service-name.onrender.com/analytics
```

### 6.3 Use Deployment Script
```bash
python deploy.py check
# Enter your Render URL when prompted
```

---

## 🔧 **Step 7: Advanced Configuration**

### 7.1 Custom Domain (Optional)
If you have a custom domain:
1. **Go to**: **"Settings"** tab
2. **Click**: **"Custom Domains"**
3. **Add**: Your domain
4. **Configure**: DNS settings as instructed

### 7.2 Auto-Deploy Settings
1. **Go to**: **"Settings"** tab
2. **Auto-Deploy**: Enable/disable automatic deployment on git push
3. **Branch**: Ensure it's set to `main`

### 7.3 Health Check Configuration
Your service is configured with:
- **Health Check Path**: `/health`
- **Grace Period**: 300 seconds
- **Timeout**: 30 seconds

---

## 📈 **Step 8: Monitoring & Maintenance**

### 8.1 Monitor Service Health
**Render Dashboard Metrics**:
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

### 8.2 View Logs
```bash
# In Render Dashboard: Logs tab
# Or use Render CLI (optional):
render logs -s your-service-name --tail
```

### 8.3 Check Deployment Status
Visit your deployment validation endpoint:
```
https://your-service-name.onrender.com/deployment/validate
```

**Healthy Response:**
```json
{
  "deployment_status": "ready",
  "checks": {
    "port": {"status": "✅", "message": "Port 10000 is valid"},
    "environment": {"status": "✅", "message": "Environment: production"},
    "vector_db": {"status": "✅", "message": "Vector database operational"},
    "llm": {"status": "✅", "message": "LLM client available"}
  },
  "errors": [],
  "warnings": []
}
```

---

## 🚨 **Troubleshooting**

### Common Issues and Solutions

#### **Issue 1: Build Fails**
**Symptoms**: Build logs show dependency errors
**Solution**:
```bash
# Check requirements.txt format
# Ensure all dependencies are correctly specified
# Common fix: Update requirements.txt versions
```

#### **Issue 2: Service Won't Start**
**Symptoms**: Build succeeds but service shows "Build failed"
**Solution**:
1. Check environment variables are set correctly
2. Verify GEMINI_API_KEY format
3. Check logs for specific error messages

#### **Issue 3: Health Check Fails**
**Symptoms**: Service shows unhealthy status
**Solutions**:
```bash
# 1. Verify health endpoint works:
curl https://your-service.onrender.com/health

# 2. Check if port is correct in logs
# 3. Increase health check grace period if needed
```

#### **Issue 4: Memory Issues**
**Symptoms**: Service crashes with memory errors
**Solution**:
```bash
# Free tier has 512MB RAM limit
# Optimize by:
# 1. Using lighter sentence transformer models
# 2. Reducing worker count to 1
# 3. Consider upgrading to paid plan
```

#### **Issue 5: Cold Start Delays**
**Symptoms**: First request takes 30+ seconds
**This is normal for free tier**:
- Free services sleep after 15 minutes of inactivity
- First request "wakes up" the service
- Consider paid plan for always-on service

---

## 💰 **Render Pricing Tiers**

### **Free Tier** (What you're using)
- ✅ 750 hours/month
- ✅ 512 MB RAM
- ✅ Shared CPU
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ Cold start delays

### **Starter Plan** ($7/month)
- ✅ Always on (no sleeping)
- ✅ 1 GB RAM
- ✅ 1 CPU
- ✅ Faster builds

### **Standard Plan** ($25/month)
- ✅ 2 GB RAM
- ✅ 2 CPUs  
- ✅ Auto-scaling
- ✅ Custom domains

---

## 🎯 **Success Checklist**

Your deployment is successful when:

- [ ] ✅ Service shows "Live" status in Render dashboard
- [ ] ✅ Health check returns 200 OK
- [ ] ✅ `/deployment/validate` shows "ready" status
- [ ] ✅ All API endpoints respond correctly
- [ ] ✅ No critical errors in service logs
- [ ] ✅ Environment variables are properly set
- [ ] ✅ Vector database is operational

---

## 🔗 **Next Steps: Connect Frontend**

Once your backend is deployed:

### 1. **Note Your Backend URL**
```
Backend URL: https://autonomous-qa-backend.onrender.com
```

### 2. **Deploy Frontend to Streamlit Cloud**
```bash
python deploy.py config
# This will show you the Streamlit configuration
```

### 3. **Set Streamlit Environment Variables**
```bash
BACKEND_URL = https://autonomous-qa-backend.onrender.com
GEMINI_API_KEY = your_api_key_here
ENVIRONMENT = production
```

---

## 📞 **Support & Resources**

### **Render Documentation**
- [Render Docs](https://render.com/docs)
- [Python Deployment Guide](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)

### **Project Resources**
- **Health Check**: `https://your-service.onrender.com/health`
- **Full Status**: `https://your-service.onrender.com/status`
- **Deployment Validation**: `https://your-service.onrender.com/deployment/validate`
- **API Documentation**: `https://your-service.onrender.com/docs` (FastAPI auto-docs)

### **Getting Help**
1. Check Render logs first
2. Use deployment validation endpoint
3. Test individual endpoints
4. Check environment variables
5. Review this guide step-by-step

---

## 🎉 **Congratulations!**

Your Autonomous QA Agent backend is now live on Render! 

**Your deployed service provides**:
- 🔄 Document processing and ingestion
- 🤖 AI-powered test case generation  
- 🧪 Selenium script generation
- 📊 Analytics and monitoring
- 🔍 Semantic search capabilities

**Access your service at**: `https://your-service-name.onrender.com`

---

## ⏱️ **Deployment Timeline**

- **Preparation**: 5-10 minutes
- **Repository Setup**: 2-3 minutes
- **Render Account**: 2-3 minutes
- **Deployment**: 5-10 minutes
- **Testing**: 3-5 minutes
- **Total**: 15-25 minutes

**🎊 Your backend is now production-ready and accessible worldwide!**