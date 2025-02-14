import math
import time

from functools import partial
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, Page, Request

import bs4
import requests

from .entities import (
    DynamicScanResultsEntity,
    DynamicScanRequestEntity,
    ScanIssueEntity,
    ScanResultsEntity,
)
from .enums import ScanIssueType

TIMEOUT = 10


# TODO finish implementing this
def match_netloc(site_netloc: str, resource_netloc: str) -> bool:
    # Extract registered domain using tld library which handles all edge cases
    from tld import get_fld

    try:
        site_domain = get_fld(f"https://{site_netloc}", fix_protocol=True)
        resource_domain = get_fld(f"https://{resource_netloc}", fix_protocol=True)
        return site_domain == resource_domain
    except Exception:
        # If domain parsing fails, fall back to exact match
        return site_netloc == resource_netloc


def is_external_resource(site_url: str, resource_url: str) -> bool:
    site_domain = urlparse(site_url).netloc

    # Handle absolute URLs
    if resource_url.startswith(("http://", "https://")):
        resource_domain = urlparse(resource_url).netloc
        return resource_domain != site_domain

    # Handle protocol-relative URLs (//example.com/script.js)
    if resource_url.startswith("//"):
        resource_domain = urlparse(f"https:{resource_url}").netloc
        return resource_domain != site_domain

    # All other URLs (relative paths, absolute paths) are internal
    return False


def scan_url_for_static_issues(url: str) -> list[ScanIssueEntity]:
    response = requests.get(url, headers={"Accept": "text/html"}, timeout=TIMEOUT)

    if "text/html" not in response.headers.get("Content-Type", ""):
        return [ScanIssueEntity(type=ScanIssueType.NON_HTML_RESPONSE)]

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    issues: list[ScanIssueEntity] = []

    # Check external scripts
    for script in soup.find_all("script", src=True):
        src = script["src"]

        ## Non-HTTPS
        if src.startswith("http://"):
            issues.append(
                ScanIssueEntity(
                    type=ScanIssueType.REMOTE_RESOURCE_LOADED_OVER_HTTP,
                    message=f"Resource loaded over HTTP: {src}",
                )
            )

        is_external = is_external_resource(url, src)

        ## No integrity hash
        if is_external and "integrity" not in script.attrs:
            issues.append(
                ScanIssueEntity(
                    type=ScanIssueType.EXTERNAL_SCRIPT_NO_INTEGRITY_HASH,
                    message=f"External script missing integrity hash: {src}",
                )
            )

    # Check external stylesheets
    for css in soup.find_all("link", rel="stylesheet"):
        href = css.get("href")

        ## Non-HTTPS
        if href and href.startswith("http://"):
            issues.append(
                ScanIssueEntity(
                    type=ScanIssueType.REMOTE_RESOURCE_LOADED_OVER_HTTP,
                    message=f"Resource loaded over HTTP: {href}",
                )
            )

        is_external = is_external_resource(url, href)

        ## No integrity hash
        if is_external and "integrity" not in css.attrs:
            issues.append(
                ScanIssueEntity(
                    type=ScanIssueType.EXTERNAL_STYLESHEET_NO_INTEGRITY_HASH,
                    message=f"External stylesheet loaded from {href}",
                )
            )

    return issues


def scan_url_for_dynamic_issues(
    url: str,
) -> tuple[list[ScanIssueEntity], DynamicScanResultsEntity]:
    issues = []
    requests: list[DynamicScanRequestEntity] = []
    event_timings = {}

    def handle_timing_event(event_name: str, *args):
        # TODO use the in-depth browser performance metrics instead
        event_timings[event_name] = math.floor((time.monotonic() - started_at) * 1_000)

    def handle_request_failed_event(request: Request):
        requests.append(
            DynamicScanRequestEntity(
                url=request.url,
                method=request.method,
                status=getattr(request.response(), "status", None),
                resource_type=request.resource_type,
                size=request.sizes().get("responseBodySize", None),
                error=request.failure,
            )
        )

    def handle_request_finished_event(request: Request):
        requests.append(
            DynamicScanRequestEntity(
                url=request.url,
                method=request.method,
                status=getattr(request.response(), "status", None),
                resource_type=request.resource_type,
                size=request.sizes().get("responseBodySize", None),
                error=request.failure,
            )
        )

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        started_at = time.monotonic()

        page.on("requestfinished", handle_request_finished_event)
        page.on("requestfailed", handle_request_failed_event)

        page.on("domcontentloaded", partial(handle_timing_event, "domcontentloaded"))
        page.on("load", partial(handle_timing_event, "load"))

        try:
            page.goto(url, wait_until="networkidle")

            handle_timing_event("networkidle")
        except Exception as e:
            print(f"Navigation failed: {e}")

        browser.close()

    scan_results = DynamicScanResultsEntity(
        dom_content_loaded_after=event_timings["domcontentloaded"],
        load_after=event_timings["load"],
        network_idle_after=event_timings["networkidle"],
        num_requests=len(requests),
        size=sum((request.size or 0 for request in requests), 0),
        requests=requests,
    )

    return issues, scan_results


def scan_url(url: str) -> ScanResultsEntity:
    static_issues = scan_url_for_static_issues(url)
    dynamic_issues, dynamic_scan_results = scan_url_for_dynamic_issues(url)

    results = ScanResultsEntity(
        issues=[*static_issues, *dynamic_issues],
        dynamic_scan_results=dynamic_scan_results,
    )

    return results
