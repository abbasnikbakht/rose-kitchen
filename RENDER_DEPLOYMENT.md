# 🚀 Render Deployment Guide for گل سرخ Rose Kitchen

## Step-by-Step Deployment to Render

### Prerequisites
- GitHub account
- Your code ready in a GitHub repository

### Step 1: Prepare Your GitHub Repository

1. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Rose Kitchen Persian App"
   ```

2. **Create GitHub Repository:**
   - Go to https://github.com
   - Click "New repository"
   - Name it: `rose-kitchen` or `persian-kitchen-app`
   - Make it public (required for free Render deployment)
   - Don't initialize with README (you already have files)

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/rose-kitchen.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Sign up for Render:**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with your GitHub account

2. **Create New Web Service:**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository
   - Choose your `rose-kitchen` repository

3. **Configure Your Service:**
   - **Name:** `rose-kitchen` or `persian-kitchen`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

4. **Add Environment Variables:**
   Click "Add Environment Variable" and add:
   - **Key:** `SECRET_KEY`
   - **Value:** `your-super-secret-key-change-this-in-production-12345`
   
   - **Key:** `FLASK_ENV`
   - **Value:** `production`

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - This process takes 5-10 minutes

### Step 3: Set Up Database

1. **Create PostgreSQL Database:**
   - In Render dashboard, click "New +"
   - Select "PostgreSQL"
   - **Name:** `rose-kitchen-db`
   - **Plan:** Free
   - Click "Create Database"

2. **Get Database URL:**
   - Go to your database dashboard
   - Copy the "External Database URL"
   - It looks like: `postgresql://username:password@host:port/database`

3. **Add Database URL to Web Service:**
   - Go back to your web service
   - Click "Environment"
   - Add new environment variable:
     - **Key:** `DATABASE_URL`
     - **Value:** (paste the database URL you copied)

4. **Redeploy:**
   - Click "Manual Deploy" → "Deploy latest commit"
   - This will restart your app with the database connection

### Step 4: Initialize Database

1. **Access Your App:**
   - Your app will be available at: `https://your-app-name.onrender.com`
   - The first time you visit, the database tables will be created automatically

2. **Add Demo Data (Optional):**
   - You can create a simple endpoint to populate demo data
   - Or manually register users through your app

### Step 5: Custom Domain (Optional)

1. **Add Custom Domain:**
   - In your web service dashboard
   - Go to "Settings" → "Custom Domains"
   - Add your domain (e.g., `rose-kitchen.com`)
   - Follow Render's DNS instructions

## Your App URLs

- **Web Service:** `https://your-app-name.onrender.com`
- **Database:** Managed by Render (internal connection)

## Environment Variables Summary

Make sure these are set in your Render web service:

```
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
FLASK_ENV=production
DATABASE_URL=postgresql://username:password@host:port/database
```

## Troubleshooting

### Common Issues:

1. **Build Fails:**
   - Check that all dependencies are in `requirements.txt`
   - Ensure `gunicorn` is included

2. **App Crashes:**
   - Check logs in Render dashboard
   - Verify environment variables are set correctly

3. **Database Connection Issues:**
   - Ensure `DATABASE_URL` is set correctly
   - Check that PostgreSQL service is running

4. **Static Files Not Loading:**
   - This is normal for Flask apps on Render
   - Static files are served by Flask, not a separate CDN

### Checking Logs:
- Go to your web service dashboard
- Click "Logs" tab to see real-time logs
- Check for any error messages

## Success! 🎉

Once deployed, your **گل سرخ Rose Kitchen** app will be:
- ✅ Live on the internet
- ✅ Accessible worldwide
- ✅ Using a production PostgreSQL database
- ✅ Automatically deploying from GitHub
- ✅ Ready for users to book Persian chefs!

## Next Steps After Deployment

1. **Test your app** thoroughly
2. **Share the URL** with friends and family
3. **Monitor usage** in Render dashboard
4. **Consider upgrading** to paid plan for more resources
5. **Add custom domain** for professional appearance

Your Persian kitchen booking service is now live! 🌹🍳
