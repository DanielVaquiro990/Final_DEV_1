from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from database import Base, engine
import models

# Routers
from routers import jugador
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Sistema de Gestión de informacion Club",
    description="SIGMOTOA FC",
    version="1.0.0"
)


app.mount("/static", StaticFiles(directory="static"), name="static")

#---Templates---
templates = Jinja2Templates(directory="templates")

#---Statics---
app.mount("/static", StaticFiles(directory="static"), name="static")



# ============================================================
#                    RUTAS (Routers)
# ============================================================
app.include_router(jugador.router)



# ============================================================
#                        RUTA RAÍZ
# ============================================================

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "mensaje": "Sistema funcionando"}
    )