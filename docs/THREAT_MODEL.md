# Threat Model

## Assets

- user credentials
- JWT tokens
- private note data
- application secret key
- database integrity
- source and CI integrity
- dependency supply chain

## Trust boundaries

1. client -> API
2. JWT -> authenticated identity
3. API user -> user-owned object
4. application -> PostgreSQL
5. repository -> CI runner
6. CI runner -> package/action registries

## Representative threats

| Threat | Example | Control |
|---|---|---|
| Broken object-level authorization | guessing another note ID | owner-filtered queryset + IsOwner |
| Ownership spoofing | posting another username as owner | owner field read-only + server-side assignment |
| Password disclosure | storing raw password | Django password hashing |
| Weak password | simple/common password | Django validators + minimum serializer length |
| Brute force | repeated login attempts | scoped auth throttling |
| Stolen access token | long-lived bearer token | 5-minute access-token lifetime |
| Secret exposure | committed production key | environment injection + .env ignored |
| Debug leakage | detailed error pages | debug off by default |
| Dependency risk | vulnerable Python package | pip-audit + Dependabot |
| Unsafe code pattern | insecure Python construct | Bandit |
| Vulnerable image | OS/package CVE | Trivy |
| Container privilege escalation | app compromise | non-root + no-new-privileges + read-only FS |

## Residual risks

- demo throttling uses process-local cache and is not distributed
- refresh-token revocation is not yet implemented
- email ownership is not verified
- no MFA flow exists
- JWT theft is still possible on an insecure client
- TLS termination is outside this repository
- third-party packages and GitHub Actions remain supply-chain dependencies

## Next controls

1. token blacklist / logout support
2. email verification
3. Redis-backed throttling
4. security event logging
5. immutable SHA pinning for third-party Actions
6. SBOM and provenance
