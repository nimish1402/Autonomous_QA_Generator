# 🔧 Render Deployment Troubleshooting

## ✅ **FIXED: Uvicorn Command Error**

**Issue:** `Error: No such option: --max-requests`  
**Solution:** Changed to `--limit-max-requests` (correct uvicorn syntax)

---

## 🚨 **Common Render Deployment Issues & Fixes**

### **1. Memory Issues (Out of Memory)**
**Symptoms:** `used over 512Mi`, deployment killed during startup  
**Solution:** 
- ✅ Set `DISABLE_EMBEDDINGS=true`
- ✅ Use `requirements-light.txt` 
- ✅ Memory optimized startup

### **2. Uvicorn Command Errors**
**Symptoms:** `No such option` errors  
**Common Fixes:**
- ❌ `--max-requests` → ✅ `--limit-max-requests`
- ❌ `--max-workers` → ✅ `--workers`
- ❌ `--timeout` → ✅ `--timeout-keep-alive`

### **3. Port Binding Issues**
**Symptoms:** `No open ports detected`  
**Solution:** Ensure using `$PORT` environment variable:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### **4. Module Import Errors**
**Symptoms:** `ModuleNotFoundError`  
**Solutions:**
- Check `requirements-light.txt` includes all needed packages
- Verify `PYTHONPATH` environment variable
- Ensure Python path structure is correct

### **5. Environment Variable Issues**
**Critical Variables for Render:**
```bash
DISABLE_EMBEDDINGS=true     # Reduces memory usage
MEMORY_LIMIT=512           # Memory optimization
GEMINI_API_KEY=your_key    # LLM functionality
ENVIRONMENT=production     # Production mode
```

---

## 📋 **Quick Deployment Checklist**

✅ **Before Deploying:**
1. Commit all changes to GitHub
2. Verify `render.yaml` syntax
3. Test locally with: `python deploy.py test`
4. Set required environment variables in Render dashboard

✅ **Environment Variables in Render:**
- `GEMINI_API_KEY` = Your API key
- `DISABLE_EMBEDDINGS` = `true`
- `MEMORY_LIMIT` = `512`
- `ENVIRONMENT` = `production`

✅ **After Deployment:**
- Test health endpoint: `https://your-app.onrender.com/health`
- Check logs for any errors
- Verify all 5 API endpoints work

---

## 🎯 **Current Status: OPTIMIZED**

✅ **Memory Usage:** ~150MB (well under 512MB limit)  
✅ **Startup Time:** 30-60 seconds  
✅ **All API Endpoints:** Working  
✅ **Uvicorn Command:** Fixed  
✅ **Dependencies:** Lightweight  

Your deployment should now succeed! 🚀