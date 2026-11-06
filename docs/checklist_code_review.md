# Checklist de code review

Se aplicó sobre el Pull Request #1 (`feature/refactoring` → `main`).
Revisor: David Gutierrez. Autor: Brian Gutierrez Colque.

Un PR se acepta solo si todos los criterios de la tabla quedan en "Cumple". Si un criterio
no se cumple, el revisor deja un comentario en la línea afectada y el autor lo corrige
antes del merge, o se registra como corrección posterior con su justificación.

## Criterios de aceptación técnica

| # | Criterio | Cómo se verifica | Resultado |
|---|---|---|---|
| 1 | El sistema levanta y Swagger muestra los 4 endpoints | `uvicorn main:app` y abrir `/docs` | Cumple |
| 2 | El controlador no tiene lógica de negocio ni acceso a datos (SRP) | `main.py` solo recibe el pedido y llama al servicio | Cumple |
| 3 | No hay valores de estado o prioridad escritos como texto suelto | `PrioridadEnum` y `EstadoEnum` en `schemas.py` | Cumple |
| 4 | Los datos de entrada llegan como un objeto y no como parámetros sueltos | DTO `SolicitudCreate` | Cumple |
| 5 | No hay código duplicado para buscar una solicitud | Método `_buscar_por_id` | Cumple |
| 6 | Los errores responden con el código HTTP que corresponde | 400, 404 y 422 en lugar de 200 con `{"error": ...}` | Cumple |
| 7 | Las operaciones válidas siguen funcionando igual | Pruebas manuales en Swagger y `pytest` | Cumple |
| 8 | No se versionan archivos generados | No hay `__pycache__/` ni `.pyc` en el repositorio | **No cumplía** → corregido |

## Observaciones del revisor (PR #1)

| Archivo | Observación | Tipo | Acción |
|---|---|---|---|
| `schemas.py` | Uso de `Enum` para estados y prioridades | Aprobación | Ninguna |
| `schemas.py` | `SolicitudCreate` resuelve la obsesión por primitivos y valida `min_length=3` | Aprobación | Ninguna |
| `schemas.py` | `SolicitudResponse` define el contrato de salida | Aprobación | Ninguna |
| `service.py` | La lógica de negocio quedó fuera del controlador | Aprobación | Ninguna |
| `main.py` | Endpoints que solo delegan y `status_code=201` en la creación | Aprobación | Ninguna |
| `__pycache__/*.pyc` | Se subieron archivos compilados de Python; falta `.gitignore` | **Cambio pedido** | Se agregó `.gitignore` y se quitaron los `.pyc` del repositorio |

## Dictamen

Aprobado y fusionado a `main` el 26/10/2026. La corrección del criterio 8 se hizo en un commit
posterior, porque el PR ya estaba fusionado cuando se tomó la observación.

## Puntos que la revisión no cubrió

Quedan anotados para la próxima iteración (ver `decisiones_tecnicas.md`):

- `service.py` lanza `HTTPException`, así que la capa de negocio depende de FastAPI.
- La lista `db_solicitudes` sigue siendo una variable global del módulo de servicio.
