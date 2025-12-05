from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from bson import ObjectId

from db.client import db_client
from db.models.libro import Libro
from db.schemas.libro import libro_schema, libros_schema

router = APIRouter(prefix="/libros", tags=["libros"])

# Lista simulada de libros
LibroList = []

#region Endpoints

# Endpoint para obtener todos los libros
@router.get("/", response_model=list[Libro])
async def get_libros():
    return libros_schema(db_client.test.libros.find())

# Endpoint para obtener un libro por su ID (Query)
@router.get("", response_model=Libro)
async def get_libro_query(id: str):
    libro = find_libro_by_id(id)
    if libro:
        return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Endpoint para obtener un libro por su ID (Path)
@router.get("/{id}", response_model=Libro)
async def get_libro(id: str):
    libro = find_libro_by_id(id)
    if libro:
        return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Endpoint para crear un nuevo libro
@router.post("/", status_code=201, response_model=Libro)
async def create_libro(libro: Libro):
    if type(find_libro_by_isbn(libro.isbn)) == Libro:
        raise HTTPException(status_code=409, detail="El libro con ese ISBN ya existe")
    libro_dict = libro.model_dump()
    del libro_dict["id"]
    id = db_client.test.libros.insert_one(libro_dict).inserted_id
    libro_dict["id"] = str(id)
    return Libro(**libro_dict)

# Endpoint para modificar un libro existente
@router.put("/{id}", response_model=Libro)
async def modify_libro(id: str, new_libro: Libro): 
    libro_dict = new_libro.model_dump()
    del libro_dict["id"]
    try:
        db_client.test.libros.find_one_and_replace({"_id":ObjectId(id)}, libro_dict)
        return find_libro_by_id(id)
    except:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

# Endpoint para eliminar un libro por su ID
@router.delete("/{id}", status_code=204, response_model=Libro)
async def delete_libro(id: str):
    found = db_client.test.libros.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return Libro(**libro_schema(found))

#endregion

#region Funciones

def find_libro_by_id(id: str):
    try:
        libro = libro_schema(db_client.test.libros.find_one({"_id":ObjectId(id)}))
        return Libro(**libro)
    except:
        return {"error":"Libro no encontrado"}    

def find_libro_by_isbn(isbn: str):
    try:
        libro = libro_schema(db_client.test.libros.find_one({"isbn":isbn}))
        return Libro(**libro)
    except:
        return {"error":"Libro no encontrado"}
#endregion
