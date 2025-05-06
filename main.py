from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from utils.db import engine, crear_db, get_session
from data.models import Usuario, EstadoUsuario, Tarea, EstadoTarea, TareaCreate
from operations.operations_db import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario,
    usuarios_por_estado,
    usuarios_premium_y_activos,
    crear_tarea,
    obtener_tareas,
    obtener_tarea,
    actualizar_tarea,
    eliminar_tarea
)

app = FastAPI()

@app.on_event("startup")
def startup():
    crear_db()

@app.post("/usuarios/")
def crear(usuario: Usuario, session: Session = Depends(get_session)):
    return crear_usuario(session, usuario)

@app.get("/usuarios/")
def listar(session: Session = Depends(get_session)):
    return obtener_usuarios(session)

@app.get("/usuarios/{id}")
def ver(id: int, session: Session = Depends(get_session)):
    usuario = obtener_usuario_por_id(session, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{id}")
def actualizar(id: int, datos: Usuario, session: Session = Depends(get_session)):
    usuario = actualizar_usuario(session, id, datos)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.delete("/usuarios/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    usuario = eliminar_usuario(session, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/estado/{estado}")
def por_estado(estado: EstadoUsuario, session: Session = Depends(get_session)):
    return usuarios_por_estado(session, estado)

@app.get("/usuarios/premium/activos")
def premium_activos(session: Session = Depends(get_session)):
    return usuarios_premium_y_activos(session)
@app.post("/tareas/", response_model=Tarea)
def crear(tarea: Tarea, session: Session = Depends(get_session)):
    return crear_tarea(session, tarea)

@app.get("/tareas/", response_model=Tarea)
def listar_tareas(session: Session = Depends(get_session)):
    return obtener_tareas(session)

@app.get("/tareas/{tarea_id}", response_model=Tarea)
def obtener(tarea_id: int, session: Session = Depends(get_session)):
    return obtener_tarea(session, tarea_id)

@app.put("/tareas/{tarea_id}", response_model=Tarea)
def actualizar(tarea_id: int, tarea: Tarea, session: Session = Depends(get_session)):
    return actualizar_tarea(session, tarea_id, tarea)

@app.delete("/tareas/{tarea_id}")
def eliminar(tarea_id: int, session: Session = Depends(get_session)):
    eliminar_tarea(session, tarea_id)
    return {"ok": True}

@app.post("/tareas/", response_model=Tarea)
def crear(tarea_data: TareaCreate, session: Session = Depends(get_session)):
    nueva_tarea = Tarea(**tarea_data.dict())
    return crear_tarea(session, nueva_tarea)