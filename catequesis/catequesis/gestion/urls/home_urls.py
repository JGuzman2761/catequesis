from django.urls import path
from ..views.home_view import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
]