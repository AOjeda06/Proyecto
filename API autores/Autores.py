from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos para un autor
class Autor(BaseModel):
    id: int
    dni: str
    nombre: str
    apellidos: str

# Lista simulada de autores
AutorList = [
    Autor(id=1, dni="12345678A", nombre="Miguel", apellidos="de Cervantes"),
    Autor(id=2, dni="87654321B", nombre="Federico", apellidos="García Lorca"),
    Autor(id=3, dni="11223344C", nombre="Rosalía", apellidos="de Castro")
]

# Endpoint para obtener todos los autores
@app.get("/autores")
def get_autores():
    return AutorList

# Endpoint para obtener un autor por su ID
@app.get("/autores/{id}")
def get_autor(id: int):
    autores = [autor for autor in AutorList if autor.id == id]
    if autores:
        return autores[0]
    raise HTTPException(status_code=404, detail="Autor no encontrado")