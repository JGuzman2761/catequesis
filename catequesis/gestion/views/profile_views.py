# gestion/views/profile_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout # Importar la función logout
from gestion.forms.profile_forms import ProfileUpdateForm

@login_required
def profile_update_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Redirigir a una página de éxito o al mismo perfil
            return redirect('profile_detail') # Asume que tendrás una URL 'profile_detail'
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'Gestion/Profile/profile_form.html', {'form': form})

# Puedes agregar una vista para mostrar el detalle del perfil si es necesario
# @login_required
# def profile_detail_view(request):
#     return render(request, 'Gestion/Profile/profile_detail.html', {'user': request.user})

@login_required
def logout_confirm_view(request):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            logout(request)
            return redirect('home') # Redirigir a la página de inicio después del logout
        else:
            return redirect('home') # Redirigir a la página de inicio si no se confirma
    return render(request, 'registration/logout_confirm.html') # Renderizar plantilla de confirmación