from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # Importar LoginRequiredMixin
from ..models import Padrino
from ..forms.padrino_forms import PadrinoForm

class PadrinoListView(LoginRequiredMixin, ListView):
    model = Padrino
    template_name = 'Gestion/padrinos/padrino_list.html'
    context_object_name = 'padrinos'

class PadrinoDetailView(DetailView):
    model = Padrino
    template_name = 'Gestion/padrinos/padrino_detail.html'
    context_object_name = 'padrino'

class PadrinoCreateView(CreateView):
    model = Padrino
    form_class = PadrinoForm
    template_name = 'Gestion/padrinos/padrino_create.html'
    title = 'Crear padrino'
    success_url = reverse_lazy('padrino_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('padrino_list')
        context['title'] = self.title
        context['view'] = self
        return context

class PadrinoUpdateView(UpdateView):
    model = Padrino
    form_class = PadrinoForm
    template_name = 'Gestion/padrinos/padrino_create.html'
    success_url = reverse_lazy('padrino_list')
    title = 'Actualizar padrino'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('padrino_list')
        context['title'] = self.title
        context['view'] = self
        return context

class PadrinoDeleteView(LoginRequiredMixin, DeleteView): # Agregar LoginRequiredMixin
    model = Padrino
    template_name = 'Gestion/padrinos/padrino_delete.html'
    success_url = reverse_lazy('padrino_list')
    title = 'Eliminar padrino'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('padrino_list')
        context['title'] = self.title
        context['view'] = self
        return context