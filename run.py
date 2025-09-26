#!/usr/bin/env python3
"""
KitchenBook Application Startup Script
Run this file to start the KitchenBook application
"""

import os
import sys
from app import app, db

def create_tables():
    """Create database tables if they don't exist"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def main():
    """Main function to start the application"""
    print("🍳 Starting KitchenBook Application...")
    print("=" * 50)
    
    # Create database tables
    create_tables()
    
    # Get configuration
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    print(f"🌐 Server will run on: http://{host}:{port}")
    print(f"🐛 Debug mode: {'ON' if debug_mode else 'OFF'}")
    print("=" * 50)
    print("🚀 Starting Flask development server...")
    print("📱 Open your browser and navigate to the URL above")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug_mode)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
