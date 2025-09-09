"""
PT: Mapeamento de URLs do projeto school-rest.
- Rotas da API com viewsets e listas específicas de matrículas.

EN: URL configuration for the school-rest project.
- API routes using viewsets and specific enrollment lists.
"""
from django.contrib import admin
from django.urls import path, include
from escola.views import (
    EstudanteViewSet,
    CursoViewSet,
    MatriculaViewSet,
    ListaMatriculasEstudante,
    ListaMatriculasCurso,
    ProfessorViewSet,
    NotaViewSet,
    ListaNotasEstudante,
    ListaNotasCurso,
    MeView,
)
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'estudantes', EstudanteViewSet, basename='Estudantes')
router.register(r'cursos', CursoViewSet, basename='Cursos')
router.register(r'matriculas', MatriculaViewSet, basename='Matriculas')
router.register(r'professores', ProfessorViewSet, basename='Professores')
router.register(r'notas', NotaViewSet, basename='Notas')

urlpatterns = [
    path('admin/', admin.site.urls),  # PT/EN: Admin
    path('', include(router.urls)),  # PT/EN: Rotas automáticas dos viewsets | router urls
    path('api-auth/', include('rest_framework.urls')),  # PT/EN: Login/logout para a browsable API
    path('estudantes/<int:pk>/matriculas/', ListaMatriculasEstudante.as_view()),  # PT/EN: Matrículas por estudante
    path('cursos/<int:pk>/matriculas/', ListaMatriculasCurso.as_view()),  # PT/EN: Matrículas por curso
    path('estudantes/<int:pk>/notas/', ListaNotasEstudante.as_view()),  # PT/EN: Notas por estudante
    path('cursos/<int:pk>/notas/', ListaNotasCurso.as_view()),  # PT/EN: Notas por curso
    path('api-token-auth/', obtain_auth_token),  # PT: Obtenção de token | EN: Token obtain endpoint
    path('me/', MeView.as_view()),  # PT/EN: Info do usuário autenticado
]
