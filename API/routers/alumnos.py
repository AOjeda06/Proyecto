from fastapi import HTTPException, APIRouter
from API.db.client import db_client
from API.db.schemas.alumno import alumno_schema, alumnos_schema
from bson import ObjectId
from API.db.models.alumno import Alumno

router = APIRouter(prefix="/alumnos", tags=["alumnos"])

#Endpoint para obtener todos los alumnos
@router.get("/", response_model=list[Alumno])
async def get_alumnos():
    return alumnos_schema(db_client.test.alumnos.find())

# Query
#@router.get("", response_model=list[Alumno])
#async def alumno(curso: str):
 #   return search_alumnos_curso(curso)

# Query
#@router.get("", response_model=list[Alumno])
#async def alumnos_by_distrito(distrito: str):
#    return search_alumnos_distrito(distrito)

# Endpoint para añadir un nuevo alumno
@router.post("/", status_code=201, response_model=Alumno)
async def add_alumno(alumno: Alumno):
    # Validar Colegio
    if check_colegio_exists(alumno.id_colegio):
        alumno_dict = alumno.model_dump()
        alumno_dict.pop("id", None)
        inserted_id = db_client.test.alumno.insert_one(alumno_dict).inserted_id
        alumno_dict["id"] = str(inserted_id)
        return Alumno(**alumno_dict)
    raise HTTPException(status_code=422, detail="El idColegio no es válido")

# Endpoint para modificar un alumno existente
@router.put("/{id}", response_model=Alumno)
async def modify_alumno(id: str, new_alumno: Alumno):
    alumno_dict = new_alumno.model_dump()
    alumno_dict.pop("id", None)
    updated = db_client.test.alumnos.find_one_and_replace({"_id": ObjectId(id)}, alumno_dict)
    if not updated:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return find_alumno_by_id(id)

# Endpoint para eliminar un alumno existente
@router.delete("/{id}", response_model=Alumno)
async def delete_alumno(id: str):
    found = db_client.test.alumnos.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return Alumno(**alumno_schema(found))

#Funciones auxiliares
def find_alumno_by_id(id: str) -> Alumno | None:
    doc = db_client.test.alumnos.find_one({"_id": ObjectId(id)})
    if doc:
        return Alumno(**alumno_schema(doc))
    return None

def check_colegio_exists(id: str) -> bool:
    found = db_client.test.colegios.find_one({"_id": ObjectId(id)})
    if found:
        return True
    return False

def search_alumnos_curso(curso: str) -> list[Alumno] | None:
    alumnos = alumnos_schema(db_client.test.alumnos.find({"curso": curso}))
    return alumnos

def search_alumnos_distrito(distrito: str) -> list[Alumno] | None:
    return