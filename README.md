# گل سرخ Rose Kitchen - Authentic Persian Home Cooking Service

A comprehensive web application that connects customers with authentic Persian and Iranian chefs for home cooking services. Experience the rich flavors of Iran, from traditional Tehran dishes to Isfahan specialties and Shiraz cuisine. Perfect for parties, family gatherings, corporate events, and special occasions.

## Features

### For Customers
- **Browse Authentic Persian Chefs**: Search through a network of experienced Iranian chefs
- **Easy Booking System**: Simple booking process with date/time selection
- **Event Types**: Support for parties, family gatherings, corporate events, birthdays, anniversaries, and more
- **Special Requests**: Custom dietary requirements and traditional Persian menu preferences
- **Rating & Reviews**: Rate and review Persian chefs after service
- **Dashboard**: Manage all your bookings in one place

### For Persian Chefs
- **Professional Profiles**: Create detailed profiles showcasing Iranian cuisine specialties and experience
- **Booking Management**: Accept, confirm, and manage customer bookings
- **Earnings Tracking**: Monitor your income and completed jobs
- **Availability Management**: Control your service availability
- **Customer Reviews**: Build reputation through customer feedback

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily upgradeable to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Styling**: Custom CSS with Bootstrap components

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Kitchen
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env file with your configuration
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Database Schema

### Users Table
- User authentication and basic information
- Support for both customers and cooks
- Contact information and address

### Cook Profiles Table
- Professional cook information
- Specialties, experience, and hourly rates
- Service radius and availability status

### Bookings Table
- Event details and scheduling
- Customer-cook relationships
- Booking status and cost calculation

### Reviews Table
- Customer feedback and ratings
- Review comments and timestamps

## Key Features Implementation

### Authentication System
- User registration with role selection (Customer/Cook)
- Secure login with password hashing
- Session management with Flask-Login

### Booking System
- Date and time selection
- Cost calculation based on duration and hourly rate
- Status management (pending, confirmed, completed, cancelled)

### Review System
- 5-star rating system
- Written reviews and comments
- Review display on cook profiles

### Dashboard Features
- Different dashboards for customers and cooks
- Booking management and status updates
- Statistics and earnings tracking

## Future Enhancements

- **Payment Integration**: Stripe payment processing
- **Email Notifications**: Booking confirmations and updates
- **Advanced Search**: Filter by cuisine, price range, availability
- **Calendar Integration**: Google Calendar sync
- **Mobile App**: React Native or Flutter mobile application
- **Real-time Chat**: Customer-cook communication
- **Photo Gallery**: Cook portfolio and food photos
- **Advanced Analytics**: Detailed performance metrics

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - User login
- `GET /register` - Registration page
- `POST /register` - User registration
- `GET /logout` - User logout

### Cook Management
- `GET /cooks` - Browse all cooks
- `GET /cook/<id>` - View cook profile
- `GET /create-cook-profile` - Create cook profile
- `POST /create-cook-profile` - Submit cook profile

### Booking System
- `GET /book/<cook_id>` - Book a cook
- `POST /book/<cook_id>` - Submit booking
- `POST /booking/<id>/update-status` - Update booking status
- `GET /booking/<id>/review` - Review booking
- `POST /booking/<id>/review` - Submit review

### Dashboard
- `GET /dashboard` - User dashboard (role-based)

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Input validation and sanitization
- SQL injection prevention with SQLAlchemy ORM
- Session management and user authentication

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables
3. Use a WSGI server like Gunicorn
4. Set up reverse proxy with Nginx
5. Enable HTTPS with SSL certificates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact:
- Email: support@kitchenbook.com
- Phone: +1 (555) 123-4567

## Screenshots

The application features a modern, responsive design with:
- Clean, professional interface
- Mobile-friendly responsive layout
- Intuitive navigation and user experience
- Beautiful cook profile cards
- Comprehensive booking management
- Real-time status updates

---

**KitchenBook** - Bringing professional cooking services to your home! 🍳✨
