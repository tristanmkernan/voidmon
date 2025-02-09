from django.contrib import admin

from .models import NotificationSubscription, Scan, ScanIssue


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
    list_display = ("scan__uuid", "type", "created_at")

    readonly_fields = ("uuid", "created_at")
