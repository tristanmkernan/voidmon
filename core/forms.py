from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit
from django import forms
from django.urls import reverse
from .models import Scan, NotificationSubscription


class ScanRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove label for url field
        self.fields["url"].label = ""
        self.fields["url"].widget.attrs["placeholder"] = "Enter URL to scan"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Launch Scan",
                "url",
            ),
            Submit("submit", "Run"),
        )
        self.helper.form_action = reverse("scan_request")

    class Meta:
        model = Scan
        fields = [
            "url",
        ]


class SubscriptionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Subscribe",
                "url",
                "email",
            ),
            Submit("submit", "Subscribe"),
        )
        self.helper.form_action = reverse("subscription_create")

    class Meta:
        model = NotificationSubscription
        fields = [
            "url",
            "email",
        ]
