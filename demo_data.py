#!/usr/bin/env python3
"""
Demo Data Script for KitchenBook
This script populates the database with sample data for testing
"""

from app import app, db, User, CookProfile, Booking, Review, Menu, MenuImage, PortfolioImage, ChefAvailability, Message, Payment, Notification
from werkzeug.security import generate_password_hash
from datetime import datetime, date, time, timedelta
import random
import json

def create_demo_data():
    """Create demo data for testing the application"""
    
    # Import app here to avoid circular imports
    from app import app, db, User, CookProfile, Booking, Review, Menu, MenuImage, PortfolioImage, ChefAvailability, Message, Payment, Notification
    from werkzeug.security import generate_password_hash
    from datetime import datetime, date, time, timedelta
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create demo users
        print("Creating demo users...")
        
        # Demo customers
        customers = [
            User(
                username='ahmad_reza',
                email='ahmad@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Ahmad',
                last_name='Reza',
                phone='555-0101',
                address='123 Persian Garden',
                city='Tehran',
                state='Tehran',
                zip_code='12345',
                country='Iran',
                is_cook=False
            ),
            User(
                username='soheila_khani',
                email='soheila@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Soheila',
                last_name='Khani',
                phone='555-0102',
                address='456 Rose Street',
                city='Isfahan',
                state='Isfahan',
                zip_code='23456',
                country='Iran',
                is_cook=False
            ),
            User(
                username='hassan_mirza',
                email='hassan@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Hassan',
                last_name='Mirza',
                phone='555-0103',
                address='789 Halal Avenue',
                city='Shiraz',
                state='Fars',
                zip_code='34567',
                country='Iran',
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
                address='321 Persian Garden',
                city='Tehran',
                state='Tehran',
                zip_code='12345',
                country='Iran',
                is_cook=True
            ),
            User(
                username='chef_soheila',
                email='soheila_chef@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Soheila',
                last_name='Nouri',
                phone='555-0202',
                address='654 Isfahan Street',
                city='Isfahan',
                state='Isfahan',
                zip_code='23456',
                country='Iran',
                is_cook=True
            ),
            User(
                username='chef_hala',
                email='hala@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Halal',
                last_name='Kazemi',
                phone='555-0203',
                address='987 Shiraz Boulevard',
                city='Shiraz',
                state='Fars',
                zip_code='34567',
                country='Iran',
                is_cook=True
            ),
            User(
                username='chef_iran',
                email='iran@example.com',
                password_hash=generate_password_hash('password123'),
                first_name='Iran',
                last_name='Mohammadi',
                phone='555-0204',
                address='147 Tehran Avenue',
                city='Tehran',
                state='Tehran',
                zip_code='12345',
                country='Iran',
                is_cook=True
            )
        ]
        
        all_users = customers + cooks
        for user in all_users:
            db.session.add(user)
        
        db.session.commit()
        print(f"Created {len(all_users)} users")
        
        # Create cook profiles
        print("Creating cook profiles...")
        
        cook_profiles = [
            CookProfile(
                user_id=cooks[0].id,
                bio="Master of traditional Persian cuisine with 8 years of experience. Specializing in authentic Tehran dishes, I bring the rich flavors of Iran to your home with recipes passed down through generations.",
                specialties="Persian Cuisine\nGhormeh Sabzi\nFesenjan\nTahdig\nKebab\nZereshk Polo",
                experience_years=8,
                hourly_rate=75.00,
                price_per_person=45.00,
                service_radius=20,
                min_guests=2,
                max_guests=20,
                travel_fee_per_mile=2.0,
                setup_fee=25.00,
                cleanup_fee=15.00,
                dietary_expertise="Halal\nVegetarian\nGluten-Free\nDairy-Free",
                certifications="Food Safety Certified\nCulinary Arts Diploma\nServSafe Certified",
                insurance_verified=True,
                background_check_verified=True,
                food_safety_certified=True,
                is_available=True,
                is_featured=True
            ),
            CookProfile(
                user_id=cooks[1].id,
                bio="Expert in Isfahan's traditional cuisine with over 12 years of experience. Trained in the art of Persian cooking, I specialize in authentic Isfahan dishes and traditional family recipes.",
                specialties="Isfahan Cuisine\nBeryani\nKhoresh Bademjan\nAsh Reshteh\nHalva\nGaz",
                experience_years=12,
                hourly_rate=85.00,
                price_per_person=50.00,
                service_radius=25,
                min_guests=1,
                max_guests=25,
                travel_fee_per_mile=2.5,
                setup_fee=30.00,
                cleanup_fee=20.00,
                dietary_expertise="Halal\nVegetarian\nVegan\nGluten-Free",
                certifications="Advanced Culinary Arts\nFood Safety Certified\nTraditional Persian Cooking",
                insurance_verified=True,
                background_check_verified=True,
                food_safety_certified=True,
                is_available=True,
                is_featured=True
            ),
            CookProfile(
                user_id=cooks[2].id,
                bio="Creative Shiraz chef with expertise in traditional Persian cooking and modern techniques. I love creating memorable dining experiences with authentic Iranian ingredients and beautiful presentations.",
                specialties="Shiraz Cuisine\nKalam Polo\nKhoresh Gheimeh\nTahchin\nFaloodeh\nRose Water Desserts",
                experience_years=6,
                hourly_rate=70.00,
                price_per_person=40.00,
                service_radius=15,
                min_guests=2,
                max_guests=15,
                travel_fee_per_mile=1.5,
                setup_fee=20.00,
                cleanup_fee=10.00,
                dietary_expertise="Halal\nVegetarian\nGluten-Free\nKeto",
                certifications="Culinary Arts Certificate\nFood Safety Certified",
                insurance_verified=True,
                background_check_verified=True,
                food_safety_certified=True,
                is_available=True
            ),
            CookProfile(
                user_id=cooks[3].id,
                bio="Expert in traditional Iranian cuisine with 10 years of experience. I combine authentic Persian cooking techniques with modern presentation to create unforgettable culinary experiences.",
                specialties="Traditional Iranian\nChelo Kebab\nKhoresh Karafs\nBaghali Polo\nSholeh Zard\nPersian Tea",
                experience_years=10,
                hourly_rate=80.00,
                price_per_person=48.00,
                service_radius=30,
                min_guests=1,
                max_guests=30,
                travel_fee_per_mile=2.0,
                setup_fee=25.00,
                cleanup_fee=15.00,
                dietary_expertise="Halal\nVegetarian\nGluten-Free\nDairy-Free\nKeto",
                certifications="Professional Chef Diploma\nFood Safety Certified\nTraditional Iranian Cooking",
                insurance_verified=True,
                background_check_verified=True,
                food_safety_certified=True,
                is_available=True
            )
        ]
        
        for profile in cook_profiles:
            db.session.add(profile)
        
        db.session.commit()
        print(f"Created {len(cook_profiles)} cook profiles")
        
        # Create demo bookings
        print("Creating demo bookings...")
        
        bookings = [
            Booking(
                customer_id=customers[0].id,
                cook_id=cook_profiles[0].id,
                event_type='birthday',
                event_date=date.today() + timedelta(days=7),
                start_time=time(18, 0),
                end_time=time(22, 0),
                guest_count=12,
                location_address='123 Persian Garden',
                location_city='Tehran',
                location_state='Tehran',
                location_zip='12345',
                special_requests='Traditional Persian birthday celebration. Please include Ghormeh Sabzi and Zereshk Polo. Vegetarian options for 3 guests.',
                dietary_restrictions='Vegetarian options for 3 guests',
                kitchen_equipment='Standard kitchen with oven, stove, refrigerator',
                shopping_preference='chef_shops',
                base_cost=540.00,  # 12 guests * $45
                travel_fee=0.0,
                setup_fee=25.00,
                cleanup_fee=15.00,
                platform_fee=81.00,  # 15% of base cost
                total_cost=661.00,
                status='confirmed',
                chef_confirmed_at=datetime.utcnow() - timedelta(days=2)
            ),
            Booking(
                customer_id=customers[1].id,
                cook_id=cook_profiles[1].id,
                event_type='anniversary',
                event_date=date.today() + timedelta(days=14),
                start_time=time(19, 0),
                end_time=time(23, 0),
                guest_count=8,
                location_address='456 Rose Street',
                location_city='Isfahan',
                location_state='Isfahan',
                location_zip='23456',
                special_requests='Romantic Persian dinner for anniversary. Please include Fesenjan and traditional Persian tea ceremony.',
                dietary_restrictions='None',
                kitchen_equipment='Full kitchen with all amenities',
                shopping_preference='chef_shops',
                base_cost=400.00,  # 8 guests * $50
                travel_fee=0.0,
                setup_fee=30.00,
                cleanup_fee=20.00,
                platform_fee=60.00,  # 15% of base cost
                total_cost=510.00,
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
                location_address='789 Halal Avenue',
                location_city='Shiraz',
                location_state='Fars',
                location_zip='34567',
                special_requests='Business dinner featuring authentic Shiraz cuisine. Professional presentation with traditional Persian hospitality.',
                dietary_restrictions='Halal requirements',
                kitchen_equipment='Commercial kitchen available',
                shopping_preference='chef_shops',
                base_cost=800.00,  # 20 guests * $40
                travel_fee=0.0,
                setup_fee=20.00,
                cleanup_fee=10.00,
                platform_fee=120.00,  # 15% of base cost
                total_cost=950.00,
                status='completed',
                chef_confirmed_at=datetime.utcnow() - timedelta(days=5),
                completed_at=datetime.utcnow() - timedelta(days=1)
            ),
            Booking(
                customer_id=customers[0].id,
                cook_id=cook_profiles[3].id,
                event_type='family_gathering',
                event_date=date.today() + timedelta(days=10),
                start_time=time(16, 0),
                end_time=time(20, 0),
                guest_count=15,
                location_address='123 Persian Garden',
                location_city='Tehran',
                location_state='Tehran',
                location_zip='12345',
                special_requests='Family reunion with traditional Iranian dishes. Please include Chelo Kebab and kids-friendly Persian desserts.',
                dietary_restrictions='Kids-friendly options',
                kitchen_equipment='Standard home kitchen',
                shopping_preference='both',
                base_cost=720.00,  # 15 guests * $48
                travel_fee=0.0,
                setup_fee=25.00,
                cleanup_fee=15.00,
                platform_fee=108.00,  # 15% of base cost
                total_cost=868.00,
                status='confirmed',
                chef_confirmed_at=datetime.utcnow() - timedelta(days=1)
            )
        ]
        
        for booking in bookings:
            db.session.add(booking)
        
        db.session.commit()
        print(f"Created {len(bookings)} bookings")
        
        # Create demo reviews
        print("Creating demo reviews...")
        
        reviews = [
            Review(
                booking_id=bookings[2].id,  # Completed booking
                reviewer_id=customers[2].id,
                cook_id=cook_profiles[2].id,
                rating=5,
                food_quality=5,
                professionalism=5,
                cleanliness=5,
                communication=5,
                value_for_money=5,
                comment="Halal was absolutely fantastic! Her authentic Shiraz cuisine and traditional Persian hospitality made our corporate event unforgettable. The Kalam Polo and Faloodeh were exceptional."
            ),
            Review(
                booking_id=bookings[2].id,
                reviewer_id=customers[2].id,
                cook_id=cook_profiles[2].id,
                rating=4,
                food_quality=4,
                professionalism=5,
                cleanliness=4,
                communication=4,
                value_for_money=4,
                comment="Amazing Persian cuisine and professional service. The traditional tea ceremony was a beautiful touch. Would definitely book again for future events."
            )
        ]
        
        for review in reviews:
            db.session.add(review)
        
        db.session.commit()
        print(f"Created {len(reviews)} reviews")
        
        # Create demo menus
        print("Creating demo menus...")
        
        menus = [
            Menu(
                chef_id=cook_profiles[0].id,
                name="Traditional Persian Feast",
                description="A complete Persian dining experience featuring classic dishes from Tehran. Perfect for special occasions and family gatherings.",
                cuisine_type="Persian",
                price_per_person=45.00,
                min_guests=2,
                max_guests=20,
                preparation_time_hours=3,
                is_customizable=True,
                dietary_accommodations="Halal, Vegetarian, Gluten-Free options available",
                ingredients="Saffron, Basmati rice, Lamb, Fresh herbs, Persian spices",
                courses="Appetizer: Mast-o-Khiar\nMain: Ghormeh Sabzi with Tahdig\nDessert: Sholeh Zard\nBeverage: Persian Tea"
            ),
            Menu(
                chef_id=cook_profiles[1].id,
                name="Isfahan Royal Dinner",
                description="Authentic Isfahan cuisine featuring the city's most famous dishes. A royal experience for your special events.",
                cuisine_type="Persian",
                price_per_person=50.00,
                min_guests=1,
                max_guests=25,
                preparation_time_hours=4,
                is_customizable=True,
                dietary_accommodations="Halal, Vegetarian, Vegan options available",
                ingredients="Beryani rice, Eggplant, Fresh herbs, Isfahan spices",
                courses="Appetizer: Ash Reshteh\nMain: Beryani with Khoresh Bademjan\nDessert: Gaz and Halva\nBeverage: Traditional Persian Tea"
            ),
            Menu(
                chef_id=cook_profiles[2].id,
                name="Shiraz Garden Party",
                description="Light and refreshing Shiraz cuisine perfect for garden parties and outdoor events. Features rose water and citrus flavors.",
                cuisine_type="Persian",
                price_per_person=40.00,
                min_guests=2,
                max_guests=15,
                preparation_time_hours=2,
                is_customizable=True,
                dietary_accommodations="Halal, Vegetarian, Gluten-Free, Keto options",
                ingredients="Rose water, Citrus fruits, Fresh herbs, Shiraz spices",
                courses="Appetizer: Kalam Polo\nMain: Khoresh Gheimeh with Tahchin\nDessert: Faloodeh\nBeverage: Rose Water Drink"
            ),
            Menu(
                chef_id=cook_profiles[3].id,
                name="Classic Iranian Celebration",
                description="Traditional Iranian dishes perfect for celebrations and family gatherings. Features the most beloved Persian recipes.",
                cuisine_type="Persian",
                price_per_person=48.00,
                min_guests=1,
                max_guests=30,
                preparation_time_hours=3,
                is_customizable=True,
                dietary_accommodations="Halal, Vegetarian, Gluten-Free, Dairy-Free, Keto options",
                ingredients="Premium basmati rice, Fresh lamb, Persian herbs, Traditional spices",
                courses="Appetizer: Persian Salad\nMain: Chelo Kebab with Baghali Polo\nDessert: Sholeh Zard\nBeverage: Persian Tea Ceremony"
            )
        ]
        
        for menu in menus:
            db.session.add(menu)
        
        db.session.commit()
        print(f"Created {len(menus)} menus")
        
        # Create demo portfolio images
        print("Creating demo portfolio images...")
        
        portfolio_images = [
            PortfolioImage(
                chef_id=cook_profiles[0].id,
                image_url="/static/images/portfolio/ghormeh_sabzi.jpg",
                caption="Traditional Ghormeh Sabzi with Tahdig",
                dish_name="Ghormeh Sabzi"
            ),
            PortfolioImage(
                chef_id=cook_profiles[0].id,
                image_url="/static/images/portfolio/zereshk_polo.jpg",
                caption="Zereshk Polo with Saffron Rice",
                dish_name="Zereshk Polo"
            ),
            PortfolioImage(
                chef_id=cook_profiles[1].id,
                image_url="/static/images/portfolio/beryani.jpg",
                caption="Authentic Isfahan Beryani",
                dish_name="Beryani"
            ),
            PortfolioImage(
                chef_id=cook_profiles[2].id,
                image_url="/static/images/portfolio/faloodeh.jpg",
                caption="Traditional Shiraz Faloodeh",
                dish_name="Faloodeh"
            ),
            PortfolioImage(
                chef_id=cook_profiles[3].id,
                image_url="/static/images/portfolio/chelo_kebab.jpg",
                caption="Classic Chelo Kebab",
                dish_name="Chelo Kebab"
            )
        ]
        
        for image in portfolio_images:
            db.session.add(image)
        
        db.session.commit()
        print(f"Created {len(portfolio_images)} portfolio images")
        
        # Create demo messages
        print("Creating demo messages...")
        
        messages = [
            Message(
                sender_id=customers[0].id,
                recipient_id=cooks[0].id,
                booking_id=bookings[0].id,
                subject="Birthday Party Details",
                content="Hi Rose! I'm excited about the birthday party next week. Could you please confirm the menu and let me know if you need any special equipment?",
                is_read=True
            ),
            Message(
                sender_id=cooks[0].id,
                recipient_id=customers[0].id,
                booking_id=bookings[0].id,
                subject="Re: Birthday Party Details",
                content="Hello Ahmad! I'm looking forward to cooking for your birthday celebration. The menu is confirmed and I'll bring all necessary equipment. See you next week!",
                is_read=True
            ),
            Message(
                sender_id=customers[1].id,
                recipient_id=cooks[1].id,
                booking_id=bookings[1].id,
                subject="Anniversary Dinner",
                content="Hi Soheila! We're celebrating our 10th anniversary and would love a romantic Persian dinner. Could you suggest a special menu?",
                is_read=False
            )
        ]
        
        for message in messages:
            db.session.add(message)
        
        db.session.commit()
        print(f"Created {len(messages)} messages")
        
        print("\nDemo data created successfully!")
        print("=" * 50)
        print("Demo Accounts Created:")
        print("=" * 50)
        print("CUSTOMERS:")
        print("   • ahmad@example.com / password123")
        print("   • soheila@example.com / password123")
        print("   • hassan@example.com / password123")
        print("\nPERSIAN CHEFS:")
        print("   • rose@example.com / password123 (Tehran Cuisine)")
        print("   • soheila_chef@example.com / password123 (Isfahan Cuisine)")
        print("   • hala@example.com / password123 (Shiraz Cuisine - Halal)")
        print("   • iran@example.com / password123 (Traditional Iranian)")
        print("=" * 50)
        print("You can now run the application with: python run.py")

if __name__ == '__main__':
    create_demo_data()
