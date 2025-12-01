from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:task_id>/', views.start_environment, name='start-environment'),
    path('stop/<int:task_id>/', views.stop_environment, name='stop-environment'),
    path('cleanup/<int:task_id>/', views.cleanup_environment, name='cleanup-environment'),
    path('status/<int:task_id>/', views.environment_status, name='environment-status'),
    path('vnc-ticket/<int:task_id>/', views.vnc_ticket, name='vnc-ticket'),
    path('has-config/<int:task_id>/', views.has_task_vm_config, name='vm-has-config'),
]
