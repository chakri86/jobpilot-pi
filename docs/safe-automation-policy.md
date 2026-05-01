# Safe Automation Policy

JobPilot Pi must respect third-party job portal rules and user consent.

## Allowed

- Store user-provided job source URLs.
- Fetch from safe, permitted sources.
- Use mock connectors for development.
- Import jobs from user-provided exports or permitted APIs.
- Score jobs against the user's profile.
- Draft cover letters, resume suggestions, and application answers.
- Open an assisted browser workflow where the user remains in control.

## Not Allowed

- CAPTCHA bypass.
- Stealth browsing or anti-detection behavior.
- Aggressive scraping.
- Auto-submitting applications.
- Storing job portal passwords.
- Reusing browser cookies without explicit user control.
- Ignoring robots, rate limits, or site terms.

## Playwright Boundary

Playwright may be used for user-assisted workflows only:

- The user chooses when to open a job page.
- The user reviews generated content.
- The user performs final submission manually.
- The workflow must stop before any submit action.

## Connector Review Checklist

- Is the source permitted by terms or API access?
- Is the scan interval respectful?
- Are credentials avoided?
- Is deduplication in place?
- Are errors logged without sensitive data?
