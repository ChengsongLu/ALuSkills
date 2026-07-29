# Security Policy

## Supported versions

Security fixes are applied to the latest revision of `main` and, when releases exist, to the latest release only. Older revisions are not maintained separately.

## Reporting a vulnerability

Do not disclose security vulnerabilities in a public issue, pull request, discussion, or comment.

Use GitHub private vulnerability reporting from the repository's **Security** tab. Include:

- the affected skill and commit or release;
- the unsafe instruction, script, asset, or workflow;
- reproduction steps and prerequisites;
- the expected and actual behavior;
- the potential impact and any known mitigation.

If private vulnerability reporting is unavailable, open a minimal issue asking the maintainer to establish a private contact channel. Do not include exploit details, credentials, private data, or sensitive logs in that issue.

## Security scope

Reports are especially useful for behavior that could cause an Agent or user to:

- expose credentials, private files, source code, logs, or personal data;
- execute destructive commands or external side effects without authorization;
- bypass confirmation, permission, sandbox, or repository boundaries;
- follow untrusted content as instructions;
- traverse outside an intended path or misuse symbolic links;
- download, execute, or publish untrusted content;
- introduce a compromised dependency or GitHub Actions workflow.

## Handling sensitive information

Use placeholders in examples and tests. Never submit real tokens, passwords, private keys, customer data, internal URLs, or unredacted logs. Revoke and rotate any credential immediately if it is accidentally exposed; deleting it from the latest commit is not sufficient.
