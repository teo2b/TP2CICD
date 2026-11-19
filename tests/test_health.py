import os
from pathlib import Path

from fastapi.testclient import TestClient

TEST_DATABASE = Path(".pytest-tp2.db")
if TEST_DATABASE.exists():
    TEST_DATABASE.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DATABASE}"

from app.main import app

client = TestClient(app)


def test_health_returns_status_and_default_version(monkeypatch) -> None:
    monkeypatch.delenv("APP_VERSION", raising=False)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "dev"}


def test_health_returns_configured_version(monkeypatch) -> None:
    monkeypatch.setenv("APP_VERSION", "sha-a1b2c3d")

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "sha-a1b2c3d"}


def test_products_are_seeded() -> None:
    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 1200


def test_order_is_created_and_stock_is_decreased() -> None:
    response = client.post("/orders", json={"product_id": 1, "quantity": 2})

    assert response.status_code == 201
    assert response.json()["product_id"] == 1
    assert response.json()["quantity"] == 2

    product = next(
        item for item in client.get("/products").json() if item["id"] == 1
    )
    assert product["stock"] == 98


def test_order_over_stock_is_refused() -> None:
    response = client.post("/orders", json={"product_id": 2, "quantity": 101})

    assert response.status_code == 409
    assert response.json() == {"detail": "Stock insuffisant"}


def test_product_stock_can_be_declared() -> None:
    response = client.put("/products/3/stock", json={"stock": 250})

    assert response.status_code == 200
    assert response.json() == {"id": 3, "stock": 250}


def test_product_stock_cannot_be_negative() -> None:
    response = client.put("/products/3/stock", json={"stock": -1})

    assert response.status_code == 422


def test_declared_stock_is_visible_in_products() -> None:
    client.put("/products/3/stock", json={"stock": 75})

    product = next(
        item for item in client.get("/products").json() if item["id"] == 3
    )
    assert product["stock"] == 75
