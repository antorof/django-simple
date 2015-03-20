# -*- encoding: utf-8 -*-
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.validators import validate_slug, RegexValidator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class loginForm(forms.Form):
    username = forms.CharField(
        label = '',
        max_length = 10,
        required = True, 
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Nombre de usuario'}))
    
    password = forms.CharField(
        label = '',
        required = True,
        widget = forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Contraseña'}),)
    
    def clean (self):
        cleaned_data = super(loginForm, self).clean()

class registroForm(forms.Form):
    username = forms.CharField(
        label='', 
        max_length = 10, 
        required = True, 
        widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Nombre de usuario'}))
    
    password1 = forms.CharField(
        label='', 
        required = True, 
        widget = forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Contraseña'}),)
        
    password2 = forms.CharField(
        label='', 
        required = True, 
        widget = forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Repita su contraseña'}),)
    
    email = forms.EmailField(
        label='', 
        required = False, 
        widget = forms.EmailInput(attrs={'class' : 'form-control','placeholder':'Correo electrónico'}))
    
    credit = forms.CharField(
        label='',
        required = False,
        max_length=16,
        validators=[RegexValidator(r'^[0-9]{16}$','Son necesarios 16 dígitos','numero_invalido'),], 
        widget = forms.TextInput(attrs={'class' : 'form-control','placeholder':'Tarjeta de crédito'}))
    
    anio_expiracion = forms.CharField(
        label='',
        required = False,
        max_length=4,
        validators=[RegexValidator(r'^[0-9]{4}$','Son necesarios 4 dígitos','anio_invalido'),],
        widget = forms.NumberInput(attrs={'class' : 'form-control','placeholder':'Año de expiración', 'min':'2000', 'max':'2100'}))
    
    mes_credito = forms.CharField(
        label='',
        required = False,
        max_length=2,
        validators=[RegexValidator(r'^[0-9]{1,2}$','Introduzca el número del mes','mes_invalido'),],
        widget = forms.NumberInput(attrs={'class' : 'form-control','placeholder':'Mes de expiración', 'min':'1', 'max':'2100'}))
    
    def faltanCampos(self):
        cleaned_data = super(registroForm, self).clean()
        un = cleaned_data.get("username")
        pw = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        return un == None or pw == None or pw2 == None
    
    def contraseniasDistintas(self):
        cleaned_data = super(registroForm, self).clean()
        pw = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        if pw != pw2:
            return True 
    
    def clean (self):
        cleaned_data = super(registroForm, self).clean()
        pw = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")
        if pw != pw2:
            raise forms.ValidationError("") # No le pongo nada para no mostrar texto en el cliente


def index (request):
    return redirect('inicio')

def inicio (request):
    'Renderiza la página principal'
    # Si usuario tiene iniciada la sesión lo dejo continuar
    if request.user.is_authenticated() :
        return render (request, 'bienvenida.html')
    else :
        context = {
            # 'username':None,
            'form':loginForm(),
            'mensaje':'Inicie sesión para continuar.',
        }
        return render (request, 'login.html', context)
    

def cerrarSesion (request):
    'Cierra la sesión del usuario si hubiera una sesión abierta'
    logout(request)
    return redirect('login')

def iniciarSesion (request):
    'Realiza el inicio de sesión de un usuario o devuelve la página de login'
    # Si viene del POST
    if request.method == 'POST':
        form = loginForm (request.POST)
        # Si el formulario es valido se comprueban los credenciales
        if form.is_valid ():
            user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('inicio')
                else:
                    context = {
                        'mensaje':'Usuario no activo',
                        'form':form,
                    }
                    return render(request, 'login.html', context)
            else:
                context = {
                    'mensaje':'Usuario o contraseña incorrectos',
                    'form':form,
                }
                return render(request, 'login.html', context)
    # Si es la primera vez que se llama (GET)
    else:
        # Si usuario tiene iniciada la sesión redirijo
        if request.user.is_authenticated() :
            return redirect('inicio')
        # Si no, le muestro el formulario de login
        else :
            form = loginForm()
            context = {
                'mensaje':'',
                'form':form,
            }
            return render(request, 'login.html', context)

def registro (request):
    'Realiza el registro de un usuario o devuelve la página de registro'
    if request.method == 'POST':
        form = registroForm (request.POST)
        if form.is_valid ():
            try:
                User.objects.create_user(username = form.cleaned_data['username'],
                                    email = form.cleaned_data['email'],
                                    password = form.cleaned_data['password1'])
            except Exception as error:
                print error
                context = {
                    'username':None,
                    'form':form,
                    'mensaje':'Ese usuario ya existe.',
                }
                return render (request, 'registro.html', context)
                
            context = {
                'username':form.cleaned_data['username'],
                'form':loginForm(),
                'mensaje':'Usuario creado con éxito. Inicie sesión.',
            }
            return render (request, 'login.html', context)
        else:
            if form.faltanCampos():
                context = {
                    'username': None,
                    'form':form,
                    'mensaje':'Revise los campos a rellenar.',
                }
            elif form.contraseniasDistintas():
                context = {
                    'username': None,
                    'form':form,
                    'mensaje':'Las contraseñas introducidas son distintas.',
                }
            else:
                context = {
                    'username': None,
                    'form':form,
                    'mensaje':'Error desconocido.',
                }
            return render (request, 'registro.html', context)
    else:
        username = 'default'
        form = registroForm()
        context = {
            'username':username,
            'form':form,
        }
        return render(request, 'registro.html', context)