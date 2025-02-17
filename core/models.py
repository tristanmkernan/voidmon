import os

from urllib.parse import urlparse
from uuid import uuid4

from django.db import models

from .enums import ScanIssueType, ScanIssueSeverity


class Scan(models.Model):
    class ScanStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        ERROR = "error", "Error"

    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    url = models.URLField(max_length=8192)
    status = models.CharField(
        max_length=255, choices=ScanStatus.choices, default=ScanStatus.PENDING
    )
    error = models.TextField(blank=True, null=True)

    @property
    def last_updated_at(self):
        return self.finished_at or self.started_at or self.created_at

    @property
    def is_complete(self):
        return (
            self.status == self.ScanStatus.SUCCESS
            or self.status == self.ScanStatus.ERROR
        )

    @property
    def friendly_url_display(self):
        return self.url.replace("https://", "").replace("http://", "")

    @property
    def grade(self):
        if self.status != self.ScanStatus.SUCCESS:
            return None

        if self.num_vulnerabilities > 0:
            return "F"
        elif self.num_warnings > 0:
            return "C"
        return "A"

    @property
    def num_vulnerabilities(self):
        return sum(
            1
            for issue in self.scanissue_set.all()
            if issue.severity == ScanIssueSeverity.VULNERABILITY
        )

    @property
    def num_warnings(self):
        return sum(
            1
            for issue in self.scanissue_set.all()
            if issue.severity == ScanIssueSeverity.WARNING
        )

    @property
    def num_info(self):
        return sum(
            1
            for issue in self.scanissue_set.all()
            if issue.severity == ScanIssueSeverity.INFO
        )

    def __str__(self):
        return f"Scan of {self.url} - {self.get_status_display()}"


class ScanIssue(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    scan = models.ForeignKey(Scan, on_delete=models.CASCADE)

    type = models.CharField(
        max_length=255,
        choices=ScanIssueType.choices,
    )
    severity = models.CharField(
        max_length=255,
        choices=ScanIssueSeverity.choices,
    )
    message = models.TextField()

    @property
    def severity_ranking(self):
        """Supports sorting a list of scan issues by severity, from least to most severe by default (ascending)"""
        return {
            ScanIssueSeverity.INFO: 1,
            ScanIssueSeverity.WARNING: 2,
            ScanIssueSeverity.VULNERABILITY: 3,
        }[self.severity]


class DynamicScanResults(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    scan = models.OneToOneField(Scan, on_delete=models.CASCADE)

    # TODO nullable stats, or something else, because page may not load!
    dom_content_loaded_after = models.IntegerField()  # ms
    load_after = models.IntegerField()  # ms
    network_idle_after = models.IntegerField()  # ms

    num_requests = models.IntegerField()
    size = models.IntegerField()  # bytes


class DynamicScanRequest(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    dynamic_scan_results = models.ForeignKey(
        DynamicScanResults, on_delete=models.CASCADE, related_name="request_set"
    )

    url = models.URLField(max_length=8192)
    method = models.CharField()  # GET, POST, etc.
    resource_type = models.CharField()  # document, script, stylesheet, image, fetch

    status = models.IntegerField(null=True)  # http status
    error = models.CharField(null=True)
    size = models.IntegerField(null=True)  # bytes

    @property
    def friendly_url_path(self):
        return os.path.basename(urlparse(self.url).path)


class NotificationSubscription(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    url = models.URLField(max_length=8192)
    email = models.EmailField()

    def __str__(self):
        return f"{self.email} -> {self.url}"
