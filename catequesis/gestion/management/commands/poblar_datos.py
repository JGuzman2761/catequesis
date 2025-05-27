from django.core.management.base import BaseCommand
from gestion.models import (
    Parroquia, Catequista, Padre, Padrino, Estudiante,
    Curso, CicloCatequesis as Ciclo, CursoAnual, Grupo, Inscripcion
)
from faker import Faker
from datetime import date
import random

fake = Faker('es_ES')

class Command(BaseCommand):
    help = "Genera datos de prueba para la aplicación"

    def handle(self, *args, **kwargs):
        self.stdout.write("⏳ Generando datos de prueba...")

        parroquias = self.crear_parroquias()
        catequistas = self.crear_catequistas(parroquias)
        padres = self.crear_padres()
        padrinos = self.crear_padrinos()
        estudiantes = self.crear_estudiantes(padres, padrinos)
        cursos = self.crear_cursos()
        ciclos = self.crear_ciclos()
        curso_anuales = self.crear_curso_anual(cursos, ciclos, catequistas)
        grupos = self.crear_grupos(curso_anuales, catequistas)
        self.crear_inscripciones(estudiantes, grupos)

        self.stdout.write(self.style.SUCCESS("✅ Datos de prueba generados correctamente."))

    def crear_parroquias(self, n=2):
        return [Parroquia.objects.create(
            nombre=fake.company(),
            direccion=fake.address(),
            codigo_postal=fake.postcode(),
            telefono=fake.phone_number(),
            email=fake.email(),
            parroco=fake.name()
        ) for _ in range(n)]

    def crear_catequistas(self, parroquias, n=8):
        return [Catequista.objects.create(
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            direccion=fake.address(),
            codigo_postal=fake.postcode(),
            telefono=fake.phone_number(),
            email=fake.email(),
            parroquia=random.choice(parroquias)
        ) for _ in range(n)]

    def crear_padres(self, n=50):
        return [Padre.objects.create(
            nombres=fake.first_name_male(),
            apellidos=fake.last_name(),
            direccion=fake.address(),
            codigo_postal=fake.postcode(),
            telefono=fake.phone_number(),
            email=fake.email()
        ) for _ in range(n)]

    def crear_padrinos(self, n=50):
        return [Padrino.objects.create(
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            direccion=fake.address(),
            codigo_postal=fake.postcode(),
            telefono=fake.phone_number(),
            email=fake.email(),
            documento_validacion=f'documentos/Padrinos/{fake.uuid4()}.pdf'
        ) for _ in range(n)]

    def crear_estudiantes(self, padres, padrinos, n=50):
        return [Estudiante.objects.create(
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            direccion=fake.address(),
            codigo_postal=fake.postcode(),
            telefono=fake.phone_number(),
            email=fake.email(),
            padre=random.choice(padres),
            padrino=random.choice(padrinos),
            fecha_nacimiento=fake.date_of_birth(minimum_age=10, maximum_age=14),
            acta_bautismo=f'documentos/Catequisandos/actas_bautismo/{fake.uuid4()}.pdf',
            acta_nacimiento=f'documentos/Catequisandos/actas_nacimiento/{fake.uuid4()}.pdf',
            acta_comunion=f'documentos/Catequisandos/actas_comunion/{fake.uuid4()}.pdf',
            acta_catequesis=f'documentos/Catequisandos/actas_catequesis/{fake.uuid4()}.pdf'
        ) for _ in range(n)]

    def crear_cursos(self, n=6):
        return [Curso.objects.create(
            codigo=fake.bothify(text='Curso##'),
            nombre=fake.word().capitalize(),
            descripcion=fake.text(60),
            acta_bautizmo=True,
            acta_nacimiento=True,
            acta_comunion=True,
            acta_matrimonio=False,
            costo=round(random.uniform(40.0, 100.0), 2)
        ) for _ in range(n)]

    def crear_ciclos(self):
        hoy = date.today()
        c1 = Ciclo.objects.create(
            nombre_ciclo="Ciclo 2023-2024",
            descripcion="Catequesis del año 2023-2024",
            fecha_inicio=hoy.replace(year=hoy.year - 1, month=9, day=1),
            fecha_fin=hoy.replace(year=hoy.year, month=6, day=30),
            activo=True,
            observaciones=fake.text(40)
        )
        c2 = Ciclo.objects.create(
            nombre_ciclo="Ciclo 2024-2025",
            descripcion="Catequesis del año 2024-2025",
            fecha_inicio=hoy.replace(month=9, day=1),
            fecha_fin=hoy.replace(year=hoy.year + 1, month=6, day=30),
            activo=True,
            observaciones=fake.text(40)
        )
        return [c1, c2]

    def crear_curso_anual(self, cursos, ciclos, catequistas):
        curso_anuales = []
        for curso in cursos:
            ca = CursoAnual.objects.create(
                curso=curso,
                ciclo=random.choice(ciclos),
                cupo_maximo=40,
                cerrado=False
            )
            ca.catequistas.set(random.sample(catequistas, 2))
            curso_anuales.append(ca)
        return curso_anuales

    def crear_grupos(self, curso_anuales, catequistas):
        grupos = []
        for ca in curso_anuales:
            g = Grupo.objects.create(
                curso_anual=ca,
                nombre=f"Grupo {fake.random_int(1, 10)}",
                cupo_maximo=20
            )
            g.catequistas.set(random.sample(catequistas, 1))
            grupos.append(g)
        return grupos

    def crear_inscripciones(self, estudiantes, grupos):
        for est in estudiantes:
            grupo = random.choice(grupos)
            Inscripcion.objects.create(
                estudiante=est,
                grupo=grupo,
                aprobado=random.choice([True, False])
            )
