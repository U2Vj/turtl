from django.urls import path
from .views import EnrollmentViewSet, EnrollmentDetailViewSet, TaskSolutionVerificationView

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
    path('<int:enrollment_id>/tasks/<int:task_id>/solve', TaskSolutionVerificationView.as_view({
        'post': 'create'
    }), name='verify_task_solution'),
]
