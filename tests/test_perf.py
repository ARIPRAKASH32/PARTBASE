import pytest

def test_static_asset_cache_headers(client):
    res = client.get("/static/css/main.css")
    assert res.status_code == 200
    assert "Cache-Control" in res.headers
    assert "max-age=86400" in res.headers["Cache-Control"]
