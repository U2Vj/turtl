from datetime import timedelta
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from vm_manager.models import LabEnvironment
from vm_manager.proxmox_manager import ProxmoxManager

logger = logging.getLogger(__name__)

# Cleanup time config
STOP_AFTER_HOURS = 1
CLEANUP_AFTER_HOURS = 48

class Command(BaseCommand):
    help = "Stops inactive lab environments and deletes stale stopped environments"

    def handle(self, *args, **options):
        now = timezone.now()
        pm = ProxmoxManager()

        active_envs = LabEnvironment.objects.filter(status='active').select_related('task', 'user')
        for env in active_envs:
            if now - env.last_seen_at >= timedelta(hours=STOP_AFTER_HOURS):
                try:
                    pm.stop_environment(env)
                    env.stopped_at = now
                    env.save(update_fields=['stopped_at'])
                    self.stdout.write(f"Stopped env {env.id} (user={env.user_id}, task={env.task_id})")
                except Exception:
                    logger.exception("Failed stopping env_id=%s", env.id)
        
        stopped_envs = LabEnvironment.objects.filter(status='stopped').select_related('task', 'user')
        for env in stopped_envs:
            if now - env.stopped_at >= timedelta(hours=CLEANUP_AFTER_HOURS):
                try:
                    pm.cleanup_environment(env.user, env.task)
                    self.stdout.write(f"Cleaned up env {env.id} (user={env.user_id}, task={env.task_id})")
                except Exception:
                    logger.exception("Failed cleaning up env_id=%s", env.id)

