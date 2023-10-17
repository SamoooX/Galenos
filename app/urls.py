from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('recuperar/', views.recuperar, name="recuperar"),
    path('hora/', views.hora, name="hora"),
    path('gestionar/', views.gestionar, name="gestionar"),
    path('medico/', views.medico, name="medico"),
]

