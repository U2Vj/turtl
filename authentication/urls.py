from django.urls import path

from .views import (ProfileUpdateView, LoginRefreshView, InvitationViewSet, AcceptInvitationView,
                    RenewInvitationView, MyInvitationsViewSet, BulkInvitationViewSet, InstructorViewSet,
                    LogoutView, LoginView)

app_name = 'authentication'
urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('login/refresh', LoginRefreshView.as_view(), name='login_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('profile', ProfileUpdateView.as_view()),
    path('invitations', InvitationViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('invitations/students/bulk', BulkInvitationViewSet.as_view({
        'post': 'create'
    })),
    path('invitations/my', MyInvitationsViewSet.as_view({
        'get': 'list'
    })),
    path('invitations/accept', AcceptInvitationView.as_view()),
    path('invitations/<int:pk>', InvitationViewSet.as_view({
        'delete': 'destroy'
    })),
    path('invitations/<int:pk>/renew', RenewInvitationView.as_view()),
    path('instructors', InstructorViewSet.as_view({'get': 'list'}))
]
