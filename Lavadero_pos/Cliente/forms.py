from django import forms
from django.contrib.auth.models import User
from Servidor.models import Orden, Vehiculo, Cliente

class loginFormulario(forms.Form):
    nombreUsuario       = forms.CharField(label='Nombre de Usuario', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contrasenaUsuario   = forms.CharField(label='Contraseña', max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class OrdenForm(forms.ModelForm):
    nombre_cliente = forms.CharField(
        label='Nombre Completo',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'})
    )
    
    class Meta:
        model = Orden
        fields = ['observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tapetes sucios, limpiar interior...',
                'rows': 4
            })
        }


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa', 'tipo', 'marca', 'modelo']
        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ABC123'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Mazda'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2024'}),
        }


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'celular']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '3001234567'}),
        }

