# 🔧 Troubleshooting Guide - Chef Marketplace Platform

## Common Issues and Solutions

### 500 Server Error

If you're getting a 500 server error, here are the most common causes and solutions:

#### 1. Database Issues
**Problem**: Database not initialized or corrupted
**Solution**:
```bash
# Delete existing database file
rm chef_marketplace.db

# Run the app to recreate database
python app.py
```

#### 2. Missing Dependencies
**Problem**: Required packages not installed
**Solution**:
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF
```

#### 3. Port Already in Use
**Problem**: Port 5000 is already being used
**Solution**:
```bash
# Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or use a different port
python -c "from app import app; app.run(port=5001)"
```

#### 4. File Permissions
**Problem**: Cannot create database or upload files
**Solution**:
```bash
# Make sure you have write permissions
# Run as administrator if needed
```

#### 5. Environment Variables
**Problem**: Missing or incorrect environment variables
**Solution**:
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env with your settings
# Make sure SECRET_KEY is set
```

### Quick Fix Commands

#### Reset Everything
```bash
# Stop any running servers (Ctrl+C)
# Delete database
rm chef_marketplace.db

# Reinstall dependencies
pip install -r requirements.txt

# Start fresh
python app.py
```

#### Test Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database OK')"
```

#### Test Routes
```bash
python -c "from app import app; client = app.test_client(); print('Home:', client.get('/').status_code)"
```

### Debug Mode

To get more detailed error information:

1. **Enable Debug Mode**:
   ```python
   app.run(debug=True)
   ```

2. **Check Console Output**: Look for error messages in the terminal

3. **Check Browser Console**: Press F12 in your browser to see JavaScript errors

### Common Error Messages

#### "Working outside of application context"
**Solution**: Make sure you're using `app.app_context()` when accessing database outside of request handlers.

#### "Table doesn't exist"
**Solution**: Run `db.create_all()` to create all tables.

#### "Permission denied"
**Solution**: Check file permissions, especially for uploads directory.

#### "Port already in use"
**Solution**: Use a different port or kill the existing process.

### Getting Help

If you're still having issues:

1. **Check the logs**: Look at the console output for error messages
2. **Run the test suite**: `python test_app.py`
3. **Check dependencies**: `pip list | grep Flask`
4. **Verify file structure**: Make sure all template files exist

### Production Deployment

For production deployment:

1. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   export DATABASE_URL=your-database-url
   ```

2. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

3. **Set up proper logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

### Still Having Issues?

If none of these solutions work:

1. Check the exact error message in your browser's developer tools
2. Look at the server console output
3. Try running the test suite: `python test_app.py`
4. Make sure you're using Python 3.8 or higher
5. Verify all files are in the correct locations

Remember: The 500 error page you're seeing is actually the custom error page from the application, which means the Flask app is running but encountering an internal error. Check the console output for the actual error details.
