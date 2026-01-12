import os
import django


# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lavadero_pos.settings')
django.setup()

from Servidor.models import Servicio


servicios_data = [
    # AUTOMÓVILES (CARRO)
    {"nombre": "LAVADO EXTERIOR", "precio": "16000.00", "categoria": "CARRO"},
    {"nombre": "TAPIZADA", "precio": "16000.00", "categoria": "CARRO"},
    {"nombre": "LAVADA + TAPIZADA", "precio": "21000.00", "categoria": "CARRO"},
    {"nombre": "LAVADA + TAPIZADA + CHASIS", "precio": "46000.00", "categoria": "CARRO"},
    {"nombre": "POLICHADA", "precio": "87000.00", "categoria": "CARRO"},
    {"nombre": "LAVADO DE COJINERIA E INTERIOR A VAPOR", "precio": "158000.00", "categoria": "CARRO"},
    {"nombre": "LAVADO PREMIUM", "precio": "0.00", "categoria": "CARRO", "activo": False}, # Sin precio visible/activo

    # CAMIONETAS 5 PASAJEROS 
    {"nombre": "Lavado Exterior", "precio": "18000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Lavada + Tapizada", "precio": "30000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Lavada + Tapizada + Chasis", "precio": "55000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Polichada", "precio": "110000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Lavado de Cojinería e Interior a Vapor", "precio": "182000.00", "categoria": "CAMIONETA_5"},

    # CAMIONETAS 7 PASAJEROS
    {"nombre": "Lavado Exterior", "precio": "21000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Tapizada", "precio": "20000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Lavada + Tapizada", "precio": "32000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Lavada + Tapizada + Chasis", "precio": "52000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Polichada", "precio": "115000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Lavado de Cojinería e Interior a Vapor", "precio": "196000.00", "categoria": "CAMIONETA_7"},

    # MOTOS
    {"nombre": "ENJUAGADA","precio": "14000.00","categoria": "MOTO"},
    {"nombre": "ENJUAGADA + LLANTIL", "precio": "15000.00", "categoria": "MOTO"},
    {"nombre": "ENJUAGADA + DESENGRASANTE + SILICONA + LLANTIL + ABRILLANTADOR DE MOTOR","precio": "18000.00","categoria": "MOTO"},
    {"nombre": "LAVADO PREMIUM (LUBRICADA DE CADENA)", "precio": "21000.00", "categoria": "MOTO"},
    
    # BICICLETAS
    {"nombre": "ENJUAGADA","precio": "7000.00","categoria": "BICICLETA"},
    {"nombre": "ENJUAGADA + DESENGRASADO DE CADENA","precio": "9000.00","categoria": "BICICLETA"},
    {"nombre": "ENJUAGADA + DESENGRASADO Y LUBRICADO DE CADENA","precio": "12000.00","categoria": "BICICLETA"}

]

print(f"Cargando servicios actualizados...")

# Busca y actualiza los servicios existentes o crea nuevos, los busca por nombre y categoria. Si no existe lo crea. Si existe actualiza su precio y estado.
for data in servicios_data:
    Servicio.objects.update_or_create(
        nombre=data['nombre'],
        categoria=data['categoria'],
        defaults={
            'precio': data['precio'],
            'activo': data.get('activo', True)
        }
    )

