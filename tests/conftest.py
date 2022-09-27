from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app.main import app
from app.database import get_db, Base
from app.config import settings
from app import models
import pytest


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_database}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "saulgoodman@speedyjustice4u.com", "password": "ethics"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "saulgoodman1@speedyjustice4u.com", "password": "ethics1"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "asdf", 403),
        ("ouhsdf@yahoo.com", "ogiuewrh", 403),
        (None, None, 422),
        (None, "test", 422),
        ("wrongemail", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": test_user[email], "password": password}
    )
    assert res.status_code == status_code
    assert res.json().get("detail") == "Invalid Credentials"


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "Best Beaches",
            "content": "Ocean, Sammy, Cliff",
            "owner_id": test_user["id"],
        },
        {
            "title": "Who is the Governor",
            "content": "Many of our subscribers have been wondering, Whos is the Governor really?",
            "owner_id": test_user["id"],
        },
        {
            "title": "Woof",
            "content": "Wood, woof, wood, wood, etc...",
            "owner_id": test_user["id"],
        },
        {
            "title": "Meow",
            "content": "cat sounds, Meow, more cat sounds, etc...",
            "owner_id": test_user2["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
