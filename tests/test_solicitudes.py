"""Pruebas de la API de solicitudes (version refactorizada).

Se dividen en dos grupos:
- Comportamiento conservado: lo mismo que hacia la version inicial.
- Cambios intencionales: diferencias de contrato que se decidieron en el refactor
  y que antes devolvian HTTP 200 con un diccionario {"error": ...}.
"""

import pytest
from fastapi.testclient import TestClient

import service
from main import app

DATOS = {
    "titulo": "Pedido de equivalencia",
    "descripcion": "Equivalencia de Programacion I",
    "id_estudiante": 1001,
    "prioridad": "ALTA",
}


@pytest.fixture
def cliente():
    # cada prueba arranca con la "base" en memoria vacia
    service.db_solicitudes.clear()
    return TestClient(app)


# ----------------------------------------------------------------- comportamiento conservado


def test_crear_solicitud_guarda_los_datos_con_estado_pendiente(cliente):
    respuesta = cliente.post("/solicitudes/", json=DATOS)

    solicitud = respuesta.json()
    assert solicitud["id"] == 1
    assert solicitud["titulo"] == "Pedido de equivalencia"
    assert solicitud["prioridad"] == "ALTA"
    assert solicitud["estado"] == "PENDIENTE"
    assert solicitud["responsable"] is None


def test_los_ids_se_asignan_en_orden(cliente):
    cliente.post("/solicitudes/", json=DATOS)
    respuesta = cliente.post("/solicitudes/", json={**DATOS, "titulo": "Cambio de comision"})

    assert respuesta.json()["id"] == 2


def test_listar_devuelve_todas_las_solicitudes(cliente):
    cliente.post("/solicitudes/", json=DATOS)
    cliente.post("/solicitudes/", json={**DATOS, "prioridad": "BAJA"})

    respuesta = cliente.get("/solicitudes/")

    assert respuesta.status_code == 200
    assert [s["prioridad"] for s in respuesta.json()] == ["ALTA", "BAJA"]


def test_cambiar_estado_actualiza_la_solicitud(cliente):
    cliente.post("/solicitudes/", json=DATOS)

    respuesta = cliente.put("/solicitudes/estado/1", params={"nuevo_estado": "EN_PROCESO"})

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "EN_PROCESO"
    assert cliente.get("/solicitudes/").json()[0]["estado"] == "EN_PROCESO"


def test_asignar_responsable_actualiza_la_solicitud(cliente):
    cliente.post("/solicitudes/", json=DATOS)

    respuesta = cliente.put("/solicitudes/responsable/1", params={"responsable": "Laura Diaz"})

    assert respuesta.status_code == 200
    assert respuesta.json()["responsable"] == "Laura Diaz"


# ----------------------------------------------------------------- cambios intencionales


def test_crear_responde_201_created(cliente):
    # antes: 200 y la solicitud envuelta en {"mensaje": ..., "solicitud": {...}}
    respuesta = cliente.post("/solicitudes/", json=DATOS)

    assert respuesta.status_code == 201
    assert "mensaje" not in respuesta.json()


@pytest.mark.parametrize("titulo", ["", "ab"])
def test_titulo_menor_a_3_caracteres_se_rechaza_con_422(cliente, titulo):
    # antes: 200 {"error": "El título es muy corto"}
    respuesta = cliente.post("/solicitudes/", json={**DATOS, "titulo": titulo})

    assert respuesta.status_code == 422
    assert cliente.get("/solicitudes/").json() == []


def test_prioridad_invalida_se_rechaza_con_422(cliente):
    # antes: 200 {"error": "Prioridad inválida"}
    respuesta = cliente.post("/solicitudes/", json={**DATOS, "prioridad": "URGENTE"})

    assert respuesta.status_code == 422


def test_estado_invalido_se_rechaza_con_422(cliente):
    # antes: 200 {"error": "Estado no permitido"}
    cliente.post("/solicitudes/", json=DATOS)

    respuesta = cliente.put("/solicitudes/estado/1", params={"nuevo_estado": "CERRADA"})

    assert respuesta.status_code == 422
    assert cliente.get("/solicitudes/").json()[0]["estado"] == "PENDIENTE"


@pytest.mark.parametrize(
    "ruta, parametros",
    [
        ("/solicitudes/estado/99", {"nuevo_estado": "RESUELTA"}),
        ("/solicitudes/responsable/99", {"responsable": "Laura Diaz"}),
    ],
)
def test_solicitud_inexistente_responde_404(cliente, ruta, parametros):
    # antes: 200 {"error": "Solicitud no encontrada"}
    respuesta = cliente.put(ruta, params=parametros)

    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Solicitud no encontrada"


def test_responsable_menor_a_3_caracteres_responde_400(cliente):
    # antes: 200 {"error": "Nombre de responsable muy corto"}
    cliente.post("/solicitudes/", json=DATOS)

    respuesta = cliente.put("/solicitudes/responsable/1", params={"responsable": "Al"})

    assert respuesta.status_code == 400
    assert cliente.get("/solicitudes/").json()[0]["responsable"] is None
