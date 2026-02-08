from django.contrib import admin
from .models import Cliente, PerfilUsuario, Vehiculo, Servicio, Orden, Pago, Lavadero, Operario_lavado

# Register your models here.
admin.site.register(PerfilUsuario)
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Servicio)
admin.site.register(Orden)
admin.site.register(Pago)
admin.site.register(Lavadero)
admin.site.register(Operario_lavado)
