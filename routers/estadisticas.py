from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import EstadisticasJugador, Jugador
from schemas import EstadisticasJugadorCreate, EstadisticasJugadorUpdate, EstadisticasJugador as EstadisticasJugadorSchema
from database import get_db

router = APIRouter(
    prefix="/estadisticas",
    tags=["Estadísticas de Jugadores"]
)

# Crear estadísticas de jugador
@router.post("/api/{jugador_id}", response_model=EstadisticasJugadorSchema)
def crear_estadisticas(jugador_id: int, estadisticas: EstadisticasJugadorCreate, db: Session = Depends(get_db)):
    # Verificar si el jugador existe
    jugador = db.query(Jugador).filter(Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    # Crear nuevo registro de estadísticas
    nueva_estadistica = EstadisticasJugador(
        goles=estadisticas.goles,
        asistencias=estadisticas.asistencias,
        tarjetas_amarillas=estadisticas.tarjetas_amarillas,
        tarjetas_rojas=estadisticas.tarjetas_rojas,
        partidos_jugados=estadisticas.partidos_jugados,
        jugador_id=jugador.id
    )
    
    db.add(nueva_estadistica)
    db.commit()
    db.refresh(nueva_estadistica)
    
    return nueva_estadistica


# Obtener estadísticas de un jugador
@router.get("/api/{jugador_id}", response_model=EstadisticasJugadorSchema)
def obtener_estadisticas(jugador_id: int, db: Session = Depends(get_db)):
    estadisticas = db.query(EstadisticasJugador).filter(EstadisticasJugador.jugador_id == jugador_id).first()
    
    if not estadisticas:
        raise HTTPException(status_code=404, detail="Estadísticas no encontradas para este jugador")
    
    return estadisticas


# Actualizar estadísticas de un jugador
@router.put("/api/{jugador_id}", response_model=EstadisticasJugadorSchema)
def actualizar_estadisticas(jugador_id: int, estadisticas: EstadisticasJugadorUpdate, db: Session = Depends(get_db)):
    estadisticas_existentes = db.query(EstadisticasJugador).filter(EstadisticasJugador.jugador_id == jugador_id).first()

    if not estadisticas_existentes:
        raise HTTPException(status_code=404, detail="Estadísticas no encontradas para este jugador")
    
    # Actualizar los campos de las estadísticas
    for key, value in estadisticas.dict(exclude_unset=True).items():
        setattr(estadisticas_existentes, key, value)

    db.commit()
    db.refresh(estadisticas_existentes)
    
    return estadisticas_existentes


# Eliminar estadísticas de un jugador
@router.delete("/api/{jugador_id}", response_model=dict)
def eliminar_estadisticas(jugador_id: int, db: Session = Depends(get_db)):
    estadisticas = db.query(EstadisticasJugador).filter(EstadisticasJugador.jugador_id == jugador_id).first()

    if not estadisticas:
        raise HTTPException(status_code=404, detail="Estadísticas no encontradas para este jugador")
    
    db.delete(estadisticas)
    db.commit()
    
    return {"mensaje": "Estadísticas eliminadas correctamente"}
