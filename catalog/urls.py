from django.urls import path

from .views import (ProjectViewSet, ProjectDetailViewSet, TaskViewSet, TaskDetailViewSet,
                    ClassroomViewSet, ClassroomDetailViewSet, MyClassroomsViewSet)

app_name = 'catalog'
urlpatterns = [
    path('classrooms', ClassroomViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('classrooms/my', MyClassroomsViewSet.as_view({
        'get': 'list'
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
