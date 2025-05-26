from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.models import User
from django.db.models import Q
from ..models import Estudiante, Grupo, Inscripcion
from ..forms import EstudianteForm, GrupoForm, InscripcionForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

class InscripcionListView(ListView):
    model = Inscripcion
    template_name = 'Gestion/Inscripciones/inscripcion_list.html'
    context_object_name = 'inscripciones'
    paginate_by = 10

    def get_queryset(self):
        grupo_id = self.kwargs.get('grupo_id')
        queryset = super().get_queryset().filter(grupo_id=grupo_id)

        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(estudiante__nombres__icontains=query) |
                Q(estudiante__apellidos__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo_id = self.kwargs.get('grupo_id')
        grupo = get_object_or_404(Grupo, pk=grupo_id)
        context['grupo'] = grupo
        context['query'] = self.request.GET.get('q', '')  # Para mantener la búsqueda en el template si quieres
        return context


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo_id = self.kwargs.get('grupo_id')
        context['grupo'] = get_object_or_404(Grupo, pk=grupo_id)
        context['request'] = self.request
        return context

class InscripcionCreateView(CreateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'Gestion/Inscripciones/inscripcion_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo_id = self.kwargs.get('grupo_id')  # Tomamos el grupo_id de la URL
        context['cancel_url'] = reverse_lazy('inscripcion_list', kwargs={'grupo_id': grupo_id})
        context['grupo_id'] = grupo_id
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        grupo_id = self.kwargs.get('grupo_id')
        grupo = get_object_or_404(Grupo, pk=grupo_id)
        kwargs['grupo'] = grupo
        return kwargs

    def form_valid(self, form):
        grupo_id = self.kwargs.get('grupo_id')
        form.instance.grupo_id = grupo_id
        return super().form_valid(form)

    def get_success_url(self):
        grupo_id = self.kwargs.get('grupo_id')
        return reverse_lazy('inscripcion_list', kwargs={'grupo_id': grupo_id})

class InscripcionUpdateView(UpdateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'Gestion/Inscripciones/inscripcion_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        grupo_id = self.kwargs.get('grupo_id')
        grupo = get_object_or_404(Grupo, pk=grupo_id)
        kwargs['grupo'] = grupo
        return kwargs 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grupo_id = self.kwargs.get('grupo_id')
        context['cancel_url'] = reverse_lazy('inscripcion_list', kwargs={'grupo_id': grupo_id})
        context['grupo_id'] = grupo_id
        return context

    def get_success_url(self):
        grupo_id = self.kwargs.get('grupo_id')
        return reverse_lazy('inscripcion_list', kwargs={'grupo_id': grupo_id})

class InscripcionGrupoCardListView(ListView):
    model = Grupo
    template_name = 'Gestion/Inscripciones/grupo_card.html'
    context_object_name = 'grupos'
    paginate_by = 10  # opcional, si tienes muchos grupos

    # Si quieres agregar búsqueda por nombre de grupo (opcional)
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(nombre__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request  # Para mantener el input de búsqueda si usas
        return context

class InscripcionDetailView(DetailView):
    model = Inscripcion
    template_name = 'Gestion/Inscripciones/inscripcion_detail.html'
    context_object_name = 'inscripcion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar el grupo para contexto (por si quieres usarlo en template)
        grupo = self.object.grupo  # asumiendo Inscripcion tiene FK grupo
        context['grupo'] = grupo
        return context

class InscripcionDeleteView(DeleteView):
    model = Inscripcion
    template_name = 'Gestion/Inscripciones/inscripcion_delete.html'

    def get_success_url(self):
        grupo_id = self.object.grupo.id  # obtiene el grupo de la inscripción que se elimina
        return reverse('inscripcion_list', kwargs={'grupo_id': grupo_id})
