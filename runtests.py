import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

DJANGO_VERSION = float('.'.join([str(i) for i in django.VERSION[0:2]]))
DIR_NAME = os.path.dirname(__file__)

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
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware'),

    TEMPLATE_LOADERS=(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
        'django.template.loaders.eggs.Loader'
    ),

    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            # 'DIRS': [],
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


TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['crudbuilder', ])

if failures:
    sys.exit(bool(failures))
