from pathlib import Path

from django.contrib.messages import constants
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(env_file=BASE_DIR / ".env", overwrite=True)

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Project apps
    "home",
    "users",
    "chat",
    # django-cleanup
    "django_cleanup",
    # django-tailwind
    "tailwind",
    "theme",
    # django-allauth
    "allauth",
    "allauth.account",
    # heroicons
    "heroicons",
    # django-htmx
    "django_htmx",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # django-allauth
    "allauth.account.middleware.AccountMiddleware",
    # django-htmx
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "global" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.theme",
            ],
            "libraries": {
                "message_tags": "core.templatetags.message_tags",
            },
        },
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # django-allauth
    "allauth.account.auth_backends.AuthenticationBackend",
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {"default": env.db_url()}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Fortaleza"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "global" / "static",
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG:
    INSTALLED_APPS.append("django_browser_reload")
    MIDDLEWARE.append("django_browser_reload.middleware.BrowserReloadMiddleware")

TAILWIND_APP_NAME = "theme"

MESSAGE_TAGS = {
    constants.INFO: "alert-info",
    constants.SUCCESS: "alert-success",
    constants.WARNING: "alert-warning",
    constants.ERROR: "alert-error",
}

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# django-allauth settings
ACCOUNT_FORMS = {
    "login": "users.forms.LoginForm",
    "signup": "users.forms.SignupForm",
    "reset_password": "users.forms.ResetPasswordForm",
    "reset_password_from_key": "users.forms.ResetPasswordKeyForm",
    "change_password": "users.forms.ChangePasswordForm",
    "add_email": "users.forms.AddEmailForm",
}
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*"]
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[ProseiAê!] "
ACCOUNT_EMAIL_NOTIFICATIONS = True
ACCOUNT_CHANGE_EMAIL = True
