"""
Django settings for FoodFlow project.
FoodFlow is an expiry-aware food donation platform connecting donors and recipients.
"""

import os
import tempfile
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Detect Vercel serverless environment
IS_VERCEL = 'VERCEL' in os.environ or os.environ.get('VERCEL_ENV') is not None

# SECURITY WARNING: keep the secret key used in production secret!
_secret_key = os.environ.get('SECRET_KEY')
_insecure_default = 'django-insecure-foodflow-university-cse-lab-secret-key-2026'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

if not _secret_key:
    if DEBUG:
        SECRET_KEY = _insecure_default
    else:
        raise ImproperlyConfigured(
            "CRITICAL: The SECRET_KEY environment variable must be set in production and cannot be empty."
        )
else:
    if not DEBUG and _secret_key == _insecure_default:
        raise ImproperlyConfigured(
            "CRITICAL: The known insecure default SECRET_KEY cannot be used in production. "
            "Please provide a unique, cryptographically random SECRET_KEY in your environment."
        )
    SECRET_KEY = _secret_key

# Allow Vercel, localhost, and custom domains
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS')
if allowed_hosts_env:
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]
elif DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [
        '.vercel.app',
        'food-flow-web.vercel.app',
        'localhost',
        '127.0.0.1',
    ]

# Security and CSRF settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ('true', '1', 'yes')
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 31536000))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = 'same-origin'

csrf_origins_env = os.environ.get('CSRF_TRUSTED_ORIGINS')
if csrf_origins_env:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins_env.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://*.vercel.app',
        'https://food-flow-web.vercel.app',
        'http://127.0.0.1:8000',
        'http://localhost:8000',
    ]

# Session and Cookie Configuration
# Default to database-backed sessions for maximum tamper-resistance and server-side revocation.
SESSION_ENGINE = os.environ.get('DJANGO_SESSION_ENGINE', 'django.contrib.sessions.backends.db')
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG  # True in production HTTPS, False in local development
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False  # Allows JS CSRF token reads if needed

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # FoodFlow Applications
    'accounts.apps.AccountsConfig',
    'locations.apps.LocationsConfig',
    'listings.apps.ListingsConfig',
    'claims.apps.ClaimsConfig',
    'notifications.apps.NotificationsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise for serving static files on Vercel
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.views.unread_notification_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database configuration
# 1. If DATABASE_URL is configured (e.g. Neon PostgreSQL), connect persistently
# 2. If running on Vercel without DATABASE_URL, fallback to /tmp/db.sqlite3
# 3. For local development, use db.sqlite3
database_url = os.environ.get('DATABASE_URL')

if database_url:
    DATABASES = {
        'default': dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
elif IS_VERCEL:
    if not DEBUG:
        raise ImproperlyConfigured(
            "Production deployment on Vercel requires DATABASE_URL to connect to a persistent database (e.g. PostgreSQL/Neon). Ephemeral SQLite in /tmp will lose all records between requests."
        )
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(tempfile.gettempdir(), 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation suite (OWASP / Django Standard)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization and Timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise storage configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Email configuration (defaults to console output in development)
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@foodflow.local')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# FoodFlow specific business logic settings (simplified for lab project)
FOODFLOW_SETTINGS = {
    'PICKUP_WINDOW_MINUTES': 90,
    'MIN_EXPIRY_MINUTES': 30,
    'MAX_EXPIRY_HOURS': 72,
}
# Uploaded food photos
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
SERVE_MEDIA_IN_PROD = os.environ.get('SERVE_MEDIA_IN_PROD', 'False').lower() in ('true', '1')