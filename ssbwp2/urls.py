from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ssbwp2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^service/', include('service.urls')),
    # url(r'^admins/', include(simple.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
