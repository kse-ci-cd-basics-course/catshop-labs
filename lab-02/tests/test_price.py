import requests

import app as app_module


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {
            "sku": "MK-II",
            "price": "123",
            "currency": "$"
        }


def test_price_ok(client, monkeypatch):
    urls = []

    def fake_get(url, timeout):
        urls.append(url)
        return FakeResponse()

    monkeypatch.setattr(app_module.requests, "get", fake_get)

    r = client.get("/price/MK-II")

    assert r.status_code == 200
    assert r.get_json()["price"] == "123"
    assert urls[0].endswith("/v1/catalog/MK-II")


def test_price_returns_502_when_partner_is_down(client, monkeypatch):
    def fake_get(url, timeout):
        raise requests.ConnectionError("partner is down")

    monkeypatch.setattr(app_module.requests, "get", fake_get)

    r = client.get("/price/MK-II")

    assert r.status_code == 502
    assert r.get_json()["error"] == "ConnectionError"