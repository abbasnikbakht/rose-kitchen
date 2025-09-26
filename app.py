from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DecimalField, DateField, TimeField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
import os
from dotenv import load_dotenv

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
    password_hash = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    is_cook = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='customer', lazy=True)
    cook_profile = db.relationship('CookProfile', backref='cook', uselist=False)
    reviews_given = db.relationship('Review', backref='reviewer', lazy=True)

class CookProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    specialties = db.Column(db.Text, nullable=False)  # JSON string of specialties
    experience_years = db.Column(db.Integer, nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    service_radius = db.Column(db.Integer, default=25)  # miles
    profile_image = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='cook_profile', lazy=True)
    reviews = db.relationship('Review', backref='cook_profile', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cook_id = db.Column(db.Integer, db.ForeignKey('cook_profile.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # party, family_gathering, event, etc.
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', backref='booking', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cook_id = db.Column(db.Integer, db.ForeignKey('cook_profile.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
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
    is_cook = SelectField('Account Type', choices=[('customer', 'Customer'), ('cook', 'Cook')], validators=[DataRequired()])
    submit = SubmitField('Register')

class CookProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[DataRequired()])
    specialties = TextAreaField('Specialties (one per line)', validators=[DataRequired()])
    experience_years = IntegerField('Years of Experience', validators=[DataRequired(), NumberRange(min=0)])
    hourly_rate = DecimalField('Hourly Rate ($)', validators=[DataRequired(), NumberRange(min=0)])
    service_radius = IntegerField('Service Radius (miles)', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Create Profile')

class BookingForm(FlaskForm):
    event_type = SelectField('Event Type', choices=[
        ('party', 'Party'),
        ('family_gathering', 'Family Gathering'),
        ('corporate_event', 'Corporate Event'),
        ('birthday', 'Birthday Celebration'),
        ('anniversary', 'Anniversary'),
        ('holiday', 'Holiday Celebration'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    guest_count = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1)])
    special_requests = TextAreaField('Special Requests')
    submit = SubmitField('Book Cook')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit Review')

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
            service_radius=form.service_radius.data
        )
        
        db.session.add(cook_profile)
        db.session.commit()
        
        flash('Cook profile created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('create_cook_profile.html', form=form)

@app.route('/cooks')
def browse_cooks():
    cooks = CookProfile.query.filter_by(is_available=True).all()
    return render_template('browse_cooks.html', cooks=cooks)

@app.route('/cook/<int:cook_id>')
def cook_profile(cook_id):
    cook = CookProfile.query.get_or_404(cook_id)
    reviews = Review.query.filter_by(cook_id=cook_id).all()
    return render_template('cook_detail.html', cook=cook, reviews=reviews)

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
        total_cost = float(duration_hours) * float(cook.hourly_rate)
        
        booking = Booking(
            customer_id=current_user.id,
            cook_id=cook_id,
            event_type=form.event_type.data,
            event_date=form.event_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            guest_count=form.guest_count.data,
            special_requests=form.special_requests.data,
            total_cost=total_cost
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
        db.session.commit()
        flash(f'Booking status updated to {new_status}', 'success')
    
    return redirect(url_for('dashboard'))

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

def initialize_database():
    """Initialize database tables"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

# Initialize database on app startup
initialize_database()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
