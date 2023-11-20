import sys

import django
from django.conf import settings
from django.test.runner import DiscoverRunner

APP = 'template_update_get'

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
        APP,
    ),
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        },
    ]
)

django.setup()


test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests([APP])
if failures:
    sys.exit(failures)
