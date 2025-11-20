## 📋 Render Backend Deployment - Quick Checklist

### ✅ Pre-Deployment (5 minutes)
- [ ] Run preparation script: `python prepare_render_deployment.py`
- [ ] Commit changes: `git add . && git commit -m "Ready for Render"`
- [ ] Push to GitHub: `git push origin main`
- [ ] Verify API key in .env: `AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24`

### 🌐 Render Setup (3 minutes)
- [ ] Go to [render.com](https://render.com)
- [ ] Sign up with GitHub account
- [ ] Connect repository: `nimish1402/Autonomous_QA_Generator`
- [ ] Create new Blueprint service

### ⚙️ Configuration (2 minutes)
- [ ] Service name: `autonomous-qa-backend`
- [ ] Branch: `main`
- [ ] Use `render.yaml` configuration
- [ ] Set environment variable: `GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24`

### 🚀 Deployment (5-10 minutes)
- [ ] Click "Apply" to start deployment
- [ ] Monitor build logs for errors
- [ ] Wait for "Live" status
- [ ] Note your backend URL: `https://[service-name].onrender.com`

### 🧪 Testing (2 minutes)
- [ ] Test health check: `curl https://your-service.onrender.com/status`
- [ ] Verify API response includes ChromaDB info
- [ ] Check for any error logs in Render dashboard

### 📝 Next Steps
- [ ] Save backend URL for frontend deployment
- [ ] Deploy frontend to Streamlit Cloud with this backend URL
- [ ] Test full application workflow

---

## 🚨 Quick Troubleshooting

**Build Fails?**
- Check requirements.txt has all dependencies
- Verify Python version in runtime.txt

**Service Won't Start?**
- Check GEMINI_API_KEY is set correctly
- Verify startCommand in render.yaml

**API Errors?**
- Check environment variables in Render dashboard
- Monitor service logs for specific error messages

**Cold Start Issues?**
- First request after 15min sleep takes 30+ seconds
- Consider upgrading to paid plan for always-on service

---

## ⏱️ Expected Timeline
- **Preparation**: 5 minutes
- **Render Setup**: 3 minutes  
- **Deployment**: 5-10 minutes
- **Testing**: 2 minutes
- **Total**: 15-20 minutes

## 🎯 Success Criteria
✅ Service status shows "Live"
✅ `/status` endpoint returns 200 OK
✅ Logs show "Using ChromaDB with semantic embeddings"
✅ No critical errors in dashboard