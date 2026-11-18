def test_health_body_and_status(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "ok\n"