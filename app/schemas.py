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

class EstadisticaBase(BaseModel):
    minutos : int
    goles : int
    faltas : int
    CantidadTarjetas : int

class EstadisticaCreate(EstadisticaBase):
    pass

class Estadistica(EstadisticaBase):
    id : int
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