from uuid import uuid4

from django.db import models


class Scan(models.Model):
    class ScanStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        ERROR = "error", "Error"

    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    url = models.URLField()  # TODO expand length from 200 to 1024 chars
    status = models.CharField(
        max_length=255, choices=ScanStatus.choices, default=ScanStatus.PENDING
    )

    @property
    def is_complete(self):
        return (
            self.status == self.ScanStatus.SUCCESS
            or self.status == self.ScanStatus.ERROR
        )

    def __str__(self):
        return f"{self.url} - {self.status}"


class ScanIssue(models.Model):
    class ScanIssueType(models.TextChoices):
        ERROR = "error", "Error"
        WARNING = "warning", "Warning"
        INFO = "info", "Info"

    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    scan = models.ForeignKey(Scan, on_delete=models.CASCADE)

    type = models.CharField(
        max_length=255, choices=ScanIssueType.choices, default=ScanIssueType.ERROR
    )
    message = models.TextField()


class NotificationSubscription(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    url = models.URLField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.email} -> {self.url}"
