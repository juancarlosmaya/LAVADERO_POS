import os
import django


# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lavadero_pos.settings')
django.setup()

from Servidor.models import Servicio, Lavadero, PerfilUsuario
from django.contrib.auth.models import User

# Crear usuario superusuario
admin_username = "juanc"
admin_password = "123"
if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(username=admin_username, password=admin_password, email="admin@lavadero.com")
    print(f"✓ Superusuario '{admin_username}' creado con contraseña '{admin_password}'")
else:
    print(f"✓ Superusuario '{admin_username}' ya existe")

# Crear usuario administrador Emotors
username = "emotorsadministrador"
password = "emotors2026"
first_name = "Jesus"
last_name = "Duarte"
#email = "admin@demo.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    print(f"✓ Usuario administrador '{username}' creado con contraseña '{password}'")
else:
    print(f"✓ Usuario administrador '{username}' ya existe")

# Crear usuario operador Emotors
username = "emotorsoperador"
password = "emotors2026"
first_name = "Julian Andres"
last_name = "Apellido Emotors"
#email = "admin@emotors.com"

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    print(f"✓ Usuario operador '{username}' creado con contraseña '{password}'")
else:
    print(f"✓ Usuario operador '{username}' ya existe")

# Obtener o crear el lavadero por defecto
if not Lavadero.objects.filter(nit='900123456').exists():
    Lavadero.objects.get_or_create(
        nombre= 'EMOTORS',
        nit = '900123456',
        direccion = 'Soacha, Cundinamarca',
        telefono = '+57 3001234567',
        correo_electronico ='info@emotors.com')
    print("✓ Lavadero 'EMOTORS' creado")
else:
    print("✓ Lavadero 'EMOTORS' ya existe")

# Obtener o crear el perfil de usuario para el administrador
lavadero = Lavadero.objects.get(nit='900123456')
admin_user = User.objects.get(username="emotorsadministrador")
if not PerfilUsuario.objects.filter(usuario=admin_user).exists():
    PerfilUsuario.objects.create(
        usuario=admin_user,
        lavadero=lavadero,
        rol='admin'
    )
    print(f"✓ Perfil de usuario para '{admin_user.username}' creado")

# Obtener o crear el perfil de usuario para el superusuario
admin_user = User.objects.get(username=admin_username)
if not PerfilUsuario.objects.filter(usuario=admin_user).exists():
    PerfilUsuario.objects.create(
        usuario=admin_user,
        lavadero=lavadero,
        rol='operador'
    )
    print(f"✓ Perfil de usuario para '{admin_user.username}' creado")   

# Obtener o crear el perfil de usuario para el operador
operador_user = User.objects.get(username="emotorsoperador")
if not PerfilUsuario.objects.filter(usuario=operador_user).exists():
    PerfilUsuario.objects.create(
        usuario=operador_user,
        lavadero=lavadero,
        rol='operador'
    )
    print(f"✓ Perfil de usuario para '{operador_user.username}' creado")   


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


ladadero = Lavadero.objects.get(nit='900123456')
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

