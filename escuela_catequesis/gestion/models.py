# gestion/models.py
import os
from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
# from gestion.middleware import CurrentUserMiddleware  # Importa el middleware
from gestion.middleware import get_current_user

user = get_user_model()

# Modelo base para estructurar los modelos con bases similares
class AcademicoModel(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        abstract = True  # Esto indica que no se creará una tabla para este modelo académico
    
# Modelo base para estructurar los modelos de Personas
class BaseModel(models.Model):
    nombres = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=250, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        abstract = True  # Esto indica que no se creará una tabla para este modelo

class AuditModel(models.Model):
    creado_por = models.CharField(max_length=150, blank=True, null=True, editable=False)
    actualizado_por = models.CharField(max_length=150, blank=True, null=True, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        username = getattr(user, 'username', 'system')

        if not self.pk:
            self.creado_por = username
        self.actualizado_por = username
        super().save(*args, **kwargs)

class Parroquia(AcademicoModel, AuditModel):
    parroco = models.CharField(max_length=150, blank=True, null=True, verbose_name='Parroco') 

    class Meta:
        verbose_name = 'Parroquia'
        verbose_name_plural = 'Parroquias'

    def __str__(self):
        return f"{self.nombre} - {self.telefono} - {self.email}"

class Catequista(BaseModel, AuditModel):
    parroquia = models.ForeignKey('Parroquia', on_delete=models.CASCADE)
    representante = models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,
        related_name='catequistas_representados',
        help_text='Seleccione al catequista que actúa como representante')
        
    class Meta:
        verbose_name = 'Catequista'
        verbose_name_plural = 'Catequistas'

    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono} - {self.email}"
    
    def listar_grupos(self):
        grupos = Grupo.objects.filter(catequistas=self)
        return ", ".join([grupo.nombre for grupo in grupos]) if grupos else "Sin grupos asignados"

class Padrino(BaseModel, AuditModel):
    documento_validacion = models.FileField(upload_to="documentos/Padrinos/", blank=False)
    
    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"

class Padre(BaseModel, AuditModel):
    
    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"
    
class Estudiante(BaseModel, AuditModel):
    padre = models.ForeignKey(Padre, on_delete=models.CASCADE, null=True, blank=True, related_name='estudiantes')
    padrino = models.OneToOneField(Padrino, on_delete=models.SET_NULL, null=True, blank=True,related_name='estudiante' )
    photo = models.ImageField(upload_to='documentos/Catequisandos/photos/', blank=True, null=True, 
            default='documentos/Catequisandos/photos/default_photo.jpg')
    fecha_nacimiento = models.DateField()
    acta_bautismo = models.FileField(upload_to='documentos/Catequisandos/actas_bautismo/', blank=True, null=True)
    acta_nacimiento = models.FileField(upload_to='documentos/Catequisandos/actas_nacimiento/', blank=True, null=True)
    acta_comunion = models.FileField(upload_to='documentos/Catequisandos/actas_comunion/', blank=True, null=True)
    acta_catequesis = models.FileField(upload_to='documentos/Catequisandos/actas_catequesis/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"

class Curso(AuditModel):
    codigo = models.CharField(max_length=10, blank=False, unique=True)
    nombre = models.CharField(max_length=100, blank=False)
    descripcion = models.CharField(max_length=255, default="Sin descripción")
    requisitos_documentos = models.TextField(blank=True)  # Lista de requisitos
    
    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.requisitos_documentos}"

    def listar_grupos(self):
        """
        Devuelve una lista de los nombres de los grupos asociados al curso.
        """
        grupos = Grupo.objects.filter(curso=self)
        return ", ".join([grupo.nombre for grupo in grupos])

    listar_grupos.short_description = 'Grupos'

class Grupo(AuditModel):
    codigo = models.CharField(max_length=10, blank=False, unique=True)
    nombre = models.CharField(max_length=50, blank=False)
    descripcion = models.CharField(max_length=255, default="Sin descripción")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, to_field="codigo")
    catequistas = models.ManyToManyField(Catequista, blank=True)  # Relación muchos a muchos
    max_estudiantes = models.PositiveIntegerField(default=20)  # Límite de estudiantes

    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.curso}"

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, to_field="codigo")
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, to_field="codigo")
    fecha_inscripcion = models.DateField(auto_now_add=True)
    documentos_entregados = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'curso')  # Un estudiante no puede inscribirse 2 veces al mismo curso

    def save(self, *args, **kwargs):
        if not self.grupo:  # Solo asigna grupo si no tiene uno
            self.grupo = self.asignar_grupo()
        super().save(*args, **kwargs)

    def asignar_grupo(self):
        """
        Busca un grupo con menos de 20 estudiantes en el curso.
        Si no hay un grupo disponible, crea uno nuevo.
        """
        grupos = Grupo.objects.filter(curso=self.curso).order_by("numero")

        for grupo in grupos:
            if Inscripcion.objects.filter(grupo=grupo).count() < 20:
                return grupo

        # Si no hay grupos con espacio, crea un nuevo grupo
        nuevo_numero = grupos.count() + 1
        nuevo_grupo = Grupo.objects.create(curso=self.curso, numero=nuevo_numero)
        return nuevo_grupo

    def __str__(self):
        return f"{self.estudiante} en {self.curso} - {self.grupo}"


