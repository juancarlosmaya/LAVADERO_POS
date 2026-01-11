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

    def create(self, request, *args, **kwargs):
        # Extraer datos extendidos Enviados desde el formulario
        placa = request.data.get('placa')
        tipo_vehiculo = request.data.get('tipo_vehiculo', 'CARRO')
        celular = request.data.get('celular')
        nombre_cliente = request.data.get('nombre_cliente', '')
        servicios_ids = request.data.get('servicios', [])
        observaciones = request.data.get('observaciones', '')
        marca = request.data.get('marca', '')
        modelo = request.data.get('modelo', '')

        if not placa or not servicios_ids:
            from rest_framework.response import Response
            return Response({"error": "Placa y servicios son obligatorios"}, status=400)

        # 1. Buscar o Crear Cliente (si hay celular)
        cliente = None
        if celular:
            cliente, created = Cliente.objects.get_or_create(celular=celular)
            if nombre_cliente and (created or not cliente.nombre):
                cliente.nombre = nombre_cliente
                cliente.save()

        # 2. Buscar o Crear Vehículo
        vehiculo, created_v = Vehiculo.objects.get_or_create(
            placa=placa,
            defaults={'tipo': tipo_vehiculo, 'cliente': cliente, 'marca': marca, 'modelo': modelo}
        )
        
        # Si el vehículo ya existía, actualizar marca/modelo si se enviaron y venían vacíos
        if not created_v:
            save_v = False
            if marca and not vehiculo.marca:
                vehiculo.marca = marca
                save_v = True
            if modelo and not vehiculo.modelo:
                vehiculo.modelo = modelo
                save_v = True
            if save_v:
                vehiculo.save()
        
        # Si el vehículo ya existía pero el cliente es nuevo/diferente, lo actualizamos opcionalmente
        if cliente and not vehiculo.cliente:
            vehiculo.cliente = cliente
            vehiculo.save()

        # 3. Crear la Orden
        orden = Orden.objects.create(
            vehiculo=vehiculo,
            observaciones=observaciones
        )
        orden.servicios.set(servicios_ids)
        
        serializer = self.get_serializer(orden)
        from rest_framework.response import Response
        return Response(serializer.data, status=201)

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

def vista_test_bluetooth(request):
    return render(request, 'aplicacion_pos/impresion_test_ble.html')
