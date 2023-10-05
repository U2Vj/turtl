from django.contrib import admin
from .models import (Classroom, ClassroomInstructor, Project, Task, AcceptanceCriteria,
                     Question, QuestionChoice, HelpfulResource, Virtualization)

# Register your models here.
admin.site.register(Classroom)

admin.site.register(ClassroomInstructor)

admin.site.register(Project)

admin.site.register(Task)

admin.site.register(AcceptanceCriteria)

admin.site.register(Question)

admin.site.register(QuestionChoice)

admin.site.register(HelpfulResource)

admin.site.register(Virtualization)
