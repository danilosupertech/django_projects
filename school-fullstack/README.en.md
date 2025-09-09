Project: School Fullstack (API + Client)

Goal
- A didactic project of a school with an API (Django REST Framework) and a web client (Django templates) that consumes that API.
- Great to learn CRUD, Token authentication, pagination, filters, relationships, and a simple enrollment + grades flow.

Repository structure
- Django/school-fullstack/school-rest: DRF API with app `escola` (models, serializers, views, urls)
- Django/school-fullstack/school-client: Django client that calls the API using `requests`
- docs/README.md: Portuguese guide; this file is the English version

Prerequisites
- Python 3.11+ (3.13 works)
- Recent pip
- Windows, macOS, or Linux

First‑run steps
1) Create and activate a virtual environment
   - Windows PowerShell:
     - py -3.13 -m venv venv
     - .\venv\Scripts\Activate
   - macOS/Linux:
     - python3 -m venv venv
     - source venv/bin/activate

2) Install dependencies
   - pip install --upgrade pip
   - pip install -r ../../../requirements.txt

3) Configure and run the backend (API)
   - cd Django/school-fullstack/school-rest
   - Open `.env` and, if you do not have Postgres locally, comment/remove `DATABASE_URL=` to use SQLite
   - Apply migrations: `python manage.py migrate`
   - Seed sample data: `python manage.py seed_escola`
   - Create an admin user: `python manage.py createsuperuser`
   - Optional roles: `python manage.py bootstrap_roles`
   - Start API: `python manage.py runserver 0.0.0.0:8000`
   - Test in the browser: http://127.0.0.1:8000/estudantes/

4) Run the client (frontend)
   - In another terminal: cd Django/school-fullstack/school-client
   - Start: `python manage.py runserver 0.0.0.0:8002`
   - Open: http://localhost:8002

Core flows (in the client)
- Login: use the “Entrar” (Login) button with API credentials. A token is stored in the session.
- Students: list, search by name, filter by course, create/edit (when logged in)
- Student enrollments: list enrollments; create a new enrollment
- Student grades: list grades; create a new grade (only for courses the student is enrolled in)
- Courses: list, view course grades, create/edit (when logged in)
- Teachers: list (seeded data)

Roles & permissions
- By default, anonymous read; write requires Django model permissions.
- Predefined roles (groups): `python manage.py bootstrap_roles`
  - api_admin: full CRUD
  - api_editor: add/change (no delete)
  - api_viewer: no write perms (read stays public)
- Assign groups to users via Django Admin at http://127.0.0.1:8000/admin/

Environment variables
- Backend (`school-rest/.env`):
  - DJANGO_SECRET_KEY=...
  - DEBUG=True
  - ALLOWED_HOSTS=localhost,127.0.0.1
  - DATABASE_URL=postgres://user:pass@host:5432/dbname  (optional; remove to use SQLite)
- Frontend (`school-client/.env`):
  - API_BASE_URL=http://127.0.0.1:8000  (the client can also auto-detect 8001 and replace 0.0.0.0→localhost)
  - API_TOKEN=  (optional; if you log in, you don’t need this)

API quick reference
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
- /me/ (GET authenticated user info)

Examples (curl)
- Get token: `curl -X POST -d "username=USER&password=PASS" http://127.0.0.1:8000/api-token-auth/`
- List students: `curl http://127.0.0.1:8000/estudantes/`
- Filter by name: `curl "http://127.0.0.1:8000/estudantes/?q=ana"`
- Filter by course (id): `curl "http://127.0.0.1:8000/estudantes/?curso=1"`
- Create a student: `curl -H "Authorization: Token XXX" -H "Content-Type: application/json" -d '{"nome":"Joao","email":"joao@example.com","cpf":"12345678900","data_nascimento":"2000-01-01","celular":"+351900000000"}' http://127.0.0.1:8000/estudantes/`

Troubleshooting
- Connection refused at 8001 from client: API is likely running at 8000. Adjust API_BASE_URL if needed (the client also tries to detect this).
- Postgres at 5432 refused during migrate: comment `DATABASE_URL` to use SQLite.
- “no such table …”: you missed migrations. Run `python manage.py migrate` on the backend and restart the API.
- 401/403 while saving: log in in the client or set a valid `API_TOKEN` in the client `.env`.

Guided tasks
1) Enroll a student
   - Client → Students → click “Matrículas” on the chosen student → “Nova matrícula” → pick course and period → Save
2) Create a grade
   - Client → Students → “Matrículas” → “Lançar nota” → pick one of the student’s courses → set non‑past Date and a grade between 0–10 → Save
3) Filter students by course
   - Client → Students → select a course in the top filter. You can combine with the name search box.

Read the code
- Models: school-rest/escola/models.py
- API: school-rest/escola/serializers.py, school-rest/escola/views.py, school-rest/setup/urls.py
- Seed: school-rest/escola/management/commands/seed_escola.py
- Client: school-client/frontend/views.py and templates at school-client/templates/frontend/

Next steps
- Add API tests (pytest or DRF APITestCase)
- Add OpenAPI/Swagger (drf-spectacular) to explore routes interactively
- Containerize/deploy (e.g., Docker Compose with Postgres + Nginx)

