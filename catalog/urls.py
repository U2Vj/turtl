from django.urls import path

from .views import ClassroomTemplateDetail, ProjectTemplateList, ProjectTemplateDetail, \
    TaskTemplateList, TaskTemplateDetail, ClassroomTemplateViewSet, ClassroomTemplateManagerViewSet

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'catalog'
urlpatterns = [
    path('classrooms', ClassroomTemplateViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('classrooms/<int:template_id>', ClassroomTemplateDetail.as_view(), name='classroom-template-detail'),
    path('projects/', ProjectTemplateList.as_view(), name='project-template-list'),
    path('projects/<int:project_id>/', ProjectTemplateDetail.as_view(), name='project-template-detail'),
    path('tasks/', TaskTemplateList.as_view(), name='task-template-list'),
    path('tasks/<int:task_id>/', TaskTemplateDetail.as_view(), name='task-template-detail'),
    path('users/managers', ClassroomTemplateManagerViewSet.as_view({'get': 'list'})),
]