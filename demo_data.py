#!/usr/bin/env python3
"""
Demo Data Script for KitchenBook
This script populates the database with sample data for testing
"""

from app import app, db, User, CookProfile, Booking, Review
from werkzeug.security import generate_password_hash
from datetime import datetime, date, time, timedelta
import random

def create_demo_data():
    """Create demo data for testing the application"""
    
    # Import app here to avoid circular imports
    from app import app, db, User, CookProfile, Booking, Review
    from werkzeug.security import generate_password_hash
    from datetime import datetime, date, time, timedelta
    
    with app.app_context():
        # Clear existing data
        print("🧹 Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create demo users
        print("👥 Creating demo users...")
        
        # Demo customers
        customers = [
            User(
                username='ahmad_reza',
                email='ahmad@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Ahmad',
                last_name='Reza',
                phone='555-0101',
                address='123 Persian Garden, Tehran, Iran',
                is_cook=False
            ),
            User(
                username='soheila_khani',
                email='soheila@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Soheila',
                last_name='Khani',
                phone='555-0102',
                address='456 Rose Street, Isfahan, Iran',
                is_cook=False
            ),
            User(
                username='hassan_mirza',
                email='hassan@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Hassan',
                last_name='Mirza',
                phone='555-0103',
                address='789 Halal Avenue, Shiraz, Iran',
                is_cook=False
            )
        ]
        
        # Demo cooks
        cooks = [
            User(
                username='chef_rose',
                email='rose@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Rose',
                last_name='Ahmadi',
                phone='555-0201',
                address='321 Persian Garden, Tehran, Iran',
                is_cook=True
            ),
            User(
                username='chef_soheila',
                email='soheila_chef@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Soheila',
                last_name='Nouri',
                phone='555-0202',
                address='654 Isfahan Street, Isfahan, Iran',
                is_cook=True
            ),
            User(
                username='chef_hala',
                email='hala@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Halal',
                last_name='Kazemi',
                phone='555-0203',
                address='987 Shiraz Boulevard, Shiraz, Iran',
                is_cook=True
            ),
            User(
                username='chef_iran',
                email='iran@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Iran',
                last_name='Mohammadi',
                phone='555-0204',
                address='147 Tehran Avenue, Tehran, Iran',
                is_cook=True
            )
        ]
        
        all_users = customers + cooks
        for user in all_users:
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(all_users)} users")
        
        # Create cook profiles
        print("👨‍🍳 Creating cook profiles...")
        
        cook_profiles = [
            CookProfile(
                user_id=cooks[0].id,
                bio="Master of traditional Persian cuisine with 8 years of experience. Specializing in authentic Tehran dishes, I bring the rich flavors of Iran to your home with recipes passed down through generations.",
                specialties="Persian Cuisine\nGhormeh Sabzi\nFesenjan\nTahdig\nKebab\nZereshk Polo",
                experience_years=8,
                hourly_rate=75.00,
                service_radius=20,
                is_available=True
            ),
            CookProfile(
                user_id=cooks[1].id,
                bio="Expert in Isfahan's traditional cuisine with over 12 years of experience. Trained in the art of Persian cooking, I specialize in authentic Isfahan dishes and traditional family recipes.",
                specialties="Isfahan Cuisine\nBeryani\nKhoresh Bademjan\nAsh Reshteh\nHalva\nGaz",
                experience_years=12,
                hourly_rate=85.00,
                service_radius=25,
                is_available=True
            ),
            CookProfile(
                user_id=cooks[2].id,
                bio="Creative Shiraz chef with expertise in traditional Persian cooking and modern techniques. I love creating memorable dining experiences with authentic Iranian ingredients and beautiful presentations.",
                specialties="Shiraz Cuisine\nKalam Polo\nKhoresh Gheimeh\nTahchin\nFaloodeh\nRose Water Desserts",
                experience_years=6,
                hourly_rate=70.00,
                service_radius=15,
                is_available=True
            ),
            CookProfile(
                user_id=cooks[3].id,
                bio="Expert in traditional Iranian cuisine with 10 years of experience. I combine authentic Persian cooking techniques with modern presentation to create unforgettable culinary experiences.",
                specialties="Traditional Iranian\nChelo Kebab\nKhoresh Karafs\nBaghali Polo\nSholeh Zard\nPersian Tea",
                experience_years=10,
                hourly_rate=80.00,
                service_radius=30,
                is_available=True
            )
        ]
        
        for profile in cook_profiles:
            db.session.add(profile)
        
        db.session.commit()
        print(f"✅ Created {len(cook_profiles)} cook profiles")
        
        # Create demo bookings
        print("📅 Creating demo bookings...")
        
        bookings = [
            Booking(
                customer_id=customers[0].id,
                cook_id=cook_profiles[0].id,
                event_type='birthday',
                event_date=date.today() + timedelta(days=7),
                start_time=time(18, 0),
                end_time=time(22, 0),
                guest_count=12,
                special_requests='Traditional Persian birthday celebration. Please include Ghormeh Sabzi and Zereshk Polo. Vegetarian options for 3 guests.',
                total_cost=300.00,
                status='confirmed'
            ),
            Booking(
                customer_id=customers[1].id,
                cook_id=cook_profiles[1].id,
                event_type='anniversary',
                event_date=date.today() + timedelta(days=14),
                start_time=time(19, 0),
                end_time=time(23, 0),
                guest_count=8,
                special_requests='Romantic Persian dinner for anniversary. Please include Fesenjan and traditional Persian tea ceremony.',
                total_cost=340.00,
                status='pending'
            ),
            Booking(
                customer_id=customers[2].id,
                cook_id=cook_profiles[2].id,
                event_type='corporate_event',
                event_date=date.today() + timedelta(days=21),
                start_time=time(17, 0),
                end_time=time(21, 0),
                guest_count=20,
                special_requests='Business dinner featuring authentic Shiraz cuisine. Professional presentation with traditional Persian hospitality.',
                total_cost=280.00,
                status='completed'
            ),
            Booking(
                customer_id=customers[0].id,
                cook_id=cook_profiles[3].id,
                event_type='family_gathering',
                event_date=date.today() + timedelta(days=10),
                start_time=time(16, 0),
                end_time=time(20, 0),
                guest_count=15,
                special_requests='Family reunion with traditional Iranian dishes. Please include Chelo Kebab and kids-friendly Persian desserts.',
                total_cost=320.00,
                status='confirmed'
            )
        ]
        
        for booking in bookings:
            db.session.add(booking)
        
        db.session.commit()
        print(f"✅ Created {len(bookings)} bookings")
        
        # Create demo reviews
        print("⭐ Creating demo reviews...")
        
        reviews = [
            Review(
                booking_id=bookings[2].id,  # Completed booking
                reviewer_id=customers[2].id,
                cook_id=cook_profiles[2].id,
                rating=5,
                comment="Halal was absolutely fantastic! Her authentic Shiraz cuisine and traditional Persian hospitality made our corporate event unforgettable. The Kalam Polo and Faloodeh were exceptional."
            ),
            Review(
                booking_id=bookings[2].id,
                reviewer_id=customers[2].id,
                cook_id=cook_profiles[2].id,
                rating=4,
                comment="Amazing Persian cuisine and professional service. The traditional tea ceremony was a beautiful touch. Would definitely book again for future events."
            )
        ]
        
        for review in reviews:
            db.session.add(review)
        
        db.session.commit()
        print(f"✅ Created {len(reviews)} reviews")
        
        print("\n🎉 Demo data created successfully!")
        print("=" * 50)
        print("📋 Demo Accounts Created:")
        print("=" * 50)
        print("👥 CUSTOMERS:")
        print("   • ahmad@example.com / password123")
        print("   • soheila@example.com / password123")
        print("   • hassan@example.com / password123")
        print("\n👨‍🍳 PERSIAN CHEFS:")
        print("   • rose@example.com / password123 (Tehran Cuisine)")
        print("   • soheila_chef@example.com / password123 (Isfahan Cuisine)")
        print("   • hala@example.com / password123 (Shiraz Cuisine - Halal)")
        print("   • iran@example.com / password123 (Traditional Iranian)")
        print("=" * 50)
        print("🚀 You can now run the application with: python run.py")

if __name__ == '__main__':
    create_demo_data()
