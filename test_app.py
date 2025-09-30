"""
Simple test script to verify the Chef Marketplace application works correctly.
"""

import os
import sys
from app import app, db, User, ChefProfile, Booking, Review

def test_database_creation():
    """Test database creation and basic operations"""
    print("Testing database creation...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
        
        # Clean up any existing test data first
        User.query.filter_by(email='test@example.com').delete()
        User.query.filter_by(email='chef@example.com').delete()
        db.session.commit()
        
        # Test user creation
        test_user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='client'
        )
        test_user.set_password('testpassword')
        
        db.session.add(test_user)
        db.session.commit()
        print("Test user created successfully")
        
        # Test chef profile creation
        test_chef = User(
            email='chef@example.com',
            first_name='Test',
            last_name='Chef',
            role='chef'
        )
        test_chef.set_password('chefpassword')
        
        db.session.add(test_chef)
        db.session.commit()
        
        chef_profile = ChefProfile(
            user_id=test_chef.id,
            bio='Test chef with amazing culinary skills',
            specialties='Italian, French, Mediterranean',
            experience_years=5,
            base_price_per_person=75.00,
            min_guests=2,
            max_guests=12,
            service_areas='New York, Brooklyn, Queens'
        )
        
        db.session.add(chef_profile)
        db.session.commit()
        print("Test chef profile created successfully")
        
        # Test booking creation
        from datetime import date, time
        test_booking = Booking(
            client_id=test_user.id,
            chef_id=test_chef.id,
            menu_id=1,
            event_date=date(2024, 12, 25),
            event_time=time(19, 0, 0),
            guest_count=4,
            location_address='123 Test Street, New York, NY',
            occasion_type='dinner_party',
            total_price=300.00,
            service_fee=30.00,
            platform_fee=45.00
        )
        
        db.session.add(test_booking)
        db.session.commit()
        print("Test booking created successfully")
        
        # Test data retrieval
        users = User.query.all()
        chefs = ChefProfile.query.all()
        bookings = Booking.query.all()
        
        print(f"Found {len(users)} users, {len(chefs)} chef profiles, {len(bookings)} bookings")
        
        # Clean up test data
        db.session.delete(test_booking)
        db.session.delete(chef_profile)
        db.session.delete(test_chef)
        db.session.delete(test_user)
        db.session.commit()
        print("Test data cleaned up successfully")

def test_routes():
    """Test basic route functionality"""
    print("\nTesting routes...")
    
    with app.test_client() as client:
        # Test home page
        response = client.get('/')
        assert response.status_code == 200
        print("Home page loads successfully")
        
        # Test login page
        response = client.get('/login')
        assert response.status_code == 200
        print("Login page loads successfully")
        
        # Test register page
        response = client.get('/register')
        assert response.status_code == 200
        print("Register page loads successfully")
        
        # Test browse chefs page
        response = client.get('/chefs')
        assert response.status_code == 200
        print("Browse chefs page loads successfully")

def test_forms():
    """Test form functionality"""
    print("\nTesting forms...")
    
    with app.test_request_context():
        from app import LoginForm, RegistrationForm, ChefProfileForm, BookingForm
        
        # Test login form
        login_form = LoginForm()
        assert login_form.email is not None
        assert login_form.password is not None
        print("Login form created successfully")
        
        # Test registration form
        reg_form = RegistrationForm()
        assert reg_form.first_name is not None
        assert reg_form.email is not None
        assert reg_form.role is not None
        print("Registration form created successfully")
        
        # Test chef profile form
        chef_form = ChefProfileForm()
        assert chef_form.bio is not None
        assert chef_form.specialties is not None
        assert chef_form.base_price_per_person is not None
        print("Chef profile form created successfully")
        
        # Test booking form
        booking_form = BookingForm()
        assert booking_form.event_date is not None
        assert booking_form.guest_count is not None
        assert booking_form.location_address is not None
        print("Booking form created successfully")

def main():
    """Run all tests"""
    print("Starting Chef Marketplace Application Tests\n")
    
    try:
        test_database_creation()
        test_routes()
        test_forms()
        
        print("\nAll tests passed successfully!")
        print("\nThe Chef Marketplace application is ready to use!")
        print("\nTo start the application, run: python app.py")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
