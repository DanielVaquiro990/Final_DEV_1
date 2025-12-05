from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Jugador(Base):
    __tablename__ = "Jugador"
    
    numero = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    fechaNacimiento = Column(Integer, nullable=False)
    Nacionalidad = Column(String(100), nullable=False)
    altura =  Column(Integer, nullable=False)
    peso = Column(Integer, nullable=False)
    pieDominante = Column(String(10), nullable=False)
    Posicion
    pass


class Estadistica(Base):
    __tablename__ ="Estadistica"

    minutos = Column(Integer, nullable=False)
    goles = Column(Integer, nullable=False)
    faltas = Column(Integer, nullable=False)
    tarjetas 
    pass


class Partido(Base):
    __tablename__ = "Partido"

    Nombrerival = Column(String(100), nullable=False) 
    fecha = Column(DateTime, default=datetime.utcnow)
    golesLocal =  Column(Integer, nullable=False)
    golesRival = Column(Integer, nullable=False)

    
    
    
    
    pass


