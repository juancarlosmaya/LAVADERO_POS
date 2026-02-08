from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test-impresora/', views.vista_test_bluetooth, name='test_impresora'),
    path('nueva-orden/', views.crear_orden, name='nueva_orden'),
    path('ticket/<int:orden_id>/', views.ticket_orden, name='ticket_orden'),
    path('estado-servicios/', views.estado_servicios, name='estado_servicios'),
    path('eliminar-orden/<int:orden_id>/', views.eliminar_orden, name='eliminar_orden'),
]
