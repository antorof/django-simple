# -*- encoding: utf-8 -*-
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.validators import validate_slug, RegexValidator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import sys

class loginForm(forms.Form):
    username = forms.CharField(label = '',max_length = 10,required = True, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Nombre de usuario'}))
    password = forms.CharField(label = '',required = True,widget = forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Contraseña'}),)
    
    def clean (self):
        cleaned_data = super(loginForm, self).clean()

class registroForm(forms.Form):
    username = forms.CharField(label='', max_length = 10, required = True, widget=forms.TextInput(attrs={'class' : 'form-control','placeholder':'Nombre de usuario'}))
    password = forms.CharField(label='', required = True, widget = forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Contraseña'}),)
    password2 = forms.CharField(label='', required = True, widget = forms.PasswordInput(attrs={'class' : 'form-control','placeholder':'Repita su contraseña'}),)
    email = forms.EmailField(label='', required = False, widget = forms.EmailInput(attrs={'class' : 'form-control','placeholder':'Correo electrónico'}))
    
    def faltanCampos(self):
        cleaned_data = super(registroForm, self).clean()
        un = cleaned_data.get("username")
        pw = cleaned_data.get("password")
        pw2 = cleaned_data.get("password2")
        return un == None or pw == None or pw2 == None
    
    def contraseniasDistintas(self):
        cleaned_data = super(registroForm, self).clean()
        pw = cleaned_data.get("password")
        pw2 = cleaned_data.get("password2")
        if pw != pw2:
            return True 
    
    def clean (self):
        cleaned_data = super(registroForm, self).clean()
        pw = cleaned_data.get("password")
        pw2 = cleaned_data.get("password2")
        if pw != pw2:
            raise forms.ValidationError("") # No le pongo nada para no mostrar texto en el cliente


def index (request):
    return render (request, 'index.html')
    
def cerrarSesion (request):    
    logout(request)
    return HttpResponseRedirect('../login')

def login (request):
    # Si viene del POST
    if request.method == 'POST':
        form = loginForm (request.POST)
        # Si el formulario es valido se comprueban los credenciales
        if form.is_valid ():
            user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    context = {
                        'username':form.cleaned_data['username'],
                    }
                    return render(request, 'bienvenida.html', context)
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
            return HttpResponseRedirect('../bienvenida')
        # Si no, le muestro el formulario de login
        else :
            form = loginForm()
            context = {
                'mensaje':'',
                'form':form,
            }
            return render(request, 'login.html', context)

def registro (request):
    if request.method == 'POST':
        form = registroForm (request.POST)
        if form.is_valid ():
            try:
                User.objects.create(username = form.cleaned_data['username'],
                                    email = form.cleaned_data['email'],
                                    password = form.cleaned_data['password'])
            except Exception as error:
                context = {
                    'username':None,
                    'form':form,
                    'mensaje':'Ese usuario ya existe.',
                }
                return render (request, 'registro-avanzado.html', context)
                
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
            return render (request, 'registro-avanzado.html', context)
    else:
        username = 'default'
        form = registroForm()
        context = {
            'username':username,
            'form':form,
        }
        return render(request, 'registro-avanzado.html', context)