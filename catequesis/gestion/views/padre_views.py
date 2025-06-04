from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # Importar LoginRequiredMixin
from ..models import Padre
from ..forms.padre_forms import PadreForm

class PadreListView(LoginRequiredMixin, ListView):
    model = Padre
    template_name = 'Gestion/Padres/padre_list.html'
    context_object_name = 'padres'

class PadreDetailView(DetailView):
    model = Padre
    template_name = 'Gestion/Padres/padre_detail.html'
    context_object_name = 'padre'

class PadreCreateView(CreateView):
    model = Padre
    form_class = PadreForm
    template_name = 'Gestion/Padres/padre_create.html'
    success_url = reverse_lazy('padre_list')
    title = 'Crear Padre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('padre_list')
        context['title'] = self.title
        context['view'] = self
        return context

class PadreUpdateView(UpdateView):
    model = Padre
    form_class = PadreForm
    template_name = 'Gestion/Padres/padre_create.html'
    success_url = reverse_lazy('padre_list')
    title = 'Actualizar Padre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('padre_list')
        context['title'] = self.title
        context['view'] = self
        return context

class PadreDeleteView(LoginRequiredMixin, DeleteView): # Agregar LoginRequiredMixin
    model = Padre
    template_name = 'Gestion/Padres/padre_delete.html'
    success_url = reverse_lazy('padre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('padre_list')
        context['title'] = 'Eliminar Padre'
        context['view'] = self
        return context