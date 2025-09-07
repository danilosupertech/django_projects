from django.urls import path
from galeria.views import index, imagem, atualizar_foto

urlpatterns = [
    path('', index, name='index'),
    path('imagem/<int:foto_id>/', imagem, name='imagem'),
    path('imagem/<int:foto_id>/editar/', atualizar_foto, name='atualizar_foto'),
]
