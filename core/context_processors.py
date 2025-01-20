from core.enums import ScanIssueSeverity, ScanIssueType


def add_enums(request):
    return {
        "ScanIssueSeverity": ScanIssueSeverity,
        "ScanIssueType": ScanIssueType,
    }
