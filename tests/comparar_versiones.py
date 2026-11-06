"""Ejecuta las mismas operaciones contra dos versiones del sistema y muestra la respuesta.

Uso (desde la raiz del repositorio):
    git worktree add ../inicial estado-inicial
    python tests/comparar_versiones.py ../inicial .

La version inicial recibe los datos por query string y la refactorizada por JSON:
el script arma cada pedido en el formato que espera cada una.
"""

import importlib
import sys

from fastapi.testclient import TestClient

DATOS = {
    "titulo": "Pedido de equivalencia",
    "descripcion": "Equivalencia de Programacion I",
    "id_estudiante": 1001,
    "prioridad": "ALTA",
}


def cargar(carpeta):
    for modulo in ("main", "schemas", "service"):
        sys.modules.pop(modulo, None)
    sys.path.insert(0, carpeta)
    app = importlib.import_module("main").app
    sys.path.pop(0)
    return TestClient(app)


def casos(cliente, inicial):
    def crear(**cambios):
        datos = {**DATOS, **cambios}
        if inicial:
            return cliente.post("/solicitudes/", params=datos)
        return cliente.post("/solicitudes/", json=datos)

    return [
        ("1. Crear solicitud valida", crear),
        ("2. Listar solicitudes", lambda: cliente.get("/solicitudes/")),
        ("3. Cambiar estado a EN_PROCESO", lambda: cliente.put("/solicitudes/estado/1", params={"nuevo_estado": "EN_PROCESO"})),
        ("4. Asignar responsable", lambda: cliente.put("/solicitudes/responsable/1", params={"responsable": "Laura Diaz"})),
        ("5. Titulo de 2 caracteres", lambda: crear(titulo="ab")),
        ("6. Prioridad inexistente", lambda: crear(prioridad="URGENTE")),
        ("7. Estado inexistente", lambda: cliente.put("/solicitudes/estado/1", params={"nuevo_estado": "CERRADA"})),
        ("8. Solicitud inexistente (id 99)", lambda: cliente.put("/solicitudes/estado/99", params={"nuevo_estado": "RESUELTA"})),
        ("9. Responsable de 2 caracteres", lambda: cliente.put("/solicitudes/responsable/1", params={"responsable": "Al"})),
    ]


def resumir(respuesta):
    cuerpo = respuesta.json()
    if isinstance(cuerpo, list):
        return f"lista de {len(cuerpo)} solicitud(es)"
    if "detail" in cuerpo and isinstance(cuerpo["detail"], list):
        return "detalle de validacion de FastAPI"
    texto = str(cuerpo)
    return texto if len(texto) <= 70 else texto[:67] + "..."


for etiqueta, carpeta in (("ANTES (estado-inicial)", sys.argv[1]), ("DESPUES (refactorizado)", sys.argv[2])):
    cliente = cargar(carpeta)
    print(f"\n=== {etiqueta}")
    for nombre, pedido in casos(cliente, inicial=etiqueta.startswith("ANTES")):
        respuesta = pedido()
        print(f"{nombre:34} HTTP {respuesta.status_code}  {resumir(respuesta)}")
