from django.urls import path

from .views import (ProjectNew, ProjectDetail, TaskNew, TaskDetail,
                    ClassroomViewSet, ClassroomInstructorViewSet, ClassroomDetailViewSet)

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'catalog'
urlpatterns = [
    path('classrooms', ClassroomViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('classrooms/<int:pk>', ClassroomDetailViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('projects', ProjectNew.as_view()),
    path('projects/<int:project_id>/', ProjectDetail.as_view()),
    path('tasks/', TaskNew.as_view()),
    path('tasks/<int:task_id>/', TaskDetail.as_view()),
    path('users/instructors', ClassroomInstructorViewSet.as_view({'get': 'list'})),
]