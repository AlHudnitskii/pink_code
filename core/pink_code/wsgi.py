import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leetcode_analogue.settings')

application = get_wsgi_application()
