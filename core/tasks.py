from celery import shared_task, chain
from django.utils import timezone

from .mail import send_subscription_confirmation_email, send_scan_results_email
from .models import (
    DynamicScanResults,
    DynamicScanRequest,
    Scan,
    ScanIssue,
    NotificationSubscription,
)
from .services import scan_url


@shared_task
def run_scan(scan_id: int):
    scan = Scan.objects.get(pk=scan_id)

    scan.status = Scan.ScanStatus.RUNNING
    scan.started_at = timezone.now()
    scan.save()

    try:
        scan_results = scan_url(scan.url)
    except Exception as e:  # TODO: more fine grained exception handling
        scan.status = Scan.ScanStatus.ERROR
    else:
        ## persistence
        for issue_entity in scan_results.issues:
            ScanIssue.objects.create(scan=scan, **issue_entity.model_dump)

        dsc = DynamicScanResults.objects.create(
            scan=scan, **scan_results.dynamic_scan_results.model_dump
        )

        for dsre in scan_results.dynamic_scan_results.requests:
            DynamicScanRequest.objects.create(
                dynamic_scan_results=dsc, **dsre.model_dump
            )

        scan.status = Scan.ScanStatus.SUCCESS

    scan.finished_at = timezone.now()
    scan.save()


@shared_task
def run_daily_scans():
    for subscription in NotificationSubscription.objects.all():
        # create a scan, then queue its running and results processing
        scan = Scan.objects.create(url=subscription.url)

        chain(
            run_scan.s(scan.pk),
            process_scan_results.s(scan_id=scan.pk, subscription_id=subscription.pk),
        ).delay()


@shared_task
def process_scan_results(*args, scan_id: int, subscription_id: int, **kwargs):
    """
    If there are any vulnerabilities, queue an email. Otherwise, ignore.
    """
    scan = Scan.objects.get(pk=scan_id)

    if scan.num_vulnerabilities > 0:
        queue_scan_results_email.delay(scan.pk, subscription_id)


@shared_task
def queue_scan_results_email(scan_id: int, subscription_id: int):
    scan = Scan.objects.get(pk=scan_id)
    subscription = NotificationSubscription.objects.get(id=subscription_id)
    send_scan_results_email(scan, subscription)


@shared_task
def queue_subscription_confirmation_email(subscription_id: int):
    subscription = NotificationSubscription.objects.get(id=subscription_id)
    send_subscription_confirmation_email(subscription)
