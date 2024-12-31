from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit
from django import forms
from django.urls import reverse
from .models import Scan, NotificationSubscription


class ScanRequestForm(forms.ModelForm):
    def __init__(self, *args, form_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove label for url field
        self.fields["url"].label = ""
        self.fields["url"].widget.attrs["placeholder"] = "Enter URL to scan"

        self.helper = FormHelper()

        if form_id:
            self.helper.form_id = form_id

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
    def __init__(self, *args, next_url=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            "url",
            "email",
            Submit("submit", "Subscribe"),
        )

        form_action = reverse("subscription_create")

        if next_url:
            form_action = f"{form_action}?next={next_url}"

        self.helper.form_action = form_action

    class Meta:
        model = NotificationSubscription
        fields = [
            "url",
            "email",
        ]
