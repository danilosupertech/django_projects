from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('estudantes/', views.students_list, name='students_list'),
    path('estudantes/<int:pk>/matriculas/', views.student_enrollments, name='student_enrollments'),
    path('estudantes/<int:pk>/matriculas/nova/', views.student_enroll_create, name='student_enroll_create'),
    path('estudantes/<int:pk>/notas/', views.student_grades, name='student_grades'),
    path('estudantes/<int:pk>/notas/nova/', views.student_grade_create, name='student_grade_create'),
    path('estudantes/novo/', views.student_create, name='student_create'),
    path('estudantes/<int:pk>/editar/', views.student_edit, name='student_edit'),
    path('cursos/', views.courses_list, name='courses_list'),
    path('cursos/<int:pk>/notas/', views.course_grades, name='course_grades'),
    path('cursos/novo/', views.course_create, name='course_create'),
    path('cursos/<int:pk>/editar/', views.course_edit, name='course_edit'),
    path('professores/', views.professors_list, name='professors_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
