from core.models import Task
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(template_name='core/index.html'),
        name='core_tast_list'),
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^admin/doc/',
        include('django.contrib.admindocs.urls')),
    url(r'^accounts/',
        include('django.contrib.auth.urls')),
)
