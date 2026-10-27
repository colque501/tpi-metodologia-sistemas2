from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional

# Eliminamos los strings "harcodeados" usando Enums
class PrioridadEnum(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

class EstadoEnum(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    RESUELTA = "RESUELTA"
    RECHAZADA = "RECHAZADA"

# Aplicamos Introduce Parameter Object (DTO)
class SolicitudCreate(BaseModel):
    titulo: str = Field(..., min_length=3, description="El título debe tener al menos 3 caracteres")
    descripcion: str
    id_estudiante: int
    prioridad: PrioridadEnum

# Modelo para la respuesta
class SolicitudResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    id_estudiante: int
    prioridad: PrioridadEnum
    estado: EstadoEnum
    fecha_creacion: str
    responsable: Optional[str] = None