from django.urls import path

from catalog.views import ClassroomTemplateList, ClassroomTemplateDetail, ProjectTemplateList, ProjectTemplateDetail, \
    TaskTemplateList, TaskTemplateDetail
from .views import (RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView)

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'authentication'
urlpatterns = [
    path('users/register', RegistrationAPIView.as_view()),
    path('users/login', LoginAPIView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('/templates/classrooms', ClassroomTemplateList.as_view(), name='classroom-template-list'),
    path('/templates/classrooms/<int:template_id>', ClassroomTemplateDetail.as_view(), name='classroom-template-detail'),
    path('projects/', ProjectTemplateList.as_view(), name='project-template-list'),
    path('projects/<int:project_id>/', ProjectTemplateDetail.as_view(), name='project-template-detail'),
    path('tasks/', TaskTemplateList.as_view(), name='task-template-list'),
    path('tasks/<int:task_id>/', TaskTemplateDetail.as_view(), name='task-template-detail')
]
