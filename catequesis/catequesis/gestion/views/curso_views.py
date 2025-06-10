from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Curso
from ..forms.curso_forms import CursoForm

class CursoListView(ListView):
    model = Curso
    template_name = 'Gestion/Cursos/curso_list.html'
    context_object_name = 'cursos'
    
class CursoDetailView(DetailView):
    model = Curso
    template_name = 'Gestion/Cursos/curso_detail.html'
    context_object_name = 'curso'

class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'Gestion/Cursos/curso_create.html'
    title = 'Crear curso'
    success_url = reverse_lazy('curso_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('curso_list')
        context['title'] = self.title
        context['view'] = self
        return context

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'Gestion/Cursos/curso_create.html'
    title = 'Actualizar curso'
    success_url = reverse_lazy('curso_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('curso_list')
        context['title'] = self.title
        context['view'] = self
        return context

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'Gestion/Cursos/curso_delete.html'
    success_url = reverse_lazy('curso_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('curso_list')
        context['title'] = 'Eliminar curso'
        context['view'] = self
        return context