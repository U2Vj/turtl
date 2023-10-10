from django.urls import path

from .views import (ProfileUpdateView, TestProtectedView, LoginRefreshView, SendInvitationEmailAPIView,
                    SetNewPasswordAPIView)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenBlacklistView,
)

# This file maps the api endpoints to the corresponding URLs.
# https://docs.djangoproject.com/en/3.1/topics/http/urls/

app_name = 'authentication'
urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', LoginRefreshView.as_view(), name='login_refresh'),
    path('logout', TokenBlacklistView.as_view(), name='logout'),
    path('login/test', TestProtectedView.as_view()),
    path('profile', ProfileUpdateView.as_view()),
    path('request-reset-email', SendInvitationEmailAPIView.as_view(), name='request-reset-email'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='SetNewPassword')
]
