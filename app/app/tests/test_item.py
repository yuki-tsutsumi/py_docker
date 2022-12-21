from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/item/10",params={"q": "aaa"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 10, "q": "aaa"}

def test_read_item_id_only():
    response = client.get("/item/10")
    assert response.status_code == 200
    assert response.json() == {"item_id": 10, "q": None}

def test_read_item_id_is_str():
    response = client.get("/item/aa")
    assert response.status_code == 422

def test_read_item_id_is_float():
    response = client.get("/item/1.1")
    assert response.status_code == 422