from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:task_id>/', views.start_environment, name='start-environment'),
    path('stop/<int:task_id>/', views.stop_environment, name='stop-environment'),
    path('status/<int:task_id>/', views.environment_status, name='environment-status'),
    path('vnc-ticket/<int:task_id>/', views.vnc_ticket, name='vnc-ticket'),
]
