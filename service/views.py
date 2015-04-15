# -*- encoding: utf-8 -*-
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.validators import validate_slug, RegexValidator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from lxml import etree
import requests
from pymongo import MongoClient
from django.http import JsonResponse
from unidecode import unidecode

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

def geoETSIIT (request):
    GEOCODE_BASE_URL = 'http://maps.google.com/maps/api/geocode/xml'
    # URL_ETSIIT = '?address=Periodista Daniel Saucedo Aranda 18014 GRANADA Spain'
    URL_ETSIIT = '?address=ETSIIT GRANADA Spain'
    result = ""
    
    tree = etree.parse(GEOCODE_BASE_URL + URL_ETSIIT)
    
    result += "<ul>"
    items = tree.xpath('//address_component')
    
    for i in items:
        lname = i.xpath('long_name')
        type = i.xpath('type')
        
        # Solo aparece un type y un solo long_name, por eso el '[0]'
        if type[0].text == 'locality' :
            print (">" + lname[0].text)
            result += "<li>Localidad: <strong>" + lname[0].text +"</strong></li>"
        
        elif type[0].text == 'administrative_area_level_4' :
            print (">" + lname[0].text)
            result += "<li>Municipio: <strong>" + lname[0].text +"</strong></li>"
        
        elif type[0].text == 'administrative_area_level_3' :
            print (">" + lname[0].text)
            result += "<li>Comarca: <strong>" + lname[0].text +"</strong></li>"
        
        elif type[0].text == 'administrative_area_level_2' :
            print (">" + lname[0].text)
            result += "<li>Provincia: <strong>" + lname[0].text +"</strong></li>"
        
        elif type[0].text == 'administrative_area_level_1' :
            print (">" + lname[0].text)
            result += "<li>Comunidad: <strong>" + lname[0].text +"</strong></li>"
    
    result += "</ul>"
    
    context = {
        'url':GEOCODE_BASE_URL + URL_ETSIIT,
        'form':result,
    }
    return render(request, 'geo-etsiit.html', context)
    
def elpais (request):
    # BASE_URL = 'http://ep00.epimg.net/rss/elpais/portada.xml'
    BASE_URL = 'http://ep00.epimg.net/rss/tecnologia/portada.xml'
    NOMBRE_URL = 'RSS de Tecnología'
    
    result = ""
    
    tree = etree.parse(BASE_URL)
    
    # result += "<ul>"
    images = tree.xpath('//enclosure/@url')
    
    for i in images:
        # print (">" + i)
        result += "<div class='col-xs-6 col-sm-4 col-md-3'>"
        result += '<a href="' + i + '" target="_blank">'
        result += '<img class="img-responsive" src="'+ i +'" alt="">'
        result += "</a>"
        result += "</div>"
    
    # result += "</ul>"
    
    context = {
        'nombre_url':NOMBRE_URL,
        'url':BASE_URL,
        'form':result,
    }
    return render(request, 'elpais.html', context)
    
def crawler (request):
    client = MongoClient()
    db = client.db_ssbw
    noticias_tb = db.noticias
    
    NOMBRE = "Servicio de búsqueda"
    result = ""
    
    if request.method == 'POST':
        categoria = request.POST.get("keyword", "")
        
        if categoria.replace(" ","") != "":
            noticias = noticias_tb.find({"categorias_clean":{ "$regex": unidecode(categoria), "$options":"i" }})
            
            # print("post:"+categoria)
            # print(unidecode(categoria))
            # print("count:"+str(noticias.count()))
            
            if noticias.count()!=0:
                result += "<p class='text-mute'>"+str(noticias.count())+" resultados encontrados.</p>"
                for i in noticias:
                    title = i["titulo"]
                    link = i["link"]
                    categorias = i["categorias"]
                    categorias_clean = i["categorias_clean"]
                    
                    result += "<div class='col-xs-6 col-sm-4 col-md-3'><div class='panel panel-default'><div class='panel-body'>"
                    result += '<h4>' + title + '</h4>'
                    result += '<p><a href="' + link + '" target="_blank">Enlace</a></p>'
                    
                    for k in range(len(categorias)):
                        if str.lower(unidecode(categoria)) == categorias_clean[k]:
                            result += "<span class='label label-success'>" + categorias[k] + "</span><br/>"
                        elif str.lower(unidecode(categoria)) in categorias_clean[k]:
                            result += "<span class='label label-primary'>" + categorias[k] + "</span><br/>"
                        else:
                            result += "<span class='label label-gray'>" + categorias[k] + "</span><br/>"
                    result += "</div></div></div>"
            else:
                result += "<p class='text-warning'>No se han encontrado resultados.</p>"
        else:
            result += "<p class='text-danger'>Debe introducir un t&eacute;rmino para la b&uacute;squeda.</p>"
        
        context = {
            'nombre':NOMBRE,
            'url':"",
            'contenido':result,
            'cabecera':'Resultados de la búsqueda',
            'keyword':categoria,
            'POST':True
        }
        return render(request, 'crawler.html', context)
    
    else:
        URL_ELPAIS = 'http://servicios.elpais.com/rss/'
        BASE_URL = 'http://ep00.epimg.net/rss/tecnologia/portada.xml'
        
            
        result += "<p class='text-muted'>Escriba una categoría en el cuadro de búsqueda para realizar una consulta.</p>"
        
        context = {
            'nombre':NOMBRE,
            'url':BASE_URL,
            'contenido':result,
            'cabecera':'Bienvenido al servicio de búsqueda de noticias',
            'POST':False
        }
        return render(request, 'crawler.html', context)

def updatebd (request):
    nuevasNoticias = 0
    client = MongoClient()
    db = client.db_ssbw
    noticias_tb = db.noticias
    
    URL_ELPAIS = 'http://servicios.elpais.com/rss/'
    BASE_URL = 'http://ep00.epimg.net/rss/tecnologia/portada.xml'
    
    tree = etree.parse(BASE_URL)
    
    items = tree.xpath('//item')
    
    for i in items:
        title = i.xpath('title')[0].text
        link = i.xpath('link')[0].text
        categorias = []
        categorias_clean = []
        for j in i.xpath('category'):
            categorias.append(j.text)
            categorias_clean.append(str.lower(unidecode(j.text)))
        
        unItem = {"titulo":title,"link":link,"categorias":categorias,"categorias_clean":categorias_clean}
        
        if noticias_tb.find(unItem).count() == 0:
            nuevasNoticias+=1
            noticias_tb.insert(unItem)
        else:
            print("WAKA")
    
    return JsonResponse( {'numItems':str(noticias_tb.count()),'nuevosItems':str(nuevasNoticias)} )
    