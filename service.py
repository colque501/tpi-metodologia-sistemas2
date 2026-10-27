from datetime import datetime
from fastapi import HTTPException
from schemas import SolicitudCreate, EstadoEnum

# Aislamos la persistencia
db_solicitudes = []

class SolicitudService:
    
    @staticmethod
    def crear_solicitud(datos: SolicitudCreate) -> dict:
        nueva_solicitud = {
            "id": len(db_solicitudes) + 1,
            "titulo": datos.titulo,
            "descripcion": datos.descripcion,
            "id_estudiante": datos.id_estudiante,
            "prioridad": datos.prioridad.value,
            "estado": EstadoEnum.PENDIENTE.value,
            "fecha_creacion": str(datetime.now()),
            "responsable": None
        }
        db_solicitudes.append(nueva_solicitud)
        return nueva_solicitud

    @staticmethod
    def listar_todas() -> list:
        return db_solicitudes

    # Aplicamos Extract Method para reutilizar la búsqueda (eliminamos Código Duplicado)
    @staticmethod
    def _buscar_por_id(solicitud_id: int) -> dict:
        for solicitud in db_solicitudes:
            if solicitud["id"] == solicitud_id:
                return solicitud
        # Manejo de errores adecuado mediante excepciones HTTP
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    @staticmethod
    def actualizar_estado(solicitud_id: int, nuevo_estado: EstadoEnum) -> dict:
        solicitud = SolicitudService._buscar_por_id(solicitud_id)
        solicitud["estado"] = nuevo_estado.value
        return solicitud

    @staticmethod
    def asignar_responsable(solicitud_id: int, responsable: str) -> dict:
        if not responsable or len(responsable) < 3:
            raise HTTPException(status_code=400, detail="Nombre de responsable muy corto")
            
        solicitud = SolicitudService._buscar_por_id(solicitud_id)
        solicitud["responsable"] = responsable
        return solicitud