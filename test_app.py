import pytest
from unittest.mock import patch
import pytest


from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_missing_item(client):
    response = client.get("/inventory/999")

    assert response.status_code == 404
    assert response.json["error"] == "Item not found"


def test_add_item(client):
    new_item = {
        "barcode": "123456789",
        "name": "Milk",
        "brand": "Brookside",
        "price": 120,
        "stock": 10
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201
    assert response.json["name"] == "Milk"
    assert response.json["brand"] == "Brookside"


def test_add_item_missing_field(client):
    new_item = {
        "name": "Milk",
        "brand": "Brookside",
        "price": 120,
        "stock": 10
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 400
    assert response.json["error"] == "Missing field: barcode"


def test_update_item(client):
    response = client.patch(
        "/inventory/1",
        json={"price": 800, "stock": 15}
    )

    assert response.status_code == 200
    assert response.json["price"] == 800
    assert response.json["stock"] == 15


def test_delete_item(client):
    response = client.delete("/inventory/2")

    assert response.status_code == 200
    assert response.json["message"] == "Item deleted successfully"


@patch("app.requests.get")
def test_lookup_product(mock_get, client):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, hazelnuts, cocoa"
        }
    }

    response = client.get("/lookup?barcode=3017624010701")

    assert response.status_code == 200
    assert response.json["name"] == "Nutella"
    assert response.json["brand"] == "Ferrero"