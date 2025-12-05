from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel


# Modelo de datos para un autor
class Autor(BaseModel):
    id: str
    dni: str
    nombre: str
    apellidos: str
