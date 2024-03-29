import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.mail.backends import smtp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "t&smw7s7s%afux0t8=z%11vz0z)crst@dk64z4v1elg!mwf6-j"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_extensions",
    "mathfilters",
    "crispy_forms",
    "django.contrib.sites",
    "bookshop.apps.BookshopConfig",
    "bootstrap4",
    "bootstrap_datepicker_plus",
    "ckeditor",
    "ckeditor_uploader",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django_countries",
    # "allauth.socialaccount.providers.facebook",
    'social_django',

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

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    'social_core.backends.facebook.FacebookOAuth2',
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "bookshop.context_processors.market",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


CRISPY_TEMPLATE_PACK = "bootstrap4"

SITE_ID = 1

# STATICFIELS_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
#
# )

# MEDIA_URL = '/media/'
#
# MEDIA_ROOT = os.path.join(BASE_DIR,'media/users/2020/')

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
#     os.path.join(BASE_DIR, 'static_files'),
#
# ]


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

CKEDITOR_UPLOAD_PATH = "content/ckeditor/"

CKEDITOR_FILENAME_GENERATOR = "utils.get_filename"


def get_filename(filename):
    return filename.upper()


ALLOW_UNICODE_SLUGS = True

POPUPCRUD = {
    "base_template": "mybase.html",
}

CRISPY_TEMPLATE_PACK = "bootstrap4"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "ranafge@gmail.com"
EMAIL_HOST_PASSWORD = "Ayesha9911@"

LOGIN_REDIRECT_URL = "/"

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

SOCIAL_AUTH_FACEBOOK_KEY = '383444829442344' # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '45d6b93e1298803dd823c9541ebf175e' # Facebook App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']