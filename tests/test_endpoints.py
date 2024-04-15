import pytest
from conftest import client

def test_create_new_contact(client):
    # Dane testowe
    contact_data = {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "email": "jan.kowalski@example.com",
        "phone_number": "123456789",
        "birth_date": "2002-12-04",
        "extra_data": "Some extra data"
    }

    # Wywołanie endpointu
    response = client.post("/contacts/", json=contact_data)

    # Sprawdzenie kodu odpowiedzi
    assert response.status_code == 200

    # Sprawdzenie danych zwróconych przez endpoint
    contact = response.json()
    assert contact["first_name"] == contact_data["first_name"]
    assert contact["last_name"] == contact_data["last_name"]
    assert contact["email"] == contact_data["email"]
    assert contact["phone_number"] == contact_data["phone_number"]
    assert contact["birth_date"] == contact_data["birth_date"]
    assert contact["extra_data"] == contact_data["extra_data"]