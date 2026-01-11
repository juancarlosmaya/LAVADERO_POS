from Servidor.models import Servicio, Orden
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

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
    # Aseguramos que tomamos la fecha local de Bogotá
    hoy = timezone.localtime(timezone.now()).date()
    ordenes_hoy = Orden.objects.filter(fecha_creacion__date=hoy).prefetch_related('servicios', 'vehiculo')
    
    # Calcular totales manual o con aggregate
    total_dia = 0
    for orden in ordenes_hoy:
        orden.total_calculado = sum(s.precio for s in orden.servicios.all())
        total_dia += orden.total_calculado
        
    return render(request, 'Cliente/estado_servicios.html', {
        'ordenes': ordenes_hoy,
        'total_dia': total_dia,
        'fecha': hoy
    })
