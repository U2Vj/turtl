from django.contrib import admin
from .models import ClassroomTemplate, ProjectTemplate, ProjectBadge, TaskTemplate


# Register your models here.
admin.site.register(ClassroomTemplate)

admin.site.register(ProjectBadge)

admin.site.register(ProjectTemplate)

admin.site.register(TaskTemplate)

