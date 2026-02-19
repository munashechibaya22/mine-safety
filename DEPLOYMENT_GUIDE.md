# Mine Safety System - Deployment Guide

## Option 1: Render.com (Recommended for School Projects)

### Prerequisites
- GitHub account
- Your code pushed to GitHub repository

### Backend Deployment (FastAPI)

1. **Prepare Backend**
   - Create `render.yaml` in project root (see below)
   - Ensure `requirements.txt` is up to date

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - Name: `mine-safety-backend`
     - Environment: `Python 3`
     - Build Command: `pip install -r mine-safety-backend/requirements.txt`
     - Start Command: `cd mine-safety-backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click "Create Web Service"

3. **Environment Variables**
   Add these in Render dashboard:
   ```
   DATABASE_URL=sqlite:///./mine_safety.db
   SECRET_KEY=your-secret-key-here
   ```

### Frontend Deployment (React)

1. **Update API URL**
   In `mine-safety-frontend/src/context/AuthContext.jsx`:
   ```javascript
   const API_URL = 'https://mine-safety-backend.onrender.com/api';
   ```

2. **Deploy on Render**
   - Click "New +" → "Static Site"
   - Connect repository
   - Configure:
     - Name: `mine-safety-frontend`
     - Build Command: `cd mine-safety-frontend && npm install && npm run build`
     - Publish Directory: `mine-safety-frontend/dist`
   - Click "Create Static Site"

### Database
- For demo: Use SQLite (included)
- For production: Upgrade to PostgreSQL on Render

---

## Option 2: Railway.app (Alternative)

### Backend Deployment

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**
   ```bash
   railway login
   cd mine-safety-backend
   railway init
   railway up
   ```

3. **Add Environment Variables**
   ```bash
   railway variables set SECRET_KEY=your-secret-key
   railway variables set DATABASE_URL=sqlite:///./mine_safety.db
   ```

### Frontend Deployment

1. **Deploy to Vercel**
   ```bash
   cd mine-safety-frontend
   npm install -g vercel
   vercel
   ```

2. **Set Environment Variable**
   - Add `VITE_API_URL` in Vercel dashboard
   - Value: Your Railway backend URL

---

## Option 3: Hugging Face Spaces (AI Showcase)

Perfect for showcasing your ML model!

1. **Create Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Gradio" or "Streamlit"

2. **Create Simple Interface**
   ```python
   # app.py
   import gradio as gr
   from detection_service import detection_service
   
   def detect_safety(image):
       result = detection_service.detect_image(image)
       return result['reason'], result['is_safe']
   
   demo = gr.Interface(
       fn=detect_safety,
       inputs=gr.Image(type="filepath"),
       outputs=[gr.Textbox(label="Result"), gr.Label(label="Status")],
       title="Mine Safety Detection System",
       description="Upload an image to check PPE compliance"
   )
   
   demo.launch()
   ```

3. **Push to Space**
   ```bash
   git remote add space https://huggingface.co/spaces/YOUR_USERNAME/mine-safety
   git push space main
   ```

---

## Option 4: Docker + Any Cloud Platform

### Create Dockerfiles

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY mine-safety-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mine-safety-backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY mine-safety-frontend/package*.json ./
RUN npm install

COPY mine-safety-frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Deploy to:
- Google Cloud Run
- AWS ECS
- Azure Container Apps
- DigitalOcean App Platform

---

## Quick Comparison

| Platform | Cost | Ease | Best For |
|----------|------|------|----------|
| Render | Free | ⭐⭐⭐⭐⭐ | School projects |
| Railway | $5/mo | ⭐⭐⭐⭐ | Quick demos |
| Vercel + Railway | Free | ⭐⭐⭐⭐ | Professional look |
| Hugging Face | Free | ⭐⭐⭐ | ML showcases |
| Google Cloud | Pay-per-use | ⭐⭐⭐ | Scalable apps |

---

## For Your School Project

**I recommend: Render.com**

Why?
1. ✓ Completely free
2. ✓ No credit card required
3. ✓ Easy to set up
4. ✓ Professional URL
5. ✓ Your teachers can access it
6. ✓ Auto-deploys from GitHub

**Estimated Setup Time:** 30 minutes

---

## Post-Deployment Checklist

- [ ] Backend is accessible at your URL
- [ ] Frontend loads correctly
- [ ] Can register new user
- [ ] Can login
- [ ] Can upload image
- [ ] Detection works
- [ ] Dashboard shows data
- [ ] History page works

---

## Troubleshooting

### Backend won't start
- Check logs in Render dashboard
- Verify all dependencies in requirements.txt
- Check environment variables

### Frontend can't connect to backend
- Update API_URL in frontend code
- Enable CORS in backend (already done)
- Check network tab in browser DevTools

### Model not loading
- Ensure best.onnx is in repository
- Check file size (GitHub has 100MB limit)
- Consider using Git LFS for large files

### Database issues
- For demo: Use SQLite
- For production: Switch to PostgreSQL
- Update DATABASE_URL environment variable

---

## Need Help?

Common issues and solutions:
1. **Port binding error**: Use `$PORT` environment variable
2. **Module not found**: Add to requirements.txt
3. **CORS error**: Already configured in main.py
4. **File upload fails**: Check UPLOAD_DIR permissions

Good luck with your deployment! 🚀
