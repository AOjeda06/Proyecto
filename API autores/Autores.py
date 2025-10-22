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
    return get_all_autores()

# Endpoint para obtener un autor por su ID
@app.get("/autores/{id}")
def get_autor(id: int):
    autor = find_autor_by_id(id)
    if autor:
        return autor
    raise HTTPException(status_code=404, detail="Autor no encontrado")

# Endpoint para crear un nuevo autor
@app.post("/autores", status_code=201, response_model=Autor)
def create_autor(autor: Autor):
    autor.id = next_id()
    add_autor(autor)
    return autor

# Endpoint para modificar un autor existente
@app.put("/autores/{id}", response_model=Autor)
def modify_autor(id: int, autor: Autor): 
    updated = update_autor(id, autor)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Autor no encontrado")

# Endpoint para eliminar un autor por su ID
@app.delete("/autores/{id}", status_code=204)
def delete_autor(id: int):
    removed = remove_autor(id)
    if removed:
        return {}
    raise HTTPException(status_code=404, detail="Autor no encontrado")

#region Funciones 
# Función para generar el siguiente ID disponible
def next_id():
    if AutorList:
        return (max(autor.id for autor in AutorList) + 1)
    return 1

# Funciones extraídas para operaciones sobre AutorList
def get_all_autores():
    return AutorList

def find_autor_by_id(id: int):
    autores = [autor for autor in AutorList if autor.id == id]
    return autores[0] if autores else None

def add_autor(autor: Autor):
    AutorList.append(autor)

def update_autor(id: int, autor: Autor):
    for index, saved_autor in enumerate(AutorList):
        if saved_autor.id == id:
            autor.id = id
            AutorList[index] = autor
            return autor
    return None

def remove_autor(id: int):
    for index, saved_autor in enumerate(AutorList):
        if saved_autor.id == id:
            AutorList.remove(saved_autor)
            return True
    return False
#endregion