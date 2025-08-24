"""
Django settings for technofatty_com project.
Cleaned up for SCSS + Bootstrap, env-based secrets, and sane static handling.
"""
from pathlib import Path
import os
import subprocess
from datetime import datetime, timezone

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
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "CHANGE_ME_DEV_ONLY")
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() == "true"
#DEBUG = False

# Application environment (development, production, etc.)
ENV = os.environ.get("ENV", "development")

# Build metadata injected at deploy time
# Falls back to local git values when running in DEBUG

_raw_branch = os.environ.get("TF_BUILD_BRANCH") or os.environ.get("BUILD_BRANCH", "")
_raw_commit = os.environ.get("TF_BUILD_COMMIT") or os.environ.get("BUILD_COMMIT", "")
BUILD_DATETIME = os.environ.get("TF_BUILD_DATETIME") or os.environ.get("BUILD_DATETIME", "")

if DEBUG and not _raw_branch:
    try:
        _raw_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        _raw_branch = ""

if DEBUG and not _raw_commit:
    try:
        _raw_commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        _raw_commit = ""

if DEBUG and not BUILD_DATETIME:
    BUILD_DATETIME = datetime.now(timezone.utc).isoformat(timespec="seconds")

BUILD_BRANCH = _raw_branch.rsplit("/", 1)[-1] if _raw_branch else ""
BUILD_COMMIT = _raw_commit[:7] if _raw_commit else ""

def _truthy(env_value: str) -> bool:
    return env_value.lower() in {"true", "1", "yes"}

# Allow deployments to toggle the banner while keeping it off in production
SHOW_BUILD_BANNER = _truthy(os.environ.get("TF_SHOW_BUILD_BANNER", "")) and ENV != "production"

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "technofatty.com,www.technofatty.com,localhost,127.0.0.1"
).split(",")

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
                "coresite.context_processors.build_metadata",
            ],
        },
    },
]

WSGI_APPLICATION = "technofatty_com.wsgi.application"

# -------------------------------------------------
# Database
# -------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "technofatty"),
        "USER": os.environ.get("POSTGRES_USER", "technofatty"),
        "PASSWORD": "friskywhisky",
        "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": int(os.environ.get("POSTGRES_CONN_MAX_AGE", "60")),
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
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Where your working static assets live (JS, images, SCSS, etc.)
# You keep assets inside your app: coresite/static/coresite/...
STATICFILES_DIRS = []

# Where collectstatic will gather files for production serving (Nginx, etc.)
STATIC_ROOT = Path("/var/www/technofatty_com/static")

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
SASS_PROCESSOR_ENABLED = DEBUG

# -------------------------------------------------
# Security / CSRF
# -------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    "https://technofatty.com",
    "https://www.technofatty.com",
]

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
ANALYTICS_ENABLED = os.environ.get("ANALYTICS_ENABLED", "false").lower() == "true"
ANALYTICS_PROVIDER = os.environ.get("ANALYTICS_PROVIDER", "plausible")
ANALYTICS_SITE_ID = os.environ.get("ANALYTICS_SITE_ID", "")
CONSENT_REQUIRED = os.environ.get("CONSENT_REQUIRED", "true").lower() == "true"
