from django.conf.urls import patterns, url

from service import views

urlpatterns = patterns ('',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^registro-de-(?P<fulanito>\w+)$', views.registro, name='registro'),
    url(r'^registro-pre/(?P<suco>\w+)', views.registro, name='registro'),
    
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^registro-avanzado/$', views.registro, name='registro'),
    url(r'^login/$', views.login, name='login'),
    url(r'^bienvenida/$', views.index, name='bienvenida'),
)