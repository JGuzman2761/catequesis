from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from ..models import Grupo, Catequista, CursoAnual # Asegúrate de importar tus modelos
from ..forms import GrupoForm # Asume que GrupoForm está en forms.py
import json # Para pasar datos a JSON en el template

# Asumiendo que tu GrupoForm se ve así (simplificado):
# from django import forms
# class GrupoForm(forms.ModelForm):
#     class Meta:
#         model = Grupo
#         fields = ['curso_anual', 'nombre', 'cupo_maximo', 'catequistas']
#         # No necesitas un widget especial aquí si vas a manejarlo manualmente en el template
#         # Pero si lo dejas, el FilteredSelectMultiple no interferirá si lo ocultas.
#         # widgets = {
#         #     'catequistas': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'5'}),
#         # }

def grupo_form_view(request, pk=None): # Una función para crear y editar
    if pk:
        instance = get_object_or_404(Grupo, pk=pk)
    else:
        instance = None

    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('grupo_list') # Redirige a tu lista de grupos
    else:
        form = GrupoForm(instance=instance)

    # Prepara los datos para el widget de catequistas
    todos_catequistas_qs = Catequista.objects.all()
    
    # Formato: [{id: 1, text: "Nombre Apellido"}, {id: 2, text: "Otro Nombre"}]
    todos_catequistas_data = [
        {"id": cat.id, "text": str(cat)} for cat in todos_catequistas_qs
    ]

    catequistas_seleccionados_ids = []
    if instance:
        catequistas_seleccionados_ids = list(instance.catequistas.all().values_list('id', flat=True))

    context = {
        'form': form,
        'todos_catequistas_json': json.dumps(todos_catequistas_data),
        'catequistas_seleccionados_ids_json': json.dumps(catequistas_seleccionados_ids),
        # 'object': instance # Si tu template lo usa para el título
    }
    return render(request, 'tu_app/grupo_form_template.html', context)


# O si prefieres Class-Based Views (CBV):

class GrupoCreateView(CreateView):
    model = Grupo
    form_class = GrupoForm
    template_name = 'Gestion/Grupos/grupo_create.html' # Tu template adaptado
    success_url = reverse_lazy('grupo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todos_catequistas_qs = Catequista.objects.all()
        todos_catequistas_data = [{"id": cat.id, "text": str(cat)} for cat in todos_catequistas_qs]
        
        context['todos_catequistas_json'] = json.dumps(todos_catequistas_data)
        context['catequistas_seleccionados_ids_json'] = json.dumps([]) # Para Create, no hay seleccionados
        return context

class GrupoUpdateView(UpdateView):
    model = Grupo
    form_class = GrupoForm
    template_name = 'Gestion/Grupos/grupo_create.html'
    success_url = reverse_lazy('grupo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        todos_catequistas_qs = Catequista.objects.all()
        todos_catequistas_data = [{"id": cat.id, "text": str(cat)} for cat in todos_catequistas_qs]
        
        seleccionados_ids = []
        if self.object: # self.object es la instancia del Grupo que se está editando
            seleccionados_ids = list(self.object.catequistas.all().values_list('id', flat=True))
            
        context['todos_catequistas_json'] = json.dumps(todos_catequistas_data)
        context['catequistas_seleccionados_ids_json'] = json.dumps(seleccionados_ids)
        return context

class GrupoDeleteView(DeleteView):
    model = Grupo
    template_name = 'Gestion/Grupos/grupo_delete.html'
    success_url = reverse_lazy('grupo_list')

class GrupoListView(ListView):
    model = Grupo
    template_name = 'Gestion/Grupos/grupo_list.html'
    context_object_name = 'grupos'

    def get_queryset(self):
        queryset = super().get_queryset()
        curso_id = self.request.GET.get('curso')
        if curso_id:
            queryset = queryset.filter(curso_anual__id=curso_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cursos'] = CursoAnual.objects.all()
        context['curso_id'] = self.request.GET.get('curso', '')
        return context

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = 'Gestion/Grupos/grupo_detail.html'
    context_object_name = 'grupo'

