# gestion/models.py
import os
from django.db import models
from django.db.models import Count
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
    nombre = models.CharField(max_length=100, blank=False,null=False)
    direccion = models.CharField(max_length=250, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        abstract = True  # Esto indica que no se creará una tabla para este modelo académico
    
# Modelo base para estructurar los modelos de Personas
class BaseModel(models.Model):
    nombres = models.CharField(max_length=100, blank=False,null=False)
    apellidos = models.CharField(max_length=100, blank=True,null=False)
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
    photo = models.ImageField(verbose_name="Foto",
            upload_to='documentos/Catequistas/Photos/',null=True,blank=True, 
            default='documentos/Catequistas/Photos/foto_default.jpg',
            help_text="Foto opcional del catequista." )
    
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
    class Meta:
        verbose_name = 'Padrino'
        verbose_name_plural = 'Padrinos'
    
    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"

class Padre(BaseModel, AuditModel):
    class Meta:
        verbose_name = 'Padre'
        verbose_name_plural = 'Padres'
    
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
    
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"

class Curso(AuditModel):
    codigo = models.CharField(max_length=10, blank=False, unique=True)
    nombre = models.CharField(max_length=100, blank=False)
    descripcion = models.CharField(max_length=255, default="Sin descripción")
    acta_bautizmo = models.BooleanField(default=False,verbose_name="Acta bautizmo")
    acta_nacimiento = models.BooleanField(default=False,verbose_name="Acta nacimiento")
    acta_comunion = models.BooleanField(default=False,verbose_name="Acta comunión")
    acta_matrimonio = models.BooleanField(default=False,verbose_name="Acta Matrimonio")
    # requisitos_documentos = models.TextField(blank=True)  # Lista de requisitos
    costo = models.DecimalField(max_digits=8, decimal_places=2,blank=True,verbose_name="Costo")
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
    
    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.costo}"

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
    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.curso}"

class Inscripcion(AuditModel):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, to_field="codigo")
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, to_field="codigo", related_name='inscripciones', null=True, blank=True)

    fecha_inscripcion = models.DateField(auto_now_add=True)
    documentos_entregados = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'curso')  # Un estudiante no puede inscribirse 2 veces al mismo curso

    def __str__(self):
        return f"{self.estudiante} en {self.curso} - {self.grupo}"


