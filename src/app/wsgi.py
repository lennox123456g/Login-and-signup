"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module = 'app.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'app.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE',settings_module )

application = get_wsgi_application()
#cd src && PYTHONPATH=. gunicorn app.asgi:application -k uvicorn.workers.UvicornWorker
#the cd src helps provide the root directory of the app
#Gunicorn by default only handles WSGI applications (synchronous)
#Your Django app is using ASGI (asynchronous)
#UvicornWorker bridges this gap - it allows Gunicorn to run ASGI applications