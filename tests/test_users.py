from app import schemas
from jose import jwt
from app.config import settings
import pytest


@pytest.fixture
def test_user(client):
    user_data = {"email": "saulgoodman@speedyjustice4u.com", "password": "ethics"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello successssss"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "jessepinkman@gmail.com", "password": "streets1"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "jessepinkman@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        settings.jose_jwt_secret_key,
        algorithms=[settings.algorithm],
    )
    id: str = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
