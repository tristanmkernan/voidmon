from celery import shared_task

from .models import Scan, ScanIssue
from .services import scan_url


@shared_task
def run_scan(scan_id: int):
    scan = Scan.objects.get(id=scan_id)

    scan.status = Scan.ScanStatus.RUNNING
    scan.save()

    try:
        issue_entities = scan_url(scan.url)
    except Exception as e:  # TODO: more fine grained exception handling
        scan.status = Scan.ScanStatus.ERROR
    else:
        for issue_entity in issue_entities:
            ScanIssue.objects.create(scan=scan, **issue_entity.model_dump)

        scan.status = Scan.ScanStatus.SUCCESS

    scan.save()
