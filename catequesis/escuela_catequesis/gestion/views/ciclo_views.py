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

class CicloUpdateView(UpdateView):
    model = CicloCatequesis
    form_class = CicloForm
    template_name = 'Gestion/Ciclo/ciclo_create.html'
    success_url = reverse_lazy('lista_ciclo')

class CicloDeleteView(DeleteView):
    model = CicloCatequesis
    template_name = 'Gestion/Ciclo/ciclo_delete.html'
    success_url = reverse_lazy('lista_ciclo')

class CicloDetailView(DetailView):
    model = CicloCatequesis
    template_name = 'Gestion/Ciclo/detail_ciclo.html'
    context_object_name = 'CicloCatequesis'
