"""
Database migration script to add new fields for cooking and teaching services
"""

import os
from app import app, db
from sqlalchemy import text

def migrate_database():
    """Add new columns to existing tables"""
    print("Starting database migration for new fields...")
    
    with app.app_context():
        try:
            # Check if new columns exist and add them if they don't
            inspector = db.inspect(db.engine)
            chef_columns = [col['name'] for col in inspector.get_columns('chef_profile')]
            booking_columns = [col['name'] for col in inspector.get_columns('booking')]
            
            print(f"Current chef_profile columns: {chef_columns}")
            print(f"Current booking columns: {booking_columns}")
            
            # Add new columns to chef_profile table
            new_chef_columns = [
                ('cuisine_types', 'TEXT'),
                ('teaching_price_per_person', 'NUMERIC(10, 2)'),
                ('offers_teaching', 'BOOLEAN DEFAULT TRUE'),
                ('teaching_experience', 'TEXT')
            ]
            
            for column_name, column_type in new_chef_columns:
                if column_name not in chef_columns:
                    try:
                        with db.engine.connect() as conn:
                            conn.execute(text(f"ALTER TABLE chef_profile ADD COLUMN {column_name} {column_type}"))
                            conn.commit()
                        print(f"Added column {column_name} to chef_profile")
                    except Exception as e:
                        print(f"Error adding {column_name}: {e}")
                else:
                    print(f"Column {column_name} already exists in chef_profile")
            
            # Add new columns to booking table
            new_booking_columns = [
                ('service_type', 'VARCHAR(20) DEFAULT "cooking_only"'),
                ('cuisine_preference', 'VARCHAR(50)')
            ]
            
            for column_name, column_type in new_booking_columns:
                if column_name not in booking_columns:
                    try:
                        with db.engine.connect() as conn:
                            conn.execute(text(f"ALTER TABLE booking ADD COLUMN {column_name} {column_type}"))
                            conn.commit()
                        print(f"Added column {column_name} to booking")
                    except Exception as e:
                        print(f"Error adding {column_name}: {e}")
                else:
                    print(f"Column {column_name} already exists in booking")
            
            # Verify the migration
            inspector = db.inspect(db.engine)
            chef_columns_after = [col['name'] for col in inspector.get_columns('chef_profile')]
            booking_columns_after = [col['name'] for col in inspector.get_columns('booking')]
            
            print(f"After migration - chef_profile columns: {chef_columns_after}")
            print(f"After migration - booking columns: {booking_columns_after}")
            
            print("Database migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    if migrate_database():
        print("Migration successful! You can now run your Flask app.")
    else:
        print("Migration failed. Check the error messages above.")
