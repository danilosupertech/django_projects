"""
PT: Popula a base de dados com dados de exemplo.
EN: Seeds the database with sample data.
"""

import random
from datetime import date

from django.core.management.base import BaseCommand

from escola.models import Estudante, Curso, Matricula, Professor, Nota


class Command(BaseCommand):
    help = "Cria cursos, estudantes e matrículas de exemplo."

    def handle(self, *args, **options):
        random.seed(42)

        # Cursos
        cursos = [
            ("PY101", "Python para Iniciantes", 'B'),
            ("DJ201", "Django Web Framework", 'I'),
            ("DB101", "Fundamentos de Bancos de Dados", 'B'),
            ("AI301", "Introdução à IA", 'A'),
            ("DS201", "Ciência de Dados Intermediário", 'I'),
            ("JS101", "JavaScript Básico", 'B'),
            ("HT101", "HTML & CSS", 'B'),
            ("AL301", "Algoritmos Avançados", 'A'),
        ]

        curso_objs = []
        for codigo, desc, nivel in cursos:
            obj, _ = Curso.objects.get_or_create(codigo=codigo, defaults={
                'descricao': desc,
                'nivel': nivel,
            })
            curso_objs.append(obj)

        # Estudantes (dados simples e determinísticos)
        nomes = [
            "Ana Silva", "Bruno Costa", "Carla Dias", "Daniel Rocha", "Eduarda Melo",
            "Felipe Souza", "Gustavo Lima", "Helena Pires", "Igor Santos", "Joana Alves",
            "Karina Reis", "Lucas Nogueira", "Mariana Teixeira", "Nicolas Prado", "Olivia Brito",
            "Paulo Xavier", "Queila Moura", "Rafael Barros", "Sofia Matos", "Tiago Neves",
        ]

        estudantes = []
        for i, nome in enumerate(nomes, start=1):
            email = f"{nome.split()[0].lower()}{i}@example.com"
            cpf = f"{i:011d}"[-11:]
            ano = 1990 + (i % 10)
            mes = (i % 12) + 1
            dia = ((i * 2) % 28) + 1
            data_nasc = date(ano, mes, dia)
            celular = f"+3519{i:09d}"[-13:]
            est, _ = Estudante.objects.get_or_create(
                cpf=cpf,
                defaults={
                    'nome': nome,
                    'email': email,
                    'data_nascimento': data_nasc,
                    'celular': celular,
                }
            )
            estudantes.append(est)

        # Matrículas (1-3 cursos por estudante)
        periodos = ['M', 'V', 'N']
        created = 0
        for est in estudantes:
            qtd = random.randint(1, 3)
            cursos_escolhidos = random.sample(curso_objs, qtd)
            for c in cursos_escolhidos:
                Matricula.objects.get_or_create(
                    estudante=est,
                    curso=c,
                    defaults={'periodo': random.choice(periodos)}
                )
                created += 1

        # Professores
        prof_nomes = [
            'Alice Pereira', 'Bruno Tavares', 'Clara Moreira', 'Diego Oliveira', 'Elaine Barbosa',
            'Fernando Vieira', 'Gabriela Souza', 'Henrique Santos'
        ]
        professores = []
        for i, nome in enumerate(prof_nomes, start=1):
            prof, _ = Professor.objects.get_or_create(
                email=f"prof{i}@example.com",
                defaults={'nome': nome, 'celular': f'+3519{i:09d}'[-13:]}
            )
            professores.append(prof)

        # Relaciona 1-3 professores por curso
        for c in curso_objs:
            qtd = random.randint(1, 3)
            c.professores.set(random.sample(professores, qtd))

        # Notas por matrícula: 2 avaliações por curso
        avals = ['Prova 1', 'Prova 2']
        notas_criadas = 0
        for m in Matricula.objects.all():
            for idx, aval in enumerate(avals, start=1):
                Nota.objects.get_or_create(
                    estudante=m.estudante,
                    curso=m.curso,
                    avaliacao=aval,
                    data=date(2024, 6 if idx == 1 else 12, 5 + idx),
                    defaults={'valor': round(random.uniform(6, 10), 2)}
                )
                notas_criadas += 1

        self.stdout.write(self.style.SUCCESS(
            (
                f"Seed concluído: {len(curso_objs)} cursos, {len(estudantes)} estudantes, "
                f"{Matricula.objects.count()} matrículas, {len(professores)} professores, {notas_criadas} notas."
            )
        ))
