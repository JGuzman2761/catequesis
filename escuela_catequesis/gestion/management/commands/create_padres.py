from django.core.management.base import BaseCommand
from faker import Faker
from gestion.models import Padre

class Command(BaseCommand):
    help = 'Pobla la base de datos con 100 padres falsos usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker('es_MX')  # Puedes ajustar el locale
        padres_creados = 0

        for _ in range(100):
            Padre.objects.create(
                nombres=fake.first_name(),
                apellidos=fake.last_name(),
                direccion=fake.address(),
                codigo_postal=fake.postcode(),
                telefono=fake.phone_number(),
                email=fake.email(),
                creado_por="admin",
                actualizado_por="admin"
            )
            padres_creados += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {padres_creados} padres creados exitosamente."))
