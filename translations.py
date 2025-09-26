# -*- coding: utf-8 -*-
"""
Translation system for گل سرخ Rose Kitchen
Supports English and Farsi (Persian) languages
"""

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Navigation
        'home': 'Home',
        'cooks': 'Chefs',
        'book': 'Book',
        'dashboard': 'Dashboard',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'profile': 'Profile',
        
        # App title and branding
        'app_title': 'Rose Kitchen',
        'app_subtitle': 'Authentic Persian Cuisine at Your Doorstep',
        'welcome_message': 'Welcome to Rose Kitchen',
        'tagline': 'Experience the rich flavors of Persian cuisine with our professional chefs',
        
        # Cuisine types
        'tehran_cuisine': 'Tehran Cuisine',
        'isfahan_cuisine': 'Isfahan Cuisine', 
        'shiraz_cuisine': 'Shiraz Cuisine',
        'traditional_iranian': 'Traditional Iranian',
        'halal_cuisine': 'Halal Cuisine',
        
        # Chef names
        'chef_rose': 'Rose Ahmadi',
        'chef_soheila': 'Soheila Nouri',
        'chef_halal': 'Halal Kazemi',
        'chef_iran': 'Iran Mohammadi',
        
        # Forms
        'username': 'Username',
        'email': 'Email',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'phone': 'Phone',
        'address': 'Address',
        'bio': 'Bio',
        'specialties': 'Specialties',
        'hourly_rate': 'Hourly Rate',
        'is_available': 'Available',
        
        # Actions
        'book_now': 'Book Now',
        'view_profile': 'View Profile',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'save': 'Save',
        'edit': 'Edit',
        'delete': 'Delete',
        'confirm': 'Confirm',
        
        # Messages
        'registration_success': 'Registration successful! Please log in.',
        'login_success': 'Login successful!',
        'logout_success': 'You have been logged out.',
        'booking_success': 'Booking created successfully!',
        'profile_updated': 'Profile updated successfully!',
        'error_occurred': 'An error occurred. Please try again.',
        'invalid_credentials': 'Invalid username or password.',
        'user_exists': 'Username or email already exists.',
        'passwords_dont_match': 'Passwords do not match.',
        
        # Booking
        'select_date': 'Select Date',
        'select_time': 'Select Time',
        'number_of_guests': 'Number of Guests',
        'special_requests': 'Special Requests',
        'booking_status': 'Booking Status',
        'pending': 'Pending',
        'confirmed': 'Confirmed',
        'completed': 'Completed',
        'cancelled': 'Cancelled',
        
        # Reviews
        'rating': 'Rating',
        'comment': 'Comment',
        'write_review': 'Write Review',
        'reviews': 'Reviews',
        'no_reviews': 'No reviews yet',
        
        # Dashboard
        'my_bookings': 'My Bookings',
        'my_profile': 'My Profile',
        'upcoming_bookings': 'Upcoming Bookings',
        'past_bookings': 'Past Bookings',
        'total_bookings': 'Total Bookings',
        'average_rating': 'Average Rating',
        
        # Persian dishes
        'ghormeh_sabzi': 'Ghormeh Sabzi',
        'fesenjan': 'Fesenjan',
        'tahdig': 'Tahdig',
        'beryani': 'Beryani',
        'khoresh_bademjan': 'Khoresh Bademjan',
        'ash_reshteh': 'Ash Reshteh',
        'kalam_polo': 'Kalam Polo',
        'khoresh_gheimeh': 'Khoresh Gheimeh',
        'faloodeh': 'Faloodeh',
        'chelo_kebab': 'Chelo Kebab',
        'baghali_polo': 'Baghali Polo',
        'sholeh_zard': 'Sholeh Zard',
        
        # Cities
        'tehran': 'Tehran',
        'isfahan': 'Isfahan',
        'shiraz': 'Shiraz',
        'iran': 'Iran',
        
        # Language
        'language': 'Language',
        'english': 'English',
        'farsi': 'فارسی',
        'switch_language': 'Switch Language',
        'create_cook_profile': 'Create Cook Profile'
    },
    
    'fa': {
        # Navigation
        'home': 'خانه',
        'cooks': 'آشپزها',
        'book': 'رزرو',
        'dashboard': 'داشبورد',
        'login': 'ورود',
        'register': 'ثبت نام',
        'logout': 'خروج',
        'profile': 'پروفایل',
        
        # App title and branding
        'app_title': 'گل سرخ',
        'app_subtitle': 'غذای اصیل ایرانی در خانه شما',
        'welcome_message': 'به گل سرخ خوش آمدید',
        'tagline': 'طعم غنی آشپزی ایرانی را با آشپزهای حرفه‌ای ما تجربه کنید',
        
        # Cuisine types
        'tehran_cuisine': 'آشپزی تهران',
        'isfahan_cuisine': 'آشپزی اصفهان',
        'shiraz_cuisine': 'آشپزی شیراز',
        'traditional_iranian': 'ایرانی سنتی',
        'halal_cuisine': 'حلال',
        
        # Chef names
        'chef_rose': 'رز احمدی',
        'chef_soheila': 'سهیلا نوری',
        'chef_halal': 'حلال کاظمی',
        'chef_iran': 'ایران محمدی',
        
        # Forms
        'username': 'نام کاربری',
        'email': 'ایمیل',
        'password': 'رمز عبور',
        'confirm_password': 'تأیید رمز عبور',
        'first_name': 'نام',
        'last_name': 'نام خانوادگی',
        'phone': 'تلفن',
        'address': 'آدرس',
        'bio': 'بیوگرافی',
        'specialties': 'تخصص‌ها',
        'hourly_rate': 'نرخ ساعتی',
        'is_available': 'در دسترس',
        
        # Actions
        'book_now': 'رزرو کنید',
        'view_profile': 'مشاهده پروفایل',
        'submit': 'ارسال',
        'cancel': 'لغو',
        'save': 'ذخیره',
        'edit': 'ویرایش',
        'delete': 'حذف',
        'confirm': 'تأیید',
        
        # Messages
        'registration_success': 'ثبت نام موفقیت‌آمیز بود! لطفاً وارد شوید.',
        'login_success': 'ورود موفقیت‌آمیز بود!',
        'logout_success': 'شما با موفقیت خارج شدید.',
        'booking_success': 'رزرو با موفقیت ایجاد شد!',
        'profile_updated': 'پروفایل با موفقیت به‌روزرسانی شد!',
        'error_occurred': 'خطایی رخ داد. لطفاً دوباره تلاش کنید.',
        'invalid_credentials': 'نام کاربری یا رمز عبور اشتباه است.',
        'user_exists': 'نام کاربری یا ایمیل قبلاً وجود دارد.',
        'passwords_dont_match': 'رمزهای عبور مطابقت ندارند.',
        
        # Booking
        'select_date': 'انتخاب تاریخ',
        'select_time': 'انتخاب زمان',
        'number_of_guests': 'تعداد مهمانان',
        'special_requests': 'درخواست‌های ویژه',
        'booking_status': 'وضعیت رزرو',
        'pending': 'در انتظار',
        'confirmed': 'تأیید شده',
        'completed': 'تکمیل شده',
        'cancelled': 'لغو شده',
        
        # Reviews
        'rating': 'امتیاز',
        'comment': 'نظر',
        'write_review': 'نوشتن نظر',
        'reviews': 'نظرات',
        'no_reviews': 'هنوز نظری وجود ندارد',
        
        # Dashboard
        'my_bookings': 'رزروهای من',
        'my_profile': 'پروفایل من',
        'upcoming_bookings': 'رزروهای آینده',
        'past_bookings': 'رزروهای گذشته',
        'total_bookings': 'کل رزروها',
        'average_rating': 'میانگین امتیاز',
        
        # Persian dishes
        'ghormeh_sabzi': 'قورمه سبزی',
        'fesenjan': 'فسنجان',
        'tahdig': 'ته دیگ',
        'beryani': 'بریانی',
        'khoresh_bademjan': 'خورش بادمجان',
        'ash_reshteh': 'آش رشته',
        'kalam_polo': 'کلم پلو',
        'khoresh_gheimeh': 'خورش قیمه',
        'faloodeh': 'فالوده',
        'chelo_kebab': 'چلو کباب',
        'baghali_polo': 'باقالی پلو',
        'sholeh_zard': 'شله زرد',
        
        # Cities
        'tehran': 'تهران',
        'isfahan': 'اصفهان',
        'shiraz': 'شیراز',
        'iran': 'ایران',
        
        # Language
        'language': 'زبان',
        'english': 'English',
        'farsi': 'فارسی',
        'switch_language': 'تغییر زبان',
        'create_cook_profile': 'ایجاد پروفایل آشپز'
    }
}

def get_translation(key, language='en'):
    """Get translation for a key in the specified language"""
    return TRANSLATIONS.get(language, {}).get(key, key)

def get_available_languages():
    """Get list of available languages"""
    return list(TRANSLATIONS.keys())

def is_rtl_language(language):
    """Check if language is right-to-left"""
    return language == 'fa'
