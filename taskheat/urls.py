from core.models import Task
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.list import ListView


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(allow_empty=True,
                         model=Task),
        name='core_tast_list'),
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^admin/doc/',
        include('django.contrib.admindocs.urls')),
    url(r'^accounts/',
        include('django.contrib.auth.urls')),
)
