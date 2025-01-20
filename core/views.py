from operator import attrgetter
from django.contrib import messages
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)
from django.urls import reverse

import django_tables2 as tables

from .models import Scan, NotificationSubscription, ScanIssue
from .forms import ScanRequestForm, SubscriptionCreateForm
from .tasks import run_scan, queue_subscription_confirmation_email


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ScanRequestForm()
        return context


class DocsView(TemplateView):
    template_name = "core/docs.html"


class ScanIssueTable(tables.Table):
    class Meta:
        model = ScanIssue
        fields = (
            "severity",
            "type",
            "message",
        )
        orderable = False
        paginate = False
        show_header = False

    message = tables.TemplateColumn(
        template_name="core/scan_issue_table/message_column.html"
    )
    severity = tables.TemplateColumn(
        template_name="core/scan_issue_table/severity_column.html"
    )


class ScanDetailView(DetailView):
    model = Scan
    template_name = "core/scan_detail.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("scanissue_set")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["subscription_form"] = SubscriptionCreateForm(
            initial={
                "url": self.object.url,
            },
            next_url=self.request.path,
        )

        context["re_scan_form"] = ScanRequestForm(
            initial={"url": self.object.url},
            form_id="re-scan-form",
        )

        sorted_scan_issues = sorted(
            self.object.scanissue_set.all(),
            key=attrgetter("severity_ranking"),
            reverse=True,
        )

        context["issues_table"] = ScanIssueTable(sorted_scan_issues)
        return context


class ScanRequestView(CreateView):
    model = Scan
    form_class = ScanRequestForm

    def form_valid(self, form):
        # queue up asynchronous scan
        scan = form.save()
        run_scan.delay(scan.id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("scan_detail", kwargs={"uuid": self.object.uuid})


class SubscriptionCreateView(CreateView):
    model = NotificationSubscription
    form_class = SubscriptionCreateForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Subscribed {self.object.email}")
        queue_subscription_confirmation_email.delay(self.object.id)
        return response

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")

        # don't have a next url, so redirect to the index page
        return reverse("index")


class UnsubscribeView(DeleteView):
    model = NotificationSubscription
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get(self, request, *args, **kwargs):
        # allow GET requests to delete the subscription, e.g. from a link in an email
        response = self.delete(request, *args, **kwargs)
        messages.success(self.request, "Unsubscribed")
        return response

    def get_success_url(self):
        return reverse("index")
