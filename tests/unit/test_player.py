import os
from http import HTTPStatus

import pytest

from app import create_app
from app.db import DB, player
from app.db.constants import PLAYERS_COLLECTION
from app.apis import MSG


@pytest.fixture(autouse=True)
def test_environment(monkeypatch):
    monkeypatch.setenv("MOCK_DB", "true")
    monkeypatch.setenv("DB_NAME", "testdb")
    monkeypatch.setenv("MONGO_URI", "mongodb://localhost:27017/testdb")
    monkeypatch.setenv("DEBUG", "false")


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["MOCK_DB"] = True
    app.config["DB_NAME"] = "testdb"
    app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"
    DB.init_app(app)
    return app


@pytest.fixture(autouse=True)
def clear_player_collection(app):
    DB.get_collection(PLAYERS_COLLECTION).delete_many({})


@pytest.fixture
def client(app):
    return app.test_client()


def test_add_player_creates_document():
    player_id = player.add_player(name="Test Player", crossing=12, passing=14)

    assert isinstance(player_id, str)
    stored = DB.get_collection(PLAYERS_COLLECTION).find_one({"name": "Test Player"})
    assert stored is not None
    assert stored["crossing"] == 12
    assert stored["passing"] == 14


def test_get_player_returns_player_document():
    player.add_player(name="Dummy Player", dribbling=10, tackling=8)

    result = player.get_player("Dummy Player")

    assert result["name"] == "Dummy Player"
    assert result["dribbling"] == 10
    assert result["tackling"] == 8
    assert "id" in result
    assert "_id" not in result


def test_get_player_returns_none_for_missing_player():
    assert player.get_player("Nonexistent Player") is None


def test_create_player_endpoint(client):
    response = client.post(
        "/players/create",
        json={"name": "Player", "crossing": 13, "passing": 11},
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data[MSG] == "Player created"
    assert "id" in data


def test_list_players_endpoint_returns_created_player(client):
    player.add_player(name="TestPlayer", marking=16)

    response = client.get("/players/list")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()

    assert any(item["name"] == "TestPlayer" for item in data)


def test_get_player_endpoint_returns_player(client):
    player.add_player(name="Endpoint Player", agility=14)

    response = client.get("/players/Endpoint Player")
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()

    assert data["name"] == "Endpoint Player"
    assert data["agility"] == 14


def test_analyse_player_endpoint_returns_rating(client):
    player.add_player(
        name="Analysed Player",
        crossing=15,
        passing=15,
        tackling=15,
        positioning=15,
    )

    response = client.post(
        "/players/analyse/Analysed Player",
        json={"role": "CenterBack"},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["player"] == "Analysed Player"
    assert data["role"] == "CenterBack"
    assert isinstance(data["rating"], float)
    assert data["rating"] >= 0


def test_best_roles_endpoint_returns_top_roles(client):
    player.add_player(
        name="Best Roles Player",
        passing=15,
        tackling=15,
        positioning=15,
        vision=15,
        teamwork=15,
    )

    response = client.post(
        "/players/analyse/Best Roles Player/best",
        json={"category": "MID"},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data["player"] == "Best Roles Player"
    assert isinstance(data["best_roles"], list)
    assert len(data["best_roles"]) <= 5

