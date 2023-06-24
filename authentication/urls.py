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
]
