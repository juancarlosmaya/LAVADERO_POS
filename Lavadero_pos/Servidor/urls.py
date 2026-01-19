from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet,
    VehiculoViewSet,
    ServicioViewSet,
    OrdenViewSet, 
    PagoViewSet,
    LavaderoViewSet,
    vista_test_bluetooth
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'ordenes', OrdenViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'lavaderos', LavaderoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-ble/', vista_test_bluetooth, name='test_ble'),
]
