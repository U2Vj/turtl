from django.urls import path

from .views import (ProjectViewSet, ProjectDetailViewSet, TaskViewSet, TaskDetailViewSet,
                    ClassroomViewSet, ClassroomDetailViewSet)

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'catalog'
urlpatterns = [
    path('classrooms', ClassroomViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('classrooms/<int:pk>', ClassroomDetailViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('projects', ProjectViewSet.as_view({
        'post': 'create'
    })),
    path('projects/<int:pk>', ProjectDetailViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('tasks', TaskViewSet.as_view({
        'post': 'create'
    })),
    path('tasks/<int:pk>', TaskDetailViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]
