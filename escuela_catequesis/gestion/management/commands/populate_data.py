# escuela_catequesis/gestion/management/commands/populate_data.py
from django.core.management.base import BaseCommand
from faker import Faker
from gestion.models import Parroquia, Catequista, Padrino, Padre, Estudiante, Curso, Grupo, Inscripcion
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with fake data'

    def handle(self, *args, **options):
        fake = Faker('es_ES')  # Use Spanish locale for Faker

        # Create Parroquias
        parroquias = []
        for _ in range(3):
            parroquia = Parroquia.objects.create(
                nombre=fake.company(),
                direccion=fake.address(),
                codigo_postal=fake.postcode(),
                telefono=fake.phone_number(),
                email=fake.email())
            parroquias.append(parroquia)
            self.stdout.write(self.style.SUCCESS(f'Created Parroquia: {parroquia.nombre}'))

        # Create Catequistas
        # Primero crea una lista vacía donde guardaremos los catequistas creados
        catequistas_creados = []

        # Creamos 10 catequistas (puedes ajustar el número)
        for _ in range(10):
            parroquia = random.choice(parroquias)
            
            # El representante será aleatoriamente uno de los ya creados (o ninguno si aún no hay)
            representante = random.choice(catequistas_creados) if catequistas_creados and random.random() > 0.3 else None

            catequista = Catequista.objects.create(
                parroquia=parroquia,
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                telefono=fake.phone_number(),
                email=fake.email(),
                representante=representante
            )

            catequistas_creados.append(catequista)

        # Create Padres
        padres = []
        for _ in range(50):
            padre = Padre.objects.create(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                direccion=fake.address(),
                codigo_postal=fake.postcode(),
                telefono=fake.phone_number(),
                email=fake.email()
            )
            padres.append(padre)
            self.stdout.write(self.style.SUCCESS(f'Created Padre: {padre.nombres} {padre.apellidos}'))

        # Create Padrinos
        for _ in range(50):
            padrino = Padrino.objects.create(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                direccion=fake.address(),
                codigo_postal=fake.postcode(),
                telefono=fake.phone_number(),
                email=fake.email(),
                documento_validacion = "documentos/Padrinos/default.pdf" # Added default value
            )
            self.stdout.write(self.style.SUCCESS(f'Created Padrino: {padrino.nombres} {padrino.apellidos}'))

        # Create Estudiantes
        for _ in range(50):
            estudiante = Estudiante.objects.create(
                padre=random.choice(padres),
                padrino=None,  # Set padrino to None initially
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                direccion=fake.address(),
                codigo_postal=fake.postcode(),
                telefono=fake.phone_number(),
                email=fake.email(),
                fecha_nacimiento=fake.date_between(start_date='-18y', end_date='-6y')
            )
            self.stdout.write(self.style.SUCCESS(f'Created Estudiante: {estudiante.nombres} {estudiante.apellidos}'))

        cursos = []

        # Crear Cursos
        for _ in range(5):
            curso = Curso.objects.create(
                codigo = fake.unique.lexify(text='CUR??###'),
                nombre=fake.job(),
                descripcion=fake.text(max_nb_chars=200),
                requisitos_documentos=fake.text(max_nb_chars=100)
            )
            cursos.append(curso)
            self.stdout.write(self.style.SUCCESS(f'Curso creado: {curso.nombre}'))

        # Crear Grupos
        for _ in range(10):
            try:
                grupo = Grupo.objects.create(
                    codigo = fake.unique.lexify(text='CUR??###'),
                    nombre=fake.word().capitalize(),
                    descripcion=fake.text(max_nb_chars=200),
                    curso=random.choice(cursos),
                    max_estudiantes=random.randint(10, 30)
                )
                self.stdout.write(self.style.SUCCESS(f'Grupo creado: {grupo.nombre}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error al crear grupo: {str(e)}'))
        # Create Inscripciones
        for _ in range(50):
            estudiante = random.choice(Estudiante.objects.all())
            curso = random.choice(Curso.objects.all())
            grupo = random.choice(Grupo.objects.all())
            inscripcion = Inscripcion.objects.create(
                estudiante=estudiante,
                curso=curso,
                grupo=grupo,
                fecha_inscripcion=timezone.now().date(),
                documentos_entregados=fake.boolean(chance_of_getting_true=80)
            )
            self.stdout.write(self.style.SUCCESS(f'Created Inscripcion: {estudiante} - {curso}'))

        self.stdout.write(self.style.SUCCESS('Data population complete!'))