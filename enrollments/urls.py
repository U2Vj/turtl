from django.urls import path
from .views import EnrollmentViewSet, EnrollmentDetailViewSet, ClassroomEnrollmentListView

app_name = 'enrollments'


urlpatterns = [
    path('my', EnrollmentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<int:pk>', EnrollmentDetailViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    })),
    path('for-classroom/<int:pk>', ClassroomEnrollmentListView.as_view({
        'get': 'list_enrollments'
    }), name='classroom-enrollments')
]
