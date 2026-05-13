from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save
from django.dispatch import receiver

from authentication.models import User


@receiver(pre_save, sender=User)
def disconnect_shell_on_deactivate(sender, instance: User, **kwargs):
    if not instance.pk:
        return
    try:
        previous = User.objects.get(pk=instance.pk)
    except User.DoesNotExist:
        return
    if not (previous.is_active and not instance.is_active):
        return

    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        f"user_{instance.pk}",
        {"type": "force_disconnect"},
    )
