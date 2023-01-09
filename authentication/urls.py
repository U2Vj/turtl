from django.urls import path

from .views import (RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView, RequestPasswordResetEmailAPIView,
                    SetNewPasswordAPIView)

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'authentication'
urlpatterns = [
    path('users/register', RegistrationAPIView.as_view()),
    path('users/login', LoginAPIView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view()),
    path('request-reset-email', RequestPasswordResetEmailAPIView.as_view(), name='request-reset-email'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='SetNewPassword')
]
