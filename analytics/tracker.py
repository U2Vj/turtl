import logging
from .models import AnalyticsEvent

logger = logging.getLogger(__name__)


def track(event_type, *, user=None, classroom=None, task=None, lab_environment=None, **metadata):
    try:
        AnalyticsEvent.objects.create(
            event_type=event_type,
            user=user if (user is not None and user.is_authenticated) else None,
            classroom=classroom,
            task=task,
            lab_environment_id=lab_environment.id if lab_environment else None,
            metadata=metadata,
        )
    except Exception:
        logger.exception('analytics tracking failed for %s', event_type)