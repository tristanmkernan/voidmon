from typing import Any
from django.views.generic import (
    CreateView,
    DetailView,
    TemplateView,
)
from django.urls import reverse

from .models import Scan, NotificationSubscription
from .forms import ScanRequestForm, SubscriptionCreateForm
from .tasks import run_scan


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ScanRequestForm()
        return context


class DocsView(TemplateView):
    template_name = "core/docs.html"


class ScanDetailView(DetailView):
    model = Scan
    template_name = "core/scan_detail.html"
    slug_field = "uuid"
    slug_url_kwarg = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscription_form"] = SubscriptionCreateForm()
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

    def get_initial(self) -> dict[str, Any]:
        # TODO pre-fill the url with the url from the scan
        return super().get_initial()

    def get_success_url(self):
        # TODO redirect back to the previous page
        # TODO show a success message
        return reverse("scan_detail", kwargs={"uuid": self.object.uuid})
