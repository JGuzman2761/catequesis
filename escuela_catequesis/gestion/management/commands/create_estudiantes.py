import random
from datetime import datetime, timedelta
from faker import Faker
from django.core.management.base import BaseCommand
from gestion.models import Estudiante  # Ajusta según la ubicación de tu modelo

fake = Faker("es_ES")

def generar_fecha_nacimiento(edad_min, edad_max):
    """Genera una fecha de nacimiento aleatoria dentro del rango de edad dado."""
    hoy = datetime.today()
    edad = random.randint(edad_min, edad_max)
    fecha_nacimiento = hoy - timedelta(days=edad * 365 + random.randint(0, 364))
    return fecha_nacimiento.date()

class Command(BaseCommand):
    help = "Genera 100 estudiantes con edades específicas"

    def handle(self, *args, **kwargs):
        estudiantes = []

        # Grupo 1: 40 estudiantes con menos de 16 años (11-15)
        for _ in range(40):
            estudiantes.append(Estudiante(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                fecha_nacimiento=generar_fecha_nacimiento(11, 15),
                email=fake.email(),
                telefono=fake.phone_number()
            ))

        # Grupo 2: 40 estudiantes entre 16 y 18 años
        for _ in range(40):
            estudiantes.append(Estudiante(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                fecha_nacimiento=generar_fecha_nacimiento(16, 18),
                email=fake.email(),
                telefono=fake.phone_number()
            ))

        # Grupo 3: 20 estudiantes mayores de 18 años
        for _ in range(20):
            estudiantes.append(Estudiante(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                fecha_nacimiento=generar_fecha_nacimiento(19, 25),  # Máximo 25 años
                email=fake.email(),
                telefono=fake.phone_number()
            ))

        # Guardar en la base de datos
        Estudiante.objects.bulk_create(estudiantes)
        self.stdout.write(self.style.SUCCESS("✅ Se han creado 100 estudiantes con éxito."))


