"""
Django settings for MightyHive project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import mysql_settings
from django.contrib import messages
from configurations import Configuration, values


class Common(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    # jyp ALLOWED_HOSTS = values.ListValue([])

    ALLOWED_HOSTS = ['*']

    LOGIN_URL = 'login'

    # Application definition
    INSTALLED_APPS = [
        #django apps
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',
        #third apps
        'django_extensions',
        'debug_toolbar',
        'django_task',
        
        #locals app
        'scraper',
        'tasks',

        'apps.main',
        'apps.main.Crawlers',
        'apps.users',
        'apps.paradise',

        # 'coupangcrawling',
        'crawling',
        #glowpictest
        'glowpick',


        # 분활
        'dashboardapp',
        'rankingapp',
        'reviewapp',
        'trand_Transitionapp',
    ]



    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'apps.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                
                os.path.join(BASE_DIR, 'templates')

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

    WSGI_APPLICATION = 'apps.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/3.2/ref/settings/#databases
    # DATABASES = values.DatabaseURLValue(
    #     'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    # )

    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }



    DATABASES = mysql_settings.DATABASES
    # DATABASES = {
    #     'default': {
    #         'ENGINE' : 'django.db.backends.mysql',
    #         'NAME' : 'jyptestdb',
    #         'USER' : 'root',
    #         'PASSWORD' : '^449qkrwndbs',
    #         'HOST' : 'localhost',
    #         'PORT' : '8092'

    #     }
    # }

    # DATABASES = {
    #     'default': {
    #         'ENGINE' : 'django.db.backends.mysql',
    #         'NAME' : 'asc_db',
    #         'USER' : '1992jyp6746',
    #         'PASSWORD' : '1q2w3e',
    #         'HOST' : '172.30.1.100',
    #         'PORT' : '3306'

    #     }
    # }


    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/3.2/topics/i18n/
    LANGUAGE_CODE = 'ko-kr'

    TIME_ZONE = 'Asia/Seoul'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    AUTH_USER_MODEL = 'users.User'

    INSTANCE_PREFIX = "asc_lc_"

    RQ_PREFIX = INSTANCE_PREFIX

    QUEUE_DEFAULT = RQ_PREFIX + '_default'
    QUEUE_LOW = RQ_PREFIX + '_low'
    QUEUE_HIGH = RQ_PREFIX + '_high'

    DJANGOTASK_LOG_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'protected', 'tasklog'))
    DJANGOTASK_ALWAYS_EAGER = False
    DJANGOTASK_JOB_TRACE_ENABLED = False
    DJANGOTASK_REJECT_IF_NO_WORKER_ACTIVE_FOR_QUEUE = True


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    ALLOWED_HOSTS = []

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]


class Staging(Common):
    """
    The in-staging settings.
    """
    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )


class Production(Staging):
    """
    The in-production settings.
    """
    pass
