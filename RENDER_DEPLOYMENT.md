# Deploy to Render with PostgreSQL

## Overview

This guide will help you deploy your Mine Safety Detection System to Render with:
- ✓ FastAPI Backend
- ✓ React Frontend  
- ✓ PostgreSQL Database
- ✓ All FREE tier

## Prerequisites

1. GitHub account
2. Render account (sign up at [render.com](https://render.com))
3. Your code pushed to GitHub

## Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for Render deployment"

# Create repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/mine-safety.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Using Blueprint (Automatic)

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" → "Blueprint"

2. **Connect Repository**
   - Select your GitHub repository
   - Render will detect `render.yaml`
   - Click "Apply"

3. **Wait for Deployment**
   - Render will automatically:
     - Create PostgreSQL database
     - Deploy backend
     - Deploy frontend
     - Connect everything
   - Takes ~5-10 minutes

4. **Get Your URLs**
   - Backend: `https://mine-safety-backend.onrender.com`
   - Frontend: `https://mine-safety-frontend.onrender.com`
   - Database: Auto-connected

### Step 3: Update Frontend API URL

After deployment, update your frontend to use the production backend:

**File:** `mine-safety-frontend/src/context/AuthContext.jsx`

```javascript
// Change this line:
const API_URL = 'http://localhost:8000/api';

// To your Render backend URL:
const API_URL = 'https://mine-safety-backend.onrender.com/api';
```

Then commit and push:
```bash
git add .
git commit -m "Update API URL for production"
git push
```

Render will auto-redeploy the frontend.

---

## Alternative: Manual Deployment

If you prefer manual setup:

### 1. Create PostgreSQL Database

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Configure:
   - Name: `mine-safety-db`
   - Database: `mine_safety_db`
   - User: `mine_safety_user`
   - Region: Oregon
   - Plan: Free
3. Click "Create Database"
4. Copy the "Internal Database URL"

### 2. Deploy Backend

1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure:
   - Name: `mine-safety-backend`
   - Root Directory: `mine-safety-backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `DATABASE_URL`: Paste the Internal Database URL
   - `SECRET_KEY`: Click "Generate" for random key
5. Click "Create Web Service"

### 3. Deploy Frontend

1. Click "New +" → "Static Site"
2. Connect your repository
3. Configure:
   - Name: `mine-safety-frontend`
   - Root Directory: `mine-safety-frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
4. Click "Create Static Site"

---

## Database Migration

After deployment, your database will be empty. The tables will be created automatically on first run thanks to SQLAlchemy.

To verify:
1. Go to your backend URL: `https://mine-safety-backend.onrender.com/docs`
2. Try the `/api/auth/register` endpoint
3. Create a test user
4. Check if it works!

---

## Environment Variables

Your backend needs these environment variables (auto-set by Blueprint):

| Variable | Value | Source |
|----------|-------|--------|
| `DATABASE_URL` | PostgreSQL connection string | From database |
| `SECRET_KEY` | Random secure key | Auto-generated |
| `PYTHON_VERSION` | 3.11.0 | Set in render.yaml |

---

## Troubleshooting

### Backend won't start

**Check logs:**
1. Go to Render dashboard
2. Click on your backend service
3. Click "Logs" tab
4. Look for errors

**Common issues:**
- Missing dependencies → Check requirements.txt
- Database connection → Verify DATABASE_URL
- Port binding → Make sure using `$PORT` variable

### Frontend can't connect to backend

**Solution:**
1. Update API_URL in `AuthContext.jsx`
2. Enable CORS (already done in main.py)
3. Check browser console for errors

### Database connection fails

**Solution:**
1. Verify DATABASE_URL is set correctly
2. Check if database is running (Render dashboard)
3. Ensure psycopg2-binary is in requirements.txt

### Model file too large

**Problem:** GitHub has 100MB file limit

**Solution:**
1. Use Git LFS:
   ```bash
   git lfs install
   git lfs track "*.onnx"
   git add .gitattributes
   git add best.onnx
   git commit -m "Add model with LFS"
   git push
   ```

2. Or host model elsewhere and download on startup

---

## Free Tier Limits

Render Free Tier includes:
- ✓ 750 hours/month (enough for 24/7)
- ✓ 512 MB RAM
- ✓ 0.1 CPU
- ✓ PostgreSQL: 1GB storage, 97 connection limit
- ✓ Auto-sleep after 15 min inactivity (wakes on request)

**Note:** First request after sleep takes ~30 seconds (cold start)

---

## Post-Deployment Checklist

- [ ] Backend is accessible
- [ ] Frontend loads
- [ ] Can register new user
- [ ] Can login
- [ ] Can upload image
- [ ] Detection works
- [ ] Dashboard shows data
- [ ] Database persists data

---

## Monitoring

**Check service health:**
1. Backend: `https://mine-safety-backend.onrender.com/docs`
2. Frontend: `https://mine-safety-frontend.onrender.com`

**View logs:**
- Render Dashboard → Your Service → Logs tab

**Database stats:**
- Render Dashboard → Your Database → Metrics tab

---

## Updating Your Deployment

**Automatic updates:**
- Push to GitHub → Render auto-deploys
- Takes ~2-5 minutes

**Manual redeploy:**
- Render Dashboard → Your Service → "Manual Deploy" → "Deploy latest commit"

---

## Custom Domain (Optional)

Want a custom domain like `mine-safety.yourdomain.com`?

1. Buy domain (Namecheap, Google Domains, etc.)
2. In Render: Service → Settings → Custom Domain
3. Add your domain
4. Update DNS records as instructed
5. SSL certificate auto-generated

---

## Cost Estimate

For your school project:
- **Development:** $0 (local)
- **Deployment:** $0 (Render free tier)
- **Total:** $0 🎉

For production with more users:
- Starter plan: $7/month (better performance)
- PostgreSQL: $7/month (more storage)
- Total: ~$14/month

---

## Support

**Render Documentation:**
- [Render Docs](https://render.com/docs)
- [Deploy FastAPI](https://render.com/docs/deploy-fastapi)
- [Deploy React](https://render.com/docs/deploy-create-react-app)

**Common Commands:**
```bash
# View logs
render logs -s mine-safety-backend

# SSH into service
render ssh -s mine-safety-backend

# Restart service
render restart -s mine-safety-backend
```

---

## Success! 🎉

Your Mine Safety Detection System is now live at:
- **Frontend:** `https://mine-safety-frontend.onrender.com`
- **Backend API:** `https://mine-safety-backend.onrender.com`
- **API Docs:** `https://mine-safety-backend.onrender.com/docs`

Share these URLs with your teachers and classmates!

---

## Next Steps

1. Test all features thoroughly
2. Add sample data for demo
3. Prepare presentation
4. Document any issues
5. Consider adding:
   - Email notifications
   - Export reports to PDF
   - Mobile app version
   - Real-time alerts

Good luck with your school project! 🚀
