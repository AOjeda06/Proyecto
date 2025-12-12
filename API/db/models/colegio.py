from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel

class Colegio(BaseModel):
    id: str
    nombre: str
    distrito: str   
    tipo: str   
    direccion: str