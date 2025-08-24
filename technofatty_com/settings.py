"""
Django settings for technofatty_com project.
Cleaned up for SCSS + Bootstrap, env-based secrets, and sane static handling.
"""
from pathlib import Path
import os
import subprocess
from datetime import datetime, timezone
from typing import List

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

# ------------------------------------------------------------------
# Build metadata sourced from git or CI-provided environment vars
# ------------------------------------------------------------------
REPO_DIR = Path(os.environ.get("TF_REPO_DIR", BASE_DIR)).resolve()


def _git_out(args: List[str]) -> str:
    """Return git command output, or an empty string on failure."""
    try:
        return subprocess.check_output(["git", "-C", str(REPO_DIR), *args], text=True).strip()
    except Exception:
        return ""


_raw_branch = os.environ.get("TF_BUILD_BRANCH") or _git_out(["rev-parse", "--abbrev-ref", "HEAD"])
_raw_commit = os.environ.get("TF_BUILD_COMMIT") or _git_out(["rev-parse", "HEAD"])
_build_dt = (
    os.environ.get("TF_BUILD_DATETIME")
    or _git_out(["show", "-s", "--format=%cI"])
    or datetime.now(timezone.utc).isoformat()
)

BUILD_BRANCH = (_raw_branch or "").rsplit("/", 1)[-1]
BUILD_COMMIT = (_raw_commit or "")[:7]
BUILD_DATETIME = _build_dt
SHOW_BUILD_BANNER = True

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
