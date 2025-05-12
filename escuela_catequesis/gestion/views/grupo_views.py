from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.admin.widgets import FilteredSelectMultiple
from gestion.models import Grupo, Catequista
from gestion.forms import GrupoForm


class GrupoListView(ListView):
    model = Grupo
    template_name = 'Gestion/Grupos/grupo_list.html'
    context_object_name = 'grupos'

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = 'Gestion/Grupos/grupo_detail.html'
    context_object_name = 'grupo'

class GrupoCreateView(CreateView):
    model = Grupo
    form_class = GrupoForm
    template_name = 'Gestion/Grupos/grupo_create.html' # Plantilla clave para el widget
    success_url = reverse_lazy('grupo_list') # URL a la lista después de crear
    title = 'Crear curso'
    cancel_url = reverse_lazy('grupo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_catequistas'] = Catequista.objects.all()
        # Pasamos todos los catequistas para construir el lado "disponible" del widget
        return context

class GrupoUpdateView(UpdateView):
    model = Grupo
    form_class = GrupoForm
    template_name = 'Gestion/Grupos/grupo_create.html' # Plantilla clave para el widget
    success_url = reverse_lazy('grupo_list') # URL a la lista después de crear
    title = 'Actualizar curso'
    cancel_url = reverse_lazy('grupo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo = self.get_object()
        seleccionados_ids = grupo.catequistas.values_list('id', flat=True)
        # Pasamos todos los catequistas y los IDs de los seleccionados
        context['todos_catequistas'] = Catequista.objects.all()
        context['seleccionados_ids'] = list(seleccionados_ids)
        return context

class GrupoDeleteView(DeleteView):
    model = Grupo
    template_name = 'Gestion/Grupos/grupo_delete.html'
    success_url = reverse_lazy('grupo_list')