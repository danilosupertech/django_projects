"""
PT: Ponto de entrada WSGI do projeto school-client (deploy tradicional).
EN: WSGI entrypoint for the school-client project (classic deploy).
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_client.settings')

application = get_wsgi_application()
