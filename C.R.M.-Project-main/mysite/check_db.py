import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mysite.settings')
import django
django.setup()
from django.conf import settings
print('ENGINE=', settings.DATABASES['default']['ENGINE'])
print('DB dict=', settings.DATABASES)
