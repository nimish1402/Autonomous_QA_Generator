## 🚀 Deployment Checklist

### ✅ Pre-Deployment Preparation
- [ ] All code committed to GitHub
- [ ] API key updated in .env
- [ ] Requirements.txt updated
- [ ] Backend configured for cloud (PORT variable)
- [ ] CORS configured for production
- [ ] Vector database path configurable

### 📋 Backend Deployment (Railway)
- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] Environment variables set:
  - [ ] GEMINI_API_KEY
  - [ ] ENVIRONMENT=production
  - [ ] VECTOR_DB_PATH=/tmp/vectordb
- [ ] Backend deployed successfully
- [ ] API health check passes: `/status`
- [ ] Backend URL noted for frontend

### 🎨 Frontend Deployment (Streamlit Cloud)
- [ ] Streamlit Cloud account created
- [ ] GitHub repository connected
- [ ] Main file set to: `streamlit_app.py`
- [ ] Environment variables set:
  - [ ] BACKEND_URL (from Railway)
  - [ ] GEMINI_API_KEY
  - [ ] ENVIRONMENT=production
- [ ] Frontend deployed successfully
- [ ] Frontend connects to backend

### 🧪 Post-Deployment Testing
- [ ] Frontend loads without errors
- [ ] Document upload works
- [ ] Backend API connectivity verified
- [ ] Test case generation functional
- [ ] Selenium script generation works
- [ ] Download functionality works
- [ ] Error handling displays properly

### 🔧 Optional Optimizations
- [ ] Custom domain configured
- [ ] Monitoring set up
- [ ] Performance optimization
- [ ] Security headers added
- [ ] Rate limiting implemented

---

## 📞 Quick Start Commands

```bash
# 1. Prepare for deployment
git add .
git commit -m "Ready for cloud deployment"
git push origin main

# 2. Deploy backend (Railway)
# Visit: https://railway.app
# Connect GitHub repo
# Deploy automatically

# 3. Deploy frontend (Streamlit Cloud)
# Visit: https://share.streamlit.io
# Connect GitHub repo
# Set main file: streamlit_app.py

# 4. Test deployment
curl https://your-backend.railway.app/status
# Visit: https://your-app.streamlit.app
```

**Expected completion time: 10-15 minutes** ⏱️