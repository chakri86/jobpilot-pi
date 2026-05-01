# Contributing

Thank you for improving JobPilot Pi.

## Workflow

1. Branch from `dev`.
2. Make focused changes.
3. Add or update tests where behavior changes.
4. Run backend tests and frontend build checks.
5. Open a pull request into `dev`.

## Commit Style

Use concise, descriptive messages:

```text
feat: add job source scan endpoint
fix: validate resume upload content type
docs: expand Raspberry Pi deployment guide
```

## Safety Policy

Contributions must respect job portal terms of service. Do not add stealth automation, CAPTCHA bypass, credential collection, or unauthorized auto-apply behavior.

## Secrets

Never commit:

- `.env`
- API keys
- Passwords
- Uploaded resumes
- Database dumps
- Browser session cookies

Use `.env.example` for documented configuration only.
