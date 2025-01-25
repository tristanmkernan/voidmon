from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from textwrap import dedent

from .models import NotificationSubscription, Scan


def send_subscription_confirmation_email(subscription: NotificationSubscription):
    unsubscribe_url = f"{settings.SITE_URL}{reverse('subscription_unsubscribe', kwargs={'uuid': subscription.uuid})}"

    message = dedent(
        f"""
        You've subscribed to receive email notifications for recurring scans of the following URL:
        {subscription.url}

        You can unsubscribe at any time by clicking the link below:
        {unsubscribe_url}
    """
    )

    send_mail(
        subject="[Voidmon] Subscription confirmed",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscription.email],
    )


def send_scan_results_email(scan: Scan, subscription: NotificationSubscription):
    unsubscribe_url = f"{settings.SITE_URL}{reverse('subscription_unsubscribe', kwargs={'uuid': subscription.uuid})}"
    scan_details_url = (
        f"{settings.SITE_URL}{reverse('scan_detail', kwargs={ 'uuid': scan.uuid })}"
    )

    message = dedent(
        f"""
        Vulnerabilities were discovered during the recurring scan of the following URL:
        {scan.url}

        You can find the full scan report here:
        {scan_details_url}

        You can unsubscribe at any time by clicking the link below:
        {unsubscribe_url}
    """
    )

    send_mail(
        subject="[Voidmon] Vulnerabilities found",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[subscription.email],
    )
