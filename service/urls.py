from django.conf.urls import patterns, url

from service import views

urlpatterns = patterns ('',
    url(r'^$', views.index, name='index'),
    url(r'^compae/$', views.compae, name='compae'),
    url(r'^registro-de-(?P<fulanito>\w+)$', views.registro, name='registro'),
    url(r'^registro-pre/(?P<suco>\w+)', views.registropro, name='registro'),
    
    url(r'^heredado/$', views.heredado, name='herencia'),
    
    url(r'^registro/$', views.heredado, name='herencia'),
    url(r'^login/$', views.login, name='login'),
    url(r'^bienvenida/$', views.heredado, name='herencia'),
)