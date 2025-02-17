## Inspiration

- https://dribbble.com/shots/20206060-Workflow-Builder-Data-Visualisation
- https://dribbble.com/shots/24093921-Scan-Details

## Links

- [https://marcusfelling.com/blog/2023/measuring-website-performance-with-playwright-test-and-navigation-timing-api/](Improve performance metrics in dynamic scan)
- [https://www.checklyhq.com/learn/playwright/performance/](Even more in depth article on performance testing in Playwright)
- [https://playwright.dev/python/docs/api/class-request](Playwright: Request class)
- [https://playwright.dev/docs/docker#run-the-image](Playwright: In Docker)

## Launch

- [x] Scanning implementation
- [x] Finish scan detail page
- [ ] ~~Email working~~
  - [x] Email disabled until post-launch
- [x] Production ready
- [x] Launched 🚀

### Post-launch

- [x] Improve scan detail page UI
  - [x] Improve the issues table
  - [x] Responsive design
- [x] Email support
  - [x] Daily email task
- [ ] Add email subscription management
- [ ] Address [SSRF](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery)
  - Limit inputs to external URLs
  - Docker internal networking security?
- [x] Add timeout to requests
- [~] Browser based / dynamic checks
  - [x] 1. DNS resolution failure for external resource aka Dangling domain
  - [ ] 2. Integrity hash violation
  - [x] 3. Dangling DNS records
- [ ] Resolve TODOs
- [ ] Static checks 
  - [ ] Verify resource integrity (see dynamic checks)
- [x] Create website that has vulnerabilities for demo and testing purposes
  - Can reproduce using Playwright request routing to failure.
- [ ] Setup Docker Chromium security. See https://playwright.dev/docs/docker#run-the-image
- [ ] Enforce timeouts/limits on browser usage.
- [ ] Crawl top N Alexa pages
  - [ ] Show results on home page. "Featured" scans?
- [ ] Use browser timings API for performance
- [ ] Improve display of dynamic scan requests table
- [ ] Is domain available for purchase? Or at least unregistered?
  - [ ] Is IP available to be allocated/assigned?
