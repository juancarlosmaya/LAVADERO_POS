from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 

class Lavadero(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo_electronico = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Extender usuario con relación al lavadero
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_usuarios')
    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE, related_name='usuarios')
    rol = models.CharField(max_length=50, choices=[('admin', 'Administrador'), ('operador', 'Operador')])
    def __str__(self):
        return f"{self.usuario.username} - {self.rol} en {self.lavadero.nombre}"

class Cliente(models.Model):
    celular = models.CharField(max_length=15) # Unique constraint removed to allow multiple clientes with same celular , unique=True
    nombre = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE, related_name='clientes')

    def __str__(self):
        return f"{self.nombre or 'Sin Nombre'} ({self.celular})"

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('CARRO', 'Automóvil'),
        ('MOTO', 'Motocicleta'),
        ('CAMIONETA_5', 'Camioneta (5 Pasajeros)'),
        ('CAMIONETA_7', 'Camioneta (7 Pasajeros)'),
        ('BICICLETA', 'Bicicleta'),
    ]
    placa = models.CharField(max_length=10) # Unique constraint removed to allow multiple vehiculos with same placa , unique=True, 
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehiculos')
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE, related_name='vehiculos')
    
    def __str__(self):
        return f"{self.placa} - {self.tipo}"

class Servicio(models.Model):
    CATEGORIA_CHOICES = [
        ('CARRO', 'Carro'),
        ('MOTO', 'Moto'),
        ('CAMIONETA_5', 'Camioneta (5 Pasajeros)'),
        ('CAMIONETA_7', 'Camioneta (7 Pasajeros)'),
        ('BICICLETA', 'Bicicleta'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='CARRO')
    activo = models.BooleanField(default=True)
    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE, related_name='servicios')

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()}) - ${self.precio}"

class Orden(models.Model):
    ESTADO_CHOICES = [
        ('EN_COLA', 'En Cola'),
        ('EN_PROCESO', 'En Proceso'),
        ('TERMINADO', 'Terminado'),
        ('ENTREGADO', 'Entregado'),
    ]
    TIEMPO_ADICIONAL_CHOICES = [
        (0 , '0 Minutos'),
        (15, '15 Minutos'),
        (30, '30 Minutos'),
        (45, '45 Minutos'),
        (60, '1 Hora'),
    ]
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name='ordenes')
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes')
    servicios = models.ManyToManyField(Servicio, related_name='ordenes')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='EN_COLA')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)
    tiempo_inicio_servicio = models.TimeField(null=True)
    tiempo_adicional_servicio = models.IntegerField(choices=TIEMPO_ADICIONAL_CHOICES, default=0, blank=True, null=True )
    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE, related_name='ordenes')

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo.placa}"

class Pago(models.Model):
    METODO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('NEQUI', 'Nequi'),
        ('DAVIPLATA', 'DaviPlata'),
        ('TARJETA', 'Tarjeta'),
    ]
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE, related_name='pago')
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    monto = models.DecimalField(max_digits=12, decimal_places=0)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    lavadero = models.ForeignKey(Lavadero, on_delete=models.CASCADE, related_name='pagos')

    def __str__(self):
        return f"Pago Orden #{self.orden.id} - {self.monto}"
