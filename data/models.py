from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class EstadoUsuario(str, Enum):
    activo = "Activo"
    inactivo = "Inactivo"
    eliminado = "Eliminado"

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str
    premium: bool = False
    estado: EstadoUsuario = Field(default=EstadoUsuario.activo)

class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    en_ejecucion = "en ejecucion"
    realizada = "realizada"
    cancelada = "cancelada"

class TareaBase(SQLModel):
    nombre: str
    descripcion: str
    estado: EstadoTarea = Field(default=EstadoTarea.pendiente)
    usuario: int

class Tarea(TareaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_modificacion: datetime = Field(default_factory=datetime.utcnow)

class TareaCreate(TareaBase):
    pass