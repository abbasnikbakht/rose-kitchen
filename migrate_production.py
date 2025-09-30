"""
Production database migration script for Render deployment
This script adds the new fields for cooking and teaching services
"""

import os
from app import app, db
from sqlalchemy import text

def migrate_production_database():
    """Add new columns to production database tables"""
    print("Starting production database migration...")
    
    with app.app_context():
        try:
            # Check if new columns exist and add them if they don't
            inspector = db.inspect(db.engine)
            
            # Get current columns
            try:
                chef_columns = [col['name'] for col in inspector.get_columns('chef_profile')]
                booking_columns = [col['name'] for col in inspector.get_columns('booking')]
            except Exception as e:
                print(f"Error getting table info: {e}")
                # If tables don't exist, create them
                db.create_all()
                print("Created all tables")
                return True
            
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
                ('service_type', 'VARCHAR(20) DEFAULT \'cooking_only\''),
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
            
            print("Production database migration completed successfully!")
            return True
            
        except Exception as e:
            print(f"Migration failed: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    if migrate_production_database():
        print("Production migration successful!")
    else:
        print("Production migration failed.")
