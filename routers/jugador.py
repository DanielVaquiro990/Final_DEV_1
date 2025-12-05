from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
import models, schemas
from database import get_db

templates = Jinja2Templates(directory="templates") 

router = APIRouter(
    prefix="/jugador",
    tags=["Jugador"]
)

# FORMULARIO HTML
@router.get("/registrar")
async def registrar_jugador_view(request: Request, db: Session = Depends(get_db)):
    equipos = db.query(models.Equipo).all()  
    return templates.TemplateResponse(
        "jugador/registrar_jugador.html",
        {"request": request, "equipos": equipos}
    )

# API POST 
@router.post("/api/", response_model=schemas.Jugador)
async def crear_jugador(
    nombre: str = Form(...),
    fecha_nacimiento: date = Form(...),
    numero_dorsal: int = Form(...),
    nacionalidad: str = Form(...),
    altura: int = Form(...),
    peso: int = Form(...),
    pie_dominante: str = Form(...),
    posicion: str = Form(...),
    equipo_id: int = Form(...),
    db: Session = Depends(get_db)
):
    nuevo_jugador = models.Jugador(
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        numero_dorsal=numero_dorsal,
        nacionalidad=nacionalidad,
        altura=altura,
        peso=peso,
        pie_dominante=pie_dominante,
        posicion=posicion,
        equipo_id=equipo_id
    )

    db.add(nuevo_jugador)
    db.commit()
    db.refresh(nuevo_jugador)
    return nuevo_jugador

# Lista jugadores
@router.get("/lista")
async def listar_jugadores_view(request: Request, db: Session = Depends(get_db)):
    jugadores = db.query(models.Jugador).all()
    return templates.TemplateResponse(
        "jugador/lista_jugadores.html",
        {"request": request, "jugadores": jugadores}
    )

# Muestra el formulario para editar Jugador 
@router.get("/editar/{jugador_id}")
async def editar_jugador_view(jugador_id: int, request: Request, db: Session = Depends(get_db)):
    """Muestra el formulario de edición, precargando datos y listas de opciones."""
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
        
    equipos = db.query(models.Equipo).all()
    
    return templates.TemplateResponse(
        "jugador/editar_jugador.html",
        {
            "request": request,
            "jugador": jugador,
            "equipos": equipos
        }
    )

# Muestra el detalle de un jugador
@router.get("/detalle/{jugador_id}") 
async def detalle_jugador_view(jugador_id: int, request: Request, db: Session = Depends(get_db)):
    """Muestra el detalle de un jugador específico."""
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    
    return templates.TemplateResponse(
        "jugador/detalle_jugador.html",
        {"request": request, "jugador": jugador}
    )

# ============================================================
#                   RUTAS DE LA API (CRUD - JSON)
# ============================================================

# Crear jugador (POST API) - URL: /jugador/api/
@router.post("/api/", response_model=schemas.Jugador)
def crear_jugador_api(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    nuevo_jugador = models.Jugador(**jugador.dict())
    db.add(nuevo_jugador)
    db.commit()
    db.refresh(nuevo_jugador)
    return nuevo_jugador

# Listar jugadores (GET API) - URL: /jugador/api/
@router.get("/api/", response_model=list[schemas.Jugador]) 
def listar_jugadores_api(db: Session = Depends(get_db)):
    return db.query(models.Jugador).all()

# Eliminar jugador (DELETE API) - URL: /jugador/api/{jugador_id}
@router.delete("/api/{jugador_id}") 
def eliminar_jugador(jugador_id: int, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    db.delete(jugador)
    db.commit()
    return {"mensaje": "Jugador eliminado correctamente"}

# Nueva función para actualizar (PUT) un registro de jugador
@router.put("/{jugador_id}", response_model=schemas.Jugador)
def actualizar_jugador(jugador_id: int, datos: schemas.JugadorUpdateData, db: Session = Depends(get_db)):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    
    if not jugador:
        raise HTTPException(status_code=404, detail="Registro de jugador no encontrado")

    # 2. Actualizar los campos con los nuevos datos (sin manejar foto)
    for key, value in datos.dict(exclude_unset=True).items():
        setattr(jugador, key, value)

    # Intentar confirmar la transacción
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback() 
        # Si la identificación es UNIQUE, maneja el error aquí:
        if 'UNIQUE constraint failed' in str(e) and 'nombre' in str(e):
            raise HTTPException(
                status_code=400,
                detail=f"El nombre '{datos.nombre}' ya está en uso por otro jugador."
            )
        # Manejo de otros errores de integridad (como claves foráneas no válidas)
        else:
            raise HTTPException(
                status_code=400,
                detail="Error de integridad de datos (Equipo no válido)."
            )

    db.refresh(jugador)
    return jugador
