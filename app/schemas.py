from pydantic import BaseModel
from typing import Optional
from datetime import date

#-------------Jugador----------

class JugadorBase(BaseModel):
    numero = int
    nombre: str
    fechaNacimiento = date
    nacionalidad = str
    altura = int
    peso = int 
    pieDominante = str
    posicion = str


class JugadorCreate(JugadorBase):
    pass


class Jugador(JugadorBase):
    id : int
    class Config:
        orm_mode = True

#-------------Estadistica----------

class EstadisticasBase(BaseModel):
    goles: int = 0
    asistencias: int = 0
    tarjetas_amarillas: int = 0
    tarjetas_rojas: int = 0
    partidos_jugados: int = 0

    class Config:
        orm_mode = True

class EstadisticasJugadorCreate(EstadisticasBase):
    pass

class EstadisticasJugadorUpdate(EstadisticasBase):
    pass

class EstadisticasJugador(EstadisticasBase):
    id: int
    jugador_id: int

    class Config:
        orm_mode = True




#-----------------Partido---------------

class PartidoBase (BaseModel):
    NombreRival : str
    fecha : date
    golesLocal : int
    golesRival : int

class ParitdoCreate(PartidoBase):
    pass

class Partido(PartidoBase):
    id : int
    class Config:
        orm_mode = True



