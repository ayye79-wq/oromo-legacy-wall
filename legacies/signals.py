import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Legacy

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Legacy)
def notify_admin_on_submission(sender, instance, created, **kwargs):
    if not created:
        return

    admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', '')
    if not admin_email:
        logger.debug('ADMIN_NOTIFICATION_EMAIL not set — skipping submission email.')
        return

    try:
        send_mail(
            subject=f'[Oromo Legacy Wall] New submission: {instance.full_name}',
            message=(
                f'A new memorial submission has been received and is awaiting moderation.\n\n'
                f'Name: {instance.full_name}\n'
                f'Zone: {instance.zone.name}\n'
                f'Relationship: {instance.relationship_to_person or "Not specified"}\n'
                f'Language: {instance.get_original_language_display()}\n'
                f'Submitted: {instance.created_at.strftime("%B %d, %Y at %H:%M UTC")}\n\n'
                f'Story preview:\n{(instance.story_en or instance.story)[:300]}...\n\n'
                f'Review at your moderation dashboard.'
            ),
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@oromolegacywall.com'),
            recipient_list=[admin_email],
            fail_silently=True,
        )
        logger.info(f'Submission notification sent for legacy {instance.pk}: {instance.full_name}')
    except Exception as e:
        logger.warning(f'Could not send submission notification: {e}')
