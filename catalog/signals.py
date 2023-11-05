from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from catalog.models import Task


@receiver(post_delete, sender=Task)
def delete_orphaned_acceptance_criteria(sender, instance, **kwargs):
    # Check if the acceptance_criteria is no longer referenced by any Task
    if not Task.objects.filter(acceptance_criteria=instance.acceptance_criteria).exists():
        # Delete the orphaned acceptance_criteria
        instance.acceptance_criteria.delete()


@receiver(pre_save, sender=Task)
def check_for_acceptance_criteria_update(sender, instance, **kwargs):
    if instance.pk:
        # Get the original Task from the database
        original_task = Task.objects.get(pk=instance.pk)
        if original_task.acceptance_criteria != instance.acceptance_criteria:
            # Check if the old acceptance_criteria is no longer referenced by any Task
            if not Task.objects.filter(acceptance_criteria=original_task.acceptance_criteria).exclude(
                    pk=instance.pk).exists():
                # Delete the orphaned acceptance_criteria
                original_task.acceptance_criteria.delete()
