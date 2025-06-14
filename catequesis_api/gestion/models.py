import os
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date
from gestion.middleware import get_current_user

user = get_user_model()

class AcademicoModel(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    direccion = models.CharField(max_length=250, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        abstract = True

class BaseModel(models.Model):
    nombres = models.CharField(max_length=100, blank=False, null=False)
    apellidos = models.CharField(max_length=100, blank=True, null=False)
    direccion = models.CharField(max_length=250, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        abstract = True

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
    parroquia = models.ForeignKey('Parroquia', on_delete=models.CASCADE, related_name='catequistas')
    photo = models.ImageField(verbose_name="Foto",
        upload_to='documentos/Catequistas/Photos/', null=True, blank=True,
        default='documentos/Catequistas/Photos/foto_default.jpg',
        help_text="Foto opcional del catequista.")

    class Meta:
        verbose_name = 'Catequista'
        verbose_name_plural = 'Catequistas'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono} - {self.email}"

    @property
    def grupos(self):
        grupos = self.grupo_set.all()
        return ", ".join([grupo.nombre for grupo in grupos]) if grupos else "Sin grupos asignados"

class Padrino(BaseModel, AuditModel):
    documento_validacion = models.FileField(upload_to="documentos/Padrinos/", blank=False)

    class Meta:
        verbose_name = 'Padrino'
        verbose_name_plural = 'Padrinos'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"

class Padre(BaseModel, AuditModel):
    class Meta:
        verbose_name = 'Padre'
        verbose_name_plural = 'Padres'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"

class Estudiante(BaseModel, AuditModel):
    padre = models.ForeignKey(Padre, on_delete=models.CASCADE, null=True, blank=True, related_name='estudiantes')
    padrino = models.ForeignKey(Padrino, on_delete=models.CASCADE, null=True, blank=True, related_name='estudiantes')
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
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f"{self.nombres} - {self.apellidos} - {self.telefono}"

class Curso(AuditModel):
    codigo = models.CharField(max_length=10, blank=False, unique=True)
    nombre = models.CharField(max_length=100, blank=False)
    descripcion = models.CharField(max_length=255, default="Sin descripción")
    acta_bautismo = models.BooleanField(default=False, verbose_name="Acta bautismo")
    acta_nacimiento = models.BooleanField(default=False, verbose_name="Acta nacimiento")
    acta_comunion = models.BooleanField(default=False, verbose_name="Acta comunión")
    acta_matrimonio = models.BooleanField(default=False, verbose_name="Acta Matrimonio")
    costo = models.DecimalField(max_digits=8, decimal_places=2, blank=True, verbose_name="Costo")

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.descripcion} - {self.costo}"

class CicloCatequesis(models.Model):
    nombre_ciclo = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.TextField(max_length=200, blank=False, null=False)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(max_length=250, blank=True, null=True)

    class Meta:
        ordering = ['-fecha_inicio']

    def clean(self):
        if self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio.')

    def __str__(self):
        return f"{self.nombre_ciclo}-{self.fecha_inicio}-{self.fecha_fin}"

class CursoAnual(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='cursos_anuales')
    ciclo = models.ForeignKey(CicloCatequesis, on_delete=models.CASCADE, related_name='cursos_anuales')
    cupo_maximo = models.PositiveIntegerField()
    cerrado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-ciclo', 'curso']

    def __str__(self):
        return self.curso.nombre + ' - ' + self.ciclo.nombre_ciclo

class Grupo(models.Model):
    curso_anual = models.ForeignKey(CursoAnual, on_delete=models.CASCADE, related_name='grupos')
    nombre = models.CharField(max_length=50)
    cupo_maximo = models.PositiveIntegerField(default=20)
    catequistas = models.ManyToManyField('Catequista', blank=True, related_name='grupos')

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Inscripcion(AuditModel):
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE, related_name='inscripciones')
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'grupo')
        ordering = ['-fecha_inscripcion']

    def __str__(self):
        return f"{self.estudiante} en {self.grupo}"