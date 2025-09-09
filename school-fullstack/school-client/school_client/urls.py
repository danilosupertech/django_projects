"""
PT: Root URLs do projeto school-client.
EN: Root URL configuration for the school-client project.

Inclui as rotas do app `frontend` que renderiza páginas HTML
consumindo a API do projeto `school-rest` via requests.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]
