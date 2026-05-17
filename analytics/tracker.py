import logging
from .models import AnalyticsEvent

logger = logging.getLogger(__name__)


def track(event_type, *, user=None, classroom_id=None, task_id=None, lab_environment_id=None, **metadata):
    try:
        AnalyticsEvent.objects.create(
            event_type=event_type,
            user=user if (user is not None and user.is_authenticated) else None,
            classroom_id=classroom_id,
            task_id=task_id,
            lab_environment_id=lab_environment_id,
            metadata=metadata,
        )
    except Exception:
        logger.exception("analytics tracking failed for %s", event_type)