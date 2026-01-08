from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Vehiculo, Servicio, Orden, Pago
from .serializers import (
    ClienteSerializer, 
    VehiculoSerializer, 
    ServicioSerializer, 
    OrdenSerializer, 
    PagoSerializer
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class OrdenViewSet(viewsets.ModelViewSet):
    queryset = Orden.objects.all()
    serializer_class = OrdenSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

def vista_test_bluetooth(request):
    return render(request, 'aplicacion_pos/impresion_test_ble.html')
