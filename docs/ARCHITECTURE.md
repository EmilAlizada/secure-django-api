# Architecture

## Goal

The project demonstrates a compact API where authentication and authorization decisions are easy to inspect.

## Runtime

```text
Client
  |
  | Bearer JWT
  v
Django REST Framework
  |
  +--> authentication
  +--> permissions
  +--> throttling
  +--> validation
  |
  v
Owner-scoped queryset
  |
  v
PostgreSQL
```

## Authentication

Simple JWT issues:

- short-lived access tokens
- longer-lived refresh tokens

The API expects:

```http
Authorization: Bearer <access-token>
```

## Authorization

Notes are user-owned resources.

Two controls protect them:

1. `get_queryset()` filters records to `owner=request.user`
2. `IsOwner` performs object-level authorization

This is deliberate defense in depth.

## Password handling

The registration serializer calls Django's configured password validators before creating the user. `create_user()` handles password hashing; raw passwords are never stored.

## Abuse resistance

Registration, token issuance, and token refresh use a scoped throttle. General authenticated and anonymous traffic also uses DRF rate limits.

The default in-memory cache is enough for this demo but is not a distributed production rate limiter. A production deployment should use a shared cache such as Redis.

## Runtime hardening

- debug disabled by default
- runtime secrets from environment variables
- non-root container user
- read-only application filesystem in Compose
- `no-new-privileges`
- restrictive browser security headers
