import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

DJANGO_VERSION = float('.'.join([str(i) for i in django.VERSION[0:2]]))
DIR_NAME = os.path.dirname(__file__)
localpath = lambda p: os.path.join(os.path.dirname(__file__), p)

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django.contrib.staticfiles',
        'crudbuilder',
        'django_tables2',

        'crudbuilder.tests',
        ),
    ROOT_URLCONF='crudbuilder.tests.urls',
    LOGIN_REQUIRED_FOR_CRUD=True,

    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'),

    TEMPLATE_LOADERS=(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader'
    ),

    STATIC_URL='/static/',

    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                localpath('templates'),
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

)

django.setup()

if DJANGO_VERSION == 1.7:
    settings.TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.request",
        "django.contrib.messages.context_processors.messages")

    settings.TEMPLATE_DIRS = (
        localpath('templates')
    )

TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['crudbuilder', ])

if failures:
    sys.exit(bool(failures))
