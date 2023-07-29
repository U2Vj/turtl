from django.contrib import admin
from .models import ClassroomTemplate, ProjectTemplate, TaskTemplate, AcceptanceCriteria, HelpfulResource, \
    Virtualization

# Register your models here.
admin.site.register(ClassroomTemplate)

admin.site.register(ProjectTemplate)

admin.site.register(TaskTemplate)

admin.site.register(AcceptanceCriteria)

admin.site.register(HelpfulResource)

admin.site.register(Virtualization)
