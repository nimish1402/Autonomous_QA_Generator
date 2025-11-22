# 🚀 Render Deployment - Quick Reference

## **One-Command Validation**
```bash
python deploy.py validate && python deploy.py test
```

## **Essential Steps**

### 1. **Prepare Repository**
```bash
git add . && git commit -m "Ready for Render" && git push origin main
```

### 2. **Deploy on Render**
1. Go to [render.com](https://render.com) → Sign up with GitHub
2. New → Blueprint → Connect `nimish1402/Autonomous_QA_Generator`
3. Branch: `main` → Apply

### 3. **Set Environment Variables**
```bash
GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
ENVIRONMENT = production
DEBUG = false
```

### 4. **Validate Deployment**
```bash
curl https://your-service.onrender.com/health
curl https://your-service.onrender.com/deployment/validate
```

## **Key URLs After Deployment**
- **Health**: `https://your-service.onrender.com/health`
- **Status**: `https://your-service.onrender.com/status`
- **Validation**: `https://your-service.onrender.com/deployment/validate`
- **API Docs**: `https://your-service.onrender.com/docs`

## **Expected Timeline: 15-20 minutes**

## **Success Indicators**
- ✅ Service shows "Live" in Render dashboard
- ✅ Health check returns `{"status": "healthy"}`
- ✅ No errors in deployment logs
- ✅ All endpoints respond with 200 OK

## **Free Tier Limitations**
- 512MB RAM
- Sleeps after 15 minutes
- 750 hours/month
- Cold start delays (30+ seconds)

## **Troubleshooting Commands**
```bash
# Local validation
python deploy.py validate

# Test deployed backend  
python deploy.py check

# Get Streamlit config
python deploy.py config
```

## **Next Step: Frontend**
After backend deployment, deploy frontend to Streamlit Cloud:
- Main file: `streamlit_cloud_app.py`
- Environment: `BACKEND_URL = https://your-service.onrender.com`

---
**🎉 Your AI-powered QA automation platform is now live!**