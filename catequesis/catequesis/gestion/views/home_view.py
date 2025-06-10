from django.shortcuts import render

def home_view(request):
    """
    Vista para la página de inicio de la aplicación.
    Renderiza el template 'home.html'.
    """
    return render(request, 'home.html')