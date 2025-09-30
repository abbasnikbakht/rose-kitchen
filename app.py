from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, DateField, TimeField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
import os
from dotenv import load_dotenv
from translations import get_translation, get_available_languages, is_rtl_language

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
# Use PostgreSQL in production, SQLite in development
if os.environ.get('DATABASE_URL'):
    # Handle PostgreSQL URL format for Render
    database_url = os.environ.get('DATABASE_URL')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kitchen_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Increased for longer hashes
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='USA')
    is_cook = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    bookings = db.relationship('Booking', backref='customer', lazy=True)
    cook_profile = db.relationship('CookProfile', backref='cook', uselist=False)
    reviews_given = db.relationship('Review', backref='reviewer', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy=True)

class CookProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    specialties = db.Column(db.Text, nullable=False)  # JSON string of specialties
    experience_years = db.Column(db.Integer, nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    price_per_person = db.Column(db.Numeric(10, 2))  # Alternative pricing model
    service_radius = db.Column(db.Integer, default=25)  # miles
    profile_image = db.Column(db.String(200))
    introduction_video = db.Column(db.String(200))  # URL to intro video
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    response_time_hours = db.Column(db.Integer, default=24)
    cancellation_rate = db.Column(db.Numeric(5, 2), default=0.0)  # Percentage
    completion_rate = db.Column(db.Numeric(5, 2), default=100.0)  # Percentage
    min_guests = db.Column(db.Integer, default=1)
    max_guests = db.Column(db.Integer, default=50)
    travel_fee_per_mile = db.Column(db.Numeric(5, 2), default=2.0)
    setup_fee = db.Column(db.Numeric(10, 2), default=0.0)
    cleanup_fee = db.Column(db.Numeric(10, 2), default=0.0)
    dietary_expertise = db.Column(db.Text)  # JSON string of dietary specialties
    certifications = db.Column(db.Text)  # JSON string of certifications
    insurance_verified = db.Column(db.Boolean, default=False)
    background_check_verified = db.Column(db.Boolean, default=False)
    food_safety_certified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='cook_profile', lazy=True)
    reviews = db.relationship('Review', backref='cook_profile', lazy=True)
    menus = db.relationship('Menu', backref='chef', lazy=True)
    availability = db.relationship('ChefAvailability', backref='chef', lazy=True)
    portfolio_images = db.relationship('PortfolioImage', backref='chef', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cook_id = db.Column(db.Integer, db.ForeignKey('cook_profile.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=True)
    event_type = db.Column(db.String(50), nullable=False)  # party, family_gathering, event, etc.
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    location_address = db.Column(db.Text, nullable=False)
    location_city = db.Column(db.String(100), nullable=False)
    location_state = db.Column(db.String(100), nullable=False)
    location_zip = db.Column(db.String(20), nullable=False)
    special_requests = db.Column(db.Text)
    dietary_restrictions = db.Column(db.Text)  # JSON string
    kitchen_equipment = db.Column(db.Text)  # JSON string of available equipment
    shopping_preference = db.Column(db.String(50), default='chef_shops')  # chef_shops, client_provides, both
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    base_cost = db.Column(db.Numeric(10, 2), nullable=False)
    travel_fee = db.Column(db.Numeric(10, 2), default=0.0)
    setup_fee = db.Column(db.Numeric(10, 2), default=0.0)
    cleanup_fee = db.Column(db.Numeric(10, 2), default=0.0)
    platform_fee = db.Column(db.Numeric(10, 2), default=0.0)
    gratuity = db.Column(db.Numeric(10, 2), default=0.0)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, in_progress, completed, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    chef_confirmed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='booking', lazy=True)
    messages = db.relationship('Message', backref='booking', lazy=True)
    payments = db.relationship('Payment', backref='booking', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cook_id = db.Column(db.Integer, db.ForeignKey('cook_profile.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    food_quality = db.Column(db.Integer)  # 1-5 stars
    professionalism = db.Column(db.Integer)  # 1-5 stars
    cleanliness = db.Column(db.Integer)  # 1-5 stars
    communication = db.Column(db.Integer)  # 1-5 stars
    value_for_money = db.Column(db.Integer)  # 1-5 stars
    comment = db.Column(db.Text)
    photos = db.Column(db.Text)  # JSON string of photo URLs
    is_verified = db.Column(db.Boolean, default=True)
    chef_response = db.Column(db.Text)
    chef_response_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer, db.ForeignKey('cook_profile.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cuisine_type = db.Column(db.String(100), nullable=False)
    price_per_person = db.Column(db.Numeric(10, 2), nullable=False)
    min_guests = db.Column(db.Integer, default=1)
    max_guests = db.Column(db.Integer, default=50)
    preparation_time_hours = db.Column(db.Integer, default=2)
    is_customizable = db.Column(db.Boolean, default=True)
    dietary_accommodations = db.Column(db.Text)  # JSON string
    ingredients = db.Column(db.Text)  # JSON string
    courses = db.Column(db.Text)  # JSON string of course details
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    menu_images = db.relationship('MenuImage', backref='menu', lazy=True)
    bookings = db.relationship('Booking', backref='selected_menu', lazy=True)

class MenuImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PortfolioImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer, db.ForeignKey('cook_profile.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200))
    dish_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChefAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer, db.ForeignKey('cook_profile.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    max_bookings = db.Column(db.Integer, default=1)
    current_bookings = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=True)
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    attachments = db.Column(db.Text)  # JSON string of file URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(200), unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    platform_fee = db.Column(db.Numeric(10, 2), nullable=False)
    chef_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, completed, failed, refunded
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # booking, message, review, payment
    is_read = db.Column(db.Boolean, default=False)
    related_id = db.Column(db.Integer)  # ID of related booking, message, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    country = StringField('Country', default='USA')
    is_cook = SelectField('Account Type', choices=[('customer', 'Customer'), ('cook', 'Chef')], validators=[DataRequired()])
    submit = SubmitField('Register')

class CookProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[DataRequired()])
    specialties = TextAreaField('Specialties (one per line)', validators=[DataRequired()])
    experience_years = IntegerField('Years of Experience', validators=[DataRequired(), NumberRange(min=0)])
    hourly_rate = DecimalField('Hourly Rate ($)', validators=[DataRequired(), NumberRange(min=0)])
    price_per_person = DecimalField('Price Per Person ($)', validators=[NumberRange(min=0)])
    service_radius = IntegerField('Service Radius (miles)', validators=[DataRequired(), NumberRange(min=1, max=100)])
    min_guests = IntegerField('Minimum Guests', validators=[DataRequired(), NumberRange(min=1)])
    max_guests = IntegerField('Maximum Guests', validators=[DataRequired(), NumberRange(min=1)])
    travel_fee_per_mile = DecimalField('Travel Fee Per Mile ($)', validators=[NumberRange(min=0)])
    setup_fee = DecimalField('Setup Fee ($)', validators=[NumberRange(min=0)])
    cleanup_fee = DecimalField('Cleanup Fee ($)', validators=[NumberRange(min=0)])
    dietary_expertise = TextAreaField('Dietary Expertise (one per line)')
    certifications = TextAreaField('Certifications (one per line)')
    insurance_verified = SelectField('Insurance Verified', choices=[(False, 'No'), (True, 'Yes')])
    background_check_verified = SelectField('Background Check Verified', choices=[(False, 'No'), (True, 'Yes')])
    food_safety_certified = SelectField('Food Safety Certified', choices=[(False, 'No'), (True, 'Yes')])
    submit = SubmitField('Create Profile')

class BookingForm(FlaskForm):
    event_type = SelectField('Event Type', choices=[
        ('private_dinner', 'Private Dinner'),
        ('meal_prep', 'Meal Prep'),
        ('cooking_class', 'Cooking Class'),
        ('special_event', 'Special Event'),
        ('birthday', 'Birthday Celebration'),
        ('anniversary', 'Anniversary'),
        ('corporate_event', 'Corporate Event'),
        ('holiday', 'Holiday Celebration'),
        ('batch_cooking', 'Batch Cooking'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    guest_count = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1)])
    location_address = TextAreaField('Event Address', validators=[DataRequired()])
    location_city = StringField('City', validators=[DataRequired()])
    location_state = StringField('State', validators=[DataRequired()])
    location_zip = StringField('ZIP Code', validators=[DataRequired()])
    dietary_restrictions = TextAreaField('Dietary Restrictions/Preferences')
    kitchen_equipment = TextAreaField('Available Kitchen Equipment')
    shopping_preference = SelectField('Shopping Preference', choices=[
        ('chef_shops', 'Chef Shops for Ingredients'),
        ('client_provides', 'Client Provides Ingredients'),
        ('both', 'Both - Discuss with Chef')
    ], validators=[DataRequired()])
    special_requests = TextAreaField('Special Requests')
    submit = SubmitField('Book Chef')

class ReviewForm(FlaskForm):
    rating = SelectField('Overall Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[DataRequired()])
    food_quality = SelectField('Food Quality', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[DataRequired()])
    professionalism = SelectField('Professionalism', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[DataRequired()])
    cleanliness = SelectField('Cleanliness', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[DataRequired()])
    communication = SelectField('Communication', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[DataRequired()])
    value_for_money = SelectField('Value for Money', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit Review')

class MenuForm(FlaskForm):
    name = StringField('Menu Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    cuisine_type = StringField('Cuisine Type', validators=[DataRequired()])
    price_per_person = DecimalField('Price Per Person ($)', validators=[DataRequired(), NumberRange(min=0)])
    min_guests = IntegerField('Minimum Guests', validators=[DataRequired(), NumberRange(min=1)])
    max_guests = IntegerField('Maximum Guests', validators=[DataRequired(), NumberRange(min=1)])
    preparation_time_hours = IntegerField('Preparation Time (hours)', validators=[DataRequired(), NumberRange(min=1)])
    is_customizable = SelectField('Customizable', choices=[(True, 'Yes'), (False, 'No')])
    dietary_accommodations = TextAreaField('Dietary Accommodations')
    ingredients = TextAreaField('Key Ingredients')
    courses = TextAreaField('Courses (one per line)')
    submit = SubmitField('Create Menu')

class MessageForm(FlaskForm):
    subject = StringField('Subject')
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class SearchForm(FlaskForm):
    location = StringField('Location')
    cuisine_type = SelectField('Cuisine Type', choices=[
        ('', 'All Cuisines'),
        ('italian', 'Italian'),
        ('french', 'French'),
        ('asian', 'Asian'),
        ('persian', 'Persian'),
        ('mexican', 'Mexican'),
        ('american', 'American'),
        ('mediterranean', 'Mediterranean'),
        ('indian', 'Indian'),
        ('thai', 'Thai'),
        ('japanese', 'Japanese'),
        ('other', 'Other')
    ])
    min_price = DecimalField('Min Price ($)', validators=[NumberRange(min=0)])
    max_price = DecimalField('Max Price ($)', validators=[NumberRange(min=0)])
    min_rating = SelectField('Minimum Rating', choices=[
        (0, 'Any Rating'),
        (1, '1+ Stars'),
        (2, '2+ Stars'),
        (3, '3+ Stars'),
        (4, '4+ Stars'),
        (5, '5 Stars')
    ])
    dietary_requirements = SelectField('Dietary Requirements', choices=[
        ('', 'No Requirements'),
        ('vegan', 'Vegan'),
        ('vegetarian', 'Vegetarian'),
        ('gluten_free', 'Gluten-Free'),
        ('keto', 'Keto'),
        ('halal', 'Halal'),
        ('kosher', 'Kosher'),
        ('allergies', 'Food Allergies')
    ])
    event_type = SelectField('Event Type', choices=[
        ('', 'Any Event'),
        ('private_dinner', 'Private Dinner'),
        ('meal_prep', 'Meal Prep'),
        ('cooking_class', 'Cooking Class'),
        ('special_event', 'Special Event'),
        ('corporate_event', 'Corporate Event')
    ])
    submit = SubmitField('Search Chefs')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    try:
        featured_cooks = CookProfile.query.filter_by(is_available=True).limit(6).all()
        return render_template('index.html', featured_cooks=featured_cooks)
    except Exception as e:
        # If database tables don't exist yet, show a setup message
        return f"""
        <h1>گل سرخ Rose Kitchen</h1>
        <p>Welcome to Rose Kitchen! The database is being set up.</p>
        <p>Please visit <a href="/init-db">/init-db</a> to initialize the database with demo data.</p>
        <p>Error: {str(e)}</p>
        """

@app.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Try to query the database
        User.query.count()
        return "OK - Database connected"
    except Exception as e:
        return f"Database error: {str(e)}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            country=form.country.data,
            is_cook=(form.is_cook.data == 'cook')
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!', 'success')
        
        if user.is_cook:
            return redirect(url_for('create_cook_profile'))
        else:
            return redirect(url_for('dashboard'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_cook:
        bookings = Booking.query.filter_by(cook_id=current_user.cook_profile.id).order_by(Booking.event_date.desc()).all()
        return render_template('cook_dashboard.html', bookings=bookings)
    else:
        bookings = Booking.query.filter_by(customer_id=current_user.id).order_by(Booking.event_date.desc()).all()
        return render_template('customer_dashboard.html', bookings=bookings)

@app.route('/create-cook-profile', methods=['GET', 'POST'])
@login_required
def create_cook_profile():
    if not current_user.is_cook:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if current_user.cook_profile:
        flash('Profile already exists', 'error')
        return redirect(url_for('dashboard'))
    
    form = CookProfileForm()
    if form.validate_on_submit():
        cook_profile = CookProfile(
            user_id=current_user.id,
            bio=form.bio.data,
            specialties=form.specialties.data,
            experience_years=form.experience_years.data,
            hourly_rate=form.hourly_rate.data,
            price_per_person=form.price_per_person.data,
            service_radius=form.service_radius.data,
            min_guests=form.min_guests.data,
            max_guests=form.max_guests.data,
            travel_fee_per_mile=form.travel_fee_per_mile.data,
            setup_fee=form.setup_fee.data,
            cleanup_fee=form.cleanup_fee.data,
            dietary_expertise=form.dietary_expertise.data,
            certifications=form.certifications.data,
            insurance_verified=form.insurance_verified.data,
            background_check_verified=form.background_check_verified.data,
            food_safety_certified=form.food_safety_certified.data
        )
        
        db.session.add(cook_profile)
        db.session.commit()
        
        flash('Cook profile created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_cook_profile.html', form=form)

@app.route('/cooks')
def browse_cooks():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    # Get search parameters
    location = request.args.get('location', '')
    cuisine_type = request.args.get('cuisine_type', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', 0, type=int)
    dietary_requirements = request.args.get('dietary_requirements', '')
    event_type = request.args.get('event_type', '')
    
    # Build query
    query = CookProfile.query.filter_by(is_available=True)
    
    if location:
        query = query.join(User).filter(
            db.or_(
                User.city.ilike(f'%{location}%'),
                User.state.ilike(f'%{location}%')
            )
        )
    
    if cuisine_type:
        query = query.filter(CookProfile.specialties.ilike(f'%{cuisine_type}%'))
    
    if min_price:
        query = query.filter(CookProfile.price_per_person >= min_price)
    
    if max_price:
        query = query.filter(CookProfile.price_per_person <= max_price)
    
    if dietary_requirements:
        query = query.filter(CookProfile.dietary_expertise.ilike(f'%{dietary_requirements}%'))
    
    # Order by rating and availability
    cooks = query.order_by(CookProfile.is_featured.desc(), CookProfile.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('browse_cooks.html', cooks=cooks, form=form)

@app.route('/search')
def search_chefs():
    form = SearchForm()
    return render_template('search_chefs.html', form=form)

@app.route('/cook/<int:cook_id>')
def cook_profile(cook_id):
    cook = CookProfile.query.get_or_404(cook_id)
    reviews = Review.query.filter_by(cook_id=cook_id).all()
    menus = Menu.query.filter_by(chef_id=cook_id, is_active=True).all()
    portfolio_images = PortfolioImage.query.filter_by(chef_id=cook_id).all()
    
    # Calculate average ratings
    avg_rating = 0
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    return render_template('cook_detail.html', cook=cook, reviews=reviews, 
                         menus=menus, portfolio_images=portfolio_images, avg_rating=avg_rating)

@app.route('/cook/<int:cook_id>/menus')
def chef_menus(cook_id):
    cook = CookProfile.query.get_or_404(cook_id)
    menus = Menu.query.filter_by(chef_id=cook_id, is_active=True).all()
    return render_template('chef_menus.html', cook=cook, menus=menus)

@app.route('/menu/<int:menu_id>')
def menu_detail(menu_id):
    menu = Menu.query.get_or_404(menu_id)
    menu_images = MenuImage.query.filter_by(menu_id=menu_id).all()
    return render_template('menu_detail.html', menu=menu, menu_images=menu_images)

@app.route('/create-menu', methods=['GET', 'POST'])
@login_required
def create_menu():
    if not current_user.is_cook or not current_user.cook_profile:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    form = MenuForm()
    if form.validate_on_submit():
        menu = Menu(
            chef_id=current_user.cook_profile.id,
            name=form.name.data,
            description=form.description.data,
            cuisine_type=form.cuisine_type.data,
            price_per_person=form.price_per_person.data,
            min_guests=form.min_guests.data,
            max_guests=form.max_guests.data,
            preparation_time_hours=form.preparation_time_hours.data,
            is_customizable=form.is_customizable.data,
            dietary_accommodations=form.dietary_accommodations.data,
            ingredients=form.ingredients.data,
            courses=form.courses.data
        )
        
        db.session.add(menu)
        db.session.commit()
        
        flash('Menu created successfully!', 'success')
        return redirect(url_for('chef_menus', cook_id=current_user.cook_profile.id))
    
    return render_template('create_menu.html', form=form)

@app.route('/messages')
@login_required
def messages():
    # Get conversations for current user
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(recipient_id=current_user.id).all()
    
    # Group messages by conversation partner
    conversations = {}
    for msg in sent_messages + received_messages:
        partner_id = msg.recipient_id if msg.sender_id == current_user.id else msg.sender_id
        if partner_id not in conversations:
            conversations[partner_id] = []
        conversations[partner_id].append(msg)
    
    return render_template('messages.html', conversations=conversations)

@app.route('/messages/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    other_user = User.query.get_or_404(user_id)
    form = MessageForm()
    
    if form.validate_on_submit():
        message = Message(
            sender_id=current_user.id,
            recipient_id=user_id,
            subject=form.subject.data,
            content=form.content.data
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('Message sent!', 'success')
        return redirect(url_for('conversation', user_id=user_id))
    
    # Get conversation messages
    messages = Message.query.filter(
        db.or_(
            db.and_(Message.sender_id == current_user.id, Message.recipient_id == user_id),
            db.and_(Message.sender_id == user_id, Message.recipient_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()
    
    # Mark messages as read
    for msg in messages:
        if msg.recipient_id == current_user.id and not msg.is_read:
            msg.is_read = True
    db.session.commit()
    
    return render_template('conversation.html', other_user=other_user, messages=messages, form=form)

@app.route('/book/<int:cook_id>', methods=['GET', 'POST'])
@login_required
def book_cook(cook_id):
    cook = CookProfile.query.get_or_404(cook_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        # Calculate total cost
        start_time = datetime.combine(date.today(), form.start_time.data)
        end_time = datetime.combine(date.today(), form.end_time.data)
        duration_hours = (end_time - start_time).total_seconds() / 3600
        
        # Calculate base cost (use price per person if available, otherwise hourly rate)
        if cook.price_per_person:
            base_cost = float(cook.price_per_person) * form.guest_count.data
        else:
            base_cost = float(duration_hours) * float(cook.hourly_rate)
        
        # Calculate additional fees
        travel_fee = 0.0  # Will be calculated based on distance
        setup_fee = float(cook.setup_fee or 0)
        cleanup_fee = float(cook.cleanup_fee or 0)
        platform_fee = base_cost * 0.15  # 15% platform fee
        
        total_cost = base_cost + travel_fee + setup_fee + cleanup_fee + platform_fee
        
        booking = Booking(
            customer_id=current_user.id,
            cook_id=cook_id,
            event_type=form.event_type.data,
            event_date=form.event_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            guest_count=form.guest_count.data,
            location_address=form.location_address.data,
            location_city=form.location_city.data,
            location_state=form.location_state.data,
            location_zip=form.location_zip.data,
            special_requests=form.special_requests.data,
            dietary_restrictions=form.dietary_restrictions.data,
            kitchen_equipment=form.kitchen_equipment.data,
            shopping_preference=form.shopping_preference.data,
            total_cost=total_cost,
            base_cost=base_cost,
            travel_fee=travel_fee,
            setup_fee=setup_fee,
            cleanup_fee=cleanup_fee,
            platform_fee=platform_fee
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking request submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('book_cook.html', cook=cook, form=form)

@app.route('/booking/<int:booking_id>/review', methods=['GET', 'POST'])
@login_required
def review_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.customer_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    if booking.status != 'completed':
        flash('Can only review completed bookings', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if review already exists
    existing_review = Review.query.filter_by(booking_id=booking_id, reviewer_id=current_user.id).first()
    if existing_review:
        flash('You have already reviewed this booking', 'error')
        return redirect(url_for('dashboard'))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            booking_id=booking_id,
            reviewer_id=current_user.id,
            cook_id=booking.cook_id,
            rating=form.rating.data,
            food_quality=form.food_quality.data,
            professionalism=form.professionalism.data,
            cleanliness=form.cleanliness.data,
            communication=form.communication.data,
            value_for_money=form.value_for_money.data,
            comment=form.comment.data
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('review_booking.html', booking=booking, form=form)

@app.route('/booking/<int:booking_id>/update-status', methods=['POST'])
@login_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if not current_user.is_cook or current_user.cook_profile.id != booking.cook_id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    new_status = request.form.get('status')
    if new_status in ['confirmed', 'completed', 'cancelled']:
        booking.status = new_status
        if new_status == 'confirmed':
            booking.chef_confirmed_at = datetime.utcnow()
        elif new_status == 'completed':
            booking.completed_at = datetime.utcnow()
        elif new_status == 'cancelled':
            booking.cancelled_at = datetime.utcnow()
        db.session.commit()
        flash(f'Booking status updated to {new_status}', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get admin statistics
    total_users = User.query.count()
    total_chefs = User.query.filter_by(is_cook=True).count()
    total_bookings = Booking.query.count()
    total_revenue = db.session.query(db.func.sum(Booking.total_cost)).scalar() or 0
    
    # Recent activity
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_chefs=total_chefs,
                         total_bookings=total_bookings,
                         total_revenue=total_revenue,
                         recent_bookings=recent_bookings,
                         recent_users=recent_users)

@app.route('/init-db')
def init_database():
    """Initialize database with demo data - for deployment setup"""
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            
            # Check if demo data already exists
            if User.query.count() == 0:
                # Import and run demo data creation
                from demo_data import create_demo_data
                create_demo_data()
                return "Database initialized with demo data successfully!"
            else:
                return "Database already has data. No initialization needed."
    except Exception as e:
        return f"Error initializing database: {str(e)}"

@app.route('/migrate-db')
def migrate_database():
    """Migrate database schema - for handling schema changes"""
    try:
        with app.app_context():
            # Drop and recreate all tables (for development)
            # In production, you'd use proper migrations
            db.drop_all()
            db.create_all()
            
            # Recreate demo data
            from demo_data import create_demo_data
            create_demo_data()
            
            return "Database migrated successfully with new schema!"
    except Exception as e:
        return f"Error migrating database: {str(e)}"

def initialize_database():
    """Initialize database tables"""
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

# Initialize database on app startup
initialize_database()

# Language support functions
def get_current_language():
    """Get current language from session, default to English"""
    return session.get('language', 'en')

def set_language(language):
    """Set language in session"""
    if language in get_available_languages():
        session['language'] = language

def get_translated_text(key):
    """Get translated text for current language"""
    return get_translation(key, get_current_language())

def is_rtl():
    """Check if current language is right-to-left"""
    return is_rtl_language(get_current_language())

# Make functions available in templates
@app.context_processor
def inject_language_functions():
    return {
        'get_translated_text': get_translated_text,
        'get_current_language': get_current_language,
        'is_rtl': is_rtl,
        'get_available_languages': get_available_languages
    }

# Language switching route
@app.route('/set_language/<language>')
def set_language_route(language):
    """Set language and redirect back"""
    set_language(language)
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
