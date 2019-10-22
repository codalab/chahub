from .base import *  # noqa: F401,F403
# these noqa comments are for flake8 ignores

DEBUG = True

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

CELERY_TASK_ALWAYS_EAGER = True

# Use in memory database
DATABASES['default'] = {  # noqa: F405
    'ENGINE': 'django.db.backends.sqlite3',
}
