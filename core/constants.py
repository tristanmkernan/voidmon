from .enums import ScanIssueSeverity, ScanIssueType

SCAN_ISSUE_TYPE_TO_SEVERITY = {
    ScanIssueType.EXTERNAL_SCRIPT_NO_INTEGRITY_HASH: ScanIssueSeverity.WARNING,
    ScanIssueType.EXTERNAL_STYLESHEET_NO_INTEGRITY_HASH: ScanIssueSeverity.WARNING,
    ScanIssueType.REMOTE_RESOURCE_LOADED_OVER_HTTP: ScanIssueSeverity.VULNERABILITY,
    ScanIssueType.NON_HTML_RESPONSE: ScanIssueSeverity.VULNERABILITY,
}

SCAN_ISSUE_TYPE_TO_DEFAULT_MESSAGE = {
    ScanIssueType.NON_HTML_RESPONSE: "URL did not return HTML content",
}
