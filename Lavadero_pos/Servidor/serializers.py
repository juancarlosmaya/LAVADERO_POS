from rest_framework import serializers
from .models import Cliente, Vehiculo, Servicio, Orden, Pago, Lavadero, Operario_lavado

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class OrdenSerializer(serializers.ModelSerializer):
    # Nested info for display
    vehiculo_placa = serializers.CharField(source='vehiculo.placa', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_celular = serializers.CharField(source='cliente.celular', read_only=True)
    servicios_details = ServicioSerializer(source='servicios', many=True, read_only=True)

    class Meta:
        model = Orden
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class LavaderoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lavadero
        fields = '__all__'  

class Operario_lavadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operario_lavado
        fields = '__all__'
