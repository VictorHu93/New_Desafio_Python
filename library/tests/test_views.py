# library/tests/test_views.py

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from oauth2_provider.models import get_application_model
from django.contrib.auth import get_user_model
from library.models import Client, Book, Loan
from datetime import timedelta
from django.utils import timezone

User = get_user_model()
Application = get_application_model()

@pytest.fixture
def api_client():
    client = APIClient()

    # Cria um usuário para autenticação
    user = User.objects.create_user(username="testuser", password="123456")
    
    # Cria uma aplicação OAuth2
    application = Application.objects.create(
        name="Test Application",
        client_id="test_client_id",
        client_secret="test_client_secret",
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_PASSWORD,
        user=user,
    )

    # Autentica e obtém um token de acesso
    token_url = reverse("oauth2_provider:token")
    response = client.post(token_url, {
        "grant_type": "password",
        "username": "testuser",
        "password": "123456",
        "client_id": "test_client_id",
        "client_secret": "test_client_secret"
    })
    access_token = response.json().get("access_token")
    
    # Configura o cabeçalho de autorização com o token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client

@pytest.mark.django_db
def test_book_list(api_client):
    url = reverse('book-list')
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_reserve_book(api_client):
    client_obj = Client.objects.create(name="John Doe", email="john@example.com")
    book = Book.objects.create(title="Sample Book", author="Author Name", status="available")

    url = reverse('book-reserve', args=[book.id])
    response = api_client.post(url, {"client_id": client_obj.id})
    assert response.status_code == 201

@pytest.mark.django_db
def test_client_books(api_client):
    client_obj = Client.objects.create(name="Jane Doe", email="jane@example.com")
    book = Book.objects.create(title="Test Book", author="Author Name", status="loaned")
    Loan.objects.create(client=client_obj, book=book, loan_date=timezone.now() - timedelta(days=4))

    url = reverse('client-books', args=[client_obj.id])
    response = api_client.get(url)
    assert response.status_code == 200

