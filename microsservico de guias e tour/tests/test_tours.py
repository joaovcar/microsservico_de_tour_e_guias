from uuid import uuid4

import os
import sys

from fastapi.testclient import TestClient


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.app.main import app


def test_create_and_list_tour():
    guia_id = uuid4()
    client = TestClient(app)

    payload = {
        "titulo": "Passeio de Teste",
        "descricao": "Desc",
        "dias": ["segunda"],
        "horarios": ["09:00"]
    }

    r = client.post(f"/guias/{guia_id}/passeios", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["titulo"] == payload["titulo"]

    r2 = client.get("/passeios")
    assert r2.status_code == 200
    all_data = r2.json()
    assert any(t["id"] == data["id"] for t in all_data)
