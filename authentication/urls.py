from django.urls import path

from .views import (ProfileUpdateView, TestProtectedView, LoginRefreshView)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenBlacklistView,
)

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'authentication'
urlpatterns = [
    path('users/login', TokenObtainPairView.as_view(), name='login'),
    path('users/login/refresh', LoginRefreshView.as_view(), name='login_refresh'),
    path('users/logout', TokenBlacklistView.as_view(), name='logout'),
    path('users/login/test', TestProtectedView.as_view()),
    path('users/profile', ProfileUpdateView.as_view()),
]
