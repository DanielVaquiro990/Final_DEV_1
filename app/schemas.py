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




#-------------Estadistica----------




#-----------------Partido---------------