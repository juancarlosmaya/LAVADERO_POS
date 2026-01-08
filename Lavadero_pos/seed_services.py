import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lavadero_pos.settings')
django.setup()

from Servidor.models import Servicio

servicios = [
    # CARRO
    {'nombre': 'Lavado General', 'precio': 25000, 'categoria': 'CARRO'},
    {'nombre': 'Lavado de Chasis', 'precio': 35000, 'categoria': 'CARRO'},
    {'nombre': 'Lavado de Motor a Vapor', 'precio': 40000, 'categoria': 'CARRO'},
    {'nombre': 'Lavado de Motor a Agua a Presión', 'precio': 30000, 'categoria': 'CARRO'},
    {'nombre': 'Tapizada', 'precio': 120000, 'categoria': 'CARRO'},
    {'nombre': 'Enjuague / Lavado Externo', 'precio': 15000, 'categoria': 'CARRO'},
    {'nombre': 'Polichada', 'precio': 60000, 'categoria': 'CARRO'},

    # MOTO
    {'nombre': 'Enjuagar', 'precio': 8000, 'categoria': 'MOTO'},
    {'nombre': 'Agua', 'precio': 5000, 'categoria': 'MOTO'},
    {'nombre': 'Lavado General', 'precio': 15000, 'categoria': 'MOTO'},
    {'nombre': 'Lavado General + Lubricada', 'precio': 20000, 'categoria': 'MOTO'},
    {'nombre': 'Polichada', 'precio': 30000, 'categoria': 'MOTO'},
]

print("Creando servicios...")
for s in servicios:
    obj, created = Servicio.objects.get_or_create(
        nombre=s['nombre'],
        categoria=s['categoria'],
        defaults={'precio': s['precio']}
    )
    if created:
        print(f"Creado: {obj}")
    else:
        print(f"Ya existe: {obj}")

print("Terminado.")
