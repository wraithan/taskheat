from django.conf.urls.defaults import patterns, include, url
from taskheat.core.views import TaskListView

urlpatterns = patterns('',
    url(r'^tasks/$',
        TaskListView.as_view(),
        name='core_task_list'),
)
