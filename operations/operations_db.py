from sqlmodel import Session, select
from data.models import Usuario, EstadoUsuario, Tarea, EstadoTarea
from datetime import datetime

def crear_usuario(session: Session, usuario: Usuario):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def obtener_usuarios(session: Session):
    return session.exec(select(Usuario).where(Usuario.estado != EstadoUsuario.eliminado)).all()

def obtener_usuario_por_id(session: Session, id: int):
    return session.get(Usuario, id)

def actualizar_usuario(session: Session, id: int, datos: Usuario):
    usuario = session.get(Usuario, id)
    if usuario:
        usuario.nombre = datos.nombre
        usuario.email = datos.email
        usuario.premium = datos.premium
        session.commit()
        session.refresh(usuario)
    return usuario

def eliminar_usuario(session: Session, id: int):
    usuario = session.get(Usuario, id)
    if usuario:
        usuario.estado = EstadoUsuario.eliminado
        session.commit()
        session.refresh(usuario)
    return usuario

def usuarios_por_estado(session: Session, estado: EstadoUsuario):
    return session.exec(select(Usuario).where(Usuario.estado == estado)).all()

def usuarios_premium_y_activos(session: Session):
    return session.exec(
        select(Usuario).where(Usuario.estado == EstadoUsuario.activo, Usuario.premium == True)
    ).all()
def crear_tarea(session: Session, tarea: Tarea) :
    existente = session.get(Tarea, tarea.id) if tarea.id else None
    if existente:
        raise HTTPException(status_code=400, detail=f"Ya existe una tarea con ID {tarea.id}")
    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea


def obtener_tareas(session: Session) :
    tareas = session.exec(select(Tarea)).all()
    if not tareas:
        raise HTTPException(status_code=404, detail="No hay tareas registradas.")
    return tareas
def obtener_tarea(session: Session, tarea_id: int) -> Tarea:
    tarea = session.get(Tarea, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail=f"Tarea con ID {tarea_id} no encontrada.")
    return tarea


def actualizar_tarea(session: Session, tarea_id: int, nueva_tarea: Tarea):
    tarea = session.get(Tarea, tarea_id)
    if tarea:
        tarea.nombre = nueva_tarea.nombre
        tarea.descripcion = nueva_tarea.descripcion
        tarea.estado = nueva_tarea.estado
        tarea.usuario = nueva_tarea.usuario
        tarea.fecha_modificacion = datetime.utcnow()
        session.add(tarea)
        session.commit()
        session.refresh(tarea)
    return tarea

def eliminar_tarea(session: Session, tarea_id: int):
    tarea = session.get(Tarea, tarea_id)
    if tarea:
        session.delete(tarea)
        session.commit()
    return tarea