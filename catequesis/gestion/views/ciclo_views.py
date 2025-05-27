from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from gestion.models import CicloCatequesis
from gestion.forms.ciclo_forms import CicloForm

class CicloListView(ListView):
    model = CicloCatequesis
    template_name = 'gestion/Ciclo/lista_ciclo.html'
    context_object_name = 'ciclos'


class CicloCreateView(CreateView):
    model = CicloCatequesis
    form_class = CicloForm
    template_name = 'Gestion/Ciclo/ciclo_create.html'
    success_url = reverse_lazy('lista_ciclo')
    title = "Crear Ciclo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('lista_ciclo')
        context['title'] = self.title
        context['view'] = self
        return context

class CicloUpdateView(UpdateView):
    model = CicloCatequesis
    form_class = CicloForm
    template_name = 'Gestion/Ciclo/ciclo_create.html'
    success_url = reverse_lazy('lista_ciclo')
    title = "Actualizar Ciclo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('lista_ciclo')
        context['title'] = self.title
        context['view'] = self
        return context

class CicloDeleteView(DeleteView):
    model = CicloCatequesis
    template_name = 'Gestion/Ciclo/ciclo_delete.html'
    success_url = reverse_lazy('lista_ciclo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('lista_ciclo')
        context['title'] = "Eliminar Ciclo"
        context['view'] = self
        return context

class CicloDetailView(DetailView):
    model = CicloCatequesis
    template_name = 'Gestion/Ciclo/detail_ciclo.html'
    context_object_name = 'ciclo'
