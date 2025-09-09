"""
PT: Comando para criar grupos de permissões padrão para a API.
EN: Command to create default permission groups for the API.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from escola.models import Estudante, Curso, Matricula


class Command(BaseCommand):
    help = (
        "Cria grupos: api_admin (todas), api_editor (add/change), api_viewer (sem escritas).\n"
        "Creates groups: api_admin (all), api_editor (add/change), api_viewer (no writes)."
    )

    def handle(self, *args, **options):
        models = [Estudante, Curso, Matricula]
        content_types = [ContentType.objects.get_for_model(m) for m in models]

        # Colete permissões relevantes
        all_perms = Permission.objects.filter(content_type__in=content_types)
        add_change = all_perms.filter(codename__regex=r'^(add_|change_)')

        # api_admin: todas as permissões desses modelos
        admin_group, _ = Group.objects.get_or_create(name="api_admin")
        admin_group.permissions.set(all_perms)

        # api_editor: add/change
        editor_group, _ = Group.objects.get_or_create(name="api_editor")
        editor_group.permissions.set(add_change)

        # api_viewer: sem permissões de escrita (leitura é aberta via DRF config)
        viewer_group, _ = Group.objects.get_or_create(name="api_viewer")
        viewer_group.permissions.clear()

        self.stdout.write(self.style.SUCCESS("Grupos e permissões configurados com sucesso."))

