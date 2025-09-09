"""
PT: Views do frontend que consomem a API school-rest via requests.
EN: Frontend views consuming the school-rest API using requests.
"""

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpRequest
import requests
from requests import HTTPError
from urllib.parse import urlparse, urlunparse


def _api_headers(request: HttpRequest | None = None):
    # Prefer session token from login; fallback to .env token
    session_token = None
    if request is not None:
        session_token = request.session.get('api_token')
    token = session_token or settings.API_TOKEN
    headers = {'Accept': 'application/json'}
    if token:
        headers['Authorization'] = f'Token {token}'
    return headers


def _resolve_api_base():
    """Return a reachable API base URL.

    Heuristics:
    - Use `API_BASE_URL` from settings when it responds.
    - If host is `0.0.0.0`, replace with `localhost`.
    - If port is 8001 and connection is refused, try same host on 8000.
    """
    configured = (settings.API_BASE_URL or '').strip().rstrip('/') or 'http://localhost:8001'

    def normalize(host_port_base: str) -> str:
        parsed = urlparse(host_port_base)
        host = parsed.hostname or 'localhost'
        # Never use 0.0.0.0 for client requests
        if host == '0.0.0.0':
            host = 'localhost'
        # Rebuild netloc preserving port if any
        port = f":{parsed.port}" if parsed.port else ''
        netloc = f"{host}{port}"
        return urlunparse((parsed.scheme or 'http', netloc, '', '', '', '')).rstrip('/')

    def reachable(base: str) -> bool:
        try:
            # hit a lightweight endpoint; allow any status code as "reachable"
            requests.get(f"{base}/estudantes/", headers=_api_headers(None), timeout=3)
            return True
        except requests.exceptions.ConnectionError:
            return False
        except Exception:
            # DNS/SSL/etc considered reachable for our purposes
            return True

    candidates = []
    first = normalize(configured)
    candidates.append(first)

    # If it's 8001, try 8000 on same host as fallback
    parsed_first = urlparse(first)
    if parsed_first.port == 8001:
        alt_netloc = f"{parsed_first.hostname}:8000"
        candidates.append(urlunparse((parsed_first.scheme, alt_netloc, '', '', '', '')).rstrip('/'))

    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            ordered.append(c)

    for base in ordered:
        if reachable(base):
            return base
    # Fall back to normalized configured even if unreachable; views will show error
    return first


def _fetch_json(url: str, params=None, request: HttpRequest | None = None):
    """GET JSON with helpful error messages and token hints."""
    try:
        resp = requests.get(url, params=params or {}, headers=_api_headers(request), timeout=10)
        try:
            resp.raise_for_status()
        except HTTPError as http_err:
            try:
                payload = resp.json()
            except Exception:
                payload = {}
            detail = payload.get('detail') or payload or resp.text
            # Friendly hint when auth is required
            if resp.status_code in (401, 403):
                hint = ' Endpoint requer autenticação. Defina API_TOKEN no .env do client.'
            else:
                hint = ''
            return None, f"HTTP {resp.status_code}: {detail}.{hint}"
        return resp.json(), None
    except Exception as exc:
        return None, f"Erro ao consultar API: {exc}"


def _ensure_user_info(request: HttpRequest, base: str):
    """If logged in but session has no user info, fetch it from the API."""
    token = request.session.get('api_token') or settings.API_TOKEN
    if not token:
        return
    if request.session.get('api_user'):
        return
    try:
        resp = requests.get(f"{base}/me/", headers={'Authorization': f'Token {token}', 'Accept': 'application/json'}, timeout=5)
        if resp.status_code == 200:
            request.session['api_user'] = resp.json()
    except Exception:
        pass


def _ctx_base(request: HttpRequest, base: str):
    has_token = bool(request.session.get('api_token') or settings.API_TOKEN)
    _ensure_user_info(request, base)
    return {
        'api_base': base,
        'has_token': has_token,
        'user_info': request.session.get('api_user') if has_token else None,
    }


def home(request: HttpRequest):
    base = _resolve_api_base()
    ctx = _ctx_base(request, base)
    students, err1 = _fetch_json(f"{base}/estudantes/", request=request)
    courses, err2 = _fetch_json(f"{base}/cursos/", request=request)
    if students:
        ctx['students_count'] = students.get('count', len(students))
    if courses:
        ctx['courses_count'] = courses.get('count', len(courses))
    ctx['error'] = err1 or err2
    return render(request, 'frontend/home.html', ctx)


def students_list(request: HttpRequest):
    base = _resolve_api_base()
    page = request.GET.get('page', '1')
    search = request.GET.get('q', '').strip()
    curso = request.GET.get('curso', '').strip()
    ctx = _ctx_base(request, base)
    # Load courses for filter select
    ctx['courses'] = _fetch_all(base, '/cursos/', request)
    params = {'page': page}
    if search:
        params['q'] = search
    if curso:
        params['curso'] = curso
    data, err = _fetch_json(f"{base}/estudantes/", params=params, request=request)
    if data:
        ctx['students'] = data.get('results', data)
        ctx['count'] = data.get('count')
        ctx['next'] = data.get('next')
        ctx['previous'] = data.get('previous')
    ctx['q'] = search
    ctx['curso_selected'] = curso
    ctx['error'] = err
    return render(request, 'frontend/students_list.html', ctx)


def student_enrollments(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    ctx = _ctx_base(request, base)
    ctx['student_id'] = pk
    # Student details for context
    sdata, serr = _fetch_json(f"{base}/estudantes/{pk}/", request=request)
    if sdata:
        ctx['student'] = sdata
    data, err = _fetch_json(f"{base}/estudantes/{pk}/matriculas/", request=request)
    if data:
        ctx['enrollments'] = data.get('results', data)
    ctx['error'] = err or serr
    return render(request, 'frontend/student_enrollments.html', ctx)


def courses_list(request: HttpRequest):
    base = _resolve_api_base()
    page = request.GET.get('page', '1')
    ctx = _ctx_base(request, base)
    data, err = _fetch_json(f"{base}/cursos/", params={'page': page}, request=request)
    if data:
        ctx['courses'] = data.get('results', data)
        ctx['count'] = data.get('count')
        ctx['next'] = data.get('next')
        ctx['previous'] = data.get('previous')
    ctx['error'] = err
    return render(request, 'frontend/courses_list.html', ctx)


def professors_list(request: HttpRequest):
    base = _resolve_api_base()
    page = request.GET.get('page', '1')
    ctx = _ctx_base(request, base)
    data, err = _fetch_json(f"{base}/professores/", params={'page': page}, request=request)
    if data:
        ctx['professors'] = data.get('results', data)
        ctx['count'] = data.get('count')
    ctx['error'] = err
    return render(request, 'frontend/professors_list.html', ctx)


def student_grades(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    ctx = _ctx_base(request, base)
    ctx['student_id'] = pk
    sdata, serr = _fetch_json(f"{base}/estudantes/{pk}/", request=request)
    if sdata:
        ctx['student'] = sdata
    data, err = _fetch_json(f"{base}/estudantes/{pk}/notas/", request=request)
    if data:
        ctx['grades'] = data.get('results', data)
    ctx['error'] = err or serr
    return render(request, 'frontend/student_grades.html', ctx)


def course_grades(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    ctx = _ctx_base(request, base)
    ctx['course_id'] = pk
    data, err = _fetch_json(f"{base}/cursos/{pk}/notas/", request=request)
    if data:
        ctx['grades'] = data.get('results', data)
    ctx['error'] = err
    return render(request, 'frontend/course_grades.html', ctx)


# --- Auth & CRUD helpers ---

def login_view(request: HttpRequest):
    base = _resolve_api_base()
    ctx = _ctx_base(request, base)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            resp = requests.post(f"{base}/api-token-auth/", data={'username': username, 'password': password}, timeout=10)
            if resp.status_code == 200:
                token = resp.json().get('token')
                if token:
                    request.session['api_token'] = token
                    # fetch and store user info
                    try:
                        me = requests.get(f"{base}/me/", headers={'Authorization': f'Token {token}', 'Accept': 'application/json'}, timeout=5)
                        if me.status_code == 200:
                            request.session['api_user'] = me.json()
                    except Exception:
                        pass
                    return redirect('home')
                ctx['error'] = 'Resposta sem token.'
            elif resp.status_code in (400, 401):
                ctx['error'] = 'Credenciais inválidas.'
            else:
                ctx['error'] = f'Falha ao autenticar (HTTP {resp.status_code}).'
        except Exception as exc:
            ctx['error'] = f'Erro ao autenticar: {exc}'
    return render(request, 'frontend/login.html', ctx)


def logout_view(request: HttpRequest):
    request.session.pop('api_token', None)
    request.session.pop('api_user', None)
    return redirect('home')


def student_form_context(base: str, has_token: bool, data=None, errors=None):
    return {'api_base': base, 'has_token': has_token, 'data': data or {}, 'errors': errors}


def student_create(request: HttpRequest):
    base = _resolve_api_base()
    has_token = bool(request.session.get('api_token') or settings.API_TOKEN)
    if request.method == 'POST':
        payload = {
            'nome': request.POST.get('nome', ''),
            'email': request.POST.get('email', ''),
            'cpf': request.POST.get('cpf', ''),
            'data_nascimento': request.POST.get('data_nascimento', ''),
            'celular': request.POST.get('celular', ''),
        }
        try:
            resp = requests.post(f"{base}/estudantes/", json=payload, headers=_api_headers(request), timeout=10)
            if resp.status_code in (200, 201):
                return redirect('students_list')
            return render(request, 'frontend/student_form.html', student_form_context(base, has_token, payload, resp.json()))
        except Exception as exc:
            return render(request, 'frontend/student_form.html', student_form_context(base, has_token, payload, {'error': str(exc)}))
    return render(request, 'frontend/student_form.html', student_form_context(base, has_token))


def student_edit(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    has_token = bool(request.session.get('api_token') or settings.API_TOKEN)
    if request.method == 'POST':
        payload = {
            'nome': request.POST.get('nome', ''),
            'email': request.POST.get('email', ''),
            'cpf': request.POST.get('cpf', ''),
            'data_nascimento': request.POST.get('data_nascimento', ''),
            'celular': request.POST.get('celular', ''),
        }
        try:
            resp = requests.put(f"{base}/estudantes/{pk}/", json=payload, headers=_api_headers(request), timeout=10)
            if resp.status_code in (200, 202):
                return redirect('students_list')
            return render(request, 'frontend/student_form.html', student_form_context(base, has_token, payload, resp.json()))
        except Exception as exc:
            return render(request, 'frontend/student_form.html', student_form_context(base, has_token, payload, {'error': str(exc)}))
    # GET: prefill
    data, err = _fetch_json(f"{base}/estudantes/{pk}/", request=request)
    return render(request, 'frontend/student_form.html', student_form_context(base, has_token, data, {'error': err} if err else None))


def course_form_context(base: str, has_token: bool, data=None, errors=None):
    return {'api_base': base, 'has_token': has_token, 'data': data or {}, 'errors': errors}


def course_create(request: HttpRequest):
    base = _resolve_api_base()
    has_token = bool(request.session.get('api_token') or settings.API_TOKEN)
    if request.method == 'POST':
        payload = {
            'codigo': request.POST.get('codigo', ''),
            'descricao': request.POST.get('descricao', ''),
            'nivel': request.POST.get('nivel', 'B'),
        }
        try:
            resp = requests.post(f"{base}/cursos/", json=payload, headers=_api_headers(request), timeout=10)
            if resp.status_code in (200, 201):
                return redirect('courses_list')
            return render(request, 'frontend/course_form.html', course_form_context(base, has_token, payload, resp.json()))
        except Exception as exc:
            return render(request, 'frontend/course_form.html', course_form_context(base, has_token, payload, {'error': str(exc)}))
    return render(request, 'frontend/course_form.html', course_form_context(base, has_token))


def course_edit(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    has_token = bool(request.session.get('api_token') or settings.API_TOKEN)
    if request.method == 'POST':
        payload = {
            'codigo': request.POST.get('codigo', ''),
            'descricao': request.POST.get('descricao', ''),
            'nivel': request.POST.get('nivel', 'B'),
        }
        try:
            resp = requests.put(f"{base}/cursos/{pk}/", json=payload, headers=_api_headers(request), timeout=10)
            if resp.status_code in (200, 202):
                return redirect('courses_list')
            return render(request, 'frontend/course_form.html', course_form_context(base, has_token, payload, resp.json()))
        except Exception as exc:
            return render(request, 'frontend/course_form.html', course_form_context(base, has_token, payload, {'error': str(exc)}))
    data, err = _fetch_json(f"{base}/cursos/{pk}/", request=request)
    return render(request, 'frontend/course_form.html', course_form_context(base, has_token, data, {'error': err} if err else None))


def _fetch_all(base: str, path: str, request: HttpRequest | None = None):
    """Fetch all pages for a paginated endpoint and return a list of items.
    If not paginated, return the data as a list (single item or list).
    """
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"
    items = []
    visited = set()
    while url and url not in visited:
        visited.add(url)
        data, err = _fetch_json(url, request=request)
        if not data:
            break
        if isinstance(data, dict) and 'results' in data:
            items.extend(data.get('results') or [])
            url = data.get('next')
        else:
            # Not paginated
            if isinstance(data, list):
                items.extend(data)
            else:
                items.append(data)
            url = None
    return items


def student_enroll_create(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    has_token = bool(request.session.get('api_token') or settings.API_TOKEN)
    # Load only student's current enrollments' courses
    sdata, _ = _fetch_json(f"{base}/estudantes/{pk}/", request=request)
    # matriculas
    md, _ = _fetch_json(f"{base}/estudantes/{pk}/matriculas/", request=request)
    courses = []
    if md:
        items = md.get('results', md)
        for m in items:
            if 'curso_id' in m and 'curso' in m:
                courses.append({'id': m['curso_id'], 'label': m['curso']})
    if request.method == 'POST':
        payload = {
            'estudante': pk,
            'curso': request.POST.get('curso'),
            'periodo': request.POST.get('periodo', 'M'),
        }
        try:
            resp = requests.post(f"{base}/matriculas/", json=payload, headers=_api_headers(request), timeout=10)
            if resp.status_code in (200, 201):
                return redirect('student_enrollments', pk=pk)
            errors = {}
            try:
                errors = resp.json()
            except Exception:
                errors = {'error': f'HTTP {resp.status_code}'}
            return render(request, 'frontend/student_enroll_form.html', {'student_id': pk, 'student': sdata, 'api_base': base, 'has_token': has_token, 'courses': courses, 'errors': errors})
        except Exception as exc:
            return render(request, 'frontend/student_enroll_form.html', {'student_id': pk, 'student': sdata, 'api_base': base, 'has_token': has_token, 'courses': courses, 'errors': {'error': str(exc)}})
    return render(request, 'frontend/student_enroll_form.html', {'student_id': pk, 'student': sdata, 'api_base': base, 'has_token': has_token, 'courses': courses})


def student_grade_create(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    has_token = bool(request.session.get('api_token') or settings.API_TOKEN)
    # Load only courses where the student is enrolled
    sdata, _ = _fetch_json(f"{base}/estudantes/{pk}/", request=request)
    md, _ = _fetch_json(f"{base}/estudantes/{pk}/matriculas/", request=request)
    courses = []
    if md:
        items = md.get('results', md)
        for m in items:
            if 'curso_id' in m and 'curso' in m:
                courses.append({'id': m['curso_id'], 'label': m['curso']})
    if not courses:
        ctx = {'student_id': pk, 'student': sdata, 'api_base': base, 'has_token': has_token, 'courses': [], 'errors': {'error': 'Estudante sem matrículas. Matricule-o em um curso antes de lançar notas.'}}
        return render(request, 'frontend/student_grade_form.html', ctx)
    if request.method == 'POST':
        payload = {
            'estudante': pk,
            'curso': request.POST.get('curso'),
            'valor': request.POST.get('valor'),
            'avaliacao': request.POST.get('avaliacao', 'Prova'),
            'data': request.POST.get('data'),
        }
        try:
            resp = requests.post(f"{base}/notas/", json=payload, headers=_api_headers(request), timeout=10)
            if resp.status_code in (200, 201):
                return redirect('student_grades', pk=pk)
            errors = {}
            try:
                errors = resp.json()
            except Exception:
                errors = {'error': f'HTTP {resp.status_code}'}
            return render(request, 'frontend/student_grade_form.html', {'student_id': pk, 'student': sdata, 'api_base': base, 'has_token': has_token, 'courses': courses, 'errors': errors})
        except Exception as exc:
            return render(request, 'frontend/student_grade_form.html', {'student_id': pk, 'student': sdata, 'api_base': base, 'has_token': has_token, 'courses': courses, 'errors': {'error': str(exc)}})
    return render(request, 'frontend/student_grade_form.html', {'student_id': pk, 'student': sdata, 'api_base': base, 'has_token': has_token, 'courses': courses})
