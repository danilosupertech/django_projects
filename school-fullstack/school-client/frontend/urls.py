"""
PT: Rotas (URLs) do frontend que consome a API school-rest.
EN: Frontend URL routes consuming the school-rest API.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home com contadores de entidades
    path('', views.home, name='home'),

    # Estudantes: listagem, matrículas, notas e formulários (CRUD simplificado)
    path('estudantes/', views.students_list, name='students_list'),
    path('estudantes/<int:pk>/matriculas/', views.student_enrollments, name='student_enrollments'),
    path('estudantes/<int:pk>/notas/', views.student_grades, name='student_grades'),
    path('estudantes/novo/', views.student_create, name='student_create'),
    path('estudantes/<int:pk>/editar/', views.student_edit, name='student_edit'),

    # Cursos: listagem, notas e formulários (CRUD simplificado)
    path('cursos/', views.courses_list, name='courses_list'),
    path('cursos/<int:pk>/notas/', views.course_grades, name='course_grades'),
    path('cursos/novo/', views.course_create, name='course_create'),
    path('cursos/<int:pk>/editar/', views.course_edit, name='course_edit'),

    # Professores: listagem
    path('professores/', views.professors_list, name='professors_list'),

    # Autenticação API Token (salva token na sessão do cliente)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
