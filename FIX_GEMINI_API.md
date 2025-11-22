# 🔧 Fix Gemini API "Template Mode" Issue

## ❌ **Problem:** Gemini API showing "template mode" in Streamlit Cloud

## ✅ **Root Cause & Solutions:**

The Gemini API key needs to be configured in **TWO places**:

---

### **1. Render Backend (Most Important)**

Your backend needs the API key to make LLM calls.

#### **A. Add to Render Environment Variables:**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your backend service: `autonomous-qa-backend`
3. Go to **Environment** tab
4. Add/Update:
   ```
   Key: GEMINI_API_KEY
   Value: AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
   ```
5. **Save Changes** and **Redeploy**

#### **B. Verify Backend Configuration:**
Test your backend directly:
```bash
curl https://autonomous-qa-backend.onrender.com/config
```
Should show: `"gemini_available": true`

---

### **2. Streamlit Cloud Frontend (Optional)**

#### **A. Update Streamlit Secrets:**
In your Streamlit Cloud app settings:

1. Go to **"Settings"** → **"Secrets"**
2. Add/Update:
```toml
BACKEND_URL = "https://autonomous-qa-backend.onrender.com"
ENVIRONMENT = "production"
GEMINI_API_KEY = "AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24"
```

#### **B. Restart Streamlit App:**
Click **"Reboot"** in Streamlit Cloud dashboard

---

## 🧪 **Testing Steps:**

### **1. Test Backend API Direct:**
```bash
# Health check
curl https://autonomous-qa-backend.onrender.com/health

# Config check (should show Gemini available)
curl https://autonomous-qa-backend.onrender.com/config

# Status check
curl https://autonomous-qa-backend.onrender.com/status
```

### **2. Test Frontend Connection:**
1. Open your Streamlit app
2. Check if backend connection shows "Connected"
3. Try uploading a document
4. Try generating test cases (should work now)

---

## 🎯 **Expected Results After Fix:**

✅ **Backend `/config` endpoint shows:**
```json
{
  "gemini_available": true,
  "gemini_model": "gemini-2.0-flash-exp"
}
```

✅ **Frontend shows:**
- Backend connection: "Connected" 
- LLM functionality: Working
- Test case generation: Enabled

---

## 🚨 **If Still Not Working:**

### **Check Backend Logs:**
1. Render Dashboard → Your service → **Logs**
2. Look for:
   - `GEMINI_API_KEY loaded successfully`
   - No `API key not found` errors

### **Verify API Key:**
Test the API key directly:
```bash
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"test"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24"
```

---

## 📋 **Quick Fix Checklist:**

1. ✅ Add `GEMINI_API_KEY` to Render environment variables
2. ✅ Redeploy Render backend service  
3. ✅ Update Streamlit Cloud secrets
4. ✅ Restart Streamlit app
5. ✅ Test backend `/config` endpoint
6. ✅ Test frontend LLM features

**Most likely fix: Step 1 (Render environment variables)** 🎯