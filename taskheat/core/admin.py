from django.contrib import admin
from models import Task, CompletedTask

admin.site.register(Task)
admin.site.register(CompletedTask)
