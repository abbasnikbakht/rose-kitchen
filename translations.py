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
        'create_cook_profile': 'Create Cook Profile',
        
        # Additional missing translations
        'find_cooks': 'Find Cooks',
        'sign_up': 'Sign Up',
        'why_choose': 'Why Choose',
        'authentic_persian_chefs': 'Authentic Persian Chefs',
        'authentic_persian_chefs_desc': 'Our chefs are masters of traditional Iranian cuisine, trained in the art of Persian cooking with authentic recipes passed down through generations.',
        'fresh_ingredients': 'Fresh Ingredients',
        'fresh_ingredients_desc': 'We use only the freshest, highest quality ingredients sourced from local markets and specialty Persian food suppliers.',
        'professional_service': 'Professional Service',
        'professional_service_desc': 'From booking to cleanup, our professional chefs provide exceptional service with attention to detail and cultural authenticity.',
        'featured_chefs': 'Featured Chefs',
        'featured_chefs_desc': 'Meet our talented Persian chefs, each specializing in different regional cuisines of Iran.',
        'view_all_chefs': 'View All Chefs',
        'get_started': 'Get Started',
        'get_started_desc': 'Ready to experience authentic Persian cuisine? Book a chef today and bring the flavors of Iran to your home.',
        'book_your_chef': 'Book Your Chef',
        'learn_more': 'Learn More',
        'traditional_persian_experience': 'Traditional Persian Experience',
        'traditional_persian_experience_desc': 'Experience the warmth of Persian hospitality in your own home with traditional cooking methods and authentic ingredients.',
        'easy_booking': 'Easy Booking',
        'easy_booking_desc': 'Simple and secure booking process. Choose your Persian chef, set your date, and enjoy an authentic Iranian culinary experience.',
        'years_experience': 'years experience',
        'view_profile': 'View Profile',
        'book_now': 'Book Now',
        'specialties': 'Specialties',
        'hourly_rate': 'Hourly Rate',
        'get_started_today': 'Get Started Today',
        'get_started_today_desc': 'Ready to experience authentic Persian cuisine? Book a chef today and bring the flavors of Iran to your home.',
        'how_it_works': 'How It Works',
        'how_it_works_desc': 'Experience authentic Persian cuisine in just a few simple steps',
        'browse_persian_chefs': 'Browse Persian Chefs',
        'browse_persian_chefs_desc': 'Search through our network of authentic Iranian chefs, read their profiles, specialties, and reviews.',
        'book_your_persian_chef': 'Book Your Persian Chef',
        'book_your_persian_chef_desc': 'Select your preferred Iranian chef, choose your event date and time, and specify your favorite Persian dishes.',
        'enjoy_authentic_cuisine': 'Enjoy Authentic Cuisine',
        'enjoy_authentic_cuisine_desc': 'Sit back and enjoy a delicious Persian meal prepared by your professional Iranian chef in the comfort of your home.',
        'ready_to_experience': 'Ready to Experience Persian Cuisine?',
        'ready_to_experience_desc': 'Join thousands of satisfied customers who have discovered the authentic flavors of Iran in their own homes.',
        'sign_up_now': 'Sign Up Now'
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
        'create_cook_profile': 'ایجاد پروفایل آشپز',
        
        # Additional missing translations
        'find_cooks': 'پیدا کردن آشپزها',
        'sign_up': 'ثبت نام',
        'why_choose': 'چرا انتخاب کنید',
        'authentic_persian_chefs': 'آشپزهای اصیل ایرانی',
        'authentic_persian_chefs_desc': 'آشپزهای ما استادان آشپزی سنتی ایرانی هستند که در هنر آشپزی فارسی با دستورهای اصیل که از نسل‌ها به ارث رسیده آموزش دیده‌اند.',
        'fresh_ingredients': 'مواد اولیه تازه',
        'fresh_ingredients_desc': 'ما فقط از تازه‌ترین و باکیفیت‌ترین مواد اولیه که از بازارهای محلی و تأمین‌کنندگان تخصصی غذاهای ایرانی تهیه می‌شود استفاده می‌کنیم.',
        'professional_service': 'خدمات حرفه‌ای',
        'professional_service_desc': 'از رزرو تا نظافت، آشپزهای حرفه‌ای ما خدمات استثنایی با توجه به جزئیات و اصالت فرهنگی ارائه می‌دهند.',
        'featured_chefs': 'آشپزهای برجسته',
        'featured_chefs_desc': 'با آشپزهای بااستعداد ایرانی ما آشنا شوید که هر کدام در آشپزی منطقه‌ای مختلف ایران تخصص دارند.',
        'view_all_chefs': 'مشاهده همه آشپزها',
        'get_started': 'شروع کنید',
        'get_started_desc': 'آماده تجربه آشپزی اصیل ایرانی هستید؟ امروز یک آشپز رزرو کنید و طعم‌های ایران را به خانه خود بیاورید.',
        'book_your_chef': 'آشپز خود را رزرو کنید',
        'learn_more': 'بیشتر بدانید',
        'traditional_persian_experience': 'تجربه سنتی ایرانی',
        'traditional_persian_experience_desc': 'گرمای مهمان‌نوازی ایرانی را در خانه خود با روش‌های آشپزی سنتی و مواد اولیه اصیل تجربه کنید.',
        'easy_booking': 'رزرو آسان',
        'easy_booking_desc': 'فرآیند رزرو ساده و امن. آشپز ایرانی خود را انتخاب کنید، تاریخ خود را تنظیم کنید و از تجربه آشپزی اصیل ایرانی لذت ببرید.',
        'years_experience': 'سال تجربه',
        'view_profile': 'مشاهده پروفایل',
        'book_now': 'رزرو کنید',
        'specialties': 'تخصص‌ها',
        'hourly_rate': 'نرخ ساعتی',
        'get_started_today': 'امروز شروع کنید',
        'get_started_today_desc': 'آماده تجربه آشپزی اصیل ایرانی هستید؟ امروز یک آشپز رزرو کنید و طعم‌های ایران را به خانه خود بیاورید.',
        'how_it_works': 'چگونه کار می‌کند',
        'how_it_works_desc': 'در چند قدم ساده آشپزی اصیل ایرانی را تجربه کنید',
        'browse_persian_chefs': 'مرور آشپزهای ایرانی',
        'browse_persian_chefs_desc': 'از شبکه آشپزهای اصیل ایرانی ما جستجو کنید، پروفایل‌ها، تخصص‌ها و نظرات آن‌ها را بخوانید.',
        'book_your_persian_chef': 'آشپز ایرانی خود را رزرو کنید',
        'book_your_persian_chef_desc': 'آشپز ایرانی مورد نظر خود را انتخاب کنید، تاریخ و زمان رویداد خود را انتخاب کنید و غذاهای ایرانی مورد علاقه خود را مشخص کنید.',
        'enjoy_authentic_cuisine': 'از آشپزی اصیل لذت ببرید',
        'enjoy_authentic_cuisine_desc': 'بنشینید و از یک وعده غذایی خوشمزه ایرانی که توسط آشپز حرفه‌ای ایرانی شما در راحتی خانه شما تهیه شده لذت ببرید.',
        'ready_to_experience': 'آماده تجربه آشپزی ایرانی هستید؟',
        'ready_to_experience_desc': 'به هزاران مشتری راضی بپیوندید که طعم‌های اصیل ایران را در خانه خود کشف کرده‌اند.',
        'sign_up_now': 'الان ثبت نام کنید'
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
