import random
from django.core.management.base import BaseCommand
from faker import Faker
from gestion.models import Catequista, Parroquia  # Ajusta según tu app

class Command(BaseCommand):
    help = "Genera 10 catequistas falsos con nombres en español"

    def handle(self, *args, **kwargs):
        fake = Faker("es_ES")

        # Obtener todas las parroquias disponibles
        parroquias = list(Parroquia.objects.all())

        if not parroquias:
            self.stdout.write(self.style.ERROR("❌ No hay parroquias en la base de datos. Agrega al menos una."))
            return

        for _ in range(10):
            catequista = Catequista.objects.create(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                telefono=fake.phone_number(),
                email=fake.email(),
                parroquia=random.choice(parroquias),
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Catequista creado: {catequista}"))

