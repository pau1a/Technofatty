"""
Django settings for technofatty_com project.
Cleaned up for SCSS + Bootstrap, env-based secrets, and sane static handling.
"""
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured


# -------------------------------------------------
# Environment
# -------------------------------------------------
ENV = os.environ.get("ENV", "development").lower()
IS_PRODUCTION = ENV == "production"

# -------------------------------------------------
# Core
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


THUMBNAIL_ALIASES = {
    '': {
        'hero_desktop': {'size': (1920, 1080), 'crop': True},
        'hero_tablet': {'size': (1280, 720), 'crop': True},
        'hero_mobile': {'size': (640, 360), 'crop': True},
    },
}

# SECURITY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if IS_PRODUCTION:
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set in production")
    SECRET_KEY = "CHANGE_ME_DEV_ONLY"

# DEBUG automatically off in production
DEBUG = not IS_PRODUCTION

# Allowed hosts derive from environment; empty env var falls back to defaults
_default_hosts = (
    "technofatty.com,www.technofatty.com"
    if IS_PRODUCTION
    else "localhost,127.0.0.1,testserver"
)
_host_env = os.environ.get("DJANGO_ALLOWED_HOSTS")
host_source = _host_env if _host_env else _default_hosts
ALLOWED_HOSTS = [h.strip() for h in host_source.split(",") if h.strip()]
# -------------------------------------------------
# Applications
# -------------------------------------------------
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local app(s)
    "coresite",
    "newsletter",

    # Third-party
    "sass_processor",
    "compressor",
    'easy_thumbnails',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "technofatty_com.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Using app templates (coresite/templates/...)
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "coresite.context_processors.analytics_flags",
            ],
        },
    },
]

WSGI_APPLICATION = "technofatty_com.wsgi.application"

# -------------------------------------------------
# Database
# -------------------------------------------------
if IS_PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "technofatty"),
            "USER": os.environ.get("POSTGRES_USER", "technofatty"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
            "CONN_MAX_AGE": int(os.environ.get("POSTGRES_CONN_MAX_AGE", "60")),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# -------------------------------------------------
# Internationalization
# -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/London"   # matches your working timezone
USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# Static files / SCSS
# -------------------------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Where your working static assets live (JS, images, SCSS, etc.)
# You keep assets inside your app: coresite/static/coresite/...
STATICFILES_DIRS = []

# Where collectstatic will gather files for production serving (Nginx, etc.)
STATIC_ROOT = BASE_DIR / "static_collected"

# Hash filenames for cache-busting in prod (works fine with Nginx or any static server)
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# Let Django find compiled CSS from sass_processor
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
    "compressor.finders.CompressorFinder",
]

# django-sass-processor settings
# Root for SCSS source files (we’ve placed them under coresite/static/coresite/scss)
SASS_PROCESSOR_ROOT = BASE_DIR / "coresite" / "static"

# Allow @import "bootstrap/..." by including node_modules
SASS_PROCESSOR_INCLUDE_DIRS = [
    BASE_DIR / "node_modules",
]

# Optional: disable on-the-fly compilation in production for speed
SASS_PROCESSOR_ENABLED = not IS_PRODUCTION

# django-compressor: compile assets during build
COMPRESS_ENABLED = IS_PRODUCTION
COMPRESS_OFFLINE = IS_PRODUCTION

# -------------------------------------------------
# Security / CSRF
# -------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    f"https://{host}"
    for host in ALLOWED_HOSTS
    if host not in {"localhost", "127.0.0.1"}
]

# Additional security hardening for production
if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin"

# -------------------------------------------------
# Auto field
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------
# Newsletter settings
# -------------------------------------------------
NEWSLETTER_PROVIDER = os.environ.get("NEWSLETTER_PROVIDER", "stub")
OPT_IN_MODE = os.environ.get("OPT_IN_MODE", "single")
NEWSLETTER_TIMEOUT_SECONDS = int(os.environ.get("NEWSLETTER_TIMEOUT_SECONDS", "3"))
NEWSLETTER_RATE_LIMITS = {"ip_per_hour": 10, "email_per_hour": 5}

# -------------------------------------------------
# Analytics
# -------------------------------------------------
ANALYTICS_ENABLED = os.environ.get(
    "ANALYTICS_ENABLED", "true" if IS_PRODUCTION else "false"
).lower() == "true"
ANALYTICS_PROVIDER = os.environ.get("ANALYTICS_PROVIDER", "plausible")
ANALYTICS_SITE_ID = os.environ.get("ANALYTICS_SITE_ID", "")
CONSENT_REQUIRED = os.environ.get("CONSENT_REQUIRED", "true").lower() == "true"


# -------------------------------------------------
# Logging & error reporting
# -------------------------------------------------
def skip_static_requests(record):
    return "/static/" not in record.getMessage()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "skip_static": {
            "()": "django.utils.log.CallbackFilter",
            "callback": skip_static_requests,
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["skip_static"],
        }
    },
    "loggers": {
        "django.server": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN:
    try:
        import sentry_sdk

        sentry_sdk.init(dsn=SENTRY_DSN, environment=ENV)
    except Exception:
        pass
