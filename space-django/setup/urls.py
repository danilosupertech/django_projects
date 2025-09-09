"""
PT: Mapeamento de URLs do projeto space-django.
- Inclui as rotas do app `galeria` e a interface administrativa.

EN: URL configuration for the space-django project.
- Includes `galeria` app routes and the admin interface.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),  # PT: Admin | EN: Admin site
    path('', include('galeria.urls')),  # PT/EN: Rotas do app galeria | gallery routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
