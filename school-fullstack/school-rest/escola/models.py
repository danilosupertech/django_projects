"""
PT: Modelos de domínio da aplicação escola.
- Estudante: dados pessoais e contato.
- Curso: informações e nível.
- Matricula: vínculo entre estudante e curso com período.

EN: Domain models for the escola app.
- Estudante (Student): personal and contact data.
- Curso (Course): information and level.
- Matricula (Enrollment): relation between student and course with period.
"""

from django.db import models


class Estudante(models.Model):
    """PT: Representa um estudante. EN: Represents a student."""
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=30,blank=False)
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    celular = models.CharField(max_length=15)

    def __str__(self):
            return self.nome
    
class Curso(models.Model):
    """PT: Representa um curso. EN: Represents a course."""
    # PT: Níveis possíveis do curso | EN: Course level choices
    NIVEL = (('B','básico'), ('I','intermediário'), ('A','avançado'))
    codigo = models.CharField(max_length=10)
    descricao = models.CharField(max_length=100, blank=False)
    nivel = models.CharField(max_length=1, choices=NIVEL, default='B')

    # PT: Professores associados ao curso (muitos-para-muitos)
    # EN: Teachers associated to the course (many-to-many)
    # Declarado no modelo Professor para manter ordem do arquivo.

    def __str__(self):
            return self.codigo
    
class Matricula(models.Model):
    """PT: Matrícula de um estudante em um curso. EN: A student's enrollment in a course."""
    # PT: Período do curso | EN: Course time period
    PERIODO = (('M','matutino'), ('V','vespertino'), ('N','noturno'))
    
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=1, choices=PERIODO, default='M')
    
    def __str__(self):
            return f'{self.estudante.nome} - {self.curso.codigo}'


class Professor(models.Model):
    """PT: Representa um professor. EN: Represents a teacher."""
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=60, blank=False)
    celular = models.CharField(max_length=15, blank=True)

    # Cursos ministrados (muitos-para-muitos)
    cursos = models.ManyToManyField('Curso', related_name='professores', blank=True)

    def __str__(self):
        return self.nome


class Nota(models.Model):
    """PT: Nota de um estudante em um curso.
    EN: A student's grade for a course.
    """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='notas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='notas')
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    avaliacao = models.CharField(max_length=100, default='Prova')
    data = models.DateField()

    class Meta:
        unique_together = ('estudante', 'curso', 'avaliacao', 'data')

    def __str__(self):
        return f'{self.estudante.nome} / {self.curso.codigo} = {self.valor}'
