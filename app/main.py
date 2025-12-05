from fastapi import FastAPI
from app.routers import estadisticas, jugador

app = FastAPI(title="sigmotoa FC")


@app.get("/")
async def root():
    return {"message": "sigmotoa FC data"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Bienvenido a sigmotoa FC {name}"}



app.include_router(estadisticas.router)
app.include_router(jugador.router)
