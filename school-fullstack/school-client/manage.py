#!/usr/bin/env python
"""
PT: Utilitário de linha de comando do Django para tarefas administrativas.
EN: Django's command-line utility for administrative tasks.

Uso comum:
  - `python manage.py runserver` para executar o servidor de desenvolvimento.
  - `python manage.py migrate` para aplicar migrações.
  - `python manage.py createsuperuser` para criar usuário admin.
"""
import os
import sys


def main() -> None:
    """Configura o módulo de settings e delega para o Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_client.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
