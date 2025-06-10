from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Parroquia
from ..forms.parroquia_forms import ParroquiaForm
from django.contrib.auth.mixins import LoginRequiredMixin # ¡Buena práctica añadir seguridad!
from django.contrib import messages # Para mostrar mensajes al usuario

class ParroquiaListView(ListView):
    model = Parroquia
    template_name = 'Gestion/Parroquias/parroquia_list.html'
    context_object_name = 'parroquias'

class ParroquiaDetailView(DetailView):
    model = Parroquia
    template_name = 'Gestion/Parroquias/parroquia_detail.html'
    context_object_name = 'parroquia'

# --- Vista para Crear Parroquias ---
class ParroquiaCreateView(CreateView):
    model = Parroquia
    form_class = ParroquiaForm
    template_name = 'Gestion/Parroquias/parroquia_create.html'
    title = 'Crear Parroquia'
    success_url = reverse_lazy('parroquia_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('parroquia_list')
        context['title'] = self.title
        context['view'] = self
        return context

class ParroquiaUpdateView(UpdateView):
    model = Parroquia
    form_class = ParroquiaForm
    template_name = 'Gestion/Parroquias/parroquia_create.html'
    title = 'Actualizar Parroquia'
    success_url = reverse_lazy('parroquia_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('parroquia_list')
        context['title'] = self.title
        context['view'] = self
        return context


class ParroquiaDeleteView(DeleteView):
    model = Parroquia
    template_name = 'Gestion/Parroquias/parroquia_delete.html'
    success_url = reverse_lazy('parroquia_list')
    title = 'Eliminar Parroquia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('parroquia_list')
        context['title'] = self.title
        context['view'] = self
        return context