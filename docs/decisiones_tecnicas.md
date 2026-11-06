# Decisiones técnicas

Registro corto de las decisiones que tomó el equipo, con el motivo y lo que se resignó.

## 1. Swagger como único cliente

**Decisión:** no construir un frontend; se usa la interfaz que genera FastAPI.
**Motivo:** el trabajo evalúa la calidad interna. Un frontend sumaba código sin aportar al diagnóstico.
**Costo:** la "calidad externa" se mide sobre la API y no sobre una pantalla para el usuario final.

## 2. Datos en memoria

**Decisión:** guardar las solicitudes en una lista de Python.
**Motivo:** la consigna permite simular la persistencia y así no se suma una base de datos.
**Costo:** los datos se pierden al reiniciar. Además, la lista quedó como variable global
dentro de `service.py` (ver punto 6).

## 3. Separación en tres archivos (controlador, esquemas y servicio)

**Decisión:** `main.py` recibe los pedidos, `schemas.py` define qué datos entran y salen, y
`service.py` aplica las reglas.
**Motivo:** en la versión inicial cualquier cambio de regla obligaba a tocar los endpoints (SRP).

## 4. Validación declarativa con Pydantic y enumeraciones

**Decisión:** el largo mínimo del título, la prioridad y el estado se validan en los modelos
(`Field(min_length=3)`, `PrioridadEnum`, `EstadoEnum`).
**Motivo:** se eliminan los `if` repetidos y los textos sueltos que podían escribirse mal.

## 5. Cambio intencional del contrato de la API

**Decisión:** corregir las respuestas para que respeten HTTP.

| Situación | Versión inicial | Versión refactorizada |
|---|---|---|
| Crear una solicitud | 200 y `{"mensaje", "solicitud"}` | 201 y la solicitud |
| Cambiar estado o asignar responsable | 200 y `{"mensaje", "solicitud"}` | 200 y la solicitud |
| Datos inválidos (título, prioridad, estado) | 200 y `{"error": ...}` | 422 con el detalle de validación |
| Solicitud inexistente | 200 y `{"error": ...}` | 404 |
| Responsable de menos de 3 letras | 200 y `{"error": ...}` | 400 |
| Forma de enviar los datos al crear | parámetros en la URL | cuerpo JSON |

**Motivo:** con 200 para todo, un cliente no puede distinguir un error de un éxito.
**Costo:** un cliente hecho para la versión inicial deja de funcionar. Por eso no se presenta
como refactoring puro: los refactorings (puntos 3 y 4) no cambian lo que hace el sistema, y
esta corrección sí, de manera intencional. Las pruebas de `tests/` separan los dos casos.

## 6. Mejoras que quedan pendientes

| Pendiente | Por qué importa | Propuesta |
|---|---|---|
| `service.py` lanza `HTTPException` | La lógica de negocio depende del framework web (DIP) | Excepciones propias (`SolicitudNoEncontrada`) traducidas a HTTP en `main.py` |
| Lista global `db_solicitudes` | No se puede cambiar el almacenamiento sin tocar el servicio | Clase `SolicitudRepository` que se le pasa al servicio |
| Métodos `@staticmethod` | No permiten reemplazar dependencias en las pruebas | Servicio como objeto con el repositorio en el constructor |
| `responsable` como texto suelto | No hay una entidad Responsable/Área | Modelo propio si el sistema crece |
| ID calculado con `len() + 1` | Se repetiría si se agregara un borrado | Contador propio o ID que asigne la base de datos |
