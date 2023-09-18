from django.contrib import admin
from .models import (ClassroomTemplate, ClassroomTemplateInstructor, ProjectTemplate, TaskTemplate, \
                     AcceptanceCriteria, Question, QuestionChoice, HelpfulResource, Virtualization)

# Register your models here.
admin.site.register(ClassroomTemplate)

admin.site.register(ClassroomTemplateInstructor)

admin.site.register(ProjectTemplate)

admin.site.register(TaskTemplate)

admin.site.register(AcceptanceCriteria)

admin.site.register(Question)

admin.site.register(QuestionChoice)

admin.site.register(HelpfulResource)

admin.site.register(Virtualization)
