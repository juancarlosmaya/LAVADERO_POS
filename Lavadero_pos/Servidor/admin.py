from django.contrib import admin
from .models import Cliente, Vehiculo, Servicio, Orden, Pago

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Servicio)
admin.site.register(Orden)
admin.site.register(Pago)
