from django import forms
from django.contrib.auth.models import User
from Servidor.models import Orden, Vehiculo, Cliente


class loginFormulario(forms.Form):
    nombreUsuario = forms.CharField(
        label='Nombre de Usuario',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
            'placeholder': 'Ingresa tu usuario'
        })
    )
    contrasenaUsuario = forms.CharField(
        label='Contraseña',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
            'placeholder': 'Ingresa tu contraseña'
        })
    )


class OrdenForm(forms.ModelForm):
    nombre_cliente = forms.CharField(
        label='Nombre Completo',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
            'placeholder': 'Nombre del cliente'
        })
    )
    
    class Meta:
        model = Orden
        fields = ['tiempo_inicio_servicio', 'observaciones', 'tiempo_adicional_servicio']
        widgets = {
            'tiempo_inicio_servicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'tiempo_adicional_servicio': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
                'rows': 4,
                'placeholder': 'Ej: Tapetes sucios, limpiar interior...'
            })
        }


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'marca'] #, 'modelo']
        widgets = {
            'placa': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
                'placeholder': 'ABC123',
                'style': 'text-transform: uppercase;'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100'
            }),
            'marca': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
                'placeholder': 'Ej: Mazda'
            }),
            #'modelo': forms.TextInput(attrs={
            #    'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
            #    'placeholder': 'Ej: 2024'
            #}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['placa'].label = 'Placa del Vehículo'
        self.fields['tipo'].label = 'Tipo de Vehículo'
        self.fields['marca'].label = 'Marca'
        #self.fields['modelo'].label = 'Modelo'


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'celular']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
                'placeholder': 'Nombre del cliente'
            }),
            'celular': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:border-blue-600 focus:ring-2 focus:ring-blue-100',
                'placeholder': '3001234567'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].label = 'Nombre Completo'
        self.fields['celular'].label = 'Número de Celular'