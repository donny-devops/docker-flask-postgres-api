# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in `docker-flask-postgres-api`, please report it via email to security@yourdomain.com rather than creating a public issue. We will acknowledge your report within 48 hours and work with you to coordinate a fix and disclosure timeline.

## Supported Versions

Security fixes are typically provided only for the latest stable release branch. Older versions may be left unpatched.

## What We Fix

- Authentication and authorization issues (missing token checks, ID‑or‑scope leaks).
- Injection vulnerabilities (SQL injection via unsafe string concatenation).
- Hard‑coded secrets in Dockerfiles, compose files, or code.
- Clear‑text transport when HTTPS/TLS should be enforced.
- Misconfigurations that expose the database container to unintended networks.

## What You Are Expected to Do

- Do not store production secrets in the repository.
- Run containers with non‑root users and minimal base images where possible.
- Keep your base images and Python dependencies up to date.
- Use a reverse proxy/load balancer with TLS in production.

## Security‑Related Engineering Practices

- Branch protection and code reviews are enforced on the main branch.
- CI includes basic security scanning and dependency checks.
- Secrets are injected via environment variables or a secrets manager, not git‑tracked files.

## License

This policy is for the `docker-flask-postgres-api` project only and does not guarantee a vulnerability‑free product; use at your own risk.
