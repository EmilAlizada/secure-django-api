# API Examples

Base URL:

```text
http://localhost:8000/api/v1
```

## Register

```http
POST /auth/register/
Content-Type: application/json

{
  "username": "alice",
  "email": "alice@example.com",
  "password": "Strong-Example-Password!42"
}
```

## Login

```http
POST /auth/token/
Content-Type: application/json

{
  "username": "alice",
  "password": "Strong-Example-Password!42"
}
```

Response:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

## Current user

```http
GET /me/
Authorization: Bearer <access-token>
```

## Create note

```http
POST /notes/
Authorization: Bearer <access-token>
Content-Type: application/json

{
  "title": "Private note",
  "body": "Only the authenticated owner can access this."
}
```

The client cannot choose the owner. Ownership is assigned from the authenticated request user.

## List notes

```http
GET /notes/
Authorization: Bearer <access-token>
```

Only records owned by the authenticated user are returned.

## Retrieve note

```http
GET /notes/1/
Authorization: Bearer <access-token>
```

If note `1` belongs to another account, it is outside the request user's queryset and the API returns `404`.
