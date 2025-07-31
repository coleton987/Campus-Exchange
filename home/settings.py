import os
from pathlib import Path
from decouple import config

# -----------------------------------------------
# Base Directory
# -----------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------
# Security
# -----------------------------------------------
# Keep the secret key out of version control
SECRET_KEY = config('SECRET_KEY')

# Turn off debug mode in production
DEBUG = config('DEBUG', default=True, cast=bool)

# Define allowed hosts (comma-separated in .env)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [h.strip() for h in v.split(',') if h])

# Trusted origins for CSRF (add your domains here)
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=lambda v: [u.strip() for u in v.split(',') if u])

# -----------------------------------------------
# Application Definition
# -----------------------------------------------
INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'cloudinary',
    'cloudinary_storage',
    'whitenoise.runserver_nostatic',

    # Local apps
    'home',
    'image_uploader_widget',
    'listings',
    'messaging',

    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files efficiently
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'home' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'home.wsgi.application'
AUTH_USER_MODEL = 'users.CustomUser'  # Custom user model

# -----------------------------------------------
# Database
# -----------------------------------------------
# Using SQLite for development; override via DATABASE_URL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------------------
# Cloudinary for Media Storage
# -----------------------------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

import cloudinary

cloudinary.config( 
    cloud_name=config('CLOUDINARY_CLOUD_NAME'), 
    api_key=config('CLOUDINARY_API_KEY'), 
    api_secret=config('CLOUDINARY_API_SECRET') 
)

# -----------------------------------------------
# Static Files (CSS, JavaScript, Images)
# -----------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# WhiteNoise compresses and caches static assets
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -----------------------------------------------
# Internationalization
# -----------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -----------------------------------------------
# Third-Party API Keys
# -----------------------------------------------
# Tell Django to use SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Sendinblue SMTP relay
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('SENDINBLUE_SMTP_USER', default='')
EMAIL_HOST_PASSWORD = config('SENDINBLUE_SMTP_PASS', default='')
EMAIL_API_KEY = config('SENDINBLUE_API_KEY', default='')
EMAIL_USE_TLS = True

# Default “from” address for all outgoing mail
DEFAULT_FROM_EMAIL = 'campusexchange.bju@gmail.com'

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')

# -----------------------------------------------
# Default Primary Key Field Type
# -----------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'