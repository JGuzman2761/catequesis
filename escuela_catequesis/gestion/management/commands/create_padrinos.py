import os
import random
from django.core.management.base import BaseCommand
from faker import Faker
from gestion.models import Padrino  # Ajusta el import según tu estructura
from django.core.files.base import ContentFile

fake = Faker(["es_ES"])  # Generar nombres en español

class Command(BaseCommand):
    help = "Genera 70 padrinos falsos con documentos ficticios"

    def handle(self, *args, **kwargs):
        for _ in range(70):
            nombres = fake.first_name()
            apellidos = fake.last_name()
            telefono = fake.phone_number()
            email = fake.email()

            # Generar un documento falso (archivo vacío)
            doc_nombre = f"Acta_Matrimonio_{nombres}_{apellidos}.pdf"
            doc_ruta = os.path.join("documentos/Padrinos/", doc_nombre)

            # Crear Padrino
            padrino = Padrino(
                nombres=nombres,
                apellidos = apellidos,
                telefono=telefono,
                email=email,
            )

            # Guardar en la BD
            padrino.documento_validacion.save(doc_nombre, ContentFile("Contenido ficticio"))
            padrino.save()

        self.stdout.write(self.style.SUCCESS("✅ Se han creado 70 padrinos falsos con documentos."))
