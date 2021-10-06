from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login as lg
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth import logout
from .forms import Registro
from .forms import Entrada
from entrada.models import Entrada as EntradaModel
from django.contrib.auth.models import User


def index(request):

    entradas = EntradaModel.objects.all()

    return render(request, 'index.html', {
        "entrada":entradas
    })

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        usuarios = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if usuarios:
            lg(request, usuarios)
            messages.success(request, f'Bienvenido {usuarios.username}')
            return redirect('index')
        else:
            messages.error(request, 'Usuario y/o contraseña Incorrecta')
    return render(request, 'users/login.html', {})

def salir(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Sesion cerrada con exito')
    return redirect('login')


def registro(request):
    if request.user.is_authenticated:
        return redirect('index')
    formulario = Registro(request.POST or None)
    if request.method == 'POST' and formulario.is_valid():
        usuario = formulario.save()
        if usuario:
            lg(request, usuario)
            messages.success(request, 'Usuario registrado con Exito, Bienvenido!')
            return redirect('index')
    return render(request, 'users/register.html',{
        'form':formulario
    })

def entrada(request):
    if request.user.is_authenticated:
        formulario = Entrada(request.POST or None)
        if request.method == 'POST' and formulario.is_valid():
            user = request.user
            entrada = EntradaModel(titulo=formulario.cleaned_data.get('titulo'), enlace=formulario.cleaned_data.get('enlace'), usuario=user.id)
            entrada.save()
            if entrada:
                messages.success(request, 'Entrada creada exitosamente!')
                return redirect('index')
    else:
        return redirect('login')            
    return render(request, 'users/entrada.html',{
        'form':formulario
    })    

def like(request):
    if request.method == 'POST':
        entrada = EntradaModel.objects.get(pk=request.POST.get('entrada_id'))
        entrada.valoracion = entrada.valoracion + 1
        entrada.save(update_fields=['valoracion'])
        messages.success(request, 'Gracias por Valorar el enlace.')
        return redirect('index')
    return render(request, "index.html")


def dislike(request):
    if request.method == 'POST':
        entrada = EntradaModel.objects.get(pk=request.POST.get('entrada_id'))
        entrada.valoracion = entrada.valoracion - 1
        entrada.save(update_fields=['valoracion'])
        messages.success(request, 'Gracias por Valorar el enlace.')
        return redirect('index')
    return render(request, "index.html")    