from django.contrib import admin
from .models import ClassroomTemplate, ProjectTemplate, TaskTemplate, AcceptanceCriteria, HelpfulResource, \
    Virtualization, AcceptanceCriteriaFlag, AcceptanceCriteriaRegex, AcceptanceCriteriaQuestionnaire

# Register your models here.
admin.site.register(ClassroomTemplate)

admin.site.register(ProjectTemplate)

admin.site.register(TaskTemplate)

admin.site.register(AcceptanceCriteriaFlag)

admin.site.register(AcceptanceCriteriaRegex)

admin.site.register(AcceptanceCriteriaQuestionnaire)

admin.site.register(HelpfulResource)

admin.site.register(Virtualization)
