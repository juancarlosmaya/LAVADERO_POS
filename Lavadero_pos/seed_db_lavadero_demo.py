import os
import django


# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lavadero_pos.settings')
django.setup()

from Servidor.models import Servicio, Lavadero, PerfilUsuario, Categoria
from django.contrib.auth.models import User, Group


# Crear usuario administrador demo
username = "demoadministrador"
password = "demo2026"
#email = "admin@demo.com"
first_name = "Pedro Andres"
last_name = "Recalde Demo-Admin"

# Crear grupo administrador
nombre_grupo_usuario = "administrador" 
if not Group.objects.filter(name=nombre_grupo_usuario).exists():
    Group.objects.create(name=nombre_grupo_usuario)
    print(f"✓ Grupo '{nombre_grupo_usuario}' creado")
else:
    print(f"✓ Grupo '{nombre_grupo_usuario}' ya existe")


if not User.objects.filter(username=username).exists():
    usuario = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
    print(f"✓ Usuario administrador '{username}' creado con contraseña '{password}'")
    usuario.groups.add(Group.objects.get(name="administrador"))
    print(f"✓ Usuario administrador '{username}' agregado al grupo '{nombre_grupo_usuario}'")
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


categorias_data = [
    {"clave_vehiculo": "CARRO_DEMO", "tipo_vehiculo": "Automóvil_demo", "activo": True},
    {"clave_vehiculo": "MOTO_DEMO", "tipo_vehiculo": "Motocicleta_demo", "activo": True},
    {"clave_vehiculo": "CAMIONETA_5_DEMO", "tipo_vehiculo": "Camioneta (5 Pasajeros)_demo", "activo": True},
    {"clave_vehiculo": "CAMIONETA_7_DEMO", "tipo_vehiculo": "Camioneta (7 Pasajeros)_demo", "activo": True},
    {"clave_vehiculo": "BICICLETA_DEMO", "tipo_vehiculo": "Bicicleta_demo", "activo": True},
    {"clave_vehiculo": "OTROS_DEMO", "tipo_vehiculo": "Otros_demo", "activo": True},
]

print(f"Cargando categotias actualizados...")
for data in categorias_data:
    Categoria.objects.update_or_create(
        clave_vehiculo=data['clave_vehiculo'],
        tipo_vehiculo=data['tipo_vehiculo'],
        lavadero=lavadero,
        # Actualizar/crear con estos valores
        defaults={
            'activo': data['activo']
        }
    )  

servicios_data = [
    # AUTOMÓVILES (CARRO)
    {"nombre": "LAVADO EXTERIOR", "precio": "16000.00", "categoria": Categoria.objects.get(clave_vehiculo="CARRO_DEMO")},
    {"nombre": "TAPIZADA", "precio": "16000.00", "categoria": Categoria.objects.get(clave_vehiculo="CARRO_DEMO")},
    {"nombre": "LAVADA + TAPIZADA", "precio": "21000.00", "categoria": Categoria.objects.get(clave_vehiculo="CARRO_DEMO")},
    {"nombre": "LAVADA + TAPIZADA + CHASIS", "precio": "46000.00", "categoria": Categoria.objects.get(clave_vehiculo="CARRO_DEMO")},
    {"nombre": "POLICHADA", "precio": "87000.00", "categoria": Categoria.objects.get(clave_vehiculo="CARRO_DEMO")},
    {"nombre": "LAVADO DE COJINERIA E INTERIOR A VAPOR", "precio": "158000.00", "categoria": Categoria.objects.get(clave_vehiculo="CARRO_DEMO")},
    {"nombre": "LAVADO PREMIUM", "precio": "0.00", "categoria": Categoria.objects.get(clave_vehiculo="CARRO_DEMO"), "activo": False}, # Sin precio visible/activo

    # CAMIONETAS 5 PASAJEROS 
    {"nombre": "Lavado Exterior", "precio": "18000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_5_DEMO")},
    {"nombre": "Lavada + Tapizada", "precio": "30000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_5_DEMO")},
    {"nombre": "Lavada + Tapizada + Chasis", "precio": "55000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_5_DEMO")},
    {"nombre": "Polichada", "precio": "110000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_5_DEMO")},
    {"nombre": "Lavado de Cojinería e Interior a Vapor", "precio": "182000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_5_DEMO")},

    # CAMIONETAS 7 PASAJEROS
    {"nombre": "Lavado Exterior", "precio": "21000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_7_DEMO")},
    {"nombre": "Tapizada", "precio": "20000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_7_DEMO")},
    {"nombre": "Lavada + Tapizada", "precio": "32000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_7_DEMO")},
    {"nombre": "Lavada + Tapizada + Chasis", "precio": "52000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_7_DEMO")},
    {"nombre": "Polichada", "precio": "115000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_7_DEMO")},
    {"nombre": "Lavado de Cojinería e Interior a Vapor", "precio": "196000.00", "categoria": Categoria.objects.get(clave_vehiculo="CAMIONETA_7_DEMO")},

    # MOTOS
    {"nombre": "ENJUAGADA","precio": "14000.00","categoria": Categoria.objects.get(clave_vehiculo="MOTO_DEMO")},
    {"nombre": "ENJUAGADA + LLANTIL", "precio": "15000.00", "categoria": Categoria.objects.get(clave_vehiculo="MOTO_DEMO")},
    {"nombre": "ENJUAGADA + DESENGRASANTE + SILICONA + LLANTIL + ABRILLANTADOR DE MOTOR","precio": "18000.00","categoria": Categoria.objects.get(clave_vehiculo="MOTO_DEMO")},
    {"nombre": "LAVADO PREMIUM (LUBRICADA DE CADENA)", "precio": "21000.00", "categoria": Categoria.objects.get(clave_vehiculo="MOTO_DEMO")},
    
    # BICICLETAS
    {"nombre": "ENJUAGADA","precio": "7000.00","categoria": Categoria.objects.get(clave_vehiculo="BICICLETA_DEMO")},
    {"nombre": "ENJUAGADA + DESENGRASADO DE CADENA","precio": "9000.00","categoria": Categoria.objects.get(clave_vehiculo="BICICLETA_DEMO")},
    {"nombre": "ENJUAGADA + DESENGRASADO Y LUBRICADO DE CADENA","precio": "12000.00","categoria": Categoria.objects.get(clave_vehiculo="BICICLETA_DEMO")},

    # OTROS
    {"nombre": "ENJUAGADA","precio": "7000.00","categoria": Categoria.objects.get(clave_vehiculo="OTROS_DEMO")},
    {"nombre": "ENJUAGADA + DESENGRASADO DE CADENA","precio": "9000.00","categoria": Categoria.objects.get(clave_vehiculo="OTROS_DEMO")},
    {"nombre": "ENJUAGADA + DESENGRASADO Y LUBRICADO DE CADENA","precio": "12000.00","categoria": Categoria.objects.get(clave_vehiculo="OTROS_DEMO")}

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

