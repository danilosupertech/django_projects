"""
PT: Ponto de entrada ASGI do projeto school-client (deploy async/WS). 
EN: ASGI entrypoint for the school-client project (async/WS deploy).
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_client.settings')

application = get_asgi_application()
