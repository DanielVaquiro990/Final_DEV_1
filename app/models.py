from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Jugador(Base):
    __tablename__ = "Jugador"
    
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, index=True)
    nombre = Column(String(100), nullable=False)
    fechaNacimiento = Column(Integer, nullable=False)
    Nacionalidad = Column(String(100), nullable=False)
    altura =  Column(Integer, nullable=False)
    peso = Column(Integer, nullable=False)
    pieDominante = Column(String(10), nullable=False)
    Posicion = Column(String(100), nullable=False)

    pass


class EstadisticasJugador(Base):
    __tablename__ = "estadisticas_jugador"

    id = Column(Integer, primary_key=True, index=True)
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    tarjetas_amarillas = Column(Integer, default=0)
    tarjetas_rojas = Column(Integer, default=0)
    partidos_jugados = Column(Integer, default=0)
    jugador_id = Column(Integer, ForeignKey("jugador.id"))

    jugador = relationship("Jugador", back_populates="estadisticas")
    


class Partido(Base):
    __tablename__ = "Partido"
    id = Column(Integer, primary_key=True, index=True)
    NombreRival = Column(String(100), nullable=False) 
    fecha = Column(DateTime, default=datetime.utcnow)
    golesLocal =  Column(Integer, nullable=False)
    golesRival = Column(Integer, nullable=False)
    pass


