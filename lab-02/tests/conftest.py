import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "COUNTER_FILE", tmp_path / "data" / "visits.txt")
    monkeypatch.setattr(app_module, "DATABASE_URL", None)
    return app_module.app.test_client()