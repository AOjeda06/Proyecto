from fastapi import HTTPException, APIRouter
from API.db.client import db_client
from API.db.schemas.colegio import colegio_schema, colegios_schema
from bson import ObjectId
from API.db.models.colegio import Colegio

router = APIRouter(prefix="/colegios", tags=["colegios"])

# Endpoint para obtener todos los colegios
@router.get("/", response_model=list[Colegio])
async def get_colegios():
    return colegios_schema(db_client.test.colegios.find())

# Endpoint para obtener un colegio por su id
@router.get("/{id}", response_model=Colegio)
async def get_colegio(id: str):
    colegio = find_colegio_by_id(id)
    if colegio:
        return colegio
    raise HTTPException(status_code=404, detail="Colegio no encontrado")

# Endpoint para crear un nuevo colegio
@router.post("/", status_code=201, response_model=Colegio)
async def add_colegio(colegio: Colegio):
    # Validar por tipo
    if check_tipo(colegio.tipo): 
        colegio_dict = colegio.model_dump()
        colegio_dict.pop("id", None)
        inserted_id = db_client.test.colegios.insert_one(colegio_dict).inserted_id
        colegio_dict["id"] = str(inserted_id)
        return Colegio(**colegio_dict)
    raise HTTPException(status_code=422, detail="El tipo no es válido")

# Funciones Auxiliares
def find_colegio_by_id(id: str) -> Colegio | None:
    doc = db_client.test.colegios.find_one({"_id": ObjectId(id)})
    if doc:
        return Colegio(**colegio_schema(doc))
    return None

def check_tipo(tipo: str) -> bool:
    valido = (tipo == "publico" or tipo == "concertado" or tipo == "privado")
    return valido