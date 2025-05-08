from django.db.models.signals import post_save
from django.dispatch import receiver

from logs.models.action_log import ActionLog
from logs.models.log import Log


@receiver(post_save, sender=ActionLog)
def create_log_from_action_log(sender, instance, created, **kwargs):
    if created:
        Log.objects.create(
            user=instance.user,
            message=instance.action
        )
