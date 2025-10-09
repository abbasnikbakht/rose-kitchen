"""
HomeTaste - Local Home Cooks & Private Chefs
A comprehensive platform connecting clients with local home cooks and professional chefs for authentic home-cooked meals.
"""

import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, DateField, TimeField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
import stripe
import json
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chef_marketplace.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_stripe_key')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'menus'), exist_ok=True)

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default='client')  # client, chef, admin
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    chef_profile = db.relationship('ChefProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    bookings_as_client = db.relationship('Booking', foreign_keys='Booking.client_id', backref='client')
    bookings_as_chef = db.relationship('Booking', foreign_keys='Booking.chef_id', backref='chef')
    reviews_given = db.relationship('Review', foreign_keys='Review.client_id', backref='reviewer')
    reviews_received = db.relationship('Review', foreign_keys='Review.chef_id', backref='chef_reviewed')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_chef(self):
        return self.role == 'chef'
    
    def is_admin(self):
        return self.role == 'admin'

class ChefProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text)
    specialties = db.Column(db.Text)  # JSON string of specialties
    cuisine_types = db.Column(db.Text)  # JSON string of cuisine types (Persian, Indian, Chinese, Italian, etc.)
    experience_years = db.Column(db.Integer)
    certifications = db.Column(db.Text)  # JSON string of certifications
    service_areas = db.Column(db.Text)  # JSON string of service areas
    base_price_per_person = db.Column(db.Numeric(10, 2))
    teaching_price_per_person = db.Column(db.Numeric(10, 2))  # Additional price for teaching
    min_guests = db.Column(db.Integer, default=2)
    max_guests = db.Column(db.Integer, default=20)
    travel_fee = db.Column(db.Numeric(10, 2), default=0)
    profile_photo = db.Column(db.String(200))
    cover_photo = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    offers_teaching = db.Column(db.Boolean, default=True)  # Whether chef offers cooking lessons
    teaching_experience = db.Column(db.Text)  # Description of teaching experience
    rating = db.Column(db.Numeric(3, 2), default=0)
    total_reviews = db.Column(db.Integer, default=0)
    response_time_hours = db.Column(db.Integer, default=24)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    menus = db.relationship('Menu', backref='chef', cascade='all, delete-orphan')
    availability = db.relationship('ChefAvailability', backref='chef', cascade='all, delete-orphan')

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef_profile.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price_per_person = db.Column(db.Numeric(10, 2))
    course_count = db.Column(db.Integer, default=3)
    prep_time_hours = db.Column(db.Integer, default=2)
    dietary_tags = db.Column(db.Text)  # JSON string of dietary tags
    ingredients = db.Column(db.Text)  # JSON string of ingredients
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    menu_items = db.relationship('MenuItem', backref='menu', cascade='all, delete-orphan')
    menu_photos = db.relationship('MenuPhoto', backref='menu', cascade='all, delete-orphan')

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    course_type = db.Column(db.String(50), nullable=False)  # appetizer, main, dessert, etc.
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

class MenuPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    photo_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)

class ChefAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef_profile.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    max_bookings = db.Column(db.Integer, default=1)
    current_bookings = db.Column(db.Integer, default=0)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    duration_hours = db.Column(db.Integer, default=3)
    guest_count = db.Column(db.Integer, nullable=False)
    location_address = db.Column(db.Text, nullable=False)
    service_type = db.Column(db.String(20), default='cooking_only')  # cooking_only, cooking_and_teaching
    cuisine_preference = db.Column(db.String(50))  # Persian, Indian, Chinese, Italian, etc.
    occasion_type = db.Column(db.String(50))  # dinner party, romantic dinner, etc.
    dietary_restrictions = db.Column(db.Text)
    special_requests = db.Column(db.Text)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    service_fee = db.Column(db.Numeric(10, 2), nullable=False)
    platform_fee = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    stripe_payment_intent_id = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    menu = db.relationship('Menu', backref='bookings')
    messages = db.relationship('Message', backref='booking', cascade='all, delete-orphan')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', backref='messages_sent')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    food_quality = db.Column(db.Integer, nullable=False)  # 1-5 stars
    professionalism = db.Column(db.Integer, nullable=False)  # 1-5 stars
    cleanliness = db.Column(db.Integer, nullable=False)  # 1-5 stars
    communication = db.Column(db.Integer, nullable=False)  # 1-5 stars
    value_for_money = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    photos = db.Column(db.Text)  # JSON string of photo URLs
    is_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    booking = db.relationship('Booking', backref='review')

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    role = SelectField('I want to', choices=[('client', 'Order Home-Cooked Meals'), ('chef', 'Cook for Others')], validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')
    
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not any(c.isupper() for c in password.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not any(c.islower() for c in password.data):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not any(c.isdigit() for c in password.data):
            raise ValidationError('Password must contain at least one number.')

class ChefProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[DataRequired(), Length(min=50, max=1000)])
    specialties = StringField('Specialties (comma-separated)', validators=[DataRequired()])
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
        ('other', 'Other')
    ], validators=[DataRequired()], multiple=True)
    experience_years = IntegerField('Years of Experience', validators=[DataRequired(), NumberRange(min=1, max=50)])
    certifications = StringField('Certifications (comma-separated)', validators=[Optional()])
    service_areas = StringField('Service Areas (comma-separated)', validators=[DataRequired()])
    base_price_per_person = DecimalField('Base Price per Person ($)', validators=[DataRequired(), NumberRange(min=25, max=500)])
    teaching_price_per_person = DecimalField('Teaching Price per Person ($)', validators=[Optional(), NumberRange(min=0, max=200)])
    min_guests = IntegerField('Minimum Guests', validators=[DataRequired(), NumberRange(min=1, max=10)])
    max_guests = IntegerField('Maximum Guests', validators=[DataRequired(), NumberRange(min=2, max=50)])
    travel_fee = DecimalField('Travel Fee ($)', validators=[Optional(), NumberRange(min=0, max=100)])
    offers_teaching = BooleanField('Offer Cooking Lessons', default=True)
    teaching_experience = TextAreaField('Teaching Experience', validators=[Optional(), Length(max=500)])
    profile_photo = FileField('Profile Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    cover_photo = FileField('Cover Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update Profile')

class BookingForm(FlaskForm):
    event_date = DateField('Event Date', validators=[DataRequired()])
    event_time = TimeField('Event Time', validators=[DataRequired()])
    guest_count = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1, max=50)])
    location_address = TextAreaField('Event Location', validators=[DataRequired(), Length(min=10, max=500)])
    service_type = SelectField('Service Type', choices=[
        ('cooking_only', 'Chef Cooks for You'),
        ('cooking_and_teaching', 'Chef Cooks & Teaches You')
    ], validators=[DataRequired()])
    cuisine_preference = SelectField('Cuisine Preference', choices=[
        ('', 'Any Cuisine'),
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
        ('other', 'Other')
    ], validators=[Optional()])
    occasion_type = SelectField('Occasion', choices=[
        ('dinner_party', 'Dinner Party'),
        ('romantic_dinner', 'Romantic Dinner'),
        ('birthday', 'Birthday Celebration'),
        ('anniversary', 'Anniversary'),
        ('corporate_event', 'Corporate Event'),
        ('meal_prep', 'Meal Prep'),
        ('cooking_class', 'Cooking Class'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    dietary_restrictions = TextAreaField('Dietary Restrictions/Preferences', validators=[Optional()])
    special_requests = TextAreaField('Special Requests', validators=[Optional()])
    submit = SubmitField('Request Booking')

class ReviewForm(FlaskForm):
    rating = SelectField('Overall Rating', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], validators=[DataRequired()])
    food_quality = SelectField('Food Quality', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], validators=[DataRequired()])
    professionalism = SelectField('Professionalism', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], validators=[DataRequired()])
    cleanliness = SelectField('Cleanliness', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], validators=[DataRequired()])
    communication = SelectField('Communication', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], validators=[DataRequired()])
    value_for_money = SelectField('Value for Money', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], validators=[DataRequired()])
    comment = TextAreaField('Review Comment', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Submit Review')

# Utility functions
def save_uploaded_file(file, folder):
    """Save uploaded file and return filename"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
        file.save(filepath)
        return filename
    return None

def resize_image(filepath, max_size=(800, 600)):
    """Resize image to max_size while maintaining aspect ratio"""
    try:
        with Image.open(filepath) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(filepath, optimize=True, quality=85)
    except Exception as e:
        print(f"Error resizing image: {e}")

def calculate_booking_total(chef_profile, guest_count, menu_price=None):
    """Calculate total booking cost including fees"""
    if menu_price:
        base_price = menu_price * guest_count
    else:
        base_price = chef_profile.base_price_per_person * guest_count
    
    travel_fee = chef_profile.travel_fee or 0
    service_fee = base_price * 0.1  # 10% service fee
    platform_fee = base_price * 0.15  # 15% platform fee
    
    total = base_price + travel_fee + service_fee + platform_fee
    return {
        'base_price': base_price,
        'travel_fee': travel_fee,
        'service_fee': service_fee,
        'platform_fee': platform_fee,
        'total': total
    }

# Routes
@app.route('/')
def index():
    """Home page with optimized queries"""
    try:
        # Optimized query with eager loading
        featured_chefs = ChefProfile.query.filter_by(is_available=True)\
            .options(db.joinedload(ChefProfile.user))\
            .order_by(ChefProfile.rating.desc())\
            .limit(6).all()
        
        # Optimized reviews query
        recent_reviews = Review.query\
            .options(db.joinedload(Review.client), db.joinedload(Review.chef_reviewed))\
            .order_by(Review.created_at.desc())\
            .limit(3).all()
            
        app.logger.info(f"Homepage loaded with {len(featured_chefs)} featured chefs")
    except Exception as e:
        app.logger.error(f"Database query error: {e}")
        featured_chefs = []
        recent_reviews = []
    
    return render_template('index.html', featured_chefs=featured_chefs, recent_reviews=recent_reviews)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('dashboard')
            return redirect(next_page)
        flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    try:
        form = RegistrationForm()
        if form.validate_on_submit():
            if form.password.data != form.password2.data:
                flash('Passwords do not match', 'error')
                return render_template('auth/register.html', form=form)
            
            user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data,
                role=form.role.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('auth/register.html', form=form)
        
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        flash('Registration failed. Please try again.', 'error')
        return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with onboarding check"""
    # Check if user needs onboarding
    if current_user.role == 'chef':
        chef_profile = current_user.chef_profile
        if not chef_profile:
            flash('Complete your chef profile to get started!', 'info')
            return redirect(url_for('chef_profile'))
        return redirect(url_for('chef_dashboard'))
    elif current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('client_dashboard'))

@app.route('/client/dashboard')
@login_required
def client_dashboard():
    """Client dashboard"""
    if current_user.role != 'client':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    upcoming_bookings = Booking.query.filter_by(
        client_id=current_user.id,
        status='confirmed'
    ).filter(Booking.event_date >= datetime.now().date()).order_by(Booking.event_date).all()
    
    past_bookings = Booking.query.filter_by(
        client_id=current_user.id,
        status='completed'
    ).order_by(Booking.event_date.desc()).limit(5).all()
    
    return render_template('client/dashboard.html', 
                         upcoming_bookings=upcoming_bookings,
                         past_bookings=past_bookings)

@app.route('/chef/dashboard')
@login_required
def chef_dashboard():
    """Chef dashboard"""
    if current_user.role != 'chef':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    chef_profile = current_user.chef_profile
    if not chef_profile:
        flash('Please complete your chef profile first', 'warning')
        return redirect(url_for('chef_profile'))
    
    upcoming_bookings = Booking.query.filter_by(
        chef_id=current_user.id,
        status='confirmed'
    ).filter(Booking.event_date >= datetime.now().date()).order_by(Booking.event_date).all()
    
    pending_requests = Booking.query.filter_by(
        chef_id=current_user.id,
        status='pending'
    ).order_by(Booking.created_at.desc()).all()
    
    recent_reviews = Review.query.filter_by(chef_id=current_user.id).order_by(Review.created_at.desc()).limit(5).all()
    
    return render_template('chef/dashboard.html',
                         chef_profile=chef_profile,
                         upcoming_bookings=upcoming_bookings,
                         pending_requests=pending_requests,
                         recent_reviews=recent_reviews)

@app.route('/chef/profile', methods=['GET', 'POST'])
@login_required
def chef_profile():
    """Chef profile management"""
    if current_user.role != 'chef':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    chef_profile = current_user.chef_profile
    form = ChefProfileForm()
    
    if form.validate_on_submit():
        if not chef_profile:
            chef_profile = ChefProfile(user_id=current_user.id)
            db.session.add(chef_profile)
        
        chef_profile.bio = form.bio.data
        chef_profile.specialties = form.specialties.data
        chef_profile.experience_years = form.experience_years.data
        chef_profile.certifications = form.certifications.data
        chef_profile.service_areas = form.service_areas.data
        chef_profile.base_price_per_person = form.base_price_per_person.data
        chef_profile.min_guests = form.min_guests.data
        chef_profile.max_guests = form.max_guests.data
        chef_profile.travel_fee = form.travel_fee.data or 0
        
        # Handle file uploads
        if form.profile_photo.data:
            filename = save_uploaded_file(form.profile_photo.data, 'profiles')
            if filename:
                chef_profile.profile_photo = filename
        
        if form.cover_photo.data:
            filename = save_uploaded_file(form.cover_photo.data, 'profiles')
            if filename:
                chef_profile.cover_photo = filename
        
        chef_profile.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('chef_dashboard'))
    
    # Pre-populate form if profile exists
    if chef_profile:
        form.bio.data = chef_profile.bio
        form.specialties.data = chef_profile.specialties
        form.experience_years.data = chef_profile.experience_years
        form.certifications.data = chef_profile.certifications
        form.service_areas.data = chef_profile.service_areas
        form.base_price_per_person.data = chef_profile.base_price_per_person
        form.min_guests.data = chef_profile.min_guests
        form.max_guests.data = chef_profile.max_guests
        form.travel_fee.data = chef_profile.travel_fee
    
    return render_template('chef/profile.html', form=form, chef_profile=chef_profile)

@app.route('/chefs')
def browse_chefs():
    """Browse all chefs with advanced filtering"""
    page = request.args.get('page', 1, type=int)
    cuisine_filter = request.args.get('cuisine', '')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    rating_min = request.args.get('rating_min', type=float)
    location_filter = request.args.get('location', '')
    service_type_filter = request.args.get('service_type', '')
    sort_by = request.args.get('sort', 'rating')  # rating, price_low, price_high, newest
    
    query = ChefProfile.query.filter_by(is_available=True)
    
    # Cuisine filtering
    if cuisine_filter:
        query = query.filter(ChefProfile.specialties.contains(cuisine_filter))
    
    # Price filtering
    if price_min:
        query = query.filter(ChefProfile.base_price_per_person >= price_min)
    
    if price_max:
        query = query.filter(ChefProfile.base_price_per_person <= price_max)
    
    # Rating filtering
    if rating_min:
        query = query.filter(ChefProfile.rating >= rating_min)
    
    # Location filtering (service areas)
    if location_filter:
        query = query.filter(ChefProfile.service_areas.contains(location_filter))
    
    # Service type filtering (cooking only vs cooking + teaching)
    if service_type_filter == 'teaching':
        query = query.filter(ChefProfile.offers_teaching == True)
    
    # Sorting
    if sort_by == 'price_low':
        query = query.order_by(ChefProfile.base_price_per_person.asc())
    elif sort_by == 'price_high':
        query = query.order_by(ChefProfile.base_price_per_person.desc())
    elif sort_by == 'newest':
        query = query.order_by(ChefProfile.created_at.desc())
    else:  # default: rating
        query = query.order_by(ChefProfile.rating.desc())
    
    chefs = query.paginate(
        page=page, per_page=12, error_out=False
    )
    
    # Get filter options for the UI
    all_cuisines = ['persian', 'indian', 'chinese', 'italian', 'french', 'mexican', 'japanese', 'thai', 'mediterranean', 'american', 'filipino', 'korean', 'vietnamese']
    all_locations = ['Metrotown', 'Brentwood', 'Edmonds', 'Lougheed', 'Burnaby Heights', 'Deer Lake', 'Highgate', 'Kingsway']
    
    return render_template('chefs/browse.html', 
                         chefs=chefs, 
                         cuisine_filter=cuisine_filter,
                         price_min=price_min, 
                         price_max=price_max,
                         rating_min=rating_min,
                         location_filter=location_filter,
                         service_type_filter=service_type_filter,
                         sort_by=sort_by,
                         all_cuisines=all_cuisines,
                         all_locations=all_locations)

@app.route('/chef/<int:chef_id>')
def chef_detail(chef_id):
    """Chef profile detail page"""
    chef_profile = ChefProfile.query.get_or_404(chef_id)
    menus = Menu.query.filter_by(chef_id=chef_id).all()
    reviews = Review.query.filter_by(chef_id=chef_profile.user_id).order_by(Review.created_at.desc()).limit(10).all()
    
    return render_template('chefs/detail.html', 
                         chef_profile=chef_profile,
                         menus=menus,
                         reviews=reviews)

@app.route('/chef/<int:chef_id>/book', methods=['GET', 'POST'])
@login_required
def book_chef(chef_id):
    """Book a chef"""
    if current_user.role != 'client':
        flash('Only clients can make bookings', 'error')
        return redirect(url_for('dashboard'))
    
    chef_profile = ChefProfile.query.get_or_404(chef_id)
    form = BookingForm()
    
    if form.validate_on_submit():
        # Calculate pricing
        pricing = calculate_booking_total(chef_profile, form.guest_count.data)
        
        booking = Booking(
            client_id=current_user.id,
            chef_id=chef_profile.user_id,
            menu_id=1,  # Default menu for now
            event_date=form.event_date.data,
            event_time=form.event_time.data,
            guest_count=form.guest_count.data,
            location_address=form.location_address.data,
            occasion_type=form.occasion_type.data,
            dietary_restrictions=form.dietary_restrictions.data,
            special_requests=form.special_requests.data,
            total_price=pricing['total'],
            service_fee=pricing['service_fee'],
            platform_fee=pricing['platform_fee']
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking request sent! The chef will respond within 24 hours.', 'success')
        return redirect(url_for('booking_detail', booking_id=booking.id))
    
    return render_template('bookings/create.html', form=form, chef_profile=chef_profile)

@app.route('/booking/<int:booking_id>')
@login_required
def booking_detail(booking_id):
    """Booking detail page"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Check if user has access to this booking
    if current_user.id not in [booking.client_id, booking.chef_id] and not current_user.is_admin():
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('bookings/detail.html', booking=booking)

@app.route('/booking/<int:booking_id>/accept', methods=['POST'])
@login_required
def accept_booking(booking_id):
    """Chef accepts a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    if current_user.id != booking.chef_id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    booking.status = 'confirmed'
    db.session.commit()
    
    flash('Booking accepted!', 'success')
    return redirect(url_for('booking_detail', booking_id=booking_id))

@app.route('/booking/<int:booking_id>/decline', methods=['POST'])
@login_required
def decline_booking(booking_id):
    """Chef declines a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    if current_user.id != booking.chef_id:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking declined', 'info')
    return redirect(url_for('chef_dashboard'))

@app.route('/booking/<int:booking_id>/review', methods=['GET', 'POST'])
@login_required
def review_booking(booking_id):
    """Review a completed booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    if current_user.id != booking.client_id or booking.status != 'completed':
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Check if review already exists
    existing_review = Review.query.filter_by(booking_id=booking_id).first()
    if existing_review:
        flash('You have already reviewed this booking', 'info')
        return redirect(url_for('booking_detail', booking_id=booking_id))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            client_id=current_user.id,
            chef_id=booking.chef_id,
            booking_id=booking_id,
            rating=form.rating.data,
            food_quality=form.food_quality.data,
            professionalism=form.professionalism.data,
            cleanliness=form.cleanliness.data,
            communication=form.communication.data,
            value_for_money=form.value_for_money.data,
            comment=form.comment.data
        )
        
        db.session.add(review)
        
        # Update chef rating
        chef_profile = ChefProfile.query.filter_by(user_id=booking.chef_id).first()
        if chef_profile:
            # Recalculate average rating
            all_reviews = Review.query.filter_by(chef_id=booking.chef_id).all()
            total_rating = sum(r.rating for r in all_reviews)
            chef_profile.rating = total_rating / len(all_reviews)
            chef_profile.total_reviews = len(all_reviews)
        
        db.session.commit()
        
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('booking_detail', booking_id=booking_id))
    
    return render_template('reviews/create.html', form=form, booking=booking)

# Debug route to check database status
@app.route('/debug-db')
def debug_database():
    """Debug database status"""
    try:
        with app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            result = f"Database tables: {tables}\n"
            
            if 'user' in tables:
                user_columns = [col['name'] for col in inspector.get_columns('user')]
                result += f"User table columns: {user_columns}\n"
            
            if 'chef_profile' in tables:
                chef_columns = [col['name'] for col in inspector.get_columns('chef_profile')]
                result += f"Chef profile columns: {chef_columns}\n"
            
            if 'booking' in tables:
                booking_columns = [col['name'] for col in inspector.get_columns('booking')]
                result += f"Booking columns: {booking_columns}\n"
            
            return f"<pre>{result}</pre>"
    except Exception as e:
        return f"Database debug error: {str(e)}", 500

# Database migration route (for production deployment)
@app.route('/migrate-db')
def migrate_database():
    """Create database tables - for production deployment"""
    try:
        with app.app_context():
            db.create_all()
            from sqlalchemy import inspect, text
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            # Add new columns if they don't exist
            try:
                chef_columns = [col['name'] for col in inspector.get_columns('chef_profile')]
                booking_columns = [col['name'] for col in inspector.get_columns('booking')]
                
                # Add new columns to chef_profile
                new_chef_columns = [
                    ('cuisine_types', 'TEXT'),
                    ('teaching_price_per_person', 'NUMERIC(10, 2)'),
                    ('offers_teaching', 'BOOLEAN DEFAULT TRUE'),
                    ('teaching_experience', 'TEXT')
                ]
                
                for column_name, column_type in new_chef_columns:
                    if column_name not in chef_columns:
                        with db.engine.connect() as conn:
                            conn.execute(text(f"ALTER TABLE chef_profile ADD COLUMN {column_name} {column_type}"))
                            conn.commit()
                
                # Add new columns to booking
                new_booking_columns = [
                    ('service_type', 'VARCHAR(20) DEFAULT \'cooking_only\''),
                    ('cuisine_preference', 'VARCHAR(50)')
                ]
                
                for column_name, column_type in new_booking_columns:
                    if column_name not in booking_columns:
                        with db.engine.connect() as conn:
                            conn.execute(text(f"ALTER TABLE booking ADD COLUMN {column_name} {column_type}"))
                            conn.commit()
                            
            except Exception as col_error:
                return f"Table creation successful but column migration failed: {str(col_error)}"
            
            return f"Database migration successful! Created tables: {tables}"
    except Exception as e:
        return f"Migration failed: {str(e)}", 500

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin():
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_chefs = User.query.filter_by(role='chef').count()
    total_bookings = Booking.query.count()
    pending_bookings = Booking.query.filter_by(status='pending').count()
    
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_chefs=total_chefs,
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         recent_bookings=recent_bookings)

# Enhanced Error handlers
@app.errorhandler(400)
def bad_request_error(error):
    return render_template('errors/400.html'), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('errors/401.html'), 401

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(413)
def too_large_error(error):
    return render_template('errors/413.html'), 413

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(503)
def service_unavailable_error(error):
    return render_template('errors/503.html'), 503

# Initialize database
def create_tables():
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
            import traceback
            traceback.print_exc()

# Configure logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/hometaste.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('HomeTaste startup')

# Initialize database on app startup (for production)
with app.app_context():
    try:
        db.create_all()
        print("Production database initialized")
        app.logger.info("Database initialized successfully")
    except Exception as e:
        print(f"Production database init error: {e}")
        app.logger.error(f"Database initialization error: {e}")

if __name__ == '__main__':
    print("Starting HomeTaste Platform...")
    print("Initializing database...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database initialized successfully")
            
            # Verify tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Database tables: {tables}")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)
