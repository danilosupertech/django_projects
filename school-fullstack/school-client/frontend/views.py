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


def home(request: HttpRequest):
    base = _resolve_api_base()
    ctx = {'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
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
    ctx = {'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
    data, err = _fetch_json(f"{base}/estudantes/", params={'page': page}, request=request)
    if data:
        ctx['students'] = data.get('results', data)
        ctx['count'] = data.get('count')
        ctx['next'] = data.get('next')
        ctx['previous'] = data.get('previous')
    ctx['error'] = err
    return render(request, 'frontend/students_list.html', ctx)


def student_enrollments(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    ctx = {'student_id': pk, 'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
    data, err = _fetch_json(f"{base}/estudantes/{pk}/matriculas/", request=request)
    if data:
        ctx['enrollments'] = data.get('results', data)
    ctx['error'] = err
    return render(request, 'frontend/student_enrollments.html', ctx)


def courses_list(request: HttpRequest):
    base = _resolve_api_base()
    page = request.GET.get('page', '1')
    ctx = {'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
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
    ctx = {'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
    data, err = _fetch_json(f"{base}/professores/", params={'page': page}, request=request)
    if data:
        ctx['professors'] = data.get('results', data)
        ctx['count'] = data.get('count')
    ctx['error'] = err
    return render(request, 'frontend/professors_list.html', ctx)


def student_grades(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    ctx = {'student_id': pk, 'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
    data, err = _fetch_json(f"{base}/estudantes/{pk}/notas/", request=request)
    if data:
        ctx['grades'] = data.get('results', data)
    ctx['error'] = err
    return render(request, 'frontend/student_grades.html', ctx)


def course_grades(request: HttpRequest, pk: int):
    base = _resolve_api_base()
    ctx = {'course_id': pk, 'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
    data, err = _fetch_json(f"{base}/cursos/{pk}/notas/", request=request)
    if data:
        ctx['grades'] = data.get('results', data)
    ctx['error'] = err
    return render(request, 'frontend/course_grades.html', ctx)


# --- Auth & CRUD helpers ---

def login_view(request: HttpRequest):
    base = _resolve_api_base()
    ctx = {'api_base': base, 'has_token': bool(request.session.get('api_token') or settings.API_TOKEN)}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            resp = requests.post(f"{base}/api-token-auth/", data={'username': username, 'password': password}, timeout=10)
            if resp.status_code == 200:
                token = resp.json().get('token')
                if token:
                    request.session['api_token'] = token
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
