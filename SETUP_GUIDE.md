# گل سرخ Rose Kitchen Setup Guide

## 🚀 Quick Start

Your گل سرخ Rose Kitchen application is now ready to use! Here's how to get started:

### 1. Application Status
✅ **Application is running on:** http://localhost:5000  
✅ **Database populated with demo data**  
✅ **All features implemented and working**

### 2. Demo Accounts

#### Customer Accounts (for booking Persian chefs):
- **Email:** ahmad@example.com | **Password:** password123
- **Email:** soheila@example.com | **Password:** password123  
- **Email:** hassan@example.com | **Password:** password123

#### Persian Chef Accounts (for offering authentic Iranian cuisine):
- **Email:** rose@example.com | **Password:** password123 (Tehran Cuisine)
- **Email:** soheila_chef@example.com | **Password:** password123 (Isfahan Cuisine)
- **Email:** hala@example.com | **Password:** password123 (Shiraz Cuisine - Halal)
- **Email:** iran@example.com | **Password:** password123 (Traditional Iranian)

### 3. How to Use the Application

#### For Customers:
1. **Login** with any customer account
2. **Browse Persian Chefs** to see available authentic Iranian chefs
3. **View Chef Profiles** to see specialties, rates, and reviews
4. **Book a Persian Chef** by selecting date, time, and event details
5. **Manage Bookings** in your dashboard
6. **Rate & Review** after completed services

#### For Persian Chefs:
1. **Login** with any chef account
2. **View Dashboard** to see booking requests and earnings
3. **Accept/Confirm** pending bookings
4. **Mark as Completed** after providing service
5. **Track Earnings** and performance metrics

### 4. Key Features to Test

#### 🏠 Homepage
- Browse featured Persian chefs
- Learn about authentic Iranian cuisine
- Quick access to registration/login

#### 👥 User Registration
- Create customer or Persian chef accounts
- Complete profile setup
- Automatic role-based routing

#### 🔍 Persian Chef Discovery
- Browse all available Iranian chefs
- Filter by specialties and rates
- View detailed chef profiles

#### 📅 Booking System
- Select event type and date/time
- Specify guest count and special requests
- Automatic cost calculation
- Booking confirmation

#### 📊 Dashboards
- **Customer Dashboard:** Manage bookings, view history
- **Chef Dashboard:** Handle requests, track earnings, update status

#### ⭐ Review System
- Rate Persian chefs after completed services
- Write detailed reviews
- View reviews on chef profiles

### 5. Application Structure

```
Kitchen/
├── app.py                 # Main Flask application
├── run.py                 # Startup script
├── demo_data.py          # Demo data population
├── requirements.txt      # Python dependencies
├── README.md            # Comprehensive documentation
├── SETUP_GUIDE.md       # This setup guide
├── env_example.txt      # Environment variables template
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── browse_cooks.html
│   ├── cook_detail.html
│   ├── book_cook.html
│   ├── customer_dashboard.html
│   ├── cook_dashboard.html
│   ├── create_cook_profile.html
│   └── review_booking.html
└── static/              # CSS, JS, images (future use)
```

### 6. Database Schema

The application uses SQLite with the following main tables:
- **Users:** Customer and cook accounts
- **CookProfiles:** Professional cook information
- **Bookings:** Event bookings and scheduling
- **Reviews:** Customer feedback and ratings

### 7. Technology Stack

- **Backend:** Python Flask
- **Database:** SQLite (easily upgradeable)
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF with WTForms
- **Styling:** Custom CSS with modern design

### 8. Next Steps for Production

1. **Environment Setup:**
   - Copy `env_example.txt` to `.env`
   - Update SECRET_KEY and database URL
   - Configure email settings

2. **Database Upgrade:**
   - Switch to PostgreSQL or MySQL
   - Set up database migrations

3. **Payment Integration:**
   - Add Stripe payment processing
   - Implement secure payment flows

4. **Email Notifications:**
   - Booking confirmations
   - Status updates
   - Review notifications

5. **Advanced Features:**
   - Real-time chat
   - Calendar integration
   - Mobile app
   - Advanced search filters

### 9. Troubleshooting

#### Application won't start:
```bash
pip install -r requirements.txt
python run.py
```

#### Database issues:
```bash
python demo_data.py  # Recreate demo data
```

#### Port already in use:
- Change port in `run.py` or kill existing process
- Use `netstat -an | findstr :5000` to check port usage

### 10. Support

The application is fully functional with:
- ✅ User authentication and registration
- ✅ Cook profile management
- ✅ Booking system with status management
- ✅ Review and rating system
- ✅ Responsive modern UI
- ✅ Role-based dashboards
- ✅ Demo data for testing

**Enjoy exploring your new گل سرخ Rose Kitchen application! 🍳🌹✨**

---

*For detailed technical documentation, see README.md*
