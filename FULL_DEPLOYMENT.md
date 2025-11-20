# 🚀 Full Deployment Instructions

## Phase 1: Deploy Backend to Railway (Recommended)

### Step 1: Prepare Your Repository
```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for cloud deployment"
git push origin main
```

### Step 2: Deploy Backend to Railway

1. **Sign up for Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `nimish1402/Autonomous_QA_Generator`

3. **Configure Backend Service**:
   - Railway will auto-detect the Python app
   - Set the start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Or use the railway.toml file (already created)

4. **Set Environment Variables**:
   ```
   GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
   ENVIRONMENT = production
   DEBUG = false
   VECTOR_DB_PATH = /tmp/vectordb
   ```

5. **Deploy and Get URL**:
   - Railway will provide a URL like: `https://your-app.railway.app`
   - Test the API: `https://your-app.railway.app/status`

## Phase 2: Deploy Frontend to Streamlit Cloud

### Step 1: Configure Frontend for Production

Update your repository with the backend URL:

```bash
# The frontend is already configured to read from environment variables
# No code changes needed
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

2. **Create New App**:
   - Click "New app"
   - Select your repository: `nimish1402/Autonomous_QA_Generator`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Set Environment Variables**:
   ```
   BACKEND_URL = https://your-app.railway.app
   GEMINI_API_KEY = AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
   ENVIRONMENT = production
   ```

4. **Deploy**:
   - Click "Deploy!"
   - Wait for deployment to complete
   - Your app will be available at: `https://your-app.streamlit.app`

## Alternative: Deploy Backend to Render

If you prefer Render over Railway:

1. **Go to Render**:
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**:
   - Connect your GitHub repository
   - Use the `render.yaml` configuration (already created)
   - Set environment variables as above

## Alternative: Deploy Backend to Heroku

If you prefer Heroku:

```bash
# Install Heroku CLI first
heroku create your-qa-backend
heroku config:set GEMINI_API_KEY=AIzaSyAmB1-hIC4CNOcYsKfrOWOIK_QmwbAyx24
heroku config:set ENVIRONMENT=production
git push heroku main
```

## Testing Your Deployment

### 1. Test Backend
```bash
curl https://your-backend-url/status
```
Should return:
```json
{
  "status": "healthy",
  "vector_database": {
    "implementation": "ChromaDB (semantic embeddings)"
  }
}
```

### 2. Test Frontend
1. Go to your Streamlit Cloud URL
2. Upload test documents
3. Generate test cases
4. Download Selenium scripts

## Troubleshooting

### Backend Issues:
- **Build fails**: Check requirements.txt dependencies
- **Start fails**: Verify PORT environment variable
- **API errors**: Check GEMINI_API_KEY is set correctly

### Frontend Issues:
- **Cannot connect to backend**: Verify BACKEND_URL
- **Import errors**: Check all dependencies in requirements.txt
- **Timeout errors**: Backend might be cold-starting (wait 30s)

## Production Optimization

### Backend Optimizations:
1. **Add Redis caching** for vector database
2. **Use PostgreSQL** for persistent storage
3. **Add rate limiting** for API calls
4. **Enable HTTPS** and CORS properly

### Frontend Optimizations:
1. **Add error boundaries** for better UX
2. **Implement caching** for repeated requests
3. **Add loading states** for long operations
4. **Optimize file uploads** with progress bars

## Monitoring & Maintenance

### Railway:
- Monitor logs in Railway dashboard
- Set up alerts for errors
- Monitor resource usage

### Streamlit Cloud:
- Check app analytics
- Monitor performance metrics
- Update dependencies regularly

---

## Quick Command Summary

```bash
# 1. Prepare repository
git add . && git commit -m "Deploy to cloud" && git push

# 2. Deploy backend to Railway
# - Use railway.app web interface
# - Connect GitHub repo
# - Set environment variables

# 3. Deploy frontend to Streamlit Cloud  
# - Use share.streamlit.io
# - Connect GitHub repo
# - Set BACKEND_URL from Railway

# 4. Test deployment
curl https://your-backend.railway.app/status
# Visit https://your-app.streamlit.app
```

**Your full-stack Autonomous QA Agent will be live in ~10 minutes!** 🚀