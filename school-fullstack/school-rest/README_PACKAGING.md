Como reutilizar o app `escola` em outro projeto
================================================

Instalação (modo desenvolvedor):
- No diretório `Django/school-fullstack/school-rest`, execute:

  - pip install -e .

- No seu `settings.py` do novo projeto, adicione:

  - INSTALLED_APPS = [ ..., 'escola', 'rest_framework', 'rest_framework.authtoken' ]

Migrações e admin:
- python manage.py makemigrations escola
- python manage.py migrate
- python manage.py createsuperuser

Modelos disponíveis:
- escola.models: Estudante, Curso, Matricula, Professor, Nota

Views/API (opcional):
- Para reutilizar as views DRF, copie/importe os viewsets em suas rotas (routers).

