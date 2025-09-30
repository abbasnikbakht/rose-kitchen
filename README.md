# 🍳 Chef Marketplace Platform

A comprehensive marketplace platform that connects clients with professional chefs for in-home cooking services. Built with Flask, this platform provides a seamless experience for booking personalized culinary experiences.

## ✨ Features

### For Clients
- **Browse & Search Chefs**: Find professional chefs by cuisine, location, rating, and price
- **Detailed Chef Profiles**: View chef backgrounds, specialties, certifications, and sample menus
- **Easy Booking System**: Simple booking flow with date/time selection and customization
- **Secure Payments**: Integrated Stripe payment processing
- **Real-time Messaging**: Direct communication with chefs
- **Review System**: Rate and review your dining experiences
- **Dashboard**: Manage bookings, view history, and track favorites

### For Chefs
- **Professional Profiles**: Create detailed profiles with photos, bio, and specialties
- **Menu Management**: Showcase sample menus and pricing
- **Booking Management**: Accept/decline requests and manage calendar
- **Earnings Tracking**: Monitor income and payout schedules
- **Client Communication**: Direct messaging with clients
- **Performance Analytics**: Track ratings and reviews

### For Admins
- **User Management**: Oversee all users, chefs, and bookings
- **Platform Analytics**: Monitor platform performance and revenue
- **Content Moderation**: Manage reviews and user-generated content
- **Support Tools**: Handle disputes and customer service

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chef-marketplace.git
   cd chef-marketplace
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python app.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `env_example.txt`:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///chef_marketplace.db

# Stripe Configuration (Required for payments)
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Database Setup

The application uses SQLite by default for development. For production, configure PostgreSQL:

```bash
DATABASE_URL=postgresql://username:password@localhost/chef_marketplace
```

## 📱 User Roles

### Client
- Browse and search for chefs
- Book cooking services
- Rate and review experiences
- Manage bookings and favorites

### Chef
- Create and manage professional profile
- Set availability and pricing
- Accept/decline booking requests
- Communicate with clients
- Track earnings and performance

### Admin
- Manage all users and content
- Monitor platform performance
- Handle support requests
- Configure platform settings

## 🎨 Design Features

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Modern UI**: Clean, professional interface with food-centric design
- **Interactive Elements**: Smooth animations and hover effects
- **Accessibility**: WCAG compliant with proper contrast and navigation
- **Performance**: Optimized images and lazy loading

## 💳 Payment Integration

The platform integrates with Stripe for secure payment processing:

- **Secure Payments**: PCI-compliant payment processing
- **Multiple Payment Methods**: Credit cards, digital wallets
- **Automatic Payouts**: Scheduled payments to chefs
- **Refund Management**: Easy refund processing
- **Fee Calculation**: Automatic platform and service fee calculation

## 🔒 Security Features

- **User Authentication**: Secure login with password hashing
- **Role-based Access**: Different permissions for clients, chefs, and admins
- **Data Validation**: Server-side validation for all forms
- **File Upload Security**: Secure image upload with validation
- **CSRF Protection**: Cross-site request forgery protection
- **SQL Injection Prevention**: Parameterized queries

## 📊 Database Schema

### Core Tables
- **Users**: Client, chef, and admin accounts
- **ChefProfiles**: Detailed chef information and settings
- **Bookings**: Service bookings and scheduling
- **Reviews**: Client ratings and feedback
- **Messages**: Communication between users
- **Menus**: Chef menu offerings and pricing

## 🚀 Deployment

### Render (Recommended)
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables
4. Deploy automatically

### Heroku
1. Install Heroku CLI
2. Create Heroku app
3. Set environment variables
4. Deploy with Git

### Docker
```bash
docker build -t chef-marketplace .
docker run -p 5000:5000 chef-marketplace
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📈 Performance Optimization

- **Image Optimization**: Automatic resizing and compression
- **Database Indexing**: Optimized queries for large datasets
- **Caching**: Redis integration for frequently accessed data
- **CDN Ready**: Static asset optimization for global delivery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, email support@chefmarketplace.com or join our Slack channel.

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Core booking system
- ✅ User authentication
- ✅ Basic payment integration
- ✅ Review system

### Phase 2 (Next)
- 🔄 Advanced search and filtering
- 🔄 Mobile app (React Native)
- 🔄 Real-time notifications
- 🔄 Advanced analytics

### Phase 3 (Future)
- 📅 AI-powered chef recommendations
- 📅 Video call integration
- 📅 Multi-language support
- 📅 Corporate accounts

## 🙏 Acknowledgments

- Bootstrap for the responsive framework
- Font Awesome for icons
- Stripe for payment processing
- Flask community for excellent documentation

---

**Built with ❤️ for food lovers everywhere**
