from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

# Modelo de datos para un libro
class Libro(BaseModel):
    id: str
    titulo: str
    idAutor: int
    isbn: str
    numPaginas: int
