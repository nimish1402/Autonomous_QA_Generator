# 🚀 Streamlit Cloud Frontend Deployment Guide

## ✅ **Prerequisites Complete**
- ✅ Backend deployed to Render and working
- ✅ Frontend configuration files created
- ✅ Dependencies optimized for Streamlit Cloud

---

## 📋 **Step-by-Step Streamlit Cloud Deployment**

### **1. Commit Frontend Changes**
```bash
git add .
git commit -m "Prepare frontend for Streamlit Cloud deployment"
git push origin main
```

### **2. Deploy to Streamlit Cloud**

#### **A. Go to Streamlit Cloud**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account

#### **B. Create New App**
1. Click **"New app"**
2. Select **"From existing repo"**
3. **Repository**: `nimish1402/Autonomous_QA_Generator`
4. **Branch**: `main`
5. **Main file path**: `streamlit_app.py`

#### **C. Configure Environment**
1. Click **"Advanced settings"**
2. **Python version**: `3.9` or `3.10` (Streamlit Cloud default)
3. **Requirements file**: `requirements-streamlit.txt`

#### **D. Set Secrets (Environment Variables)**
In the Streamlit Cloud dashboard, go to **"Secrets"** and add:
```toml
BACKEND_URL = "https://YOUR-RENDER-APP-NAME.onrender.com"
ENVIRONMENT = "production"
```

**Replace `YOUR-RENDER-APP-NAME` with your actual Render app URL!**

**⚠️ Important**: The `GEMINI_API_KEY` should be set in your **Render backend**, not Streamlit Cloud. The frontend connects to your backend via API calls.

### **3. Deploy**
Click **"Deploy!"** - Streamlit will build and deploy your frontend.

---

## 🔗 **Important: Update Backend URL**

### **Find Your Render Backend URL:**
1. Go to your Render dashboard
2. Copy your backend service URL (e.g., `https://autonomous-qa-backend-xyz.onrender.com`)

### **Update the Frontend Configuration:**
Replace `YOUR-RENDER-APP-NAME` in these files:
1. `.streamlit/secrets.toml`
2. Your Streamlit Cloud secrets

---

## 🧪 **Testing Your Deployment**

### **Frontend Tests:**
1. **Homepage loads**: Streamlit app appears
2. **Backend connection**: Status shows "Connected"
3. **File upload**: Can upload documents
4. **API calls**: Generate test cases and scripts work

### **Full Integration Test:**
1. Upload a document via frontend
2. Generate test cases
3. Create Selenium scripts
4. Verify all features work end-to-end

---

## 📁 **Files Created for Deployment:**

✅ `streamlit_app.py` - Main entry point  
✅ `requirements-streamlit.txt` - Lightweight dependencies  
✅ `.streamlit/config.toml` - UI configuration  
✅ `.streamlit/secrets.toml` - Environment variables template  
✅ Updated `frontend/app_enhanced.py` - Dynamic backend URL  

---

## 🔧 **Troubleshooting**

### **Common Issues:**

**1. "Cannot connect to backend"**
- Check backend URL in Streamlit secrets
- Verify Render backend is running
- Check CORS settings

**2. "Module not found"**
- Verify `requirements-streamlit.txt` has all needed packages
- Check Python version compatibility

**3. "Streamlit app won't start"**
- Verify `streamlit_app.py` is in repo root
- Check file path in Streamlit Cloud settings

---

## 🎯 **Expected Result**

After deployment, you'll have:
- **Backend**: `https://your-backend.onrender.com` (✅ Already deployed)  
- **Frontend**: `https://your-app.streamlit.app` (🔄 To be deployed)

Both services will communicate via API calls, providing a complete autonomous QA solution accessible from anywhere! 🎉

---

## 📞 **Next Steps After Reading This:**

1. **Commit the frontend changes** (commands above)
2. **Get your Render backend URL** from dashboard
3. **Deploy to Streamlit Cloud** following steps 2A-2D
4. **Test the full application**

Ready to deploy? 🚀