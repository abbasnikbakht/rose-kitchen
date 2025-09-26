#!/usr/bin/env python3
"""
Production startup script for گل سرخ Rose Kitchen
This script ensures the database is properly initialized before starting the app
"""

import os
from app import app, db

def main():
    """Main startup function"""
    print("🌹 Starting گل سرخ Rose Kitchen...")
    
    # Ensure database tables exist
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables verified/created")
        except Exception as e:
            print(f"❌ Database error: {e}")
            return
    
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🚀 Starting server on {host}:{port}")
    print(f"🐛 Debug mode: {'ON' if debug else 'OFF'}")
    
    # Start the application
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
