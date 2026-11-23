import pytest

def test_html_404_handler(client):
    res = client.get("/nonexistent-route-xyz")
    assert res.status_code == 404
    assert b"404" in res.data
    assert b"Listing or Route Not Found" in res.data

def test_api_404_json_envelope(client):
    res = client.get("/api/nonexistent-endpoint")
    assert res.status_code == 404
    data = res.get_json()
    assert data["ok"] is False
    assert data["error"] == "Not Found"
    assert "not found" in data["message"].lower()
