from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('test-impresora/', views.vista_test_bluetooth, name='test_impresora'),
    path('nueva-orden/', views.crear_orden, name='nueva_orden'),
]
