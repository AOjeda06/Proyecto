from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/peliculas", tags=["peliculas"])

# Modelo de datos para una película
class Pelicula(BaseModel):
    id: int
    titulo: str
    duracionMins: int
    idDirector: int

# Lista simulada de películas
PeliculaList = [
    Pelicula(id=1, titulo="El Padrino", duracionMins=175, idDirector=1),
    Pelicula(id=2, titulo="E.T. el Extraterrestre", duracionMins=115, idDirector=2),
    Pelicula(id=3, titulo="La La Land", duracionMins=128, idDirector=3)
]

#region Endpoints

# Endpoint para obtener todas las películas
@router.get("/")
def get_peliculas():
    return get_all_peliculas()

# Endpoint para obtener una película por su ID
@router.get("/{id}")
def get_pelicula(id: int):
    pelicula = find_pelicula_by_id(id)
    if pelicula:
        return pelicula
    raise HTTPException(status_code=404, detail="Película no encontrada")

# Endpoint para crear una nueva película
@router.post("/", status_code=201, response_model=Pelicula)
def create_pelicula(pelicula: Pelicula):
    pelicula.id = next_id()
    add_pelicula(pelicula)
    return pelicula

# Endpoint para modificar una película existente
@router.put("/{id}", response_model=Pelicula)
def modify_pelicula(id: int, pelicula: Pelicula): 
    updated = update_pelicula(id, pelicula)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Película no encontrada")

# Endpoint para eliminar una película por su ID
@router.delete("/{id}", status_code=204)
def delete_pelicula(id: int):
    removed = remove_pelicula(id)
    if removed:
        return {}
    raise HTTPException(status_code=404, detail="Película no encontrada")

#endregion

#region Funciones

#Función para generar el siguiente ID disponible
def next_id():
    if PeliculaList:
        return (max(pelicula.id for pelicula in PeliculaList) + 1)
    return 1

# Función para obtener todas las películas
def get_all_peliculas():
    return PeliculaList

#Función para buscar una película por su ID
def find_pelicula_by_id(id: int):
    resultados = [pelicula for pelicula in PeliculaList if pelicula.id == id]
    return resultados[0] if resultados else None

#Función para agregar una nueva película
def add_pelicula(pelicula: Pelicula):
    PeliculaList.append(pelicula)

#Función para actualizar una película existente
def update_pelicula(id: int, pelicula: Pelicula):
    for index, existing_pelicula in enumerate(PeliculaList):
        if existing_pelicula.id == id:
            PeliculaList[index] = pelicula
            return pelicula
    return None

#Función para eliminar una película por su ID
def remove_pelicula(id: int):
    for pelicula in PeliculaList:
        if pelicula.id == id:
             PeliculaList.remove(pelicula)
             return True
    return False

#endregion