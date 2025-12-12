from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel

class Alumno(BaseModel):
    id: str 
    nombre: str
    apellidos: str
    fecha_nacimiento: str
    curso: str
    repetidor: bool
    id_colegio: str