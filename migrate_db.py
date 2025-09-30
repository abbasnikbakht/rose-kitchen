"""
Database migration script for production deployment
Run this script on Render to create all necessary tables
"""

import os
from app import app, db

def migrate_database():
    """Create all database tables"""
    print("Starting database migration...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("All tables created successfully!")
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Created tables: {tables}")
            
            # Test basic functionality
            from app import User, ChefProfile
            user_count = User.query.count()
            chef_count = ChefProfile.query.count()
            print(f"Users: {user_count}, Chefs: {chef_count}")
            
            print("Database migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    migrate_database()
