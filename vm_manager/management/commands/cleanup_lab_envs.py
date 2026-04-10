from datetime import timedelta
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from django.db.models import Q

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
        stop_threshold = now - timedelta(hours=STOP_AFTER_HOURS)  
        cleanup_threshold = now - timedelta(hours=CLEANUP_AFTER_HOURS)

        active_envs = LabEnvironment.objects.filter(
            Q(status='active') | Q(status='degraded'),
            last_seen_at__lt=stop_threshold,
        ).select_related('task', 'user')
        for env in active_envs:
            try:
                pm.stop_environment(env)
                logger.info("Stopped env_id=%s (user=%s, task=%s)", env.id, env.user_id, env.task_id)
            except Exception:
                logger.exception("Failed stopping env_id=%s", env.id)
        
        stopped_envs = LabEnvironment.objects.filter(status='stopped', stopped_at__isnull=False, stopped_at__lt=cleanup_threshold).select_related('task', 'user')
        for env in stopped_envs:
            try:
                result = pm.cleanup_environment(env.user, env.task)
                if result == 'deleted':
                    logger.info(f"Cleaned up env {env.id} (user={env.user_id}, task={env.task_id})")
                elif result == 'locked':
                    logger.info(
                        "Cleanup locked env_id=%s user_id=%s task_id=%s (will retry next run)",
                        env.id,
                        env.user_id,
                        env.task_id,
                    )
                elif result == 'not_found':
                    logger.info(
                        "Cleanup skipped: env already gone env_id=%s user_id=%s task_id=%s",
                        env.id,
                        env.user_id,
                        env.task_id,
                    )
                else:
                    logger.warning(
                        "Cleanup failed env_id=%s user_id=%s task_id=%s (will retry next run)",
                        env.id,
                        env.user_id,
                        env.task_id,
                    )
            except Exception:
                logger.exception("Failed cleaning up env_id=%s", env.id)

        # cleanup orphans
        try:
            pm.cleanup_orphans()
            logger.info("Finished orphan cleanup sweep")
        except Exception:
            logger.exception("Failed orphan cleanup sweep")
