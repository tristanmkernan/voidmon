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
