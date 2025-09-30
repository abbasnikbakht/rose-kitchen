"""
Startup script for Render deployment
This ensures database tables are created on startup
"""

import os
from app import app, db

def main():
    """Main startup function"""
    print("Starting Chef Marketplace Platform on Render...")
    
    with app.app_context():
        try:
            # Create all database tables
            print("Creating database tables...")
            db.create_all()
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Database tables created: {tables}")
            
            print("Database initialization complete!")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            import traceback
            traceback.print_exc()
    
    # Start the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    main()
