"""
PT: Configuração de app do Django para a aplicação "escola".
EN: Django app configuration for the "escola" application.
"""
from django.apps import AppConfig


class EscolaConfig(AppConfig):
    """Define metadados do app e configurações padrão.

    - default_auto_field: usa BigAutoField para chaves primárias auto-incrementais.
    - name: caminho do app (usado pelo Django para registro).
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'escola'
