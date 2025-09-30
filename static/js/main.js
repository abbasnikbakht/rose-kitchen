// Chef Marketplace JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Image lazy loading
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }

    // Filter functionality
    const filterForm = document.querySelector('form[method="GET"]');
    if (filterForm) {
        const filterInputs = filterForm.querySelectorAll('input, select');
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Auto-submit form when filters change
                filterForm.submit();
            });
        });
    }

    // Chef card interactions
    document.querySelectorAll('.chef-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Booking form enhancements
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        const guestCountInput = bookingForm.querySelector('input[name="guest_count"]');
        const priceDisplay = document.getElementById('priceDisplay');
        
        if (guestCountInput && priceDisplay) {
            guestCountInput.addEventListener('input', function() {
                updatePriceDisplay(this.value);
            });
        }
    }

    // Review form star rating
    document.querySelectorAll('.star-rating').forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                setRating(rating, index + 1);
            });
            
            star.addEventListener('mouseenter', function() {
                highlightStars(rating, index + 1);
            });
        });
        
        rating.addEventListener('mouseleave', function() {
            const currentRating = rating.dataset.rating || 0;
            highlightStars(rating, currentRating);
        });
    });

    // Modal enhancements
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            // Focus first input in modal
            const firstInput = this.querySelector('input, textarea, select');
            if (firstInput) {
                firstInput.focus();
            }
        });
    });

    // File upload preview
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById(this.dataset.preview);
                    if (preview) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Infinite scroll for chef listings
    const chefContainer = document.getElementById('chefContainer');
    if (chefContainer) {
        let page = 2;
        let loading = false;
        
        window.addEventListener('scroll', function() {
            if (loading) return;
            
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 1000) {
                loading = true;
                loadMoreChefs(page);
                page++;
            }
        });
    }

    // Notification system
    window.showNotification = function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(notification);
            bsAlert.close();
        }, 5000);
    };

    // Share functionality
    window.shareContent = function(title, text, url) {
        if (navigator.share) {
            navigator.share({
                title: title,
                text: text,
                url: url
            });
        } else {
            // Fallback: copy to clipboard
            navigator.clipboard.writeText(url).then(() => {
                showNotification('Link copied to clipboard!', 'success');
            });
        }
    };

    // Calendar functionality
    const calendarInputs = document.querySelectorAll('input[type="date"]');
    calendarInputs.forEach(input => {
        // Set minimum date to today
        input.min = new Date().toISOString().split('T')[0];
        
        // Set maximum date to 1 year from now
        const maxDate = new Date();
        maxDate.setFullYear(maxDate.getFullYear() + 1);
        input.max = maxDate.toISOString().split('T')[0];
    });

    // Price calculator
    window.calculatePrice = function(basePrice, guestCount, travelFee = 0) {
        const subtotal = basePrice * guestCount;
        const serviceFee = subtotal * 0.1; // 10%
        const platformFee = subtotal * 0.15; // 15%
        const total = subtotal + travelFee + serviceFee + platformFee;
        
        return {
            subtotal: subtotal,
            travelFee: travelFee,
            serviceFee: serviceFee,
            platformFee: platformFee,
            total: total
        };
    };

    // Update price display
    window.updatePriceDisplay = function(guestCount) {
        const basePrice = parseFloat(document.getElementById('basePrice').textContent) || 0;
        const travelFee = parseFloat(document.getElementById('travelFee').textContent) || 0;
        
        const pricing = calculatePrice(basePrice, guestCount, travelFee);
        
        document.getElementById('subtotal').textContent = pricing.subtotal.toFixed(2);
        document.getElementById('serviceFee').textContent = pricing.serviceFee.toFixed(2);
        document.getElementById('platformFee').textContent = pricing.platformFee.toFixed(2);
        document.getElementById('totalPrice').textContent = pricing.total.toFixed(2);
    };

    // Star rating functions
    window.setRating = function(ratingContainer, rating) {
        ratingContainer.dataset.rating = rating;
        const stars = ratingContainer.querySelectorAll('.star');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
            } else {
                star.classList.remove('active');
            }
        });
        
        // Update hidden input if exists
        const hiddenInput = ratingContainer.querySelector('input[type="hidden"]');
        if (hiddenInput) {
            hiddenInput.value = rating;
        }
    };

    window.highlightStars = function(ratingContainer, rating) {
        const stars = ratingContainer.querySelectorAll('.star');
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('highlight');
            } else {
                star.classList.remove('highlight');
            }
        });
    };

    // Search function
    window.performSearch = function(query) {
        if (query.length < 2) return;
        
        // This would typically make an AJAX request to search endpoint
        console.log('Searching for:', query);
        
        // For now, just filter visible elements
        const chefCards = document.querySelectorAll('.chef-card');
        chefCards.forEach(card => {
            const text = card.textContent.toLowerCase();
            if (text.includes(query.toLowerCase())) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    };

    // Load more chefs function
    window.loadMoreChefs = function(page) {
        // This would typically make an AJAX request
        console.log('Loading page:', page);
        
        // Simulate loading
        setTimeout(() => {
            loading = false;
        }, 1000);
    };

    // Initialize animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.chef-card, .feature-card, .review-card').forEach(card => {
        observer.observe(card);
    });
});

// Utility functions
window.formatCurrency = function(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
};

window.formatDate = function(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

window.formatTime = function(timeString) {
    return new Date('2000-01-01T' + timeString).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
};

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // You could send this to an error tracking service
});

// Service Worker registration (for PWA features)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}
