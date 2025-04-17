from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Parroquia, Catequista, Padre,Padrino
from .forms import ParroquiaForm, CatequistaForm , PadreForm, PadrinoForm

from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')


class ParroquiaListView(ListView):
    model = Parroquia
    template_name = 'Gestion/Parroquias/parroquia_list.html'
    context_object_name = 'parroquias'

class ParroquiaDetailView(DetailView):
    model = Parroquia
    template_name = 'Gestion/Parroquias/parroquia_detail.html'

class ParroquiaCreateView(CreateView):
    model = Parroquia
    fields = '__all__'
    template_name = 'Gestion/Parroquias/parroquia_form.html'
    success_url = reverse_lazy('parroquia_list')
    cancel_url = reverse_lazy('parroquia_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('parroquia_list')
        context['title'] = "Registrar Parroquia"
        return context

class ParroquiaUpdateView(UpdateView):
    model = Parroquia
    form_class = ParroquiaForm
    template_name = 'Gestion/Parroquias/parroquia_form.html'
    success_url = reverse_lazy('parroquia_list')

class ParroquiaDeleteView(DeleteView):
    model = Parroquia
    template_name = 'Gestion/Parroquias/parroquia_confirm_delete.html'
    success_url = reverse_lazy('parroquia_list')

# Catequistas

class CatequistaListView(ListView):
    model = Catequista
    template_name = 'gestion/Catequistas/catequista_list.html'
    context_object_name = 'catequistas'

class CatequistaCreateView(CreateView):
    model = Catequista
    fields = '__all__'
    template_name = 'Gestion/catequistas/catequista_form.html'
    success_url = reverse_lazy('catequista_list')
    cancel_url = reverse_lazy('catequista_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('catequista_list')
        context['title'] = "Registrar Catequista"
        return context

class CatequistaUpdateView(UpdateView):
    model = Catequista
    form_class = CatequistaForm
    template_name = 'gestion/Catequistas/catequista_form.html'
    success_url = reverse_lazy('catequista_list')

class CatequistaDetailView(DetailView):
    model = Catequista
    template_name = 'gestion/Catequistas/catequista_detail.html'
    context_object_name = 'object'  

class CatequistaDeleteView(DeleteView):
    model = Catequista
    template_name = 'gestion/Catequistas/catequista_confirm_delete.html'
    success_url = reverse_lazy('catequista_list')

# Padres

class PadreListView(ListView):
    model = Padre
    template_name = 'Gestion/Padres/padre_list.html'

class PadreCreateView(CreateView):
    model = Padre
    form_class = PadreForm
    template_name = 'Gestion/Padres/padre_form.html'
    success_url = reverse_lazy('padre_list')
    cancel_url = reverse_lazy('padre_list')

class PadreUpdateView(UpdateView):
    model = Padre
    form_class = PadreForm
    template_name = 'Gestion/Padres/padre_form.html'
    success_url = reverse_lazy('padre_list')

class PadreDetailView(DetailView):
    model = Padre
    template_name = 'Gestion/Padres/padre_detail.html'

class PadreDeleteView(DeleteView):
    model = Padre
    template_name = 'Gestion/Padres/padre_confirm_delete.html'
    success_url = reverse_lazy('padre_list')
# Padrinos

class PadrinoListView(ListView):
    model = Padrino
    template_name = 'Gestion/padrinos/padrino_list.html'

class PadrinoCreateView(CreateView):
    model = Padrino
    form_class = PadrinoForm
    template_name = 'Gestion/padrinos/padrino_form.html'
    success_url = reverse_lazy('padrino_list')

class PadrinoUpdateView(UpdateView):
    model = Padrino
    form_class = PadrinoForm
    template_name = 'Gestion/padrinos/padrino_form.html'
    success_url = reverse_lazy('padrino_list')

class PadrinoDeleteView(DeleteView):
    model = Padrino
    template_name = 'Gestion/padrinos/padrino_confirm_delete.html'
    success_url = reverse_lazy('padrino_list')

class PadrinoDetailView(DetailView):
    model = Padrino
    template_name = 'Gestion/padrinos/padrino_detail.html'
