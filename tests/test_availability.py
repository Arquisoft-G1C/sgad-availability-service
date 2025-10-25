import pytest
from httpx import AsyncClient
from fastapi import status
from datetime import date, timedelta

from app.main import app
from app.database import init_db


# ==========================================================
# ⚙️ FIXTURES DE CONFIGURACIÓN
# ==========================================================
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Inicializa la base de datos antes de ejecutar los tests."""
    init_db()
    yield


@pytest.fixture
async def client():
    """Cliente HTTP asíncrono para pruebas."""
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.fixture
def fake_token():
    """Token simulado para pruebas (mock del auth-service)."""
    return "Bearer test_token_123"


@pytest.fixture
def fake_referee_header(fake_token):
    """Header simulado con token."""
    return {"Authorization": fake_token}


# ==========================================================
# 🧩 TEST 1 — CREAR DISPONIBILIDAD
# ==========================================================
@pytest.mark.asyncio
async def test_create_availability(client, fake_referee_header, monkeypatch):
    """Prueba crear disponibilidad para una fecha específica."""

    # Mock de validación de token (simula auth-service)
    from app import auth_utils
    monkeypatch.setattr(
        auth_utils,
        "get_current_referee",
        lambda authorization=fake_token: {"id": 1, "role": "referee"}
    )

    today = date.today() + timedelta(days=1)
    payload = {
        "date": str(today),
        "slot_morning": True,
        "slot_afternoon": False,
        "slot_evening": True,
    }

    response = await client.post("/availability/", json=payload, headers=fake_referee_header)
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_201_CREATED)
    data = response.json()
    assert data["referee_id"] == 1
    assert data["date"] == str(today)
    assert data["slot_morning"] is True


# ==========================================================
# 🧩 TEST 2 — CONSULTAR DISPONIBILIDAD SEMANAL
# ==========================================================
@pytest.mark.asyncio
async def test_get_my_weekly_availability(client, fake_referee_header, monkeypatch):
    """Prueba obtener la disponibilidad semanal del árbitro."""

    # Mock de autenticación
    from app import auth_utils
    monkeypatch.setattr(
        auth_utils,
        "get_current_referee",
        lambda authorization=fake_token: {"id": 1, "role": "referee"}
    )

    response = await client.get("/availability/me", headers=fake_referee_header)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "availability" in data
    assert isinstance(data["availability"], list)


# ==========================================================
# 🧩 TEST 3 — CONSULTAR DISPONIBILIDAD POR FECHA
# ==========================================================
@pytest.mark.asyncio
async def test_get_availability_by_date(client, fake_referee_header, monkeypatch):
    """Prueba consultar árbitros disponibles en una fecha."""

    from app import auth_utils
    monkeypatch.setattr(
        auth_utils,
        "get_current_referee",
        lambda authorization=fake_token: {"id": 2, "role": "referee"}
    )

    target_date = (date.today() + timedelta(days=1)).isoformat()
    response = await client.get(f"/availability/date/{target_date}", headers=fake_referee_header)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
