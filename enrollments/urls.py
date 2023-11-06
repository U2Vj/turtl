from django.urls import path
from .views import EnrollmentViewSet

app_name = 'enrollments'


urlpatterns = [
    path('my', EnrollmentViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('my/<int:pk>', EnrollmentViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    })),
]
