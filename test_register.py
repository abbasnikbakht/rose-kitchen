"""
Test registration functionality
"""

from app import app, db, User, RegistrationForm

def test_registration():
    with app.app_context():
        with app.test_request_context():
            try:
                # Test form creation
                form = RegistrationForm()
                print("Form created successfully")
                
                # Test user creation
                user = User(
                    email='test@example.com',
                    first_name='Test',
                    last_name='User',
                    phone='1234567890',
                    role='client'
                )
                user.set_password('password123')
                print("User object created successfully")
                
                # Test database operations
                db.session.add(user)
                db.session.commit()
                print("User saved to database successfully")
                
                # Clean up
                db.session.delete(user)
                db.session.commit()
                print("User deleted successfully")
                
                print("All tests passed!")
                return True
                
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
                return False

if __name__ == '__main__':
    test_registration()
