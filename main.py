from fastapi import FastAPI
from schemas import SolicitudCreate, EstadoEnum, SolicitudResponse
from service import SolicitudService

app = FastAPI(title="Gestión de Solicitudes Académicas (Refactorizado)")

@app.post("/solicitudes/", response_model=SolicitudResponse, status_code=201)
def registrar_solicitud(solicitud: SolicitudCreate):
    return SolicitudService.crear_solicitud(solicitud)

@app.get("/solicitudes/", response_model=list[SolicitudResponse])
def listar_solicitudes():
    return SolicitudService.listar_todas()

@app.put("/solicitudes/estado/{solicitud_id}", response_model=SolicitudResponse)
def cambiar_estado(solicitud_id: int, nuevo_estado: EstadoEnum):
    return SolicitudService.actualizar_estado(solicitud_id, nuevo_estado)

@app.put("/solicitudes/responsable/{solicitud_id}", response_model=SolicitudResponse)
def asignar_responsable(solicitud_id: int, responsable: str):
    return SolicitudService.asignar_responsable(solicitud_id, responsable)