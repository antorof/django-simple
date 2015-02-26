from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index (request):
    return HttpResponse ("Hola desde servicio/")
    
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
    context = {
        'user':'',
    }
    return render (request, 'login.html', context)
    
def registro (request):
    context = {
        'user':'',
    }
    return render (request, 'registro.html', context)