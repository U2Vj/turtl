from django.urls import path

from .views import EnrollmentViewSet, EnrollmentDetailViewSet, ClassroomEnrollmentListView, TaskSubmissionView

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
    })),
    path('<int:enrollment_id>/tasks/<int:task_id>/submit', TaskSubmissionView.as_view())
]