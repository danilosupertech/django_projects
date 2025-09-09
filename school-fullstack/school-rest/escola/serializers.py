"""
PT: Serializers da aplicação escola para (de)serialização e validação.
- EstudanteSerializer, CursoSerializer, MatriculaSerializer: CRUD principal.
- Listas específicas para matrículas por estudante e por curso.

EN: Serializers for the escola app for (de)serialization and validation.
- EstudanteSerializer, CursoSerializer, MatriculaSerializer: main CRUD.
- Specific lists for enrollments by student and by course.
"""

from rest_framework import serializers
from escola.models import Estudante, Curso, Matricula, Professor, Nota
from datetime import date


class EstudanteSerializer(serializers.ModelSerializer):
    """PT: Campos públicos do estudante. EN: Public student fields."""
    class Meta:
        model = Estudante
        fields = ('id', 'nome', 'email', 'cpf', 'data_nascimento', 'celular')


class CursoSerializer(serializers.ModelSerializer):
    """PT: Serializa todos os campos do curso. EN: Serializes all course fields."""
    professores = serializers.SlugRelatedField(
        slug_field='nome', many=True, read_only=True
    )
    class Meta:
        model = Curso
        fields = ('id', 'codigo', 'descricao', 'nivel', 'professores')


class MatriculaSerializer(serializers.ModelSerializer):
    """PT: Serializa todos os campos da matrícula. EN: Serializes all enrollment fields."""
    class Meta:
        model = Matricula
        fields = '__all__'


class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    """PT: Lista de matrículas de um estudante. EN: A student's enrollment list."""
    curso = serializers.ReadOnlyField(source='curso.descricao')
    curso_id = serializers.ReadOnlyField(source='curso.id')
    periodo = serializers.ReadOnlyField(source='get_periodo_display')

    class Meta:
        model = Matricula
        fields = ['curso_id', 'curso', 'periodo']


class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    """PT: Lista de estudantes matriculados em um curso. EN: Students enrolled in a course."""
    estudante_nome = serializers.ReadOnlyField(source='estudante.nome')

    class Meta:
        model = Matricula
        fields = ['estudante_nome']


class ProfessorSerializer(serializers.ModelSerializer):
    """PT: Serializa professores, incluindo nomes de cursos.
    EN: Serializes teachers, including course names.
    """
    cursos = serializers.SlugRelatedField(slug_field='codigo', many=True, read_only=True)

    class Meta:
        model = Professor
        fields = ('id', 'nome', 'email', 'celular', 'cursos')


class NotaSerializer(serializers.ModelSerializer):
    """PT: Serializa notas de estudantes. EN: Serializes student grades."""
    estudante_nome = serializers.ReadOnlyField(source='estudante.nome')
    curso_codigo = serializers.ReadOnlyField(source='curso.codigo')

    class Meta:
        model = Nota
        fields = ('id', 'estudante', 'estudante_nome', 'curso', 'curso_codigo', 'valor', 'avaliacao', 'data')

    def validate_valor(self, value):
        """PT: Garante valor entre 0 e 10. EN: Ensure grade in [0, 10]."""
        if value is None:
            raise serializers.ValidationError('Nota é obrigatória.')
        try:
            v = float(value)
        except Exception:
            raise serializers.ValidationError('Nota inválida.')
        if v < 0 or v > 10:
            raise serializers.ValidationError('A nota deve estar entre 0 e 10.')
        return value

    def validate_data(self, value):
        """Rejeita datas no passado para lançamento de prova."""
        if value and value < date.today():
            raise serializers.ValidationError('A data não pode ser retroativa.')
        return value

    def validate(self, attrs):
        """Verifica se o estudante está matriculado no curso informado."""
        estudante = attrs.get('estudante')
        curso = attrs.get('curso')
        if estudante and curso:
            exists = Matricula.objects.filter(estudante=estudante, curso=curso).exists()
            if not exists:
                raise serializers.ValidationError('Estudante não está matriculado neste curso.')
        return attrs
