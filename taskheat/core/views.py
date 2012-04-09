from django.views.generic import ListView
from taskheat.core.models import Task

class TaskListView(ListView):
    allow_empty=True

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)