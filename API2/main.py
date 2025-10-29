from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import directores, peliculas

app = FastAPI()

app.include_router(directores.router)
app.include_router(peliculas.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "1"}