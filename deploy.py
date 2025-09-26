#!/usr/bin/env python3
"""
Deployment script for گل سرخ Rose Kitchen
This script helps prepare the app for deployment
"""

import os
import sys
from app import app, db

def prepare_for_deployment():
    """Prepare the application for deployment"""
    print("🚀 Preparing گل سرخ Rose Kitchen for deployment...")
    print("=" * 60)
    
    # Check if we're in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if is_production:
        print("✅ Production environment detected")
        print("📊 Using PostgreSQL database")
    else:
        print("🔧 Development environment detected")
        print("📊 Using SQLite database")
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
            return False
    
    # Check required environment variables
    required_vars = ['SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        if is_production:
            print("❌ Cannot deploy without required environment variables")
            return False
        else:
            print("🔧 Using default values for development")
    
    # Check if demo data exists
    from app import User
    with app.app_context():
        user_count = User.query.count()
        if user_count == 0:
            print("📝 No users found. Demo data may need to be loaded.")
            print("💡 Run 'python demo_data.py' to populate with sample data")
        else:
            print(f"✅ Found {user_count} users in database")
    
    print("=" * 60)
    print("🎉 Application is ready for deployment!")
    print("🌐 Your گل سرخ Rose Kitchen app is ready to serve Persian cuisine!")
    
    return True

def main():
    """Main deployment function"""
    if prepare_for_deployment():
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Deploy to your chosen platform (Render, PythonAnywhere, etc.)")
        print("3. Set environment variables on your hosting platform")
        print("4. Access your live app!")
        print("\n🍳 Enjoy your Persian kitchen app! 🌹")
    else:
        print("\n❌ Deployment preparation failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
