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
    success_url = reverse_lazy('estudiante_list')
    cancel_url = reverse_lazy('estudiante_list')
    title = 'Crear Estudiante'

class EstudianteUpdateView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'Gestion/Estudiantes/estudiante_create.html'
    success_url = reverse_lazy('estudiante_list')
    cancel_url = reverse_lazy('estudiante_list')
    title = 'Actualizar estudiante'

class EstudianteDeleteView(DeleteView):
    model = Estudiante
    template_name = 'Gestion/Estudiantes/estudiante_delete.html'
    success_url = reverse_lazy('gestion:estudiante_list')