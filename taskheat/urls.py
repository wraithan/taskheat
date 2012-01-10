from django.conf.urls.defaults import patterns, include, url
from django.views.generic.list import ListView
from core.models import Task

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$',
        ListView.as_view(allow_empty=True,
                         model=Task),
        name='core_tast_list'),
    # url(r'^taskheat/', include('taskheat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
