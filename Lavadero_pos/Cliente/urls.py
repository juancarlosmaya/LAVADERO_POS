from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('test-impresora/', views.vista_test_bluetooth, name='test_impresora'),
    path('nueva-orden/', views.crear_orden, name='nueva_orden'),
    path('ticket/<int:orden_id>/', views.ticket_orden, name='ticket_orden'),
    path('estado-ordenes/', views.estado_ordenes, name='estado_ordenes'),
    path('eliminar-orden/<int:orden_id>/', views.eliminar_orden, name='eliminar_orden'),
    path('nuevo-gasto/', views.nuevo_gasto, name='nuevo_gasto'),
    path('estado-gastos/', views.estado_gastos, name='estado_gastos'),
]
