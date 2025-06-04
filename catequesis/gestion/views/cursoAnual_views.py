from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin # Importar LoginRequiredMixin
from ..models import CursoAnual
from ..forms import CursoAnualForm

class CursoAnualListView(LoginRequiredMixin, ListView):
    model = CursoAnual
    template_name = 'Gestion/CursoAnual/cursoanual_list.html'
    context_object_name = 'cursos_anuales'

class CursoAnualCreateView(CreateView):
    model = CursoAnual
    form_class = CursoAnualForm
    template_name = 'Gestion/CursoAnual/cursoanual_create.html'
    success_url = reverse_lazy('cursoanual_list')
    title = "Crear Curso anual"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('cursoanual_list')
        context['title'] = self.title
        context['view'] = self
        return context

class CursoAnualUpdateView(UpdateView):
    model = CursoAnual
    form_class = CursoAnualForm
    template_name = 'Gestion/CursoAnual/cursoanual_create.html'
    success_url = reverse_lazy('cursoanual_list')
    title = "Modificar Curso anual"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('cursoanual_list')
        context['title'] = self.title
        context['view'] = self
        return context

class CursoAnualDeleteView(DeleteView):
    model = CursoAnual
    template_name = 'Gestion/CursoAnual/cursoanual_delete.html'
    success_url = reverse_lazy('cursoanual_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('cursoanual_list')
        context['title'] = "Eliminar Curso anual"
        context['view'] = self
        return context

class CursoAnualDetailView(LoginRequiredMixin, DetailView): # Agregar LoginRequiredMixin
    model = CursoAnual
    template_name = 'Gestion/CursoAnual/cursoanual_detail.html'
    context_object_name = 'cursoanual'
