import os
import sys
import django
from django.conf import settings

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
        'crudbuilder.tests'
    ),
    MIDDLEWARE_CLASSES=[],
    ROOT_URLCONF='test_urls'
)

django.setup()

failures = None
if DJANGO_VERSION >= 1.8:
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['crudbuilder', ])

if failures:
    sys.exit(bool(failures))