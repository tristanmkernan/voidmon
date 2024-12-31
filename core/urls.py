from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("scan/", views.ScanRequestView.as_view(), name="scan_request"),
    path("scan/<uuid:uuid>/", views.ScanDetailView.as_view(), name="scan_detail"),
    path(
        "subscribe/", views.SubscriptionCreateView.as_view(), name="subscription_create"
    ),
    path("docs/", views.DocsView.as_view(), name="docs"),
]
