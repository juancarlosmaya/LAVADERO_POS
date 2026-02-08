from django.forms import model_to_dict
from django.test import Client
from Servidor.models import Servicio, Orden, Vehiculo, Cliente, Lavadero, Operario_lavado
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from .forms import loginFormulario, OrdenForm, VehiculoForm, ClienteForm, OperarioLavadoForm
import requests
import json

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    grupo_usuario = request.user.groups.first()  # Obtiene el primer grupo del usuario
    nombre_grupo_usuario = grupo_usuario.name if grupo_usuario else ""  # Extrae el nombre
    
    lavadero_sesion = Lavadero.objects.get(nombre= request.user.perfil_usuarios.lavadero.nombre)
    print("Lavadero dash de la sesión:", lavadero_sesion)
    return render(request, 'Cliente/dashboard.html', {'lavadero': lavadero_sesion, 'nombre_grupo_usuario': nombre_grupo_usuario})

def vista_test_bluetooth(request):
    return render(request, 'Cliente/impresion_test_ble.html')

def crear_orden(request):
    lavadero_sesion = Lavadero.objects.get(nombre= request.user.perfil_usuarios.lavadero.nombre)
    print("Lavadero de la sesión:", lavadero_sesion)
    if not request.user.is_authenticated:
        return redirect('login')
    
    grupo_usuario = request.user.groups.first()  # Obtiene el primer grupo del usuario
    nombre_grupo_usuario = grupo_usuario.name if grupo_usuario else ""  # Extrae el nombre

    if request.method == 'POST':
        print("datos recibidos en POST:", request.POST)
        vehiculo_form = VehiculoForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        orden_form = OrdenForm(request.POST)
        operario_lavado_form = OperarioLavadoForm(request.POST)
        servicios_ids = request.POST.getlist('servicios')
        if vehiculo_form.is_valid() and cliente_form.is_valid() and orden_form.is_valid() and operario_lavado_form.is_valid() and servicios_ids:
            print("formularios validos")
            # Obtener o crear cliente
            cliente, _ = Cliente.objects.get_or_create(
                celular=cliente_form.cleaned_data['celular'],
                nombre=(cliente_form.cleaned_data.get('nombre') or '').strip().upper(),
                fecha_registro=timezone.now(),
                lavadero=lavadero_sesion
            )
            
            # Obtener o crear vehículo
            vehiculo, _ = Vehiculo.objects.get_or_create(
                placa=(vehiculo_form.cleaned_data.get('placa') or '').strip().upper(),
                tipo= vehiculo_form.cleaned_data['tipo'],
                marca=(vehiculo_form.cleaned_data.get('marca') or '').strip().upper(),
                modelo= (vehiculo_form.cleaned_data.get('modelo') or '').strip().upper(),
                cliente= cliente,
                lavadero=lavadero_sesion
            )
            # Obtener o crear operario de lavado (similar a Vehiculo)
            operario_nombre = (operario_lavado_form.cleaned_data.get('nombre_operario') or '').strip()
            operario, _ = Operario_lavado.objects.get_or_create(
                nombre_operario=operario_nombre,
                lavadero_operario=lavadero_sesion,
                defaults={
                    'celular_operario': '',
                    'correo_operario': None,
                }
            )
            print("EL NOMBRE DEL OPERARIO ES:", operario.nombre_operario)

            # Crear orden
            orden = orden_form.save(commit=False)
            orden.vehiculo = vehiculo
            orden.cliente = cliente
            orden.lavadero = lavadero_sesion
            orden.operario_lavado = operario
            orden.save()
            
            # Agregar servicios
            orden.servicios.set(servicios_ids)
            server_sms="https://mensajeriaremota.pythonanywhere.com/APIMensaje/"
            numero_telefonico ="+57"+cliente.celular
            message = f"Hola {cliente.nombre}, tu orden #{orden.id} ha sido creada exitosamente. Gracias por elegirnos. {lavadero_sesion.nombre}."
            nuevo_mensaje = {'estado': 'PENDIENTE', 'numero_telefonico': numero_telefonico, 'mensaje': message}
            response = requests.post(server_sms, data=json.dumps(nuevo_mensaje), headers={"Content-Type": "application/json"})
            print("Respuesta del servidor SMS:", response.text)
            print("message enviado:", message )
            print("Número telefónico:", numero_telefonico )
            
            metadatos = model_to_dict(orden)
            #print("metadatos antes de modificar:", metadatos)
            metadatos['vehiculo'] = orden.vehiculo.tipo
            metadatos['cliente'] = orden.cliente.nombre
            metadatos['tiempo_inicio_servicio'] = orden.tiempo_inicio_servicio.strftime("%H:%M:%S") if orden.tiempo_inicio_servicio else ""
            metadatos['fecha_creacion'] = orden.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
            metadatos['servicios'] = [servicio.nombre for servicio in orden.servicios.all()]
            print("metadatos después de modificar:", metadatos)
            message = f"Hola, tu orden #{orden.id} - {orden.vehiculo.tipo} ha finalizado, pasa por tu vehiculo en {lavadero_sesion.nombre}. Tienes 30 minutos antes de cobro de parqueadero adicional. Gracias por tu confianza."
            nuevo_mensaje = {'estado': 'PENDIENTE', 'numero_telefonico': numero_telefonico, 'mensaje': message, 'metadatos': metadatos}
            response = requests.post(server_sms, data=json.dumps(nuevo_mensaje), headers={"Content-Type": "application/json"})
            print("Respuesta del servidor SMS:", response.text)
            print("message enviado:", message )
            print("Número telefónico:", numero_telefonico )
            return redirect('ticket_orden', orden_id=orden.id)
    else:
        vehiculo_form = VehiculoForm()
        cliente_form = ClienteForm()
        orden_form = OrdenForm()
        operario_lavado_form = OperarioLavadoForm()
    
    servicios_sesion = Servicio.objects.filter(lavadero = request.user.perfil_usuarios.lavadero)
    #print(request.user.perfil_usuarios.lavadero)
    #print("Servicios del lavadero en sesión:", servicios_sesion)

    #Servicio.objects.get(lavadero= request.user.perfil_usuarios.lavadero.nombre)
    #servicios = Servicio.objects.filter(activo=True)
    
    # Organizar servicios por categoría
    servicios_por_categoria = {}
    for servicio in servicios_sesion:
        if servicio.categoria not in servicios_por_categoria:
            servicios_por_categoria[servicio.categoria] = []
        servicios_por_categoria[servicio.categoria].append(servicio)

    operarios_sesion = Operario_lavado.objects.filter(lavadero_operario = request.user.perfil_usuarios.lavadero)
    
    return render(request, 'Cliente/nueva_orden.html', {
        'vehiculo_form': vehiculo_form,
        'cliente_form': cliente_form,
        'orden_form': orden_form,
        'servicios': servicios_sesion,
        'servicios_por_categoria': servicios_por_categoria,
        'lavadero': lavadero_sesion,
        'nombre_grupo_usuario': nombre_grupo_usuario,
        'operario_lavado_form': operario_lavado_form,
        'operarios': operarios_sesion    
    })

def ticket_orden(request, orden_id):
    if not request.user.is_authenticated:
        return redirect('login')
    orden = Orden.objects.get(id=orden_id)
    lavadero_sesion = Lavadero.objects.get(nombre= request.user.perfil_usuarios.lavadero.nombre)
    return render(request, 'Cliente/ticket_orden.html', {'orden': orden, 'lavadero': lavadero_sesion})

def estado_servicios(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    lavadero_sesion = Lavadero.objects.get(nombre= request.user.perfil_usuarios.lavadero.nombre)
    print("Lavadero de la sesión:", lavadero_sesion)
    
    grupo_usuario = request.user.groups.first()  # Obtiene el primer grupo del usuario
    nombre_grupo_usuario = grupo_usuario.name if grupo_usuario else ""  # Extrae el nombre
    
    periodo = request.GET.get('periodo', 'dia')
    hoy = timezone.localtime(timezone.now()).date()
    
    # Definir fecha de inicio según periodo
    if periodo == 'semana':
        fecha_inicio = hoy - timedelta(days=7)
        titulo_periodo = "Última Semana"
    elif periodo == 'mes':
        fecha_inicio = hoy - timedelta(days=30)
        titulo_periodo = "Último Mes"
    elif periodo == 'anio':
        fecha_inicio = hoy - timedelta(days=365)
        titulo_periodo = "Último Año"
    else:
        fecha_inicio = hoy
        titulo_periodo = "Día Actual"

    ordenes = lavadero_sesion.ordenes.filter(fecha_creacion__date__gte=fecha_inicio).prefetch_related('servicios', 'vehiculo', 'cliente').order_by('-fecha_creacion')
    
    total_periodo = 0
    for orden in ordenes:
        orden.total_calculado = sum(s.precio for s in orden.servicios.all())
        total_periodo += orden.total_calculado
        
    return render(request, 'Cliente/estado_servicios.html', {
        'ordenes': ordenes,
        'total_dia': total_periodo,
        'fecha': hoy,
        'titulo': titulo_periodo,
        'periodo': periodo,
        'lavadero': lavadero_sesion,
        'nombre_grupo_usuario': nombre_grupo_usuario
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        formulario = loginFormulario(request.POST)
        if formulario.is_valid():
            nombreUsuario = formulario.cleaned_data['nombreUsuario']
            contrasenaUsuario = formulario.cleaned_data['contrasenaUsuario']
            usuario = authenticate(request, username = nombreUsuario, password = contrasenaUsuario)
            if usuario is not None:
                login(request, usuario)
                return redirect('dashboard')
            else:
                formulario.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        formulario = loginFormulario()
    return render(request, 'Cliente/login.html', {'formulario': formulario})

def eliminar_orden(request, orden_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    lavadero_sesion = Lavadero.objects.get(nombre= request.user.perfil_usuarios.lavadero.nombre)
    print("Lavadero de la sesión:", lavadero_sesion)
    
    grupo_usuario = request.user.groups.first()  # Obtiene el primer grupo del usuario
    nombre_grupo_usuario = grupo_usuario.name if grupo_usuario else ""  # Extrae el nombre
    
    if nombre_grupo_usuario != "administrador":
        return redirect('estado_servicios')
    
    try:
        orden = Orden.objects.get(id=orden_id, lavadero=lavadero_sesion)
        orden.delete()
    except Orden.DoesNotExist:
        pass
    
    return redirect('estado_servicios')

def logout_view(request):
    logout(request)
    return redirect('login')