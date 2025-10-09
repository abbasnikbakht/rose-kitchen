# 🔄 Update Guide - Chef Marketplace Platform

## Overview
This guide provides instructions for updating the Chef Marketplace Platform with new features, bug fixes, and improvements.

## Current Version Features
- ✅ User Authentication (Client, Chef, Admin roles)
- ✅ Chef Profile Management
- ✅ Booking System with dual service types (cooking only / cooking & teaching)
- ✅ Review and Rating System
- ✅ Payment Integration (Stripe)
- ✅ Multi-cuisine Support (Persian, Indian, Chinese, Italian, etc.)
- ✅ Responsive Design with Take a Chef theme
- ✅ Database Migration System
- ✅ Production Deployment on Render

## Update Categories

### 1. Feature Updates

#### Adding New Cuisine Types
To add new cuisine types to the platform:

1. **Update the ChefProfileForm in `app.py`:**
```python
cuisine_types = SelectField('Cuisine Types', choices=[
    ('persian', 'Persian'),
    ('indian', 'Indian'),
    ('chinese', 'Chinese'),
    ('italian', 'Italian'),
    ('french', 'French'),
    ('mexican', 'Mexican'),
    ('japanese', 'Japanese'),
    ('thai', 'Thai'),
    ('mediterranean', 'Mediterranean'),
    ('american', 'American'),
    ('korean', 'Korean'),  # Add new cuisine
    ('vietnamese', 'Vietnamese'),  # Add new cuisine
    ('other', 'Other')
], validators=[DataRequired()], multiple=True)
```

2. **Update the BookingForm cuisine choices:**
```python
cuisine_preference = SelectField('Cuisine Preference', choices=[
    ('', 'Any Cuisine'),
    ('persian', 'Persian'),
    ('indian', 'Indian'),
    # ... existing choices
    ('korean', 'Korean'),  # Add new cuisine
    ('vietnamese', 'Vietnamese'),  # Add new cuisine
    ('other', 'Other')
], validators=[Optional()])
```

3. **Run database migration:**
```bash
python migrate_db.py
```

#### Adding New Service Types
To add new service types beyond cooking and teaching:

1. **Update the BookingForm in `app.py`:**
```python
service_type = SelectField('Service Type', choices=[
    ('cooking_only', 'Chef Cooks for You'),
    ('cooking_and_teaching', 'Chef Cooks & Teaches You'),
    ('meal_prep', 'Meal Preparation'),  # Add new service
    ('catering', 'Event Catering'),  # Add new service
    ('consultation', 'Cooking Consultation')  # Add new service
], validators=[DataRequired()])
```

2. **Update the Booking model if needed:**
```python
# Add new fields to Booking model if required
service_duration = db.Column(db.Integer, default=3)  # hours
service_location = db.Column(db.String(50), default='client_home')  # client_home, chef_kitchen, venue
```

3. **Update pricing calculation:**
```python
def calculate_booking_total(chef_profile, guest_count, menu_price=None, service_type='cooking_only'):
    # Add service type specific pricing logic
    if service_type == 'meal_prep':
        base_price = chef_profile.meal_prep_price * guest_count
    elif service_type == 'catering':
        base_price = chef_profile.catering_price * guest_count
    else:
        # Existing logic
        pass
```

#### Adding New User Roles
To add new user roles (e.g., 'manager', 'supervisor'):

1. **Update the User model:**
```python
role = db.Column(db.String(20), nullable=False, default='client')  # client, chef, admin, manager, supervisor
```

2. **Update the RegistrationForm:**
```python
role = SelectField('I want to', choices=[
    ('client', 'Hire a Chef'), 
    ('chef', 'Work as a Chef'),
    ('manager', 'Manage Chefs'),  # Add new role
    ('supervisor', 'Supervise Operations')  # Add new role
], validators=[DataRequired()])
```

3. **Add role-specific dashboards:**
```python
@app.route('/manager/dashboard')
@login_required
def manager_dashboard():
    if current_user.role != 'manager':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    # Manager-specific logic
    return render_template('manager/dashboard.html')
```

### 2. Database Updates

#### Adding New Columns
To add new columns to existing tables:

1. **Create a migration script:**
```python
# migrate_new_columns.py
from app import app, db
from sqlalchemy import text

def add_new_columns():
    with app.app_context():
        with db.engine.connect() as conn:
            # Add new columns
            conn.execute(text("ALTER TABLE chef_profile ADD COLUMN new_field VARCHAR(100)"))
            conn.execute(text("ALTER TABLE booking ADD COLUMN new_field INTEGER"))
            conn.commit()
            print("New columns added successfully")

if __name__ == '__main__':
    add_new_columns()
```

2. **Run the migration:**
```bash
python migrate_new_columns.py
```

3. **Update the models in `app.py`:**
```python
class ChefProfile(db.Model):
    # ... existing fields
    new_field = db.Column(db.String(100))  # Add new field
```

#### Adding New Tables
To add new tables:

1. **Define the new model in `app.py`:**
```python
class NewTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

2. **Run database creation:**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 3. UI/UX Updates

#### Updating the Theme
To update the visual theme:

1. **Update CSS variables in `static/css/style.css`:**
```css
:root {
    --primary-color: #your-new-color;
    --secondary-color: #your-new-color;
    --accent-color: #your-new-color;
    /* ... other variables */
}
```

2. **Update templates in `templates/` directory:**
- Modify `base.html` for global changes
- Update specific page templates as needed
- Ensure responsive design is maintained

#### Adding New Pages
To add new pages:

1. **Create the route in `app.py`:**
```python
@app.route('/new-page')
def new_page():
    return render_template('new_page.html')
```

2. **Create the template:**
```html
<!-- templates/new_page.html -->
{% extends "base.html" %}

{% block content %}
<div class="container">
    <h1>New Page</h1>
    <!-- Page content -->
</div>
{% endblock %}
```

3. **Add navigation links in `base.html`:**
```html
<li class="nav-item">
    <a class="nav-link" href="{{ url_for('new_page') }}">New Page</a>
</li>
```

### 4. API Updates

#### Adding New Endpoints
To add new API endpoints:

1. **Create the route:**
```python
@app.route('/api/new-endpoint', methods=['GET', 'POST'])
@login_required
def new_api_endpoint():
    if request.method == 'POST':
        data = request.get_json()
        # Process data
        return jsonify({'status': 'success', 'data': data})
    else:
        # Handle GET request
        return jsonify({'status': 'success', 'message': 'Hello'})
```

2. **Add error handling:**
```python
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400
```

### 5. Security Updates

#### Adding New Security Features
To add new security features:

1. **Rate limiting:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/sensitive-endpoint')
@limiter.limit("10 per minute")
def sensitive_endpoint():
    # Protected endpoint
    pass
```

2. **Input validation:**
```python
from wtforms.validators import ValidationError

def validate_custom_field(form, field):
    if not field.data or len(field.data) < 5:
        raise ValidationError('Field must be at least 5 characters long')

class CustomForm(FlaskForm):
    custom_field = StringField('Custom Field', validators=[DataRequired(), validate_custom_field])
```

### 6. Performance Updates

#### Adding Caching
To add caching:

1. **Install Redis:**
```bash
pip install redis flask-caching
```

2. **Configure caching in `app.py`:**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/expensive-operation')
@cache.cached(timeout=300)  # Cache for 5 minutes
def expensive_operation():
    # Expensive operation
    pass
```

#### Database Optimization
To optimize database performance:

1. **Add indexes:**
```python
class User(db.Model):
    # ... existing fields
    __table_args__ = (
        db.Index('idx_user_email', 'email'),
        db.Index('idx_user_role', 'role'),
    )
```

2. **Optimize queries:**
```python
# Use eager loading for relationships
chefs = ChefProfile.query.options(db.joinedload(ChefProfile.user)).all()
```

### 7. Testing Updates

#### Adding New Tests
To add new tests:

1. **Create test file:**
```python
# test_new_features.py
import unittest
from app import app, db

class TestNewFeatures(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def test_new_feature(self):
        response = self.app.get('/new-endpoint')
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        with app.app_context():
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
```

2. **Run tests:**
```bash
python test_new_features.py
```

### 8. Deployment Updates

#### Updating Production
To update the production deployment:

1. **Test locally:**
```bash
python app.py
# Test all new features
```

2. **Commit changes:**
```bash
git add .
git commit -m "Add new feature: description"
git push origin main
```

3. **Deploy to Render:**
- Changes will automatically deploy from GitHub
- Monitor logs in Render dashboard
- Test the live application

#### Database Migration in Production
To migrate production database:

1. **Access Render shell:**
```bash
# In Render dashboard, go to your web service
# Click "Shell" tab
```

2. **Run migration:**
```bash
python migrate_db.py
```

3. **Verify migration:**
```bash
python -c "from app import app, db; app.app_context().push(); from sqlalchemy import inspect; inspector = inspect(db.engine); print(inspector.get_table_names())"
```

### 9. Monitoring Updates

#### Adding Logging
To add comprehensive logging:

1. **Configure logging in `app.py`:**
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/chef_marketplace.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Chef Marketplace startup')
```

2. **Add logging to routes:**
```python
@app.route('/important-route')
def important_route():
    app.logger.info('Important route accessed')
    # Route logic
    app.logger.info('Important route completed successfully')
```

### 10. Backup and Recovery

#### Database Backup
To backup the database:

1. **Create backup script:**
```python
# backup_db.py
import os
from datetime import datetime
from app import app, db

def backup_database():
    with app.app_context():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'backup_{timestamp}.db'
        
        # For SQLite
        if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
            import shutil
            shutil.copy2('instance/chef_marketplace.db', f'backups/{backup_file}')
            print(f"Database backed up to {backup_file}")
        
        # For PostgreSQL (production)
        else:
            # Use pg_dump for PostgreSQL
            os.system(f'pg_dump {app.config["SQLALCHEMY_DATABASE_URI"]} > backups/{backup_file}.sql')
            print(f"Database backed up to {backup_file}.sql")

if __name__ == '__main__':
    backup_database()
```

2. **Schedule regular backups:**
```bash
# Add to crontab for daily backups
0 2 * * * cd /path/to/app && python backup_db.py
```

## Update Checklist

Before deploying any update:

- [ ] Test all new features locally
- [ ] Run the test suite
- [ ] Check database migrations
- [ ] Verify security measures
- [ ] Test responsive design
- [ ] Check error handling
- [ ] Update documentation
- [ ] Backup production database
- [ ] Deploy to staging (if available)
- [ ] Monitor logs after deployment
- [ ] Test live application
- [ ] Notify users of changes (if significant)

## Rollback Procedure

If an update causes issues:

1. **Immediate rollback:**
```bash
git revert HEAD
git push origin main
```

2. **Database rollback:**
```bash
# Restore from backup
python restore_db.py backup_20240101_120000.db
```

3. **Monitor and fix:**
- Check logs for errors
- Fix issues in development
- Test thoroughly before redeploying

## Support

For update-related issues:
- Check the troubleshooting guide
- Review error logs
- Test in development environment
- Contact support if needed

---

**Remember**: Always test updates thoroughly in a development environment before deploying to production!
