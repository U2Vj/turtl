from django.urls import path

from .views import (RegistrationAPIView, UserRetrieveUpdateAPIView, TestProtectedView)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'authentication'
urlpatterns = [
    path('users/register', RegistrationAPIView.as_view()),
    path('users/login', TokenObtainPairView.as_view(), name='login'),
    path('users/login/refresh', TokenRefreshView.as_view(), name='login_refresh'),
    path('users/login/test', TestProtectedView.as_view()),
    path('user', UserRetrieveUpdateAPIView.as_view()),
]
