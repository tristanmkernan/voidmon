import bs4
import requests

from .entities import ScanIssueEntity


def scan_url(url: str) -> list[ScanIssueEntity]:
    response = requests.get(url, headers={"Accept": "text/html"})

    if "text/html" not in response.headers.get("Content-Type", ""):
        return [
            ScanIssueEntity(type="error", message="URL did not return HTML content")
        ]

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    issues = []

    # Check external scripts
    for script in soup.find_all("script", src=True):
        src = script["src"]
        if src.startswith(("http://", "https://")):
            issues.append(
                ScanIssueEntity(
                    type="warning", message=f"External script loaded from {src}"
                )
            )

    # Check external stylesheets
    for css in soup.find_all("link", rel="stylesheet"):
        href = css.get("href")
        if href and href.startswith(("http://", "https://")):
            issues.append(
                ScanIssueEntity(
                    type="warning", message=f"External stylesheet loaded from {href}"
                )
            )

    # Check external images
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if src.startswith(("http://", "https://")):
            issues.append(
                ScanIssueEntity(
                    type="info", message=f"External image loaded from {src}"
                )
            )

    return issues
