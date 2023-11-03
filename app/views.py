import json
import requests

from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.core.mail import send_mail
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
        password2 = request.POST.get('password2', None)

        if rut is not None and nombre is not None and email is not None and password is not None and password == password2:
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
        else:
            mensaje_error = "Las contraseñas no coinciden."
            print("hola")
            return render(request, 'pac/register.html', {'mensaje_error': mensaje_error})

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
        password2 = request.POST.get('password2', None)

        if rut is not None and nombre is not None and email is not None and password is not None and password == password2:
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
        else:
            mensaje_error = "Las contraseñas no coinciden."
            print("hola")
            return render(request, 'admin/registrar_med.html', {'mensaje_error': mensaje_error})

    return render(request, 'admin/registrar_med.html')

def registrar_sec(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        nombre = request.POST.get('nombre', None)
        email = request.POST.get('email', None).strip()
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if rut is not None and nombre is not None and email is not None and password is not None and password == password2:
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
        else:
            mensaje_error = "Las contraseñas no coinciden."
            print("hola")
            return render(request, 'admin/registrar_sec.html', {'mensaje_error': mensaje_error})

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
            agendas = [(agenda['fecha'], agenda['hora'], agenda['disponibilidad'], rut) for agenda in data]
            print("Agendas:", agendas)
            return render(request, 'med/medico.html', {'agendas': agendas, 'rut_consulta': rut})
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

def secretaria(request):
    return render(request, 'sec/secretaria.html')

def gestionarAtencion(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        data = {'rut_pac': rut}
        api_url = 'https://galenos.samgarrido.repl.co/api/atenciones/allatenciones'

        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = response.json()
            agendas = [(agenda['fecha'], agenda['hora'], agenda['rut_med'], agenda['rut_pac'], agenda['rut_sec'], agenda['costo'], agenda['estado'], agenda['cancelado']) for agenda in data]
            print("Agendas:", agendas)
            return render(request, 'sec/gestionarAtencion.html', {'agendas': agendas})
        else:
            print("aaa")
            return render(request, 'sec/gestionarAtencion.html')
    return render(request, 'sec/gestionarAtencion.html')

def gestionarAgenda(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        data = {'rut_med': rut}
        api_url = 'https://galenos.samgarrido.repl.co/api/agendas/allfechas'

        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = response.json()
            agendas = [(agenda['fecha'], agenda['hora'], agenda['disponibilidad'], rut) for agenda in data]
            print("Agendas:", agendas)
            return render(request, 'sec/gestionarAgenda.html', {'agendas': agendas, 'rut_consulta': rut})
        else:
            print("aaa")
            return render(request, 'sec/gestionarAgenda.html')
    return render(request, 'sec/gestionarAgenda.html')

def obtener_feriados():
    # Hacer una solicitud GET a la API de feriados y obtener la lista de feriados en formato JSON
    api_url = 'https://apis.digital.gob.cl/fl/feriados/2023'
    response = requests.get(api_url)
    if response.status_code == 200:
        feriados = response.json()
    else:
        feriados = []

    # Extraer las fechas de los feriados
    fechas_feriados = [feriado['fecha'] for feriado in feriados]

    return fechas_feriados

def generarAgenda(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        if rut is not None:
            # Obten la fecha de inicio (hoy)
            fecha_inicio = datetime.now()
            
            # Calcula la fecha de finalización, 3 meses a partir de hoy
            fecha_fin = fecha_inicio + timedelta(days=16)
            
            # Inicializa una lista para almacenar los datos de agenda
            agenda_data = []
            
            fechas_feriados = obtener_feriados()
            
            while fecha_inicio <= fecha_fin:
                # Verifica si la fecha es un día laborable (lunes a viernes)
                if fecha_inicio.weekday() < 5 and fecha_inicio.strftime('%Y-%m-%d') not in fechas_feriados:
                    # Crea un rango horario de 8 AM a 5 PM con intervalos de 1 hora
                    hora_inicio = datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day, 8, 0)
                    hora_fin = datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day, 11, 0)
                    while hora_inicio < hora_fin:
                        agenda_data.append({
                            'fecha': fecha_inicio.strftime('%Y-%m-%d'),
                            'hora': hora_inicio.strftime('%H:%M'),
                            'rut_med': rut,
                            'disponibilidad': True
                        })
                        hora_inicio += timedelta(hours=1)

                fecha_inicio += timedelta(days=1)
            
            # Envia los datos a la API en formato JSON
            api_url = 'https://galenos.samgarrido.repl.co/api/agendas/add'  # Reemplaza con la URL de tu API
            for agenda_entry in agenda_data:
                response = requests.post(api_url, data=json.dumps(agenda_entry), headers={'Content-Type': 'application/json'})
                if response.status_code != 201:
                    return JsonResponse({'mensaje': 'Error al registrar la agenda'})

            return redirect(to='secretaria')
    
    return render(request, 'sec/generarAgenda.html')

def agregarAtencion(request):
    nombres_medicos = get_nombres_medicos()
    return render(request, 'sec/agregarAtencion.html', {'nombres_medicos': nombres_medicos})


def gestionarHoras(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        data = {'rut_pac': rut}
        api_url = 'https://galenos.samgarrido.repl.co/api/atenciones/allatenciones'

        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = response.json()
            agendas = [(agenda['fecha'], agenda['hora'], agenda['rut_med'], agenda['rut_pac'], agenda['rut_sec'], agenda['costo'], agenda['estado'], agenda['cancelado']) for agenda in data]
            print("Agendas:", agendas)
            return render(request, 'pac/gestionarHoras.html', {'agendas': agendas})
        else:
            print("aaa")
            return render(request, 'pac/gestionarHoras.html')
    return render(request, 'pac/gestionarHoras.html')

def medAtencion(request):
    if request.method == 'POST':
        rut = request.POST.get('rut', None).strip()
        data = {'rut_med': rut}
        api_url = 'https://galenos.samgarrido.repl.co/api/atenciones/allatencionesmed'

        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = response.json()
            agendas = [(agenda['fecha'], agenda['hora'], agenda['rut_med'], agenda['rut_pac'], agenda['rut_sec'], agenda['costo'], agenda['estado'], agenda['cancelado']) for agenda in data]
            print("Agendas:", agendas)
            return render(request, 'med/medAtencion.html', {'agendas': agendas})
        else:
            print("aaa")
            return render(request, 'med/medAtencion.html')
    return render(request, 'med/medAtencion.html')

def enviar_correo_hora_fecha(fecha, hora, email_destino):
    subject = 'Registro de Atención'
    message = f'Se ha registrado una atención para la fecha {fecha} a las {hora}.'
    from_email = 'tu_correo@gmail.com'  # Remplaza con tu dirección de correo
    recipient_list = [email_destino]  # Lista de destinatarios

    try:
        send_mail(subject, message, from_email, recipient_list)
        return True
    except Exception as e:
        print(f'Error al enviar el correo: {str(e)}')
        return False