import os
from pathlib import Path
import environ


env = environ.Env()
environ.Env.read_env()

DEBUG = env.bool('DEBUG', default=False)
PRODUCTION = not DEBUG

if PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000 
else:
    SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
    SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)
    CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)
    SECURE_HSTS_SECONDS = 300
if PRODUCTION:
    ALLOWED_HOSTS = [
        'yourdomain.com',
        'www.yourdomain.com',
        'api.yourdomain.com',
    ]
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = env('SECRET_KEY', default='your-production-secret-key-change-this-in-production')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'csp',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True


CSRF_COOKIE_SECURE = not DEBUG  
SESSION_COOKIE_SECURE = not DEBUG  
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True


CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'" if DEBUG else "'self'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'" if DEBUG else "'self'")
CSP_IMG_SRC = ("'self'", "data:")
CSP_FONT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True 
CSRF_COOKIE_HTTPONLY = False

X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_REFERRER_POLICY = 'same-origin'

SECURE_REDIRECT_EXEMPT = []

SECURE_SSL_REDIRECT = not DEBUG

# ... rest of your settings

