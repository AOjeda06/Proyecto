from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

# Modelo de datos para un libro
class Libro(BaseModel):
    id: int
    titulo: str
    idAutor: int
    isbn: str
    numPaginas: int
