from django.urls import path

from .views import EnrollmentViewSet, EnrollmentDetailViewSet, ClassroomEnrollmentListView, task_submission_view

app_name = 'enrollments'


urlpatterns = [
    path('my', EnrollmentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='enrollments'),
    path('<int:pk>', EnrollmentDetailViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='enrollment-detail'),
    path('for-classroom/<int:pk>', ClassroomEnrollmentListView.as_view({
        'get': 'list_enrollments'
    }), name='classroom-enrollments'),
    path('<int:enrollment_id>/tasks/<int:task_id>/submit', task_submission_view, name='verify_task_solution')
]