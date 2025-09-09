"""
PT: Views da API da aplicação escola.
- ViewSets para Estudante, Curso e Matricula (CRUD completo).
- ListAPIView para listar matrículas por estudante e por curso.

EN: API views for the escola app.
- ViewSets for Estudante, Curso and Matricula (full CRUD).
- ListAPIView to list enrollments by student and by course.
"""

from escola.models import Estudante, Curso, Matricula, Professor, Nota
from escola.serializers import (
    EstudanteSerializer,
    CursoSerializer,
    MatriculaSerializer,
    ListaMatriculasEstudanteSerializer,
    ListaMatriculasCursoSerializer,
    ProfessorSerializer,
    NotaSerializer,
)

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class EstudanteViewSet(viewsets.ModelViewSet):
    """PT: CRUD de estudantes com filtros por nome e curso.
    EN: Student CRUD with filters by name and course.
    """
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        q = params.get('q') or params.get('nome')
        if q:
            qs = qs.filter(nome__icontains=q)
        # Filter by enrolled course (id or code)
        curso_id = params.get('curso') or params.get('curso_id')
        curso_codigo = params.get('curso_codigo') or params.get('codigo')
        if curso_id:
            try:
                qs = qs.filter(matricula__curso_id=int(curso_id))
            except ValueError:
                # Not an int; fall back to code
                qs = qs.filter(matricula__curso__codigo__iexact=str(curso_id))
        if curso_codigo:
            qs = qs.filter(matricula__curso__codigo__iexact=curso_codigo)
        return qs.distinct()


class CursoViewSet(viewsets.ModelViewSet):
    """PT: CRUD de cursos. EN: Course CRUD."""
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class MatriculaViewSet(viewsets.ModelViewSet):
    """PT: CRUD de matrículas. EN: Enrollment CRUD."""
    queryset = Matricula.objects.all()
    serializer_class = MatriculaSerializer


class ListaMatriculasEstudante(generics.ListAPIView):
    """PT: Lista matrículas de um estudante.
    EN: Lists a student's enrollments.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ListaMatriculasEstudanteSerializer

    def get_queryset(self):
        """PT: Filtra por ID do estudante na URL.
        EN: Filter by student ID from the URL.
        """
        return Matricula.objects.filter(estudante_id=self.kwargs['pk'])


class ListaMatriculasCurso(generics.ListAPIView):
    """PT: Lista estudantes matriculados em um curso.
    EN: Lists students enrolled in a course.
    """
    serializer_class = ListaMatriculasCursoSerializer

    def get_queryset(self):
        """PT: Filtra por ID do curso na URL.
        EN: Filter by course ID from the URL.
        """
        return Matricula.objects.filter(curso_id=self.kwargs['pk'])


class ProfessorViewSet(viewsets.ModelViewSet):
    """PT: CRUD de professores. EN: Teacher CRUD."""
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class NotaViewSet(viewsets.ModelViewSet):
    """PT: CRUD de notas. EN: Grade CRUD."""
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer


class ListaNotasEstudante(generics.ListAPIView):
    """PT: Lista notas de um estudante. EN: Lists a student's grades."""
    serializer_class = NotaSerializer

    def get_queryset(self):
        return Nota.objects.filter(estudante_id=self.kwargs['pk']).order_by('-data')


class ListaNotasCurso(generics.ListAPIView):
    """PT: Lista notas de um curso. EN: Lists grades for a course."""
    serializer_class = NotaSerializer

    def get_queryset(self):
        return Nota.objects.filter(curso_id=self.kwargs['pk']).order_by('-data')


class MeView(APIView):
    """PT: Retorna informações do usuário autenticado.
    EN: Returns the authenticated user's info.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        groups = list(u.groups.values_list('name', flat=True))
        return Response({
            'username': u.get_username(),
            'email': u.email,
            'is_superuser': bool(u.is_superuser),
            'is_staff': bool(u.is_staff),
            'groups': groups,
        })
