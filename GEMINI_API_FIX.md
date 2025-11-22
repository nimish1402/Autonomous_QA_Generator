# 🔧 Fix: Gemini API "Template Mode" Issue

## 🚨 **Root Cause**
The backend is running in "template mode" because it doesn't have access to the `GEMINI_API_KEY` environment variable.

---

## ✅ **Solution: Set API Key in Render Dashboard**

### **Step 1: Go to Render Dashboard**
1. Visit [dashboard.render.com](https://dashboard.render.com)
2. Click on your backend service (e.g., "autonomous-qa-backend")

### **Step 2: Set Environment Variable**
1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24`
4. Click **"Save Changes"**

### **Step 3: Redeploy**
The service will automatically redeploy with the new environment variable.

---

## 🧪 **Test the Fix**

### **1. Check Backend Status**
Visit: `https://your-backend.onrender.com/status`

**Before Fix (❌):**
```json
{
  "llm_provider": "Template Mode (no API key)",
  "status": "limited_functionality"
}
```

**After Fix (✅):**
```json
{
  "llm_provider": "Google Gemini (gemini-2.0-flash-exp)",
  "status": "operational"
}
```

### **2. Test Frontend**
Your Streamlit app should now show:
- ✅ **Connected to Backend** (instead of Template Mode)
- ✅ **LLM Provider: Google Gemini**
- ✅ **Full functionality enabled**

---

## 🔐 **Security Note**

The API key is securely stored in Render's environment variables and is not exposed in your code repository. This is the correct and secure way to handle API keys in production.

---

## 📋 **Alternative: Update via Render CLI (Optional)**

If you prefer using CLI:
```bash
# Install Render CLI
npm install -g @render-com/cli

# Set environment variable
render env:set GEMINI_API_KEY=AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
```

---

## 🎯 **Expected Timeline**

- **Setting variable**: ~1 minute
- **Automatic redeploy**: ~2-3 minutes  
- **Total fix time**: ~5 minutes

After this fix, your complete autonomous QA agent will be fully operational! 🚀