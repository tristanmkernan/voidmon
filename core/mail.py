from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from .models import NotificationSubscription


def send_subscription_confirmation_email(subscription: NotificationSubscription):
    unsubscribe_url = f"{settings.SITE_URL}{reverse('subscription_unsubscribe', kwargs={'uuid': subscription.uuid})}"

    message = f"""
        You've subscribed to receive email notifications for recurring scans of the following URL:
        {subscription.url}

        You can unsubscribe at any time by clicking the link below:
        {unsubscribe_url}
    """

    send_mail(
        subject="[Voidmon] Subscription confirmed",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscription.email],
    )


def send_scan_report_email():
    pass
