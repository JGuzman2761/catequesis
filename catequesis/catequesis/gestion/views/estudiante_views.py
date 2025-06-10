from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models import Estudiante
from ..forms.estudiante_forms import EstudianteForm

class EstudianteListView(ListView):
    model = Estudiante
    template_name = 'Gestion/Estudiantes/estudiante_list.html'
    context_object_name = 'estudiantes'
    paginate_by = 10  # Opcional, si usas paginación

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super().get_queryset().order_by('apellidos')
        if query:
            queryset = queryset.filter(
                Q(nombres__icontains=query) |
                Q(apellidos__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset


class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = 'Gestion/Estudiantes/estudiante_detail.html'
    context_object_name = 'estudiante'

class EstudianteCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'Gestion/Estudiantes/estudiante_create.html'
    title = 'Crear Estudiante'

    def get_success_url(self):
        return self.request.POST.get('next') or self.request.GET.get('next') or reverse_lazy('estudiante_list')
    
    def get_cancel_url(self):
        return self.request.POST.get('next') or self.request.GET.get('next') or reverse_lazy('estudiante_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        context['cancel_url'] = self.get_cancel_url()
        context['title'] = self.title
        context['view'] = self
        return context

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.creado_por = self.request.user
        form.instance.actualizado_por = self.request.user
        return super().form_valid(form)

class EstudianteUpdateView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'Gestion/Estudiantes/estudiante_create.html'
    title = 'Actualizar estudiante'
    success_url = reverse_lazy('estudiante_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('estudiante_list')
        context['title'] = self.title
        context['view'] = self
        return context

    def form_valid(self, form):
        form.instance.actualizado_por = self.request.user
        return super().form_valid(form)

class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'Gestion/Estudiantes/estudiante_delete.html'
    success_url = reverse_lazy('estudiante_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('estudiante_list')
        context['title'] = 'Eliminar estudiante'
        context['view'] = self
        return context