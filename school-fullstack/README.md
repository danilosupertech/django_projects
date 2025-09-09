Projeto Fullstack: School (API + Client)

Objetivo
- Projeto didático de uma escola com API (Django REST Framework) e cliente web (Django templates) consumindo essa API.
- Ideal para aprender CRUDs, autenticação por Token, paginação, filtros, relacionamentos e um fluxo simples de matrícula e notas.

Estrutura do projeto
- school-rest: API DRF com app `escola` (models, serializers, views, urls)
- school-client: Cliente Django que consome a API via `requests`
- docs/README.md: guia geral do repositório

Pré‑requisitos
- Python 3.11+ (3.13 funciona)
- pip atualizado
- Windows, macOS ou Linux

Passo a passo (primeira execução)
1) Crie e ative ambiente virtual (recomendado)
   - Windows PowerShell:
     - py -3.13 -m venv venv
     - .\venv\Scripts\Activate
   - macOS/Linux:
     - python3 -m venv venv
     - source venv/bin/activate

2) Instale as dependências
   - pip install --upgrade pip
   - pip install -r ../../../requirements.txt

3) Configure o backend (API)
   - cd Django/school-fullstack/school-rest
   - Abra `.env` e, se não tiver Postgres local, comente/remova `DATABASE_URL=` para usar SQLite
   - Aplique migrações: `python manage.py migrate`
   - Popule dados: `python manage.py seed_escola`
   - Crie um usuário admin: `python manage.py createsuperuser`
   - Opcional: papéis (grupos) prontos: `python manage.py bootstrap_roles`
   - Rode a API: `python manage.py runserver 0.0.0.0:8000`
   - Teste no browser: http://127.0.0.1:8000/estudantes/

4) Rode o cliente (frontend)
   - Em outro terminal: cd Django/school-fullstack/school-client
   - Inicie: `python manage.py runserver 0.0.0.0:8002`
   - Acesse: http://localhost:8002

Fluxos principais (no client)
- Login: botão “Entrar” → informe usuário/senha da API. O token é salvo em sessão.
- Estudantes: listar, buscar por nome, filtrar por curso, criar/editar (quando logado)
- Matrículas do estudante: ver matrículas; criar nova matrícula
- Notas do estudante: ver notas; lançar nota (somente cursos em que o aluno está matriculado)
- Cursos: listar, ver notas do curso, criar/editar (quando logado)
- Professores: listar (dados criados pelo seed)

Perfis e permissões
- Por padrão, leitura anônima; escrita exige permissões de modelo.
- Comando de papéis: `python manage.py bootstrap_roles`
  - api_admin: CRUD completo
  - api_editor: add/change (sem delete)
  - api_viewer: sem permissões de escrita (leitura permanece pública)
- Atribua grupos ao usuário via Django Admin (http://127.0.0.1:8000/admin/)

Variáveis de ambiente
- Backend (`school-rest/.env`):
  - DJANGO_SECRET_KEY=...
  - DEBUG=True
  - ALLOWED_HOSTS=localhost,127.0.0.1
  - DATABASE_URL=postgres://user:pass@host:5432/dbname  (opcional; remova para usar SQLite)
- Frontend (`school-client/.env`):
  - API_BASE_URL=http://127.0.0.1:8000  (o client também detecta 8001 e corrige 0.0.0.0→localhost)
  - API_TOKEN=  (opcional; se fizer login, não precisa)

Cheat‑sheet de endpoints da API
- /estudantes/ (GET, POST)
- /estudantes/{id}/ (GET, PUT, PATCH, DELETE)
- /estudantes/{id}/matriculas/ (GET)
- /estudantes/{id}/notas/ (GET)
- /cursos/ (GET, POST), /cursos/{id}/ (CRUD)
- /cursos/{id}/matriculas/ (GET), /cursos/{id}/notas/ (GET)
- /professores/ (CRUD)
- /matriculas/ (CRUD)
- /notas/ (CRUD)
- /api-token-auth/ (POST username, password → token)
- /me/ (GET info do usuário autenticado)

Exemplos rápidos (curl)
- Obter token: `curl -X POST -d "username=USER&password=PASS" http://127.0.0.1:8000/api-token-auth/`
- Listar estudantes: `curl http://127.0.0.1:8000/estudantes/`
- Filtrar por nome: `curl "http://127.0.0.1:8000/estudantes/?q=ana"`
- Filtrar por curso (id): `curl "http://127.0.0.1:8000/estudantes/?curso=1"`
- Criar estudante: `curl -H "Authorization: Token XXX" -H "Content-Type: application/json" -d '{"nome":"João","email":"joao@example.com","cpf":"12345678900","data_nascimento":"2000-01-01","celular":"+351900000000"}' http://127.0.0.1:8000/estudantes/`

Erros comuns e soluções
- Connection refused 8001 no client: a API está em 8000. O client tenta detectar, mas ajuste `API_BASE_URL` se necessário.
- Postgres 5432 refused ao migrar: comente `DATABASE_URL` no `.env` do backend para usar SQLite.
- no such table (ex.: escola_professor/escola_nota): faltam migrações. Rode `python manage.py migrate` no backend correto.
- “Sem Token” ou 401/403 ao salvar: faça login no client ou use `API_TOKEN` válido.

Tarefas guiadas (passo a passo)
1) Matricular um estudante
   - Client → Estudantes → clique em “Matrículas” no aluno → “Nova matrícula” → escolha curso e período → Salvar
2) Lançar uma nota
   - Client → Estudantes → “Matrículas” → “Lançar nota” → escolha um curso do aluno → preencha Data (não retroativa), Avaliação e Nota (0–10) → Salvar
3) Filtrar estudantes por curso
   - Client → Estudantes → selecione um curso no filtro do topo → Filtrar. Opcionalmente, combine com “Pesquisar por nome”.

Onde estudar no código
- Modelos: school-rest/escola/models.py
- API: school-rest/escola/serializers.py, school-rest/escola/views.py, school-rest/setup/urls.py
- Seed: school-rest/escola/management/commands/seed_escola.py
- Client: school-client/frontend/views.py e templates em school-client/templates/frontend/

Próximos passos
- Adicionar testes de API (pytest ou DRF APITestCase)
- Documentação OpenAPI/Swagger (drf-spectacular) para explorar rotas dinamicamente
- Deploy (Docker Compose com Postgres + Nginx)

