import os
import django


# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lavadero_pos.settings')
django.setup()

from Servidor.models import Servicio, Lavadero, PerfilUsuario
from django.contrib.auth.models import User


# Crear usuario administrador demo
username = "demoadministrador"
password = "demo2026"
#email = "admin@demo.com"
first_name = "Pedro Andres"
last_name = "Recalde Demo-Admin"


if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    print(f"✓ Usuario administrador '{username}' creado con contraseña '{password}'")
else:
    print(f"✓ Usuario administrador '{username}' ya existe")

# Crear usuario operador demo
username = "demooperador"
password = "demo2026"
#email = "admin@demo.com"
first_name = "Luis Albertp"
last_name = "Fernandes Demo-Operador"

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    print(f"✓ Usuario operador '{username}' creado con contraseña '{password}'")
else:
    print(f"✓ Usuario operador '{username}' ya existe")

# Obtener o crear el lavadero por defecto
if not Lavadero.objects.filter(nit='88888888').exists():
    Lavadero.objects.get_or_create(
        nombre= 'DEMO',
        nit = '88888888',
        direccion = 'BOSA, BOGOTA',
        telefono = '+57 33333333',
        correo_electronico ='info@demo.com')
    print("✓ Lavadero 'DEMO' creado")
else:
    print("✓ Lavadero 'DEMO' ya existe")

# Obtener o crear el perfil de usuario para el administrador
lavadero = Lavadero.objects.get(nit='88888888')
admin_user = User.objects.get(username="demoadministrador")
if not PerfilUsuario.objects.filter(usuario=admin_user).exists():
    PerfilUsuario.objects.create(
        usuario=admin_user,
        lavadero=lavadero,
        rol='admin'
    )
    print(f"✓ Perfil de usuario para '{admin_user.username}' creado")

# Obtener o crear el perfil de usuario para el operador
operador_user = User.objects.get(username="demooperador")
if not PerfilUsuario.objects.filter(usuario=operador_user).exists():
    PerfilUsuario.objects.create(
        usuario=operador_user,
        lavadero=lavadero,
        rol='operador'
    )
    print(f"✓ Perfil de usuario para '{operador_user.username}' creado")   


servicios_data = [
    # AUTOMÓVILES (CARRO)
    {"nombre": "LAVADO EXTERIOR", "precio": "38000.00", "categoria": "CARRO"},
    {"nombre": "TAPIZADA", "precio": "36000.00", "categoria": "CARRO"},
    {"nombre": "LAVADA + TAPIZADA", "precio": "41000.00", "categoria": "CARRO"},
    {"nombre": "LAVADA + TAPIZADA + CHASIS", "precio": "66000.00", "categoria": "CARRO"},
    {"nombre": "POLICHADA", "precio": "87000.00", "categoria": "CARRO"},
    {"nombre": "LAVADO DE COJINERIA E INTERIOR A VAPOR", "precio": "358000.00", "categoria": "CARRO"},
    {"nombre": "LAVADO PREMIUM", "precio": "0.00", "categoria": "CARRO", "activo": False}, # Sin precio visible/activo

    # CAMIONETAS 5 PASAJEROS 
    {"nombre": "Lavado Exterior", "precio": "28000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Lavada + Tapizada", "precio": "40000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Lavada + Tapizada + Chasis", "precio": "65000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Polichada", "precio": "210000.00", "categoria": "CAMIONETA_5"},
    {"nombre": "Lavado de Cojinería e Interior a Vapor", "precio": "282000.00", "categoria": "CAMIONETA_5"},

    # CAMIONETAS 7 PASAJEROS
    {"nombre": "Lavado Exterior", "precio": "31000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Tapizada", "precio": "30000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Lavada + Tapizada", "precio": "42000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Lavada + Tapizada + Chasis", "precio": "62000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Polichada", "precio": "215000.00", "categoria": "CAMIONETA_7"},
    {"nombre": "Lavado de Cojinería e Interior a Vapor", "precio": "296000.00", "categoria": "CAMIONETA_7"},

    # MOTOS
    {"nombre": "ENJUAGADA","precio": "24000.00","categoria": "MOTO"},
    {"nombre": "ENJUAGADA + LLANTIL", "precio": "25000.00", "categoria": "MOTO"},
    {"nombre": "ENJUAGADA + DESENGRASANTE + SILICONA + LLANTIL + ABRILLANTADOR DE MOTOR","precio": "28000.00","categoria": "MOTO"},
    {"nombre": "LAVADO PREMIUM (LUBRICADA DE CADENA)", "precio": "31000.00", "categoria": "MOTO"},
    
    # BICICLETAS
    {"nombre": "ENJUAGADA","precio": "8000.00","categoria": "BICICLETA"},
    {"nombre": "ENJUAGADA + DESENGRASADO DE CADENA","precio": "10000.00","categoria": "BICICLETA"},
    {"nombre": "ENJUAGADA + DESENGRASADO Y LUBRICADO DE CADENA","precio": "22000.00","categoria": "BICICLETA"}

]

print(f"Cargando servicios actualizados...")


ladadero = Lavadero.objects.get(nit='88888888')
# Busca y actualiza los servicios existentes o crea nuevos, los busca por nombre y categoria. Si no existe lo crea. Si existe actualiza su precio y estado.
for data in servicios_data:
    Servicio.objects.update_or_create(
        nombre=data['nombre'],
        categoria=data['categoria'],
        lavadero=lavadero,
        # Actualizar/crear con estos valores
        defaults={
            'precio': data['precio'],
            'activo': True
        }
    )



print(f"✓ {len(servicios_data)} servicios cargados/actualizados")

