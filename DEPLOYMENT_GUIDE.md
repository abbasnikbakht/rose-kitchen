# 🚀 Deployment Guide for گل سرخ Rose Kitchen

## Quick Deployment Options

### Option 1: Render (Recommended) ⭐

1. **Prepare Your Code:**
   ```bash
   # Create a GitHub repository
   git init
   git add .
   git commit -m "Initial commit - Rose Kitchen Persian App"
   git remote add origin https://github.com/yourusername/rose-kitchen.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to https://render.com
   - Sign up with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Environment:** Python 3
   - Add environment variables:
     - `SECRET_KEY`: Your secret key
     - `DATABASE_URL`: Will be provided by Render

3. **Database Setup:**
   - In Render dashboard, create a PostgreSQL database
   - Copy the database URL to your environment variables
   - Update your app to use PostgreSQL in production

### Option 2: PythonAnywhere (Easiest) ⭐

1. **Sign Up:**
   - Go to https://pythonanywhere.com
   - Create a free account

2. **Upload Your Code:**
   - Use the Files tab to upload your files
   - Or clone from GitHub using the Bash console

3. **Configure Web App:**
   - Go to Web tab
   - Create new web app
   - Choose Flask
   - Set your source code directory

4. **Install Dependencies:**
   ```bash
   pip3.10 install --user flask flask-sqlalchemy flask-login flask-wtf
   ```

5. **Database Setup:**
   - Use SQLite (included) or upgrade for PostgreSQL

### Option 3: Railway

1. **Prepare Repository:**
   - Push your code to GitHub

2. **Deploy:**
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy

3. **Environment Variables:**
   - Add `SECRET_KEY` and `DATABASE_URL` in Railway dashboard

## Environment Variables Setup

Create these environment variables on your hosting platform:

```bash
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://username:password@host:port/database
FLASK_ENV=production
```

## Database Migration

For production deployment, you'll need to:

1. **Update app.py for production database:**
   ```python
   import os
   
   # Use PostgreSQL in production, SQLite in development
   if os.environ.get('DATABASE_URL'):
       app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
   else:
       app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kitchen_booking.db'
   ```

2. **Initialize database:**
   ```python
   # Add this to your deployment script
   with app.app_context():
       db.create_all()
   ```

## Custom Domain (Optional)

Most platforms allow custom domains:
- **Render:** Free custom domain support
- **PythonAnywhere:** Custom domain with paid plan
- **Railway:** Custom domain support

## Monitoring & Analytics

1. **Add logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

2. **Error tracking:** Consider Sentry (free tier available)

## Security Checklist

- [ ] Set strong SECRET_KEY
- [ ] Use HTTPS (automatic on most platforms)
- [ ] Set up proper CORS if needed
- [ ] Use environment variables for sensitive data
- [ ] Enable database backups

## Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| Render | 750 hours/month | $7+/month | Production apps |
| PythonAnywhere | 100s CPU/day | $5+/month | Learning/development |
| Railway | $5 credit/month | $5+/month | Modern deployment |
| Heroku | No free tier | $7+/month | Enterprise features |

## Recommended: Render

For your **گل سرخ Rose Kitchen** app, I recommend **Render** because:
- ✅ 750 hours free (enough for continuous running)
- ✅ Automatic deployments from GitHub
- ✅ Free PostgreSQL database
- ✅ Custom domain support
- ✅ Easy environment variable management
- ✅ Great for Flask applications

## Next Steps

1. **Choose a platform** (Render recommended)
2. **Push your code to GitHub**
3. **Follow the deployment steps above**
4. **Set up your database**
5. **Configure environment variables**
6. **Test your deployed app**

Your Persian kitchen app will be live and accessible to users worldwide! 🌹🍳

---

**Need help with deployment?** Each platform has excellent documentation and community support.
