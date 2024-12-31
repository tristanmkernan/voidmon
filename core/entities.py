from dataclasses import dataclass


@dataclass
class ScanIssueEntity:
    type: str  # TODO enum
    message: str

    @property
    def model_dump(self):
        return {
            "type": self.type,
            "message": self.message,
        }
