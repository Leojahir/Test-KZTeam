from django import forms
from django.contrib.auth.models import User
from entrada.models import Entrada
from django.forms.forms import Form

class Registro(forms.Form):
    username = forms.CharField(required=True, min_length=5, max_length=40, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'Nombre de Usuario'
    }))
    correo = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder': 'ejemplo@correo.com'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder': 'Contraseña'
    }))


    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de Usuario ya Existe.')

        return username

    def clean_email(self):
        correo = self.cleaned_data.get('email')

        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError('El correo ya existe!')

        return correo

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )

class Entrada(forms.Form):
    titulo = forms.CharField(required=True, min_length=5, max_length=40, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'Titulo'
    }))
    enlace = forms.CharField(required=True, min_length=5, max_length=40, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder': 'Enlace'
    }))


    def save(self):
        return Entrada(
            self.cleaned_data.get('titulo'),
            self.cleaned_data.get('enlace'),
        )