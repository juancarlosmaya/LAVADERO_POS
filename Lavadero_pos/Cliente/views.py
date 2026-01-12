from Servidor.models import Servicio, Orden
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

def dashboard(request):
    return render(request, 'Cliente/dashboard.html')

def vista_test_bluetooth(request):
    return render(request, 'Cliente/impresion_test_ble.html')

def crear_orden(request):
    servicios = Servicio.objects.filter(activo=True)
    return render(request, 'Cliente/nueva_orden.html', {'servicios': servicios})

def ticket_orden(request, orden_id):
    orden = Orden.objects.get(id=orden_id)
    return render(request, 'Cliente/ticket_orden.html', {'orden': orden})

def estado_servicios(request):
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

    ordenes = Orden.objects.filter(fecha_creacion__date__gte=fecha_inicio).prefetch_related('servicios', 'vehiculo', 'cliente').order_by('-fecha_creacion')
    
    total_periodo = 0
    for orden in ordenes:
        orden.total_calculado = sum(s.precio for s in orden.servicios.all())
        total_periodo += orden.total_calculado
        
    return render(request, 'Cliente/estado_servicios.html', {
        'ordenes': ordenes,
        'total_dia': total_periodo,
        'fecha': hoy,
        'titulo': titulo_periodo,
        'periodo_actual': periodo
    })
