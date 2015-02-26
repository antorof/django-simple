# -*- encoding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.validators import validate_slug, RegexValidator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import sys

class NameForm(forms.Form):
    your_name = forms.CharField(label='name', max_length=100)

class loginForm(forms.Form):
    username = forms.CharField (label = 'Nombre de usuario',max_length = 10,required = True,)
    password = forms.CharField( label = 'Contraseña',required = True,widget = forms.PasswordInput,)
    
    def clean (self):
        cleaned_data = super(loginForm, self).clean()

class registroForm(forms.Form):
    username = forms.CharField(label = 'Nombre', max_length = 10, required = True,)
    password = forms.CharField(label = 'Contrasena', required = True, widget = forms.PasswordInput,)
    password2 = forms.CharField(label = 'Repita su contrasena', required = True, widget = forms.PasswordInput,)
    email = forms.EmailField(label = 'Correo electronico')
    
    def clean (self):
        cleaned_data = super(registroForm, self).clean()
        password = cleaned_data.get("pw")
        password2 = cleaned_data.get("pw_again")
        if password != password2:
            raise forms.ValidationError ('las contrasenas no coinciden')


def index (request):
    return render (request, 'index.html')
    
def compae (request):
    return HttpResponse ("La vin, compae")
    
def registro_ (request, fulanito):
    return HttpResponse ("Queda usted registrado, %s" % fulanito)
    
def registropro (request, suco):
    context = {
        'fulanito':suco,
    }
    return render (request, 'index.html', context)
    
def heredado (request):
    context = {
        'fulanito':'',
    }
    return render (request, 'heredado.html', context)
    
def login (request):
    # Si viene del POST del boton de submit
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
        fulanito = 'default'
        form = loginForm()
        context = {
        'mensaje':'',
        'form':form,
        }
        return render(request, 'login.html', context)
    
def registro (request):
    context = {
        'user':'',
    }
    return render (request, 'registro.html', context)

def registroAvanzado (request):
    if request.method == 'POST':
        form = registroForm (request.POST)
        if form.is_valid ():
            try:
                User.objects.create(username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password'])
            except Exception as error:
                context = {
                    'username':'error',
                    'form':form,
                    'mensaje':'Ese usuario ya existe',
                }
                return render (request, 'registro-avanzado.html', context)
                
            context = {
                'username':form.cleaned_data['username'],
                'form':form,
            }
            return render (request, 'login.html', context)
        else:
            context = {
                'username': 'error',
                'form':form,
                'mensaje':'EEERRRRRROOOOOOOOOOORR',
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