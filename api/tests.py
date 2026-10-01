import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from .models import Note

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def alice(db):
    return User.objects.create_user(username="alice", password="A-Strong-Test-Pass!42")


@pytest.fixture
def bob(db):
    return User.objects.create_user(username="bob", password="Another-Strong-Pass!42")


@pytest.mark.django_db
def test_health_is_public(client):
    response = client.get("/api/v1/health/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok", "service": "secure-django-api"}


@pytest.mark.django_db
def test_registration_hashes_password(client):
    response = client.post(
        "/api/v1/auth/register/",
        {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Secure-Registration-Pass!42",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    user = User.objects.get(username="newuser")
    assert user.password != "Secure-Registration-Pass!42"
    assert user.check_password("Secure-Registration-Pass!42")


@pytest.mark.django_db
def test_token_endpoint_returns_jwt_pair(client, alice):
    response = client.post(
        "/api/v1/auth/token/",
        {"username": "alice", "password": "A-Strong-Test-Pass!42"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_me_requires_authentication(client):
    response = client.get("/api/v1/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_only_lists_owned_notes(client, alice, bob):
    alice_note = Note.objects.create(owner=alice, title="Alice private note")
    Note.objects.create(owner=bob, title="Bob private note")

    client.force_authenticate(user=alice)
    response = client.get("/api/v1/notes/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == alice_note.id
    assert response.data[0]["owner"] == "alice"


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_note(client, alice, bob):
    bob_note = Note.objects.create(owner=bob, title="Bob private note")

    client.force_authenticate(user=alice)
    response = client.get(f"/api/v1/notes/{bob_note.id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_owner_cannot_be_spoofed_on_create(client, alice, bob):
    client.force_authenticate(user=alice)
    response = client.post(
        "/api/v1/notes/",
        {"title": "Owned safely", "body": "Test", "owner": "bob"},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    note = Note.objects.get(id=response.data["id"])
    assert note.owner == alice
    assert note.owner != bob
