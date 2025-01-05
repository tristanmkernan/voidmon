from django.db import models


class ScanIssueSeverity(models.TextChoices):
    INFO = "info", "Info"
    WARNING = "warning", "Warning"
    VULNERABILITY = "vulnerability", "Vulnerability"


class ScanIssueType(models.TextChoices):
    EXTERNAL_SCRIPT_NO_INTEGRITY_HASH = (
        "external_script_no_integrity_hash",
        "External Script No Integrity Hash",
    )
    EXTERNAL_STYLESHEET_NO_INTEGRITY_HASH = (
        "external_stylesheet_no_integrity_hash",
        "External Stylesheet No Integrity Hash",
    )
    REMOTE_RESOURCE_LOADED_OVER_HTTP = (
        "remote_resource_loaded_over_http",
        "Remote Resource Loaded Over HTTP",
    )
    NON_HTML_RESPONSE = "non_html_response", "Non HTML Response"
