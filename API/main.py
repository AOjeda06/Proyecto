from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from API.routers import libros, autores, auth_users, alumnos, colegios


app = FastAPI()

app.include_router(libros.router)
app.include_router(autores.router)
app.include_router(auth_users.router)
app.include_router(alumnos.router)
app.include_router(colegios.router)



app.mount("/static", StaticFiles(directory="API/static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library API"}
