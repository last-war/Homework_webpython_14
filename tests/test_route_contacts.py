from unittest.mock import MagicMock, patch

from pytest import mark, fixture

from src.database.models import User
from src.services.auth import auth_service


@fixture(scope='function')
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


@mark.usefixtures('mock_rate_limit')
def test_create_contact(client, token):
    with patch.object(auth_service, 'redis_db') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json={"first_name": "John", "last_name": "Dow", "email": "user@example.com", "phone": "2877064128",
                  "birthday": "2023-04-23T15:28:13.286Z"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Dow"
    assert data["email"] == "user@example.com"
    assert "id" in data

