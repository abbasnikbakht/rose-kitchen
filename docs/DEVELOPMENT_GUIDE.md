# 👨‍💻 Development Guide - Chef Marketplace Platform

## Overview
This guide provides comprehensive instructions for setting up, developing, and contributing to the Chef Marketplace Platform.

## Prerequisites

### Required Software
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher (for frontend tools)
- **Git**: Latest version
- **Database**: SQLite (development) or PostgreSQL (production)

### Recommended Tools
- **IDE**: VS Code, PyCharm, or similar
- **Database Client**: DBeaver, pgAdmin, or similar
- **API Testing**: Postman, Insomnia, or similar
- **Version Control**: Git with GitHub

## Development Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/chef-marketplace.git
cd chef-marketplace
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env with your configuration
# Required variables:
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///chef_marketplace.db
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Database Setup
```bash
# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Run migrations (if any)
python migrate_db.py
```

### 6. Start Development Server
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
chef-marketplace/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Development dependencies
├── Procfile             # Production deployment
├── runtime.txt          # Python version specification
├── .env                 # Environment variables (not in git)
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
├── docs/                # Documentation
│   ├── UPDATE_GUIDE.md
│   ├── API_REFERENCE.md
│   ├── FEATURE_ROADMAP.md
│   └── DEVELOPMENT_GUIDE.md
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── uploads/
│       ├── profiles/
│       └── menus/
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   ├── chef/
│   ├── client/
│   ├── admin/
│   ├── bookings/
│   ├── reviews/
│   └── errors/
├── tests/               # Test files
│   ├── test_app.py
│   ├── test_models.py
│   └── test_routes.py
├── migrations/          # Database migrations
│   ├── migrate_db.py
│   └── migrate_production.py
└── instance/            # Instance-specific files
    └── chef_marketplace.db
```

## Development Workflow

### 1. Feature Development
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
# ... develop feature ...

# Test changes
python test_app.py

# Commit changes
git add .
git commit -m "Add new feature: description"

# Push to remote
git push origin feature/new-feature

# Create pull request
```

### 2. Bug Fixes
```bash
# Create bugfix branch
git checkout -b bugfix/issue-description

# Fix the bug
# ... implement fix ...

# Test fix
python test_app.py

# Commit fix
git add .
git commit -m "Fix: description of fix"

# Push and create PR
git push origin bugfix/issue-description
```

### 3. Database Changes
```bash
# Create migration script
touch migrations/migrate_new_feature.py

# Implement migration
# ... add migration code ...

# Test migration
python migrations/migrate_new_feature.py

# Update models in app.py
# ... update model definitions ...

# Test application
python app.py
```

## Code Standards

### Python Code Style
- **PEP 8**: Follow Python PEP 8 style guide
- **Line Length**: Maximum 88 characters (Black formatter)
- **Imports**: Use absolute imports, group by standard/third-party/local
- **Docstrings**: Use Google-style docstrings for functions and classes

```python
def calculate_booking_total(chef_profile, guest_count, menu_price=None):
    """Calculate total booking cost including fees.
    
    Args:
        chef_profile: ChefProfile instance
        guest_count: Number of guests
        menu_price: Optional menu price override
        
    Returns:
        dict: Pricing breakdown with total cost
    """
    # Implementation here
    pass
```

### HTML/CSS Standards
- **HTML5**: Use semantic HTML5 elements
- **CSS**: Use BEM methodology for class naming
- **Responsive**: Mobile-first responsive design
- **Accessibility**: WCAG 2.1 AA compliance

```html
<!-- Good HTML structure -->
<section class="chef-profile">
    <div class="chef-profile__header">
        <h1 class="chef-profile__title">Chef Name</h1>
    </div>
    <div class="chef-profile__content">
        <p class="chef-profile__bio">Chef bio text</p>
    </div>
</section>
```

```css
/* Good CSS structure */
.chef-profile {
    /* Block styles */
}

.chef-profile__header {
    /* Element styles */
}

.chef-profile__title {
    /* Element styles */
}

.chef-profile--featured {
    /* Modifier styles */
}
```

### JavaScript Standards
- **ES6+**: Use modern JavaScript features
- **Functions**: Use arrow functions for callbacks
- **Variables**: Use const/let instead of var
- **Async/Await**: Prefer async/await over promises

```javascript
// Good JavaScript
const fetchChefData = async (chefId) => {
    try {
        const response = await fetch(`/api/chef/${chefId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching chef data:', error);
        throw error;
    }
};
```

## Testing

### Test Structure
```python
# tests/test_models.py
import unittest
from app import app, db, User, ChefProfile

class TestModels(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        with app.app_context():
            db.drop_all()
    
    def test_user_creation(self):
        user = User(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role='client'
        )
        user.set_password('password123')
        
        with app.app_context():
            db.session.add(user)
            db.session.commit()
            
            self.assertEqual(user.email, 'test@example.com')
            self.assertTrue(user.check_password('password123'))
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_models.py

# Run with coverage
python -m pytest --cov=app tests/

# Run with verbose output
python -m pytest -v tests/
```

### Test Data
```python
# tests/fixtures.py
def create_test_user():
    user = User(
        email='test@example.com',
        first_name='Test',
        last_name='User',
        role='client'
    )
    user.set_password('password123')
    return user

def create_test_chef():
    user = create_test_user()
    user.role = 'chef'
    
    chef_profile = ChefProfile(
        user_id=user.id,
        bio='Test chef bio',
        specialties='Persian, Italian',
        experience_years=5,
        base_price_per_person=75.00
    )
    return user, chef_profile
```

## Database Development

### Model Development
```python
# app.py
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NewModel {self.name}>'
```

### Migration Scripts
```python
# migrations/migrate_new_model.py
from app import app, db
from sqlalchemy import text

def migrate_new_model():
    with app.app_context():
        with db.engine.connect() as conn:
            # Create new table
            conn.execute(text("""
                CREATE TABLE new_model (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("New model table created successfully")

if __name__ == '__main__':
    migrate_new_model()
```

### Database Queries
```python
# Good query practices
def get_chefs_by_cuisine(cuisine_type):
    """Get chefs specializing in specific cuisine."""
    return ChefProfile.query.filter(
        ChefProfile.specialties.contains(cuisine_type),
        ChefProfile.is_available == True
    ).order_by(ChefProfile.rating.desc()).all()

def get_upcoming_bookings(user_id, role):
    """Get upcoming bookings for user."""
    if role == 'client':
        return Booking.query.filter(
            Booking.client_id == user_id,
            Booking.status == 'confirmed',
            Booking.event_date >= datetime.now().date()
        ).order_by(Booking.event_date).all()
    elif role == 'chef':
        return Booking.query.filter(
            Booking.chef_id == user_id,
            Booking.status == 'confirmed',
            Booking.event_date >= datetime.now().date()
        ).order_by(Booking.event_date).all()
```

## API Development

### Route Development
```python
@app.route('/api/chefs', methods=['GET'])
def api_get_chefs():
    """Get list of available chefs."""
    try:
        page = request.args.get('page', 1, type=int)
        cuisine = request.args.get('cuisine', '')
        rating_min = request.args.get('rating_min', type=float)
        
        query = ChefProfile.query.filter_by(is_available=True)
        
        if cuisine:
            query = query.filter(ChefProfile.specialties.contains(cuisine))
        
        if rating_min:
            query = query.filter(ChefProfile.rating >= rating_min)
        
        chefs = query.order_by(ChefProfile.rating.desc()).paginate(
            page=page, per_page=12, error_out=False
        )
        
        return jsonify({
            'chefs': [chef.to_dict() for chef in chefs.items],
            'pagination': {
                'page': chefs.page,
                'pages': chefs.pages,
                'per_page': chefs.per_page,
                'total': chefs.total
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Model Serialization
```python
# Add to model classes
def to_dict(self):
    """Convert model to dictionary."""
    return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'role': self.role,
        'created_at': self.created_at.isoformat() if self.created_at else None
    }
```

## Frontend Development

### Template Development
```html
<!-- templates/chefs/browse.html -->
{% extends "base.html" %}

{% block title %}Browse Chefs{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-3">
            <!-- Filters -->
            <div class="card">
                <div class="card-header">
                    <h5>Filters</h5>
                </div>
                <div class="card-body">
                    <form method="GET">
                        <div class="mb-3">
                            <label for="cuisine" class="form-label">Cuisine</label>
                            <select name="cuisine" id="cuisine" class="form-select">
                                <option value="">All Cuisines</option>
                                <option value="persian" {% if cuisine_filter == 'persian' %}selected{% endif %}>Persian</option>
                                <option value="italian" {% if cuisine_filter == 'italian' %}selected{% endif %}>Italian</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary">Apply Filters</button>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-9">
            <!-- Chef Grid -->
            <div class="row">
                {% for chef in chefs.items %}
                <div class="col-md-4 mb-4">
                    <div class="card chef-card">
                        <img src="{{ url_for('static', filename='uploads/profiles/' + chef.profile_photo) if chef.profile_photo else url_for('static', filename='images/default-chef.jpg') }}" class="card-img-top" alt="Chef Photo">
                        <div class="card-body">
                            <h5 class="card-title">{{ chef.user.first_name }} {{ chef.user.last_name }}</h5>
                            <p class="card-text">{{ chef.bio[:100] }}...</p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="badge bg-primary">${{ chef.base_price_per_person }}/person</span>
                                <span class="text-warning">★ {{ chef.rating }}</span>
                            </div>
                            <a href="{{ url_for('chef_detail', chef_id=chef.id) }}" class="btn btn-primary mt-2">View Profile</a>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Pagination -->
            {% if chefs.pages > 1 %}
            <nav aria-label="Chef pagination">
                <ul class="pagination justify-content-center">
                    {% if chefs.has_prev %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('browse_chefs', page=chefs.prev_num, cuisine=cuisine_filter) }}">Previous</a>
                    </li>
                    {% endif %}
                    
                    {% for page_num in chefs.iter_pages() %}
                    {% if page_num %}
                    <li class="page-item {% if page_num == chefs.page %}active{% endif %}">
                        <a class="page-link" href="{{ url_for('browse_chefs', page=page_num, cuisine=cuisine_filter) }}">{{ page_num }}</a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <span class="page-link">...</span>
                    </li>
                    {% endif %}
                    {% endfor %}
                    
                    {% if chefs.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="{{ url_for('browse_chefs', page=chefs.next_num, cuisine=cuisine_filter) }}">Next</a>
                    </li>
                    {% endif %}
                </ul>
            </nav>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

### JavaScript Development
```javascript
// static/js/chef-browse.js
class ChefBrowse {
    constructor() {
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadChefs();
    }
    
    bindEvents() {
        // Filter form submission
        document.getElementById('filter-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.applyFilters();
        });
        
        // Chef card clicks
        document.addEventListener('click', (e) => {
            if (e.target.closest('.chef-card')) {
                const chefId = e.target.closest('.chef-card').dataset.chefId;
                this.viewChefProfile(chefId);
            }
        });
    }
    
    async loadChefs(page = 1) {
        try {
            const response = await fetch(`/api/chefs?page=${page}`);
            const data = await response.json();
            this.renderChefs(data.chefs);
            this.renderPagination(data.pagination);
        } catch (error) {
            console.error('Error loading chefs:', error);
            this.showError('Failed to load chefs');
        }
    }
    
    renderChefs(chefs) {
        const container = document.getElementById('chef-grid');
        container.innerHTML = chefs.map(chef => this.createChefCard(chef)).join('');
    }
    
    createChefCard(chef) {
        return `
            <div class="col-md-4 mb-4">
                <div class="card chef-card" data-chef-id="${chef.id}">
                    <img src="${chef.profile_photo || '/static/images/default-chef.jpg'}" 
                         class="card-img-top" alt="Chef Photo">
                    <div class="card-body">
                        <h5 class="card-title">${chef.user.first_name} ${chef.user.last_name}</h5>
                        <p class="card-text">${chef.bio.substring(0, 100)}...</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-primary">$${chef.base_price_per_person}/person</span>
                            <span class="text-warning">★ ${chef.rating}</span>
                        </div>
                        <button class="btn btn-primary mt-2" onclick="viewChefProfile(${chef.id})">
                            View Profile
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.getElementById('alerts').appendChild(alert);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChefBrowse();
});
```

## Deployment

### Local Testing
```bash
# Run development server
python app.py

# Run tests
python -m pytest tests/

# Check code style
flake8 app.py
black app.py

# Check security
bandit -r app.py
```

### Production Deployment
```bash
# Install production dependencies
pip install gunicorn

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host:port/db

# Run database migrations
python migrate_production.py

# Start production server
gunicorn app:app
```

## Debugging

### Common Issues
1. **Database Connection Errors**
   - Check DATABASE_URL format
   - Verify database server is running
   - Check network connectivity

2. **Import Errors**
   - Verify virtual environment is activated
   - Check Python path
   - Ensure all dependencies are installed

3. **Template Errors**
   - Check template syntax
   - Verify template files exist
   - Check template inheritance

4. **Static File Issues**
   - Verify static file paths
   - Check file permissions
   - Ensure files exist in static directory

### Debug Tools
```python
# Add to app.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Debug route
@app.route('/debug')
def debug_info():
    return {
        'app_config': dict(app.config),
        'database_url': app.config.get('SQLALCHEMY_DATABASE_URI'),
        'debug_mode': app.debug,
        'environment': os.environ.get('FLASK_ENV')
    }
```

## Contributing

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Update documentation
7. Submit a pull request

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Error handling is proper

---

**Last Updated**: January 2024
**Version**: 1.0
