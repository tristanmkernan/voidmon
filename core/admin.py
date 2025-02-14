from django.contrib import admin

from .models import (
    NotificationSubscription,
    Scan,
    ScanIssue,
    DynamicScanResults,
    DynamicScanRequest,
)


@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ("url", "status", "created_at")

    readonly_fields = ("uuid", "created_at")


@admin.register(NotificationSubscription)
class NotificationSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("url", "email", "created_at")

    readonly_fields = ("uuid", "created_at")


@admin.register(ScanIssue)
class ScanIssueAdmin(admin.ModelAdmin):
    list_display = ("uuid", "type", "created_at")

    readonly_fields = ("uuid", "created_at")


@admin.register(DynamicScanRequest)
class DynamicScanRequestAdmin(admin.ModelAdmin):
    list_display = ("url", "dynamic_scan_results__uuid", "created_at")

    readonly_fields = ("uuid", "created_at")


@admin.register(DynamicScanResults)
class DynamicScanResultsAdmin(admin.ModelAdmin):
    list_display = ("uuid", "created_at")

    readonly_fields = ("uuid", "created_at")
