from django.contrib import admin
from .models import AnalyticsEvent


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'event_type', 'user', 'task', 'classroom', 'lab_environment_id']
    list_filter = ['event_type', 'created_at']
