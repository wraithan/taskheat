from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from taskheat.utils.views import ExtraContextTemplateView


admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$',
        ExtraContextTemplateView.as_view(template_name='core/index.html',
                                         extra_context={
                                             'page_name': 'Home'
                                         }),
        name='home'),
    url(r'^', include('taskheat.core.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)
