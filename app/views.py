import json
import requests

from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password']

        data = {'email': email}
        # Realiza una solicitud a la API para obtener la contraseña almacenada
        api_url = 'https://galenos.samgarrido.repl.co/api/pacientes/login'
        response = requests.post(api_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        print(f"API URL: {api_url}")
        print(f"Request: {response.request.url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")
        if response.status_code == 200:
            stored_password = response.json().get('password', '')
           
            if check_password(password, stored_password) and email == 'admin@admin.cl':
                # Contraseña válida, permite el inicio de sesión
                return redirect(to='administrador')
            elif check_password(password, stored_password):
                return redirect(to='paciente')
            else:
                # Contraseña incorrecta
                return JsonResponse({'mensaje': 'Contraseña incorrecta'})
        else:
            # Usuario no encontrado o error en la API
            return JsonResponse({'mensaje': 'Usuario no encontrado'})

    return render(request, 'pac/login.html')

def register(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        nombre = request.POST.get('nombre', None)
        email = request.POST.get('email', None).strip()
        password = request.POST.get('password', None)

        if rut is not None and nombre is not None and email is not None and password is not None:
            # Hashea la contraseña
            hashed_password = make_password(password)

            # Crea un diccionario con los datos del usuario
            user_data = {
                'rut_pac': rut,
                'nom_pac': nombre,
                'email': email,
                'contraseña': hashed_password  # Asegúrate de que el campo coincida con tu API
            }

            # Envia los datos a la API en formato JSON
            api_url = 'https://galenos.samgarrido.repl.co/api/pacientes/add'  # Reemplaza con la URL de tu API
            response = requests.post(api_url, data=json.dumps(user_data), headers={'Content-Type': 'application/json'})
            print(f"API URL: {api_url}")
            print(f"Request: {response.request.url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content}")
            if response.status_code == 201:
                return redirect(to='login')
            else:
                return JsonResponse({'mensaje': 'Error al registrar usuario'})

    return render(request, 'pac/register.html')

def recuperar(request):
    return render(request, 'pac/recuperar.html')

def get_nombres_medicos():
    api_url = 'https://galenos.samgarrido.repl.co/api/medicos/'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        nombres_medicos = [(medico['rut_med'], medico['nom_med']) for medico in data]
        return nombres_medicos
    else:
        return []
    
def get_horas(rut_med, fecha):

    data = {'rut_med': rut_med,
            'fecha': fecha}

    api_url = 'https://galenos.samgarrido.repl.co/api/agendas/horas'

    response = requests.post(api_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        data = response.json()
        horas_disponibles = [(horas['horas']) for horas in data]
        return horas_disponibles
    else:
        return []
    
def hora(request):
    nombres_medicos = get_nombres_medicos()



    return render(request, 'pac/hora.html', {'nombres_medicos': nombres_medicos})


def administrador(request):
    return render(request, 'admin/administrador.html')

def gestionar_med(request):
    api_url = 'https://galenos.samgarrido.repl.co/api/medicos/'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        nombres_medicos = [(medico['rut_med'], medico['nom_med'], medico['email']) for medico in data]
        return render(request, 'admin/gestionar_med.html', {'nombres_medicos': nombres_medicos})
    else:
        return render(request, 'admin/gestionar_med.html', [])
    
def gestionar_sec(request):
    api_url = 'https://galenos.samgarrido.repl.co/api/secretarias/'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        secretarias = [(sec['rut_sec'], sec['nom_sec'], sec['email']) for sec in data]
        return render(request, 'admin/gestionar_sec.html', {'secretarias': secretarias})
    else:
        return render(request, 'admin/gestionar_sec.html', [])


def gestionar_pac(request):
    api_url = 'https://galenos.samgarrido.repl.co/api/pacientes/'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        pacientes = [(pac['rut_pac'], pac['nom_pac'], pac['email']) for pac in data]
        return render(request, 'admin/gestionar_pac.html', {'pacientes': pacientes})
    else:
        return render(request, 'admin/gestionar_pac.html', [])

def registrar_med(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        nombre = request.POST.get('nombre', None)
        email = request.POST.get('email', None).strip()
        password = request.POST.get('password', None)

        if rut is not None and nombre is not None and email is not None and password is not None:
            # Hashea la contraseña
            hashed_password = make_password(password)

            # Crea un diccionario con los datos del usuario
            user_data = {
                'rut_med': rut,
                'nom_med': nombre,
                'email': email,
                'contraseña': hashed_password  # Asegúrate de que el campo coincida con tu API
            }

            # Envia los datos a la API en formato JSON
            api_url = 'https://galenos.samgarrido.repl.co/api/medicos/add'  # Reemplaza con la URL de tu API
            response = requests.post(api_url, data=json.dumps(user_data), headers={'Content-Type': 'application/json'})
            print(f"API URL: {api_url}")
            print(f"Request: {response.request.url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content}")
            if response.status_code == 201:
                return JsonResponse({'mensaje': 'Medico registrado con exito'})
            else:
                return JsonResponse({'mensaje': 'Error al registrar medico'})

    return render(request, 'admin/registrar_med.html')

def registrar_sec(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        nombre = request.POST.get('nombre', None)
        email = request.POST.get('email', None).strip()
        password = request.POST.get('password', None)

        if rut is not None and nombre is not None and email is not None and password is not None:
            # Hashea la contraseña
            hashed_password = make_password(password)

            # Crea un diccionario con los datos del usuario
            user_data = {
                'rut_sec': rut,
                'nom_sec': nombre,
                'email': email,
                'contraseña': hashed_password  # Asegúrate de que el campo coincida con tu API
            }

            # Envia los datos a la API en formato JSON
            api_url = 'https://galenos.samgarrido.repl.co/api/secretarias/add'  # Reemplaza con la URL de tu API
            response = requests.post(api_url, data=json.dumps(user_data), headers={'Content-Type': 'application/json'})
            print(f"API URL: {api_url}")
            print(f"Request: {response.request.url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.content}")
            if response.status_code == 201:
                return JsonResponse({'mensaje': 'Secretaria registrado con exito'})
            else:
                return JsonResponse({'mensaje': 'Error al registrar secretaria'})

    return render(request, 'admin/registrar_sec.html')


@csrf_exempt
def login_medico(request):
    if request.method == 'POST':
        email = request.POST['email'].strip()
        password = request.POST['password']

        data = {'email': email}
        # Realiza una solicitud a la API para obtener la contraseña almacenada
        api_url = 'https://galenos.samgarrido.repl.co/api/medicos/login'
        response = requests.post(api_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        print(f"API URL: {api_url}")
        print(f"Request: {response.request.url}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")
        if response.status_code == 200:
            stored_password = response.json().get('password', '')
           
            if check_password(password, stored_password) and email == 'admin@admin.cl':
                # Contraseña válida, permite el inicio de sesión
                return redirect(to='administrador')
            elif check_password(password, stored_password):
                return redirect(to='medico')
            else:
                # Contraseña incorrecta
                return JsonResponse({'mensaje': 'Contraseña incorrecta'})
        else:
            # Usuario no encontrado o error en la API
            return JsonResponse({'mensaje': 'Medico no encontrado'})

    return render(request, 'med/login_medico.html')

def medico(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        data = {'rut_med': rut}
        api_url = 'https://galenos.samgarrido.repl.co/api/agendas/allfechas'

        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = response.json()
            agendas = [(agen['fecha'], agen['hora'], agen['disponibilidad']) for agen in data]
            print("Agendas:", agendas)
            return render(request, 'med/medico.html', {'agendas': agendas})
        else:
            print("aaa")
            return render(request, 'med/medico.html')

    return render(request, 'med/medico.html')

def gestionar(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        fecha = request.POST.get('fecha', None)
        hora = request.POST.get('hora', None)

        if rut is not None and fecha is not None and hora is not None:

            # Crea un diccionario con los datos de agenda
            user_data = {
                'fecha': fecha,
                'hora': hora,
                'rut_med': rut,
                'disponibilidad' : True
            }

            # Envia los datos a la API en formato JSON
            api_url = 'https://galenos.samgarrido.repl.co/api/agendas/add'  # Reemplaza con la URL de tu API
            response = requests.post(api_url, data=json.dumps(user_data), headers={'Content-Type': 'application/json'})

            if response.status_code == 201:
                return redirect(to='medico')
            else:
                return JsonResponse({'mensaje': 'Error al registrar dia'})
    return render(request, 'med/gestionar.html')

def paciente(request):
    return render(request, 'pac/paciente.html')