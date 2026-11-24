import app as app_module


def test_visits_counts_up(client):
    r = client.get("/visits")
    assert r.get_json() == {"visits": 1, "store": "file"}

    r = client.get("/visits")
    assert r.get_json()["visits"] == 2


def test_visits_saves_counter(client):
    client.get("/visits")
    client.get("/visits")

    assert app_module.COUNTER_FILE.read_text() == "2"


def test_visits_starts_from_saved_value(client):
    app_module.COUNTER_FILE.parent.mkdir(parents=True)
    app_module.COUNTER_FILE.write_text("41")

    r = client.get("/visits")
    assert r.get_json()["visits"] == 42


def test_visits_returns_error_when_file_unavailable(client, tmp_path, monkeypatch):
    file = tmp_path / "blocker"
    file.write_text("not a directory")

    monkeypatch.setattr(app_module, "COUNTER_FILE", file / "visits.txt")

    r = client.get("/visits")

    assert r.status_code == 503
    assert "error" in r.get_json()