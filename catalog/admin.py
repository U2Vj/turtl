from django.contrib import admin
from .models import ClassroomTemplate, ProjectTemplate, TaskTemplate, AcceptanceCriteria

# Register your models here.
admin.site.register(ClassroomTemplate)

admin.site.register(ProjectTemplate)

admin.site.register(TaskTemplate)

admin.site.register(AcceptanceCriteria)


