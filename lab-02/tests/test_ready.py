import app as app_module


def test_ready_ok(client):
    r = client.get("/ready")

    assert r.status_code == 200

    data = r.get_json()
    assert data["ready"] is True
    assert data["store"] == f"file:{app_module.COUNTER_FILE}"


def test_ready_returns_503_when_file_unavailable(client, tmp_path, monkeypatch):
    file = tmp_path / "blocker"
    file.write_text("x")

    monkeypatch.setattr(app_module, "COUNTER_FILE", file / "visits.txt")

    r = client.get("/ready")

    assert r.status_code == 503
    assert r.get_json()["ready"] is False