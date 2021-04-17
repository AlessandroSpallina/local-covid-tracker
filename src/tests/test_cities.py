import json

import pytest

from app.api import crud


def test_create_city(test_app, monkeypatch):
    test_request_payload = {
        "codice_comune": 999,
        "distretto": 1234,
        "denominazione_comune": "villarossa",
        "lat": 154.5965,
        "long": 11.9874
    }
    test_response_payload = {
        "id": 1,
        "codice_comune": 999,
        "distretto": 1234,
        "denominazione_comune": "villarossa",
        "lat": 154.5965,
        "long": 11.9874
    }

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/cities/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_city_invalid_json(test_app):
    response = test_app.post("/cities/", data=json.dumps({"codice_comune": 222}))
    assert response.status_code == 422


def test_read_city(test_app, monkeypatch):
    test_data = {
        "id": 1,
        "codice_comune": 999,
        "distretto": 1234,
        "denominazione_comune": "villarossa",
        "lat": 154.5965,
        "long": 11.9874
    }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/cities/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_city_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/cities/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"


def test_read_all_cities(test_app, monkeypatch):
    test_data = [
        {
            "id": 1,
            "codice_comune": 999,
            "distretto": 1234,
            "denominazione_comune": "villarossa",
            "lat": 154.5965,
            "long": 11.9874
        },
        {
            "id": 2,
            "codice_comune": 998,
            "distretto": 1233,
            "denominazione_comune": "villaverde",
            "lat": 153.5965,
            "long": 10.9874
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/cities/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_update_city(test_app, monkeypatch):
    test_update_data = {
            "id": 1,
            "codice_comune": 999,
            "distretto": 1234,
            "denominazione_comune": "enna",
            "lat": 154.5965,
            "long": 11.9874
        }

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/cities/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"codice_comune": 14}, 422],
        [999, {
            "codice_comune": 999,
            "distretto": 1234,
            "denominazione_comune": "enna",
            "lat": 154.5965,
            "long": 11.9874
        }, 404],
    ],
)
def test_update_city_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/cities/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


def test_remove_city(test_app, monkeypatch):
    test_data = {
            "id": 1,
            "codice_comune": 999,
            "distretto": 1234,
            "denominazione_comune": "enna",
            "lat": 154.5965,
            "long": 11.9874
        }

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/cities/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_city_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/cities/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"

