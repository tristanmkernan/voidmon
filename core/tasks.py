from celery import shared_task
from django.utils import timezone

from .mail import send_subscription_confirmation_email
from .models import Scan, ScanIssue, NotificationSubscription
from .services import scan_url


@shared_task
def run_scan(scan_id: int):
    scan = Scan.objects.get(id=scan_id)

    scan.status = Scan.ScanStatus.RUNNING
    scan.started_at = timezone.now()
    scan.save()

    try:
        issue_entities = scan_url(scan.url)
    except Exception as e:  # TODO: more fine grained exception handling
        scan.status = Scan.ScanStatus.ERROR
    else:
        for issue_entity in issue_entities:
            ScanIssue.objects.create(scan=scan, **issue_entity.model_dump)

        scan.status = Scan.ScanStatus.SUCCESS

    scan.finished_at = timezone.now()
    scan.save()


@shared_task
def run_daily_scans():
    # Bulk create scans for all subscriptions
    scans = [
        Scan(url=subscription.url)
        for subscription in NotificationSubscription.objects.all()
    ]
    created_scans = Scan.objects.bulk_create(scans)

    # Run scans asynchronously
    for scan in created_scans:
        # TODO
        pass
        # result = run_scan.delay(scan.id)

        # TODO email the user if the scan has vulnerabilities


@shared_task
def queue_subscription_confirmation_email(subscription_id: int):
    subscription = NotificationSubscription.objects.get(id=subscription_id)
    send_subscription_confirmation_email(subscription)
