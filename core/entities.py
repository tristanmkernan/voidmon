from dataclasses import dataclass

from .constants import SCAN_ISSUE_TYPE_TO_DEFAULT_MESSAGE, SCAN_ISSUE_TYPE_TO_SEVERITY
from .enums import ScanIssueSeverity, ScanIssueType


@dataclass
class ScanIssueEntity:
    type: ScanIssueType
    message: str | None = None

    def __post_init__(self):
        if self.message is None:
            self.message = SCAN_ISSUE_TYPE_TO_DEFAULT_MESSAGE[self.type]

    @property
    def severity(self) -> ScanIssueSeverity:
        return SCAN_ISSUE_TYPE_TO_SEVERITY[self.type]

    @property
    def model_dump(self) -> dict:
        return {
            "type": self.type,
            "message": self.message,
            "severity": self.severity,
        }


@dataclass
class DynamicScanRequestEntity:
    url: str
    method: str
    resource_type: str

    status: str | None
    error: str | None
    size: int | None

    @property
    def model_dump(self) -> dict:
        return {
            "url": self.url,
            "method": self.method,
            "resource_type": self.resource_type,
            "status": self.status,
            "error": self.error,
            "size": self.size,
        }


@dataclass
class DynamicScanResultsEntity:
    dom_content_loaded_after: int
    load_after: int
    network_idle_after: int

    num_requests: int
    size: int

    requests: list[DynamicScanRequestEntity]

    @property
    def model_dump(self) -> dict:
        return {
            "dom_content_loaded_after": self.dom_content_loaded_after,
            "load_after": self.load_after,
            "network_idle_after": self.network_idle_after,
            "num_requests": self.num_requests,
            "size": self.size,
        }


@dataclass
class ScanResultsEntity:
    issues: list[ScanIssueEntity]
    dynamic_scan_results: DynamicScanResultsEntity
