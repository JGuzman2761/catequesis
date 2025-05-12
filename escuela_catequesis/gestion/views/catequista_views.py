from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Catequista
from ..forms.catequista_forms import CatequistaForm

class CatequistaListView(ListView):
    model = Catequista
    template_name = 'gestion/Catequistas/catequista_list.html'
    context_object_name = 'catequistas'

class CatequistaCreateView(CreateView):
    model = Catequista
    form_class = CatequistaForm
    template_name = 'gestion/Catequistas/catequista_form.html'
    success_url = reverse_lazy('catequista_list')
    cancel_url = reverse_lazy('catequista_list')
    title = "Crear Catequista"

class CatequistaUpdateView(UpdateView):
    model = Catequista
    form_class = CatequistaForm
    template_name = 'gestion/Catequistas/catequista_form.html'
    success_url = reverse_lazy('catequista_list')
    cancel_url = reverse_lazy('catequista_list')
    title = "Actualizar Catequista"
    context_object_name = 'catequistas'

class CatequistaDetailView(DetailView):
    model = Catequista
    template_name = 'gestion/Catequistas/catequista_detail.html'
    context_object_name = 'catequista'

class CatequistaDeleteView(DeleteView):
    model = Catequista
    template_name = 'gestion/Catequistas/catequista_delete.html'
    success_url = reverse_lazy('catequista_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('catequista_list')
        context['title'] = "Eliminar Catequista"
        context['view'] = self
        return context
