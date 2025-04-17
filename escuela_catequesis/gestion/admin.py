from django.contrib import admin
from .models import Parroquia,Catequista, Padrino, Padre, Estudiante, Curso, Grupo, Inscripcion
from django.utils.html import format_html

# Registro de modelos base para administración
@admin.register(Parroquia)
class ParroquiaAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'actualizado_por')  # Oculta los campos en el formulario de administración
    list_display = ('nombre', 'direccion', 'codigo_postal', 'telefono', 'email', 'parroco')
    search_fields = ('nombre', 'codigo_postal')
    list_filter = ('codigo_postal',)

@admin.register(Catequista)
class CatequistaAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'actualizado_por')  # Oculta los campos en el formulario de administración
    list_display = ('nombres', 'apellidos', 'email', 'telefono', 'listar_grupos')
    search_fields = ('nombres', 'apellidos', 'email')
    list_filter = ('parroquia',)
    
@admin.register(Padrino)
class PadrinoAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'actualizado_por')  # Oculta los campos en el formulario de administración
    list_display = ('nombres', 'apellidos', 'telefono', 'email', 'documento_validacion')
    search_fields = ('nombres', 'apellidos', 'email')
    list_filter = ('documento_validacion',)

@admin.register(Padre)
class PadreAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'actualizado_por')  # Oculta los campos en el formulario de administración
    list_display = ('nombres', 'apellidos', 'telefono', 'email',"fecha_creacion")
    list_filter = ("nombres", "apellidos", "fecha_creacion")
    search_fields = ('nombres', 'apellidos', 'email')

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'actualizado_por')  # Oculta los campos en el formulario de administración
    list_display = ('nombres', 'apellidos', 'email', 'telefono', 'fecha_nacimiento', )
    search_fields = ('nombres', 'apellidos', 'email')
    list_filter = ('fecha_nacimiento',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'actualizado_por')  # Oculta los campos en el formulario de administración
    list_display = ('nombre', 'descripcion', 'requisitos_documentos', 'listar_grupos')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('nombre',)

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    exclude = ('creado_por', 'actualizado_por')  # Oculta los campos en el formulario de administración
    list_display = ('nombre', 'descripcion','curso', 'mostrar_catequistas', 'listar_inscripciones')
    filter_horizontal = ('catequistas',)  # 👈 Activa la interfaz de selección con dos cuadros
    search_fields = ('nombre', 'curso__nombre')
    list_filter = ('curso',)

    def mostrar_catequistas(self, obj):
        return ", ".join([catequista.nombres for catequista in obj.catequistas.all()])  # 👈 Concatenamos los nombres

    mostrar_catequistas.short_description = "Catequistas"  # 👈 Nombre de la columna en Django Admin

    def listar_inscripciones(self, obj):
        return format_html("<b>{}</b>", Inscripcion.objects.filter(grupo=obj).count())

    listar_inscripciones.short_description = 'Inscripciones'

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'grupo', 'fecha_inscripcion', 'documentos_entregados')
    search_fields = ('estudiante__nombres', 'curso__nombre', 'grupo__nombre')
    list_filter = ('documentos_entregados', 'curso', 'grupo')

    def save_model(self, request, obj, form, change):
        if not obj.grupo:  # Asignar automáticamente el grupo si no se ha asignado uno
            obj.grupo = obj.asignar_grupo()
        super().save_model(request, obj, form, change)



