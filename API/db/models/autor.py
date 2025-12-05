from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from .libro import LibroList  # Importar aquí para evitar dependencias circulares


# Modelo de datos para un autor
class Autor(BaseModel):
    id: int
    dni: str
    nombre: str
    apellidos: str
