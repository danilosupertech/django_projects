"""
PT: Configurações do Django Admin para os modelos da aplicação escola.
EN: Django Admin configurations for the escola app models.
"""

from django.contrib import admin
from escola.models import Estudante, Curso, Matricula, Professor, Nota


class Estudantes(admin.ModelAdmin):
    """PT: Lista e busca de estudantes no admin. EN: Student list and search in admin."""
    list_display = ('id', 'nome', 'email', 'cpf', 'data_nascimento', 'celular')
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'email', 'cpf')
    list_per_page = 10

class Cursos(admin.ModelAdmin):
    """PT: Lista, filtros e busca de cursos. EN: Course list, filters and search."""
    list_display = ('id', 'codigo', 'descricao', 'nivel')
    list_display_links = ('id', 'codigo')
    list_filter = ('nivel',)
    search_fields = ('codigo', 'descricao', 'nivel')
    list_per_page = 10
        
class Matriculas(admin.ModelAdmin):
    """PT: Lista e busca de matrículas. EN: Enrollment list and search."""
    list_display = ('id', 'estudante', 'curso', 'periodo')
    list_display_links = ('id', 'estudante')
    list_filter = ('periodo',)
    search_fields = ('estudante__nome', 'curso__codigo')
    list_per_page = 10
        

admin.site.register(Estudante, Estudantes)
admin.site.register(Curso, Cursos)
admin.site.register(Matricula, Matriculas)
admin.site.register(Professor)
admin.site.register(Nota)
