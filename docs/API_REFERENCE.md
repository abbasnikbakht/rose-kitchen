# 📚 API Reference - Chef Marketplace Platform

## Overview
This document provides a comprehensive reference for all API endpoints, data models, and integration points in the Chef Marketplace Platform.

## Base URL
- **Development**: `http://localhost:5000`
- **Production**: `https://your-app-name.onrender.com`

## Authentication
Most endpoints require authentication. Include the session cookie or use the login endpoint to authenticate.

## Endpoints

### Authentication

#### POST /login
User login endpoint.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123",
    "remember_me": true
}
```

**Response:**
- **200**: Login successful, redirects to dashboard
- **400**: Invalid credentials

#### POST /register
User registration endpoint.

**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "password": "password123",
    "password2": "password123",
    "role": "client"
}
```

**Response:**
- **200**: Registration successful
- **400**: Validation errors

#### GET /logout
User logout endpoint.

**Response:**
- **302**: Redirects to home page

### User Management

#### GET /dashboard
Redirects to role-specific dashboard.

**Response:**
- **302**: Redirects to appropriate dashboard

#### GET /client/dashboard
Client dashboard with upcoming and past bookings.

**Response:**
```json
{
    "upcoming_bookings": [...],
    "past_bookings": [...]
}
```

#### GET /chef/dashboard
Chef dashboard with bookings and reviews.

**Response:**
```json
{
    "chef_profile": {...},
    "upcoming_bookings": [...],
    "pending_requests": [...],
    "recent_reviews": [...]
}
```

#### GET /admin/dashboard
Admin dashboard with platform statistics.

**Response:**
```json
{
    "total_users": 150,
    "total_chefs": 25,
    "total_bookings": 300,
    "pending_bookings": 15,
    "recent_bookings": [...]
}
```

### Chef Management

#### GET /chef/profile
Get or edit chef profile.

**Response:**
```json
{
    "form": {...},
    "chef_profile": {
        "id": 1,
        "bio": "Professional chef with 10 years experience",
        "specialties": "Persian, Italian",
        "cuisine_types": ["persian", "italian"],
        "experience_years": 10,
        "base_price_per_person": 75.00,
        "teaching_price_per_person": 25.00,
        "min_guests": 2,
        "max_guests": 20,
        "offers_teaching": true,
        "rating": 4.8,
        "total_reviews": 45
    }
}
```

#### POST /chef/profile
Update chef profile.

**Request Body:**
```json
{
    "bio": "Updated bio",
    "specialties": "Persian, Italian, French",
    "cuisine_types": ["persian", "italian", "french"],
    "experience_years": 12,
    "base_price_per_person": 80.00,
    "teaching_price_per_person": 30.00,
    "min_guests": 2,
    "max_guests": 25,
    "offers_teaching": true,
    "teaching_experience": "I have taught cooking classes for 5 years"
}
```

### Chef Discovery

#### GET /chefs
Browse all available chefs with filtering.

**Query Parameters:**
- `page`: Page number (default: 1)
- `cuisine`: Filter by cuisine type
- `price_min`: Minimum price per person
- `price_max`: Maximum price per person
- `rating_min`: Minimum rating

**Response:**
```json
{
    "chefs": {
        "items": [...],
        "page": 1,
        "pages": 5,
        "per_page": 12,
        "total": 50
    },
    "cuisine_filter": "persian",
    "price_min": 50,
    "price_max": 100,
    "rating_min": 4.0
}
```

#### GET /chef/{chef_id}
Get detailed chef profile.

**Response:**
```json
{
    "chef_profile": {
        "id": 1,
        "user": {
            "first_name": "Ahmad",
            "last_name": "Hassani"
        },
        "bio": "Professional Persian chef",
        "specialties": "Persian, Middle Eastern",
        "cuisine_types": ["persian"],
        "experience_years": 15,
        "base_price_per_person": 85.00,
        "teaching_price_per_person": 35.00,
        "rating": 4.9,
        "total_reviews": 67,
        "response_time_hours": 12
    },
    "menus": [...],
    "reviews": [...]
}
```

### Booking Management

#### GET /chef/{chef_id}/book
Get booking form for a specific chef.

**Response:**
```json
{
    "form": {...},
    "chef_profile": {...}
}
```

#### POST /chef/{chef_id}/book
Create a new booking request.

**Request Body:**
```json
{
    "event_date": "2024-02-15",
    "event_time": "19:00",
    "guest_count": 4,
    "location_address": "123 Main St, City, State",
    "service_type": "cooking_and_teaching",
    "cuisine_preference": "persian",
    "occasion_type": "dinner_party",
    "dietary_restrictions": "No nuts, vegetarian options",
    "special_requests": "Please bring Persian tea"
}
```

**Response:**
- **302**: Redirects to booking detail page

#### GET /booking/{booking_id}
Get booking details.

**Response:**
```json
{
    "booking": {
        "id": 1,
        "client": {...},
        "chef": {...},
        "menu": {...},
        "event_date": "2024-02-15",
        "event_time": "19:00",
        "guest_count": 4,
        "service_type": "cooking_and_teaching",
        "cuisine_preference": "persian",
        "total_price": 420.00,
        "service_fee": 42.00,
        "platform_fee": 63.00,
        "status": "pending",
        "payment_status": "pending"
    }
}
```

#### POST /booking/{booking_id}/accept
Chef accepts a booking request.

**Response:**
- **302**: Redirects to booking detail page

#### POST /booking/{booking_id}/decline
Chef declines a booking request.

**Response:**
- **302**: Redirects to chef dashboard

### Review System

#### GET /booking/{booking_id}/review
Get review form for a completed booking.

**Response:**
```json
{
    "form": {...},
    "booking": {...}
}
```

#### POST /booking/{booking_id}/review
Submit a review for a completed booking.

**Request Body:**
```json
{
    "rating": 5,
    "food_quality": 5,
    "professionalism": 5,
    "cleanliness": 5,
    "communication": 5,
    "value_for_money": 5,
    "comment": "Excellent experience! The chef was professional and the food was amazing."
}
```

**Response:**
- **302**: Redirects to booking detail page

### Utility Endpoints

#### GET /debug-db
Debug database status (development only).

**Response:**
```html
<pre>
Database tables: ['user', 'chef_profile', 'booking', 'review', 'menu', 'menu_item', 'menu_photo', 'chef_availability', 'message']
User table columns: ['id', 'email', 'password_hash', 'first_name', 'last_name', 'phone', 'role', 'is_verified', 'created_at', 'last_login']
Chef profile columns: ['id', 'user_id', 'bio', 'specialties', 'cuisine_types', 'experience_years', 'certifications', 'service_areas', 'base_price_per_person', 'teaching_price_per_person', 'min_guests', 'max_guests', 'travel_fee', 'profile_photo', 'cover_photo', 'is_available', 'offers_teaching', 'teaching_experience', 'rating', 'total_reviews', 'response_time_hours', 'created_at', 'updated_at']
Booking columns: ['id', 'client_id', 'chef_id', 'menu_id', 'event_date', 'event_time', 'duration_hours', 'guest_count', 'location_address', 'service_type', 'cuisine_preference', 'occasion_type', 'dietary_restrictions', 'special_requests', 'total_price', 'service_fee', 'platform_fee', 'status', 'payment_status', 'stripe_payment_intent_id', 'created_at', 'updated_at']
</pre>
```

#### GET /migrate-db
Initialize database tables (production deployment).

**Response:**
```
Database migration successful! Created tables: ['user', 'chef_profile', 'booking', 'review', 'menu', 'menu_item', 'menu_photo', 'chef_availability', 'message']
```

## Data Models

### User
```json
{
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890",
    "role": "client",
    "is_verified": false,
    "created_at": "2024-01-01T00:00:00Z",
    "last_login": "2024-01-15T10:30:00Z"
}
```

### ChefProfile
```json
{
    "id": 1,
    "user_id": 1,
    "bio": "Professional chef with 10 years experience",
    "specialties": "Persian, Italian, French",
    "cuisine_types": "[\"persian\", \"italian\", \"french\"]",
    "experience_years": 10,
    "certifications": "Culinary Institute, Food Safety Certified",
    "service_areas": "Downtown, Midtown, Uptown",
    "base_price_per_person": 75.00,
    "teaching_price_per_person": 25.00,
    "min_guests": 2,
    "max_guests": 20,
    "travel_fee": 15.00,
    "profile_photo": "profile_123.jpg",
    "cover_photo": "cover_123.jpg",
    "is_available": true,
    "offers_teaching": true,
    "teaching_experience": "I have taught cooking classes for 5 years",
    "rating": 4.8,
    "total_reviews": 45,
    "response_time_hours": 24,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
}
```

### Booking
```json
{
    "id": 1,
    "client_id": 1,
    "chef_id": 2,
    "menu_id": 1,
    "event_date": "2024-02-15",
    "event_time": "19:00",
    "duration_hours": 3,
    "guest_count": 4,
    "location_address": "123 Main St, City, State 12345",
    "service_type": "cooking_and_teaching",
    "cuisine_preference": "persian",
    "occasion_type": "dinner_party",
    "dietary_restrictions": "No nuts, vegetarian options",
    "special_requests": "Please bring Persian tea",
    "total_price": 420.00,
    "service_fee": 42.00,
    "platform_fee": 63.00,
    "status": "confirmed",
    "payment_status": "paid",
    "stripe_payment_intent_id": "pi_1234567890",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
}
```

### Review
```json
{
    "id": 1,
    "client_id": 1,
    "chef_id": 2,
    "booking_id": 1,
    "rating": 5,
    "food_quality": 5,
    "professionalism": 5,
    "cleanliness": 5,
    "communication": 5,
    "value_for_money": 5,
    "comment": "Excellent experience! The chef was professional and the food was amazing.",
    "photos": "[]",
    "is_verified": true,
    "created_at": "2024-02-16T10:30:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "Validation failed",
    "details": {
        "email": ["Invalid email format"],
        "password": ["Password must be at least 6 characters"]
    }
}
```

### 401 Unauthorized
```json
{
    "error": "Authentication required",
    "message": "Please log in to access this resource"
}
```

### 403 Forbidden
```json
{
    "error": "Access denied",
    "message": "You don't have permission to access this resource"
}
```

### 404 Not Found
```json
{
    "error": "Resource not found",
    "message": "The requested resource was not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error",
    "message": "Something went wrong. Please try again later."
}
```

## Rate Limiting
- **Default**: 200 requests per day, 50 per hour
- **Sensitive endpoints**: 10 requests per minute
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## CORS
- **Allowed Origins**: Same origin only
- **Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization

## Webhooks

### Stripe Webhook
**Endpoint**: `/stripe-webhook`

**Events Handled**:
- `payment_intent.succeeded`
- `payment_intent.payment_failed`
- `charge.dispute.created`

**Request Body**:
```json
{
    "id": "evt_1234567890",
    "object": "event",
    "type": "payment_intent.succeeded",
    "data": {
        "object": {
            "id": "pi_1234567890",
            "amount": 42000,
            "currency": "usd",
            "status": "succeeded"
        }
    }
}
```

## SDK Examples

### Python
```python
import requests

# Login
response = requests.post('https://your-app.onrender.com/login', data={
    'email': 'user@example.com',
    'password': 'password123'
})

# Get chefs
response = requests.get('https://your-app.onrender.com/chefs?cuisine=persian&rating_min=4.0')
chefs = response.json()

# Create booking
response = requests.post('https://your-app.onrender.com/chef/1/book', data={
    'event_date': '2024-02-15',
    'event_time': '19:00',
    'guest_count': 4,
    'service_type': 'cooking_and_teaching'
})
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
        email: 'user@example.com',
        password: 'password123'
    })
});

// Get chefs
const chefsResponse = await fetch('/chefs?cuisine=persian&rating_min=4.0');
const chefs = await chefsResponse.json();

// Create booking
const bookingResponse = await fetch('/chef/1/book', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
        event_date: '2024-02-15',
        event_time: '19:00',
        guest_count: '4',
        service_type: 'cooking_and_teaching'
    })
});
```

## Testing

### Test Data
Use the following test data for development:

**Test Users**:
- Client: `client@test.com` / `password123`
- Chef: `chef@test.com` / `password123`
- Admin: `admin@test.com` / `password123`

**Test Chef Profile**:
- ID: 1
- Cuisine: Persian, Italian
- Price: $75/person
- Rating: 4.8

### Postman Collection
Import the following Postman collection for API testing:

```json
{
    "info": {
        "name": "Chef Marketplace API",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    },
    "item": [
        {
            "name": "Authentication",
            "item": [
                {
                    "name": "Login",
                    "request": {
                        "method": "POST",
                        "header": [],
                        "body": {
                            "mode": "urlencoded",
                            "urlencoded": [
                                {"key": "email", "value": "client@test.com"},
                                {"key": "password", "value": "password123"}
                            ]
                        },
                        "url": {
                            "raw": "{{base_url}}/login",
                            "host": ["{{base_url}}"],
                            "path": ["login"]
                        }
                    }
                }
            ]
        }
    ]
}
```

## Changelog

### Version 1.0.0
- Initial release
- User authentication
- Chef profiles
- Booking system
- Review system
- Payment integration

### Version 1.1.0
- Added dual service types (cooking only / cooking & teaching)
- Added multi-cuisine support
- Added database migration system
- Updated UI theme to Take a Chef style

---

**Last Updated**: January 2024
**API Version**: 1.1.0
