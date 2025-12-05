from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
import routers
from API.db.schemas.libro import libro_schema, libros_schema
from .libros import LibroList  
from db.models.autor import Autor 
from db.client import db_client
from db.schemas.autor import autor_schema, autores_schema
from bson import ObjectId

router = APIRouter(prefix="/autores", tags=["autores"])

# Lista simulada de autores
AutorList = []

# Endpoint para obtener todos los autores
@router.get("/", response_model=list[Autor])
async def autores():
    return autores_schema(db_client.test.autores.find())

# Endpoint para obtener un autor por su ID (Query)
@router.get("", response_model=Autor)
async def autor(id : str):
    autor = find_autor_by_id(id)
    if autor:
        return autor
    raise HTTPException(status_code=404, detail="Autor no encontrado")

# Endpoint para obtener un autor por su ID
@router.get("/{id}", response_model=Autor)
async def autor(id: str):
    autor = find_autor_by_id(id)
    if autor:
        return autor
    raise HTTPException(status_code=404, detail="Autor no encontrado")

# Endpoint para crear un nuevo autor
@router.post("/", status_code=201, response_model=Autor)
async def add_autor(autor: Autor):
    if type(find_autor_by_dni(autor.dni)) == Autor:
        raise HTTPException(status_code=409, detail="El autor con ese DNI ya existe")
    autor_dict = autor.model_dump()
    del autor_dict["id"]
    id = db_client.test.autores.insert_one(autor_dict).inserted_id
    autor_dict["id"] = str(id)
    return Autor(**autor_dict)

# Endpoint para modificar un autor existente
@router.put("/{id}", response_model=Autor)
async def modify_autor(id: str, new_autor: Autor): 
    autor_dict = new_autor.model_dump()
    del autor_dict["id"]
    try:
        db_client.test.autores.find_one_and_replace({"_id":ObjectId(id)}, autor_dict)
        return find_autor_by_id(id)
    except:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    
# Endpoint para eliminar un autor por su ID
@router.delete("/{id}", status_code=204, response_model=Autor)
async def delete_autor(id: str):
    found = db_client.test.autores.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return Autor(**autor_schema(found))

# Endpoint para obtener los libros de un autor por su ID
@router.get("/{id}/libros", response_model=list[routers.libros.Libro])
async def get_libros_by_autor(id: str):
    autor = find_autor_by_id(id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    libros_del_autor = libros_schema(db_client.test.libros.find({"idAutor":ObjectId(id)}))
    return libros_del_autor   

#region Funciones 

def find_autor_by_id(id: str):
    try:
        autor = autor_schema(db_client.test.autores.find_one({"_id":ObjectId(id)}))
        return autor(**autor)
    except:
        return {"error":"Autor no encontrado"}    

def find_autor_by_dni(dni: str):
    try:
        autor = autor_schema(db_client.test.autores.find_one({"dni":dni}))
        return autor(**autor)
    except:
        return {"error":"Autor no encontrado"}
#endregion