from django.db import models
from django.conf import settings

class AnalyticsEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    event_type = models.CharField(max_length=255, db_index=True)

    classroom = models.ForeignKey('catalog.Classroom', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    task = models.ForeignKey('catalog.Task', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    lab_environment_id = models.IntegerField(null=True, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['user', 'event_type', 'created_at']),
        ]
