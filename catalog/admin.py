from django.contrib import admin
from .models import (ClassroomTemplate, ClassroomTemplateManager, ProjectTemplate, TaskTemplate, \
                     AcceptanceCriteria, Question, HelpfulResource, Virtualization)

# Register your models here.
admin.site.register(ClassroomTemplate)

admin.site.register(ClassroomTemplateManager)

admin.site.register(ProjectTemplate)

admin.site.register(TaskTemplate)

admin.site.register(AcceptanceCriteria)

admin.site.register(Question)

admin.site.register(Question.QuestionChoice)

admin.site.register(HelpfulResource)

admin.site.register(Virtualization)
