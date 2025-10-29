from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import libros, autores

app = FastAPI()

app.include_router(libros.router)
app.include_router(autores.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library API"}
