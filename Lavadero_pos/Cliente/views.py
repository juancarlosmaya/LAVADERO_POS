from django.shortcuts import render
from Servidor.models import Servicio

def dashboard(self):
    return render(self, 'Cliente/dashboard.html')

def vista_test_bluetooth(request):
    return render(request, 'Cliente/impresion_test_ble.html')

def crear_orden(request):
    servicios = Servicio.objects.filter(activo=True)
    return render(request, 'Cliente/nueva_orden.html', {'servicios': servicios})
