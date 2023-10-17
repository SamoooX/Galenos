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
    path('administrador/', views.administrador, name="administrador"),
    path('gestionar_med/', views.gestionar_med, name="gestionar_med"),
    path('gestionar_sec/', views.gestionar_sec, name="gestionar_sec"),
    path('gestionar_pac/', views.gestionar_pac, name="gestionar_pac"),
    path('registrar_sec/', views.registrar_sec, name="registrar_sec"),
    path('registrar_med/', views.registrar_med, name="registrar_med"),
    path('login_medico/', views.login_medico, name="login_medico"),
]

