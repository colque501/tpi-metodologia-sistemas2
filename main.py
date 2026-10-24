from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Gestión de Solicitudes Académicas (Versión Inicial)")

# Base de datos simulada en memoria
db_solicitudes = []

# SMELL 1: Obsesión por primitivos (se reciben parámetros sueltos en vez de un DTO/Pydantic Model)
# SMELL 2: Método largo y baja cohesión (mezcla validación, lógica de negocio y persistencia)
@app.post("/solicitudes/")
def registrar_solicitud(titulo: str, descripcion: str, id_estudiante: int, prioridad: str):
    # SMELL 3: Código duplicado y mal manejo de errores (retorna un dict en vez de HTTPException)
    if not titulo or len(titulo) < 3:
        return {"error": "El título es muy corto"}
    
    if prioridad not in ["ALTA", "MEDIA", "BAJA"]:
        return {"error": "Prioridad inválida"}
    
    nueva_solicitud = {
        "id": len(db_solicitudes) + 1,
        "titulo": titulo,
        "descripcion": descripcion,
        "id_estudiante": id_estudiante,
        "prioridad": prioridad,
        "estado": "PENDIENTE",
        "fecha_creacion": str(datetime.now()),
        "responsable": None
    }
    db_solicitudes.append(nueva_solicitud)
    return {"mensaje": "Solicitud creada exitosamente", "solicitud": nueva_solicitud}

@app.get("/solicitudes/")
def listar_solicitudes():
    return db_solicitudes

# SMELL 4: Acoplamiento fuerte (busca manualmente en la lista en cada endpoint)
@app.put("/solicitudes/estado/{solicitud_id}")
def cambiar_estado(solicitud_id: int, nuevo_estado: str):
    if nuevo_estado not in ["PENDIENTE", "EN_PROCESO", "RESUELTA", "RECHAZADA"]:
        return {"error": "Estado no permitido"}
        
    for solicitud in db_solicitudes:
        if solicitud["id"] == solicitud_id:
            solicitud["estado"] = nuevo_estado
            return {"mensaje": "Estado actualizado", "solicitud": solicitud}
            
    return {"error": "Solicitud no encontrada"}

@app.put("/solicitudes/responsable/{solicitud_id}")
def asignar_responsable(solicitud_id: int, responsable: str):
    if not responsable or len(responsable) < 3:
        return {"error": "Nombre de responsable muy corto"}
        
    # SMELL 4 (Repetido): Lógica de búsqueda duplicada
    for solicitud in db_solicitudes:
        if solicitud["id"] == solicitud_id:
            solicitud["responsable"] = responsable
            return {"mensaje": "Responsable asignado", "solicitud": solicitud}
            
    return {"error": "Solicitud no encontrada"}