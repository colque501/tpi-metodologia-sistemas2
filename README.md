# Gestión de Solicitudes Académicas

Trabajo Práctico Integrador de Metodología de Sistemas II (UTN, Tecnicatura Universitaria en
Programación a Distancia).

API REST para registrar solicitudes de estudiantes, cambiarles el estado y asignarles un
responsable administrativo. El sistema se usó como caso de estudio: se partió de una versión
inicial con problemas de diseño a propósito y se la mejoró con refactoring, sin agregar
funcionalidad.

**Integrantes:** Brian Gutierrez Colque, David Gutierrez y Federico Iacono.

## Funcionalidades

| Operación | Método y ruta |
|---|---|
| Registrar una solicitud | `POST /solicitudes/` |
| Listar las solicitudes | `GET /solicitudes/` |
| Cambiar el estado (PENDIENTE, EN_PROCESO, RESUELTA, RECHAZADA) | `PUT /solicitudes/estado/{id}` |
| Asignar un responsable | `PUT /solicitudes/responsable/{id}` |

Los datos se guardan en memoria: al reiniciar el servidor se pierden.

## Tecnologías

Python 3.12 o superior, FastAPI, Pydantic, Uvicorn y pytest. Como cliente se usa la interfaz
Swagger que genera FastAPI (no hay frontend propio).

## Instalación y uso

```sh
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

Con el servidor levantado, la interfaz Swagger está en http://127.0.0.1:8000/docs.

## Pruebas

```sh
python -m pytest -v
```

Para comparar las respuestas de la versión inicial y la refactorizada:

```sh
git worktree add ../inicial estado-inicial
python tests/comparar_versiones.py ../inicial .
```

## Estructura

```text
main.py      rutas HTTP (controlador)
schemas.py   modelos de entrada y salida (Pydantic) y enumeraciones
service.py   lógica de negocio y datos en memoria
tests/       pruebas automatizadas y comparación entre versiones
docs/        checklist de code review, decisiones técnicas y evidencias
```

## Versiones (tags)

| Tag | Qué marca |
|---|---|
| `estado-inicial` | Sistema base con los problemas a diagnosticar |
| `etapa-diagnostico` | Código sobre el que se hizo el diagnóstico de code smells |
| `etapa-refactoring` | Refactorización en capas (PR #1) |
| `etapa-pruebas` | Pruebas automatizadas |
| `etapa-docs` | README y documentación en `docs/` |
| `estado-refactorizado` | Estado final del trabajo |
