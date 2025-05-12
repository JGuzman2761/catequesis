# gestion/views/inscripcion_views.py
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from ..models import Curso, Estudiante, Inscripcion
from ..forms import InscripcionForm  # Lo crearemos ahora
from django.views.generic import CreateView

class CursoListView(ListView):
    model = Curso
    template_name = 'gestion/inscripciones/lista_cursos.html'
    context_object_name = 'cursos'

class EstudiantesPorCursoView(DetailView):
    model = Curso
    template_name = 'gestion/inscripciones/lista_inscritos.html'
    cancel_url = reverse_lazy('lista_cursos')
    context_object_name = 'curso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inscripciones'] = Inscripcion.objects.filter(curso=self.object)
        return context

class InscripcionCreateView(CreateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'gestion/inscripciones/formulario_inscripcion.html'
    success_url = reverse_lazy('lista_inscritos')
    cancel_url = reverse_lazy('lista_inscritos')
    title = 'Crear nuevo estudiante'

    def dispatch(self, request, *args, **kwargs):
        self.curso = Curso.objects.get(pk=kwargs['pk'])  # curso.id pasado desde URL
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.curso = self.curso
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = self.curso
        context['cancel_url'] = reverse('lista_inscritos', kwargs={'pk': self.curso.pk})
        return context

    def get_success_url(self):
        return reverse_lazy('lista_inscritos', kwargs={'pk': self.curso.pk})


class InscripcionUpdateView(UpdateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'gestion/inscripciones/formulario_inscripcion.html'  # Usamos el mismo template
    success_url = reverse_lazy('lista_inscritos')
    cancel_url = reverse_lazy('lista_inscritos')

    def get_success_url(self):
        return reverse_lazy('lista_inscritos', kwargs={'pk': self.object.curso.pk})

class InscripcionDeleteView(DeleteView):
    model = Inscripcion
    template_name = 'gestion/inscripciones/eliminar_inscripcion.html'
    cancel_url = reverse_lazy('lista_inscritos')

    def get_success_url(self):
        return reverse_lazy('lista_inscritos', kwargs={'pk': self.object.curso.pk})
