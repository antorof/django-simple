from django.conf.urls import patterns, url

from service import views

urlpatterns = patterns ('',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^inicio/$', views.inicio, name='inicio'),
    
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^registrarse/$', views.registro, name='registro'),
    
    url(r'^login/$', views.iniciarSesion, name='login'),
    url(r'^iniciar-sesion/$', views.iniciarSesion, name='iniciar-sesion'),
    
    url(r'^bienvenida/$', views.index, name='bienvenida'),
    
    url(r'^logout/$', views.cerrarSesion, name='logout'),
    url(r'^cerrar-sesion/$', views.cerrarSesion, name='cerrar-sesion'),
    
    url(r'^geo-etsiit/$', views.geoETSIIT, name='geoetsiit'),
    
    url(r'^elpais/$', views.elpais, name='elpais'),
    
    url(r'^crawler/$', views.crawler, name='crawler'),
    url(r'^update-bd/$', views.updatebd, name='update-bd'),
    
    
)