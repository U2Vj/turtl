from django.urls import path

from .views import ClassroomTemplateList, ClassroomTemplateDetail, ProjectTemplateList, ProjectTemplateDetail, \
    TaskTemplateList, TaskTemplateDetail


# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'authentication'
urlpatterns = [
    path('/templates/classrooms', ClassroomTemplateList.as_view(), name='classroom-template-list'),
    path('/templates/classrooms/<int:template_id>', ClassroomTemplateDetail.as_view(), name='classroom-template-detail'),
    path('/templates/projects/', ProjectTemplateList.as_view(), name='project-template-list'),
    path('/templates/projects/<int:project_id>/', ProjectTemplateDetail.as_view(), name='project-template-detail'),
    path('/templates/tasks/', TaskTemplateList.as_view(), name='task-template-list'),
    path('/templates/tasks/<int:task_id>/', TaskTemplateDetail.as_view(), name='task-template-detail')
]