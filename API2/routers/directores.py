from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/directores", tags=["directores"])

# Modelo de datos para un director
class Director(BaseModel):
    id: int
    dni: str
    nombre: str
    apellidos: str
    nacionalidad: str

# Lista simulada de directores
DirectorList = [
    Director(id=1, dni="23456789D", nombre="Steven", apellidos ="Spielberg", nacionalidad="Estadounidense"),
    Director(id=2, dni="98765432E", nombre="Martin", apellidos ="Scorsese", nacionalidad="Estadounidense"),
    Director(id=3, dni="22334455F", nombre="Pedro", apellidos ="Almodóvar", nacionalidad="Española")
]

#region Endpoints

# Endpoint para obtener todos los directores
@router.get("/")
def get_directores():
    return get_all_directores()

# Endpoint para obtener un director por su ID
@router.get("/{id}")
def get_director(id: int):
    director = find_director_by_id(id)
    if director:
        return director
    raise HTTPException(status_code=404, detail="Director no encontrado")

# Endpoint para crear un nuevo director
@router.post("/", status_code=201, response_model=Director)
def create_director(director: Director):
    director.id = next_id()
    add_director(director)
    return director

# Endpoint para modificar un director existente
@router.put("/{id}", response_model=Director)
def modify_director(id: int, director: Director): 
    updated = update_director(id, director)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Director no encontrado")

# Endpoint para eliminar un director por su ID
@router.delete("/{id}", status_code=204)
def delete_director(id: int):
    removed = remove_director(id)
    if removed:
        return {}
    raise HTTPException(status_code=404, detail="Director no encontrado")

#endregion

#region Funciones

# Función para generar el siguiente ID disponible
def next_id():
    if DirectorList:
        return (max(director.id for director in DirectorList) + 1)
    return 1

# Funcion para obtener todos los directores
def get_all_directores():
    return DirectorList

#Funcion para buscar un director por su ID
def find_director_by_id(id: int):
    resultados = [director for director in DirectorList if director.id == id]
    return resultados[0] if resultados else None

#Función para añadir un nuevo director
def add_director(director: Director):
    DirectorList.append(director)

#Función para actualizar un director existente
def update_director(id: int, director: Director):
    for index, d in enumerate(DirectorList):
        if d.id == id:
            director.id = id
            DirectorList[index] = director
            return director
    return None

#Función para eliminar un director por su ID
def remove_director(id: int):
    for d in DirectorList:
        if d.id == id:
             DirectorList.remove(d)
             return True
    return False
#endregion